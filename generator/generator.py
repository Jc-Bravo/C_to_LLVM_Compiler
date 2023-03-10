from antlr4 import *

from parser.myCParser import myCParser
from parser.myCVisitor import myCVisitor
from parser.myCLexer import myCLexer
from llvmlite import ir
from generator.symbolTable import SymbolTable, Structure
from generator.errorListener import syntaxErrorListener
from generator.errorListener import SemanticError

double = ir.DoubleType()
int1 = ir.IntType(1)
int32 = ir.IntType(32)
int8 = ir.IntType(8)
void = ir.VoidType()


class Visitor(myCVisitor):
    def __init__(self):
        super(myCVisitor, self).__init__()

        #控制llvm生成
        self.ARCH = 'x86_64' # or 'arm64'
        self.Module = ir.Module()
        self.Module.triple = f"{self.ARCH}-pc-linux-gnu" # llvm.Target.from_default_triple()
        self.Module.data_layout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128" # llvm.create_mcjit_compiler(backing_mod, target_machine)
        
        #语句块
        self.Blocks = []

        #待生成的llvm语句块
        self.Builders = []

        #函数列表
        self.Functions = dict()

        #结构体列表
        self.Structure = Structure()

        #当前所在函数
        self.CurrentFunction = ''
        self.Constants = 0

        #这个变量是否需要加载
        self.WhetherNeedLoad = True
        
        #endif块
        self.EndifBlock = None

        #符号表
        self.SymbolTable = SymbolTable()


    def visitProg(self, ctx:myCParser.ProgContext):
        '''
        语法规则：prog :(include)* (initialBlock|arrayInitBlock|structInitBlock|mStructDef|mFunction)*;
        描述：代码主文件
        返回：无
        '''
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i))

    #结构体相关函数
    def visitMStructDef(self, ctx:myCParser.MStructContext):
        NewStructName = ctx.getChild(0).getChild(1).getText()

        #遍历结构体的变量，并且存储
        i = 2
        ParameterTypeList = []
        ParameterNameList = []
        TotalParams = ctx.getChildCount() - 2
        #逐行读取并且存储
        while i < TotalParams:
            ParameterTypeLine, ParameterNameLine = self.visit(ctx.getChild(i))
            ParameterTypeList = ParameterTypeList + ParameterTypeLine
            ParameterNameList = ParameterNameList + ParameterNameLine
            i += 1

        #存储结构体
        TheResult = self.Structure.AddItem(NewStructName, ParameterNameList, ParameterTypeList)
        if TheResult["result"] != "success":
            raise SemanticError(ctx=ctx,msg=TheResult["reason"])

    def visitStructParam(self, ctx:myCParser.StructParamContext):
        ParameterTypeLine = []
        ParameterNameLine = []
        #必须有类型
        if ctx.getChild(0).getChildCount() == 1:
            i = 1
            ParameterType = self.visit(ctx.getChild(0))
            Length = ctx.getChildCount()
            while i < Length:
                #处理MID的情况（单一变量）
                if ctx.getChild(i).getChildCount() == 1:
                    ParameterNameLine.append(ctx.getChild(i).getText())
                    ParameterTypeLine.append(ParameterType)
                #处理mArray的情况（数组）
                else:
                    ArrayInfo = self.visit(ctx.getChild(i))
                    ParameterNameLine.append(ArrayInfo['IDname'])
                    ParameterTypeLine.append(ir.ArrayType(ParameterType, ArrayInfo['length']))
                i = i + 2
            return ParameterTypeLine, ParameterNameLine

    def visitStructInitBlock(self, ctx:myCParser.StructInitBlockContext):
        VariableInfo = self.visit(ctx.getChild(0))
        VariableType = VariableInfo['Type']
        StructName = ctx.getChild(0).getChild(1).getText()

        #处理结构体变量是单一变量的情况
        if ctx.getChild(1).getChildCount() == 1: 
            IDname = ctx.getChild(1).getText()
            CurrentType = VariableType
            #全局变量
            if self.SymbolTable.JudgeWhetherGlobal() == True:
                NewVariable = ir.GlobalVariable(self.Module, VariableType, name = IDname)
                NewVariable.linkage = 'internal'
                NewVariable.initializer = ir.Constant(CurrentType, None)
            #局部变量
            else:
                TheBuilder = self.Builders[-1]
                NewVariable = TheBuilder.alloca(CurrentType, name = IDname)

        #处理结构体变量是数组的情况
        else:
            VariableInfo = self.visit(ctx.getChild(1))
            IDname = VariableInfo['IDname']
            CurrentType = ir.ArrayType(VariableType, VariableInfo['length'])
            #全局变量
            if self.SymbolTable.JudgeWhetherGlobal() == True:
                NewVariable = ir.GlobalVariable(self.Module, CurrentType, name = IDname)
                NewVariable.linkage = 'internal'
                NewVariable.initializer = ir.Constant(CurrentType, None)
            else:
                TheBuilder = self.Builders[-1]
                NewVariable = TheBuilder.alloca(CurrentType, name = IDname)
        
        #存储这个结构体变量
        TheVariable = {}
        TheVariable["StructName"] = StructName
        TheVariable["Type"] = CurrentType
        TheVariable["Name"] = NewVariable
        TheResult = self.SymbolTable.AddItem(IDname, TheVariable)
        if TheResult["result"] != "success":
            raise SemanticError(ctx=ctx, msg=TheResult["reason"])
        return

    def visitStructMember(self, ctx:myCParser.StructMemberContext):
        TheBuilder = self.Builders[-1]
        #处理成员元素是单一变量的情况，TODO g4修改后删除
        if ctx.getChild(2).getChildCount() == 1: # mID
            CurrentNeedLoad = self.WhetherNeedLoad
            self.WhetherNeedLoad = False
            StructInfo = self.visit(ctx.getChild(0))
            self.WhetherNeedLoad = CurrentNeedLoad

            #读取结构体信息
            StructName = StructInfo['struct_name']
            FatherName = StructInfo["name"]
            Index = self.Structure.GetMemberIndex(StructName, ctx.getChild(2).getText())
            if Index == None:
                raise SemanticError(ctx=ctx, msg="未找到这个变量")
            Type = self.Structure.GetMemberType(StructName, ctx.getChild(2).getText())

            zero = ir.Constant(int32, 0)
            idx = ir.Constant(int32, Index)
            NewVariable = TheBuilder.gep(FatherName, [zero, idx], inbounds = True)
                
            if self.WhetherNeedLoad:
                NewVariable = TheBuilder.load(NewVariable)

            Result = {}
            Result["type"] = Type
            Result["name"] = NewVariable
            return Result
        else:
            raise NotImplementedError()

    #函数相关函数
    def visitMFunction(self, ctx:myCParser.MFunctionContext):

        #获取返回值类型
        ReturnType = self.visit(ctx.getChild(0)) # mtype
        
        #获取函数名 todo
        FunctionName = ctx.getChild(1).getText() # func name
        
        #获取参数列表
        ParameterList = self.visit(ctx.getChild(3)) # func params

        #根据返回值，函数名称和参数生成llvm函数
        ParameterTypeList = []
        for i in range(len(ParameterList)):
            ParameterTypeList.append(ParameterList[i]['type'])
        LLVMFunctionType = ir.FunctionType(ReturnType, ParameterTypeList)
        LLVMFunction = ir.Function(self.Module, LLVMFunctionType, name = FunctionName)

        #存储函数的变量        
        for i in range(len(ParameterList)):
            LLVMFunction.args[i].name = ParameterList[i]['IDname']

        #存储函数的block
        TheBlock = LLVMFunction.append_basic_block(name = FunctionName + '.entry')

        #判断重定义，存储函数
        if FunctionName in self.Functions:
            raise SemanticError(ctx=ctx,msg="函数重定义错误！")
        else:
            self.Functions[FunctionName] = LLVMFunction

        TheBuilder = ir.IRBuilder(TheBlock)
        self.Blocks.append(TheBlock)
        self.Builders.append(TheBuilder)

        #进一层
        self.CurrentFunction = FunctionName
        self.SymbolTable.EnterScope()

        #存储函数的变量
        VariableList = {}
        for i in range(len(ParameterList)):
            NewVariable = TheBuilder.alloca(ParameterList[i]['type'])
            TheBuilder.store(LLVMFunction.args[i], NewVariable)
            TheVariable = {}
            TheVariable["Type"] = ParameterList[i]['type']
            TheVariable["Name"] = NewVariable
            TheResult = self.SymbolTable.AddItem(ParameterList[i]['IDname'], TheVariable)
            if TheResult["result"] != "success":
                raise SemanticError(ctx=ctx,msg=TheResult["reason"])

        #处理函数body
        self.visit(ctx.getChild(6)) # func body

        #处理完毕，退一层
        self.CurrentFunction = ''
        self.Blocks.pop()
        self.Builders.pop()
        self.SymbolTable.QuitScope()
        return

    def visitParams(self, ctx:myCParser.ParamsContext):
        Length = ctx.getChildCount()
        if (Length == 0):
            return []
        ParameterList = []
        i = 0
        while i < Length:
            NewParameter = self.visit(ctx.getChild(i))
            ParameterList.append(NewParameter)
            i += 2
        return ParameterList

    def visitParam(self, ctx:myCParser.ParamContext):
        '''
        语法规则：param : mType mID;
        描述：返回函数参数
        返回：一个字典，字典的Type是类型，Name是参数名
        '''
        Type = self.visit(ctx.getChild(0))
        IDname = ctx.getChild(1).getText()
        Result = {'type': Type, 'IDname': IDname}
        return Result

    def visitFuncBody(self, ctx:myCParser.FuncBodyContext):
        self.SymbolTable.EnterScope()
        for index in range(ctx.getChildCount()):
            self.visit(ctx.getChild(index))
        self.SymbolTable.QuitScope()
        return

    def visitBody(self, ctx:myCParser.BodyContext):
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i))
            if self.Blocks[-1].is_terminated:
                break
        return

    #调用函数相关函数
    def visitFunc(self, ctx:myCParser.FuncContext):
        return self.visit(ctx.getChild(0))

    def visitStrlenFunc(self, ctx:myCParser.StrlenFuncContext):
        if 'strlen' in self.Functions:
            strlen = self.Functions['strlen']
        else:
            strlenType = ir.FunctionType(int32, [ir.PointerType(int8)], var_arg = False)
            strlen = ir.Function(self.Module, strlenType, name = "strlen")
            self.Functions['strlen'] = strlen

        TheBuilder = self.Builders[-1]
        zero = ir.Constant(int32, 0)

        #加载变量
        PreviousNeedLoad = self.WhetherNeedLoad
        self.WhetherNeedLoad = False
        res = self.visit(ctx.getChild(2))
        self.WhetherNeedLoad = PreviousNeedLoad

        Arguments = TheBuilder.gep(res['name'], [zero, zero], inbounds = True)
        ReturnVariableName = TheBuilder.call(strlen, [Arguments])

        Result = {'type': int32, 'name': ReturnVariableName}
        return Result

    def visitPrintfFunc(self, ctx:myCParser.PrintfFuncContext):      
        if 'printf' in self.Functions:
            printf = self.Functions['printf']
        else:
            printfType = ir.FunctionType(int32, [ir.PointerType(int8)], var_arg = True)
            printf = ir.Function(self.Module, printfType, name = "printf")
            self.Functions['printf'] = printf

        TheBuilder = self.Builders[-1]
        zero = ir.Constant(int32, 0)

        #就一个变量
        if ctx.getChildCount() == 4:
            ParameterInfo = self.visit(ctx.getChild(2)) 
            Argument = TheBuilder.gep(ParameterInfo['name'], [zero, zero], inbounds = True)
            ReturnVariableName = TheBuilder.call(printf, [Argument])
        else:
            ParameterInfo = self.visit(ctx.getChild(2))
            Arguments = [TheBuilder.gep(ParameterInfo['name'], [zero, zero], inbounds = True)]

            Length = ctx.getChildCount()
            i = 4
            while i < Length - 1:
                OneParameter = self.visit(ctx.getChild(i))
                Arguments.append(OneParameter['name'])
                i += 2
            ReturnVariableName = TheBuilder.call(printf, Arguments)
        Result = {'type': int32, 'name': ReturnVariableName}
        return Result


    def visitScanfFunc(self, ctx:myCParser.ScanfFuncContext):       
        if 'scanf' in self.Functions:
            scanf = self.Functions['scanf']
        else:
            scanfType = ir.FunctionType(int32, [ir.PointerType(int8)], var_arg = True)
            scanf = ir.Function(self.Module, scanfType, name="scanf")
            self.Functions['scanf'] = scanf

        TheBuilder = self.Builders[-1]
        zero = ir.Constant(int32, 0)
        ParameterList = self.visit(ctx.getChild(2)) # MString
        Arguments = [TheBuilder.gep(ParameterList['name'], [zero, zero], inbounds = True)]

        Length = ctx.getChildCount()
        i = 4
        while i < Length - 1:
            if ctx.getChild(i).getText() == '&':
                #读取变量
                PreviousNeedLoad = self.WhetherNeedLoad
                self.WhetherNeedLoad = False
                TheParameter = self.visit(ctx.getChild(i + 1))
                self.WhetherNeedLoad = PreviousNeedLoad
                Arguments.append(TheParameter['name'])
                i += 3
            else:
                PreviousNeedLoad = self.WhetherNeedLoad
                self.WhetherNeedLoad = True
                TheParameter = self.visit(ctx.getChild(i))
                self.WhetherNeedLoad = PreviousNeedLoad
                Arguments.append(TheParameter['name'])
                i += 2

        ReturnVariableName = TheBuilder.call(scanf, Arguments)
        Result = {'type': int32, 'name': ReturnVariableName}
        return Result


    def visitGetsFunc(self, ctx:myCParser.GetsFuncContext):     
        if 'gets' in self.Functions:
            gets = self.Functions['gets']
        else:
            getsType = ir.FunctionType(int32, [], var_arg = True)
            gets = ir.Function(self.Module, getsType, name = "gets")
            self.Functions['gets'] = gets

        TheBuilder = self.Builders[-1]
        zero = ir.Constant(int32, 0)

        PreviousNeedLoad = self.WhetherNeedLoad
        self.WhetherNeedLoad = False
        ParameterInfo = self.visit(ctx.getChild(2))
        self.WhetherNeedLoad = PreviousNeedLoad

        Arguments = [TheBuilder.gep(ParameterInfo['name'], [zero, zero], inbounds = True)]
        ReturnVariableName = TheBuilder.call(gets, Arguments)
        Result = {'type': int32, 'name': ReturnVariableName}
        return Result


    def visitSelfDefinedFunc(self, ctx:myCParser.SelfDefinedFuncContext):
        TheBuilder = self.Builders[-1]
        FunctionName = ctx.getChild(0).getText() # func name
        if FunctionName in self.Functions:
            TheFunction = self.Functions[FunctionName]

            Length = ctx.getChildCount()
            ParameterList = []
            i = 2
            while i < Length - 1:
                TheParameter = self.visit(ctx.getChild(i))
                TheParameter = self.assignConvert(TheParameter, TheFunction.args[i // 2 - 1].type)
                ParameterList.append(TheParameter['name'])
                i += 2
            ReturnVariableName = TheBuilder.call(TheFunction, ParameterList)
            Result = {'type': TheFunction.function_type.return_type, 'name': ReturnVariableName}
            return Result
        else:
            raise SemanticError(ctx=ctx,msg="函数未定义！")

    #语句块相关函数
    def visitBlock(self, ctx:myCParser.BlockContext):
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i))
        return

    def visitInitialBlock(self, ctx:myCParser.InitialBlockContext):
        #初始化全局变量
        ParameterType = self.visit(ctx.getChild(0))
        Length = ctx.getChildCount()
        
        i = 1
        while i < Length:
            IDname = ctx.getChild(i).getText()
            if self.SymbolTable.JudgeWhetherGlobal() == True:   
                NewVariable = ir.GlobalVariable(self.Module, ParameterType, name = IDname)
                NewVariable.linkage = 'internal'
            else:
                TheBuilder = self.Builders[-1]
                NewVariable = TheBuilder.alloca(ParameterType, name = IDname)
            TheVariable = {}
            TheVariable["Type"] = ParameterType
            TheVariable["Name"] = NewVariable
            TheResult = self.SymbolTable.AddItem(IDname, TheVariable)
            if TheResult["result"] != "success":
                raise SemanticError(ctx=ctx,msg=TheResult["reason"])

            if ctx.getChild(i + 1).getText() != '=':
                i += 2
            else:
                #初始化
                Value = self.visit(ctx.getChild(i + 2))
                if self.SymbolTable.JudgeWhetherGlobal() == True:   
                    #全局变量
                    NewVariable.initializer = ir.Constant(Value['type'], Value['name'].constant)
                    #print(Value['name'].constant)
                else:
                    #局部变量，可能有强制类型转换
                    Value = self.assignConvert(Value, ParameterType)
                    TheBuilder = self.Builders[-1]
                    TheBuilder.store(Value['name'], NewVariable)
                i += 4
        return

    def visitArrayInitBlock(self, ctx:myCParser.ArrayInitBlockContext):
        Type = self.visit(ctx.getChild(0))
        IDname = ctx.getChild(1).getText()
        Length = int(ctx.getChild(3).getText())

        if self.SymbolTable.JudgeWhetherGlobal() == True:   
            #全局变量
            NewVariable = ir.GlobalVariable(self.Module, ir.ArrayType(Type, Length), name = IDname)
            NewVariable.linkage = 'internal'
        else:
            TheBuilder = self.Builders[-1]
            NewVariable = TheBuilder.alloca(ir.ArrayType(Type, Length), name = IDname)

        TheVariable = {}
        TheVariable["Type"] = ir.ArrayType(Type, Length)
        TheVariable["Name"] = NewVariable
        TheResult = self.SymbolTable.AddItem(IDname, TheVariable)
        if TheResult["result"] != "success":
            raise SemanticError(ctx=ctx,msg=TheResult["reason"])
        return

    def visitAssignBlock(self, ctx:myCParser.AssignBlockContext):
        TheBuilder = self.Builders[-1]
        Length = ctx.getChildCount()
        IDname = ctx.getChild(0).getText()
        if not '[' in IDname and self.SymbolTable.JudgeExist(IDname) == False:
            raise SemanticError(ctx=ctx,msg="变量未定义！")

        #待赋值结果 
        ValueToBeAssigned = self.visit(ctx.getChild(Length - 2))

        i = 0
        Result = {'type': ValueToBeAssigned['type'], 'name': ValueToBeAssigned['name']}
        #遍历全部左边变量赋值
        while i < Length - 2:
            PreviousNeedLoad = self.WhetherNeedLoad
            self.WhetherNeedLoad = False
            TheVariable = self.visit(ctx.getChild(i))
            self.WhetherNeedLoad = PreviousNeedLoad

            TheValueToBeAssigned = ValueToBeAssigned
            TheValueToBeAssigned = self.assignConvert(TheValueToBeAssigned, TheVariable['type'])
            TheBuilder.store(TheValueToBeAssigned['name'], TheVariable['name'])
            if i > 0:
                ReturnVariable = TheBuilder.load(TheVariable['name'])
                Result = {'type': TheVariable['type'], 'name': ReturnVariable}
            i += 2
        return Result

    #TODO
    def visitCondition(self, ctx:myCParser.ConditionContext):

        result = self.visit(ctx.getChild(0))
        return self.toBoolean(result, notFlag=False)

    def visitIfBlocks(self, ctx:myCParser.IfBlocksContext):

        #增加两个block，对应If分支和If结束后的分支
        TheBuilder = self.Builders[-1]
        IfBlock = TheBuilder.append_basic_block()
        EndifBlock = TheBuilder.append_basic_block()
        TheBuilder.branch(IfBlock)

        #载入IfBlock
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(IfBlock)
        self.Builders.append(ir.IRBuilder(IfBlock))

        tmp = self.EndifBlock
        self.EndifBlock = EndifBlock
        Length = ctx.getChildCount()
        for i in range(Length):
            self.visit(ctx.getChild(i))  #分别处理每个if ,elseif, else块
        self.EndifBlock = tmp

        #结束后导向EndIf块
        blockTemp = self.Blocks.pop()
        builderTemp = self.Builders.pop()
        if not blockTemp.is_terminated:
            builderTemp.branch(EndifBlock)

        self.Blocks.append(EndifBlock)
        self.Builders.append(ir.IRBuilder(EndifBlock))
        return


    def visitIfBlock(self, ctx:myCParser.IfBlockContext):

        #在If块中，有True和False两种可能的导向
        self.SymbolTable.EnterScope()
        TheBuilder = self.Builders[-1]
        TrueBlock = TheBuilder.append_basic_block()
        FalseBlock = TheBuilder.append_basic_block()

        #根据condition结果转向某个代码块
        result = self.visit(ctx.getChild(2))
        TheBuilder.cbranch(result['name'], TrueBlock, FalseBlock)

        #如果condition为真，处理TrueBlock,即body部分
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(TrueBlock)
        self.Builders.append(ir.IRBuilder(TrueBlock))
        self.visit(ctx.getChild(5)) # body

        if not self.Blocks[-1].is_terminated:
            self.Builders[-1].branch(self.EndifBlock)

        #处理condition为假的代码部分
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(FalseBlock)
        self.Builders.append(ir.IRBuilder(FalseBlock))
        self.SymbolTable.QuitScope()
        return


    def visitElifBlock(self, ctx:myCParser.ElifBlockContext):
        #在ElseIf块中，有True和False两种可能的导向
        self.SymbolTable.EnterScope()
        TheBuilder = self.Builders[-1]
        TrueBlock = TheBuilder.append_basic_block()
        FalseBlock = TheBuilder.append_basic_block()

        #根据condition结果转向某个代码块
        result = self.visit(ctx.getChild(3))
        TheBuilder.cbranch(result['name'], TrueBlock, FalseBlock)
        
        #如果condition为真，处理TrueBlock,即body部分
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(TrueBlock)
        self.Builders.append(ir.IRBuilder(TrueBlock))
        self.visit(ctx.getChild(6)) # body

        if not self.Blocks[-1].is_terminated:
            self.Builders[-1].branch(self.EndifBlock)
        
        #处理condition为假的代码部分
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(FalseBlock)
        self.Builders.append(ir.IRBuilder(FalseBlock))
        self.SymbolTable.QuitScope()
        return


    def visitElseBlock(self, ctx:myCParser.ElseBlockContext):
        #Else分块直接处理body内容
        self.SymbolTable.EnterScope()
        self.visit(ctx.getChild(2)) # body
        self.SymbolTable.QuitScope()
        return

    def visitWhileBlock(self, ctx:myCParser.WhileBlockContext):
        self.SymbolTable.EnterScope()
        TheBuilder = self.Builders[-1]
        #while语句分为三个分块
        WhileCondition = TheBuilder.append_basic_block()
        WhileBody = TheBuilder.append_basic_block()
        WhileEnd = TheBuilder.append_basic_block()

        #首先执行Condition分块
        TheBuilder.branch(WhileCondition)
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(WhileCondition)
        self.Builders.append(ir.IRBuilder(WhileCondition))
        
        #根据condition结果决定执行body还是结束while循环
        result = self.visit(ctx.getChild(2)) # condition
        self.Builders[-1].cbranch(result['name'], WhileBody, WhileEnd)
        
        #执行body
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(WhileBody)
        self.Builders.append(ir.IRBuilder(WhileBody))
        self.visit(ctx.getChild(5)) # body

        #执行body后重新判断condition
        self.Builders[-1].branch(WhileCondition)

        #结束while循环
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(WhileEnd)
        self.Builders.append(ir.IRBuilder(WhileEnd))
        self.SymbolTable.QuitScope()
        return


    def visitForBlock(self, ctx:myCParser.ForBlockContext):
        self.SymbolTable.EnterScope()
        
        #for循环首先初始化局部变量
        self.visit(ctx.getChild(2))
        #for循环的三种block
        TheBuilder = self.Builders[-1]
        ForCondition = TheBuilder.append_basic_block()
        ForBody = TheBuilder.append_basic_block()
        ForEnd = TheBuilder.append_basic_block()
       
        #判断condition
        TheBuilder.branch(ForCondition)
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(ForCondition)
        self.Builders.append(ir.IRBuilder(ForCondition))
                
        #根据condition结果决定跳转到body或者结束
        result = self.visit(ctx.getChild(4)) # condition block
        self.Builders[-1].cbranch(result['name'], ForBody, ForEnd)
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(ForBody)
        self.Builders.append(ir.IRBuilder(ForBody))

        #处理body
        if (ctx.getChildCount() == 11):
            self.visit(ctx.getChild(9)) # main body
        
        #处理step语句
        self.visit(ctx.getChild(6)) # step block
        
        #一次循环后重新判断condition
        self.Builders[-1].branch(ForCondition)

        #结束循环
        self.Blocks.pop()
        self.Builders.pop()
        self.Blocks.append(ForEnd)
        self.Builders.append(ir.IRBuilder(ForEnd))
        self.SymbolTable.QuitScope()
        return

    def visitFor1Block(self, ctx:myCParser.For1BlockContext):
        '''
        语法规则：for1Block :  mID '=' expr (',' for1Block)?|;
        描述：for语句块的第一个参数
        返回：无
        '''
        #初始化参数为空
        Length = ctx.getChildCount()
        if Length == 0:
            return

        TmpNeedLoad = self.WhetherNeedLoad
        self.WhetherNeedLoad = False
        result0 = self.visit(ctx.getChild(0)) # mID
        self.WhetherNeedLoad = TmpNeedLoad
        
        #访问表达式
        result1 = self.visit(ctx.getChild(2)) # expr
        result1 = self.assignConvert(result1, result0['type'])
        self.Builders[-1].store(result1['name'], result0['name'])

        if Length > 3:
            self.visit(ctx.getChild(4))
        return


    def visitFor3Block(self, ctx:myCParser.For3BlockContext):
        Length = ctx.getChildCount()
        if Length == 0:
            return
            
        TmpNeedLoad = self.WhetherNeedLoad
        self.WhetherNeedLoad = False
        result0 = self.visit(ctx.getChild(0))
        self.WhetherNeedLoad = TmpNeedLoad

        result1 = self.visit(ctx.getChild(2))
        result1 = self.assignConvert(result1, result0['type'])
        self.Builders[-1].store(result1['name'], result0['name'])

        if Length > 3:
            self.visit(ctx.getChild(4))
        return


    def visitReturnBlock(self, ctx:myCParser.ReturnBlockContext):
        #返回空
        if ctx.getChildCount() == 2:
            RealReturnValue = self.Builders[-1].ret_void()
            JudgeTruth = False
            return {
                    'type': void,
                    'const': JudgeTruth,
                    'name': RealReturnValue
            }

        #访问返回值
        ReturnIndex = self.visit(ctx.getChild(1))
        RealReturnValue = self.Builders[-1].ret(ReturnIndex['name'])
        JudgeTruth = False
        return {
                'type': void,
                'const': JudgeTruth,
                'name': RealReturnValue
        }


    #运算和表达式求值，类型转换相关函数
    def assignConvert(self, CalcIndex, DType):
        if (CalcIndex['type'] == DType):
            return CalcIndex
        if self.isInteger(CalcIndex['type']) and self.isInteger(DType):
            if (CalcIndex['type'] == int1):
                CalcIndex = self.convertIIZ(CalcIndex, DType)
            else:
                CalcIndex = self.convertIIS(CalcIndex, DType)
        elif self.isInteger(CalcIndex['type']) and DType == double:
            CalcIndex = self.convertIDS(CalcIndex)
        elif self.isInteger(DType) and CalcIndex['type'] == double:
            CalcIndex = self.convertDIS(CalcIndex)
        return CalcIndex
    
    def convertIIZ(self, CalcIndex, DType):
        Builder = self.Builders[-1]
        ConfirmedVal = Builder.zext(CalcIndex['name'], DType)
        JudgeReg = False
        return {
                'type': DType,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    def convertIIS(self, CalcIndex, DType):
        Builder = self.Builders[-1]
        ConfirmedVal = Builder.sext(CalcIndex['name'], DType)
        JudgeReg = False
        return {
                'type': DType,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    def convertDIS(self, CalcIndex, DType):
        Builder = self.Builders[-1]
        ConfirmedVal = Builder.fptosi(CalcIndex['name'], DType)
        JudgeReg = False
        return {
                'type': DType,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    def convertDIU(self, CalcIndex, DType):
        Builder = self.Builders[-1]
        ConfirmedVal = Builder.fptoui(CalcIndex['name'], DType)
        JudgeReg = False
        return {
                'type': DType,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    def convertIDS(self, CalcIndex):
        Builder = self.Builders[-1]
        ConfirmedVal = Builder.sitofp(CalcIndex['name'], double)
        JudgeReg = False
        return {
                'type': double,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    def convertIDU(self, CalcIndex):
        Builder = self.Builders[-1]
        JudgeReg = False
        ConfirmedVal = Builder.uitofp(CalcIndex['name'], double)
        return {
                'type': double,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    # 类型转换至布尔型
    def toBoolean(self, ManipulateIndex, notFlag = True):
        Builder = self.Builders[-1]
        if notFlag:
            OperationChar = '=='
        else:
            OperationChar = '!='
        if ManipulateIndex['type'] == int8 or ManipulateIndex['type'] == int32:
            RealReturnValue = Builder.icmp_signed(OperationChar, ManipulateIndex['name'], ir.Constant(ManipulateIndex['type'], 0))
            return {
                    'tpye': int1,
                    'const': False,
                    'name': RealReturnValue
            }
        elif ManipulateIndex['type'] == double:
            RealReturnValue = Builder.fcmp_ordered(OperationChar, ManipulateIndex['name'], ir.Constant(double, 0))
            return {
                    'tpye': int1,
                    'const': False,
                    'name': RealReturnValue
            }
        return ManipulateIndex

    def visitNeg(self, ctx:myCParser.NegContext):
        RealReturnValue = self.visit(ctx.getChild(1))
        RealReturnValue = self.toBoolean(RealReturnValue, notFlag = True)
        # res 未返回
        return self.visitChildren(ctx)


    def visitOR(self, ctx:myCParser.ORContext):
        Index1 = self.visit(ctx.getChild(0))
        Index1 = self.toBoolean(Index1, notFlag=False)
        Index2 = self.visit(ctx.getChild(2))
        Index2 = self.toBoolean(Index2, notFlag=False)
        Builder = self.Builders[-1]
        RealReturnValue = Builder.or_(Index1['name'], Index2['name'])
        return {
                'type': Index1['type'],
                'const': False,
                'name': RealReturnValue
        }

    def visitAND(self, ctx:myCParser.ANDContext):
        Index1 = self.visit(ctx.getChild(0))
        Index1 = self.toBoolean(Index1, notFlag=False)
        Index2 = self.visit(ctx.getChild(2))
        Index2 = self.toBoolean(Index2, notFlag=False)
        Builder = self.Builders[-1]
        JudgeReg = False
        RealReturnValue = Builder.and_(Index1['name'], Index2['name'])
        return {
                'type': Index1['type'],
                'const': JudgeReg,
                'name': RealReturnValue
        }


    def visitIdentifier(self, ctx:myCParser.IdentifierContext):
        return self.visit(ctx.getChild(0))


    def visitParens(self, ctx:myCParser.ParensContext):
        return self.visit(ctx.getChild(1))


    def visitArrayitem(self, ctx:myCParser.ArrayitemContext):
        return self.visit(ctx.getChild(0))


    def visitString(self, ctx:myCParser.StringContext):
        return self.visit(ctx.getChild(0))


    def isInteger(self, typ):
        ReturnValue = 'width'
        return hasattr(typ, ReturnValue)


    def exprConvert(self, Index1, Index2):
        if Index1['type'] == Index2['type']:
            return Index1, Index2
        if self.isInteger(Index1['type']) and self.isInteger(Index2['type']):
            if Index1['type'].width < Index2['type'].width:
                if Index1['type'].width == 1:
                    Index1 = self.convertIIZ(Index1, Index2['type'])
                else:
                    Index1 = self.convertIIS(Index1, Index2['type'])
            else:
                if Index2['type'].width == 1:
                    Index2 = self.convertIIZ(Index2, Index1['type'])
                else:
                    Index2 = self.convertIIS(Index2, Index1['type'])
        elif self.isInteger(Index1['type']) and Index2['type'] == double:
            Index1 = self.convertIDS(Index1, Index2['type'])
        elif self.isInteger(Index2['type']) and Index1['type'] == double:
            Index2 = self.convertIDS(Index2, Index1['type'])
        else:
            raise SemanticError(ctx=self.ctx,msg="类型不匹配")
        return Index1, Index2


    def visitMulDiv(self, ctx:myCParser.MulDivContext):
        Builder = self.Builders[-1]
        Index1 = self.visit(ctx.getChild(0))
        Index2 = self.visit(ctx.getChild(2))
        Index1, Index2 = self.exprConvert(Index1, Index2)
        JudgeReg = False
        if ctx.getChild(1).getText() == '*':
            RealReturnValue = Builder.mul(Index1['name'], Index2['name'])
        elif ctx.getChild(1).getText() == '/':
            RealReturnValue = Builder.sdiv(Index1['name'], Index2['name'])
        elif ctx.getChild(1).getText() == '%':
            RealReturnValue = Builder.srem(Index1['name'], Index2['name'])
        return {
                'type': Index1['type'],
                'const': JudgeReg,
                'name': RealReturnValue
        }


    def visitAddSub(self, ctx:myCParser.AddSubContext):
        Builder = self.Builders[-1]
        Index1 = self.visit(ctx.getChild(0))
        Index2 = self.visit(ctx.getChild(2))
        Index1, Index2 = self.exprConvert(Index1, Index2)
        JudgeReg = False
        if ctx.getChild(1).getText() == '+':
            RealReturnValue = Builder.add(Index1['name'], Index2['name'])
        elif ctx.getChild(1).getText() == '-':
            RealReturnValue = Builder.sub(Index1['name'], Index2['name'])
        return {
                'type': Index1['type'],
                'const': JudgeReg,
                'name': RealReturnValue
        }


    def visitDouble(self, ctx:myCParser.DoubleContext):
        if ctx.getChild(0).getText() == '-':
            IndexMid = self.visit(ctx.getChild(1))
            Builder = self.Builders[-1]
            RealReturnValue = Builder.neg(IndexMid['name'])
            return {
                    'type': IndexMid['type'],
                    'name': RealReturnValue
            }
        return self.visit(ctx.getChild(0))


    def visitFunction(self, ctx:myCParser.FunctionContext):
        return self.visit(ctx.getChild(0))


    def visitChar(self, ctx:myCParser.CharContext):
        return self.visit(ctx.getChild(0))


    def visitInt(self, ctx:myCParser.IntContext):
        if ctx.getChild(0).getText() == '-':
            IndexMid = self.visit(ctx.getChild(1))
            Builder = self.Builders[-1]
            RealReturnValue = Builder.neg(IndexMid['name'])
            return {
                    'type': IndexMid['type'],
                    'name': RealReturnValue
            }
        return self.visit(ctx.getChild(0))


    def visitMVoid(self, ctx:myCParser.MVoidContext):
        return void

    def visitMArray(self, ctx:myCParser.MArrayContext):
        return {
            'IDname': ctx.getChild(0).getText(),
            'length': int(ctx.getChild(2).getText())
        }

    def visitJudge(self, ctx:myCParser.JudgeContext):
        Builder = self.Builders[-1]
        Index1 = self.visit(ctx.getChild(0))
        Index2 = self.visit(ctx.getChild(2))
        Index1, Index2 = self.exprConvert(Index1, Index2)
        OperationChar = ctx.getChild(1).getText()
        JudgeReg = False
        if Index1['type'] == double:
            RealReturnValue = Builder.fcmp_ordered(OperationChar, Index1['name'], Index2['name'])
        elif self.isInteger(Index1['type']):
            RealReturnValue = Builder.icmp_signed(OperationChar, Index1['name'], Index2['name'])
        return {
                'type': int1,
                'const': JudgeReg,
                'name': RealReturnValue
        }

    #变量和变量类型相关函数
    def visitMType(self, ctx:myCParser.MTypeContext):
        if ctx.getText() == 'int':
            return int32
        if ctx.getText() == 'char':
            return int8
        if ctx.getText() == 'double':
            return double
        return void

    def visitArrayItem(self, ctx:myCParser.ArrayItemContext):
        TempRequireLoad = self.WhetherNeedLoad
        self.WhetherNeedLoad = False
        res = self.visit(ctx.getChild(0)) # mID
        # print("res is", res)
        JudgeReg = False
        self.WhetherNeedLoad = TempRequireLoad
        
        if isinstance(res['type'], ir.types.ArrayType):
            Builder = self.Builders[-1]

            TempRequireLoad = self.WhetherNeedLoad
            self.WhetherNeedLoad = True
            IndexRe1 = self.visit(ctx.getChild(2)) # subscript
            self.WhetherNeedLoad = TempRequireLoad
            
            Int32Zero = ir.Constant(int32, 0)
            RealReturnValue = Builder.gep(res['name'], [Int32Zero, IndexRe1['name']], inbounds=True)
            if self.WhetherNeedLoad:
                RealReturnValue = Builder.load(RealReturnValue)
            return {
                    'type': res['type'].element,
                    'const': JudgeReg,
                    'name': RealReturnValue,
                    'struct_name': res['struct_name'] if 'struct_name' in res else None
            }
        else:   # error!
            raise SemanticError(ctx=ctx,msg="类型错误")

    def visitArgument(self, ctx:myCParser.ArgumentContext):
        return self.visit(ctx.getChild(0))

    def visitMStruct(self, ctx:myCParser.MStructContext):
        return self.Structure.List[ctx.getChild(1).getText()]

    def visitMID(self, ctx:myCParser.MIDContext):
        IDname = ctx.getText()
        JudgeReg = False
        if self.SymbolTable.JudgeExist(IDname) != True:
           return {
                'type': int32,
                'const': JudgeReg,
                'name': ir.Constant(int32, None)
            }
        Builder = self.Builders[-1]
        TheItem = self.SymbolTable.GetItem(IDname)
        # print(TheItem)
        if TheItem != None:
            if self.WhetherNeedLoad:
                ReturnValue = Builder.load(TheItem["Name"])
                return {
                    "type" : TheItem["Type"],
                    "const" : JudgeReg,
                    "name" : ReturnValue,
                    "struct_name" : TheItem["StructName"] if "StructName" in TheItem else None
                }
            else:
                return {
                    "type" : TheItem["Type"],
                    "const" : JudgeReg,
                    "name" : TheItem["Name"],
                    "struct_name" : TheItem["StructName"] if "StructName" in TheItem else None
                }
        else:
            return {
                'type': void,
                'const': JudgeReg,
                'name': ir.Constant(void, None)
            }

    def visitMINT(self, ctx:myCParser.MINTContext):
        JudgeReg = True
        return {
                'type': int32,
                'const': JudgeReg,
                'name': ir.Constant(int32, int(ctx.getText()))
        }

    def visitMDOUBLE(self, ctx:myCParser.MDOUBLEContext):
        JudgeReg = True
        return {
                'type': double,
                'const': JudgeReg,
                'name': ir.Constant(double, float(ctx.getText()))
        }

    def visitMCHAR(self, ctx:myCParser.MCHARContext):
        JudgeReg = True
        return {
                'type': int8,
                'const': JudgeReg,
                'name': ir.Constant(int8, ord(ctx.getText()[1]))
        }

    def visitMSTRING(self, ctx:myCParser.MSTRINGContext):
        MarkIndex = self.Constants
        self.Constants += 1
        ProcessIndex = ctx.getText().replace('\\n', '\n')
        ProcessIndex = ProcessIndex[1:-1]
        ProcessIndex += '\0'
        Len = len(bytearray(ProcessIndex, 'utf-8'))
        JudgeReg = False
        RealReturnValue = ir.GlobalVariable(self.Module, ir.ArrayType(int8, Len), ".str%d"%MarkIndex)
        RealReturnValue.global_constant = True
        RealReturnValue.initializer = ir.Constant(ir.ArrayType(int8, Len), bytearray(ProcessIndex, 'utf-8'))
        return {
                'type': ir.ArrayType(int8, Len),
                'const': JudgeReg,
                'name': RealReturnValue
        }

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(repr(self.Module))

def generate(input_filename, output_filename):
    lexer = myCLexer(FileStream(input_filename))
    stream = CommonTokenStream(lexer)
    parser = myCParser(stream)
    parser.removeErrorListeners()
    errorListener = syntaxErrorListener()
    parser.addErrorListener(errorListener)

    tree = parser.prog()
    v = Visitor()
    v.visit(tree)
    v.save(output_filename)

