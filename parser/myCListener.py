# Generated from myC.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .myCParser import myCParser
else:
    from myCParser import myCParser

# This class defines a complete listener for a parse tree produced by myCParser.
class myCListener(ParseTreeListener):

    # Enter a parse tree produced by myCParser#prog.
    def enterProg(self, ctx:myCParser.ProgContext):
        pass

    # Exit a parse tree produced by myCParser#prog.
    def exitProg(self, ctx:myCParser.ProgContext):
        pass


    # Enter a parse tree produced by myCParser#include.
    def enterInclude(self, ctx:myCParser.IncludeContext):
        pass

    # Exit a parse tree produced by myCParser#include.
    def exitInclude(self, ctx:myCParser.IncludeContext):
        pass


    # Enter a parse tree produced by myCParser#mStructDef.
    def enterMStructDef(self, ctx:myCParser.MStructDefContext):
        pass

    # Exit a parse tree produced by myCParser#mStructDef.
    def exitMStructDef(self, ctx:myCParser.MStructDefContext):
        pass


    # Enter a parse tree produced by myCParser#structParam.
    def enterStructParam(self, ctx:myCParser.StructParamContext):
        pass

    # Exit a parse tree produced by myCParser#structParam.
    def exitStructParam(self, ctx:myCParser.StructParamContext):
        pass


    # Enter a parse tree produced by myCParser#mFunction.
    def enterMFunction(self, ctx:myCParser.MFunctionContext):
        pass

    # Exit a parse tree produced by myCParser#mFunction.
    def exitMFunction(self, ctx:myCParser.MFunctionContext):
        pass


    # Enter a parse tree produced by myCParser#params.
    def enterParams(self, ctx:myCParser.ParamsContext):
        pass

    # Exit a parse tree produced by myCParser#params.
    def exitParams(self, ctx:myCParser.ParamsContext):
        pass


    # Enter a parse tree produced by myCParser#param.
    def enterParam(self, ctx:myCParser.ParamContext):
        pass

    # Exit a parse tree produced by myCParser#param.
    def exitParam(self, ctx:myCParser.ParamContext):
        pass


    # Enter a parse tree produced by myCParser#funcBody.
    def enterFuncBody(self, ctx:myCParser.FuncBodyContext):
        pass

    # Exit a parse tree produced by myCParser#funcBody.
    def exitFuncBody(self, ctx:myCParser.FuncBodyContext):
        pass


    # Enter a parse tree produced by myCParser#body.
    def enterBody(self, ctx:myCParser.BodyContext):
        pass

    # Exit a parse tree produced by myCParser#body.
    def exitBody(self, ctx:myCParser.BodyContext):
        pass


    # Enter a parse tree produced by myCParser#block.
    def enterBlock(self, ctx:myCParser.BlockContext):
        pass

    # Exit a parse tree produced by myCParser#block.
    def exitBlock(self, ctx:myCParser.BlockContext):
        pass


    # Enter a parse tree produced by myCParser#initialBlock.
    def enterInitialBlock(self, ctx:myCParser.InitialBlockContext):
        pass

    # Exit a parse tree produced by myCParser#initialBlock.
    def exitInitialBlock(self, ctx:myCParser.InitialBlockContext):
        pass


    # Enter a parse tree produced by myCParser#arrayInitBlock.
    def enterArrayInitBlock(self, ctx:myCParser.ArrayInitBlockContext):
        pass

    # Exit a parse tree produced by myCParser#arrayInitBlock.
    def exitArrayInitBlock(self, ctx:myCParser.ArrayInitBlockContext):
        pass


    # Enter a parse tree produced by myCParser#structInitBlock.
    def enterStructInitBlock(self, ctx:myCParser.StructInitBlockContext):
        pass

    # Exit a parse tree produced by myCParser#structInitBlock.
    def exitStructInitBlock(self, ctx:myCParser.StructInitBlockContext):
        pass


    # Enter a parse tree produced by myCParser#assignBlock.
    def enterAssignBlock(self, ctx:myCParser.AssignBlockContext):
        pass

    # Exit a parse tree produced by myCParser#assignBlock.
    def exitAssignBlock(self, ctx:myCParser.AssignBlockContext):
        pass


    # Enter a parse tree produced by myCParser#ifBlocks.
    def enterIfBlocks(self, ctx:myCParser.IfBlocksContext):
        pass

    # Exit a parse tree produced by myCParser#ifBlocks.
    def exitIfBlocks(self, ctx:myCParser.IfBlocksContext):
        pass


    # Enter a parse tree produced by myCParser#ifBlock.
    def enterIfBlock(self, ctx:myCParser.IfBlockContext):
        pass

    # Exit a parse tree produced by myCParser#ifBlock.
    def exitIfBlock(self, ctx:myCParser.IfBlockContext):
        pass


    # Enter a parse tree produced by myCParser#elifBlock.
    def enterElifBlock(self, ctx:myCParser.ElifBlockContext):
        pass

    # Exit a parse tree produced by myCParser#elifBlock.
    def exitElifBlock(self, ctx:myCParser.ElifBlockContext):
        pass


    # Enter a parse tree produced by myCParser#elseBlock.
    def enterElseBlock(self, ctx:myCParser.ElseBlockContext):
        pass

    # Exit a parse tree produced by myCParser#elseBlock.
    def exitElseBlock(self, ctx:myCParser.ElseBlockContext):
        pass


    # Enter a parse tree produced by myCParser#condition.
    def enterCondition(self, ctx:myCParser.ConditionContext):
        pass

    # Exit a parse tree produced by myCParser#condition.
    def exitCondition(self, ctx:myCParser.ConditionContext):
        pass


    # Enter a parse tree produced by myCParser#whileBlock.
    def enterWhileBlock(self, ctx:myCParser.WhileBlockContext):
        pass

    # Exit a parse tree produced by myCParser#whileBlock.
    def exitWhileBlock(self, ctx:myCParser.WhileBlockContext):
        pass


    # Enter a parse tree produced by myCParser#forBlock.
    def enterForBlock(self, ctx:myCParser.ForBlockContext):
        pass

    # Exit a parse tree produced by myCParser#forBlock.
    def exitForBlock(self, ctx:myCParser.ForBlockContext):
        pass


    # Enter a parse tree produced by myCParser#for1Block.
    def enterFor1Block(self, ctx:myCParser.For1BlockContext):
        pass

    # Exit a parse tree produced by myCParser#for1Block.
    def exitFor1Block(self, ctx:myCParser.For1BlockContext):
        pass


    # Enter a parse tree produced by myCParser#for3Block.
    def enterFor3Block(self, ctx:myCParser.For3BlockContext):
        pass

    # Exit a parse tree produced by myCParser#for3Block.
    def exitFor3Block(self, ctx:myCParser.For3BlockContext):
        pass


    # Enter a parse tree produced by myCParser#returnBlock.
    def enterReturnBlock(self, ctx:myCParser.ReturnBlockContext):
        pass

    # Exit a parse tree produced by myCParser#returnBlock.
    def exitReturnBlock(self, ctx:myCParser.ReturnBlockContext):
        pass


    # Enter a parse tree produced by myCParser#identifier.
    def enterIdentifier(self, ctx:myCParser.IdentifierContext):
        pass

    # Exit a parse tree produced by myCParser#identifier.
    def exitIdentifier(self, ctx:myCParser.IdentifierContext):
        pass


    # Enter a parse tree produced by myCParser#parens.
    def enterParens(self, ctx:myCParser.ParensContext):
        pass

    # Exit a parse tree produced by myCParser#parens.
    def exitParens(self, ctx:myCParser.ParensContext):
        pass


    # Enter a parse tree produced by myCParser#OR.
    def enterOR(self, ctx:myCParser.ORContext):
        pass

    # Exit a parse tree produced by myCParser#OR.
    def exitOR(self, ctx:myCParser.ORContext):
        pass


    # Enter a parse tree produced by myCParser#string.
    def enterString(self, ctx:myCParser.StringContext):
        pass

    # Exit a parse tree produced by myCParser#string.
    def exitString(self, ctx:myCParser.StringContext):
        pass


    # Enter a parse tree produced by myCParser#MulDiv.
    def enterMulDiv(self, ctx:myCParser.MulDivContext):
        pass

    # Exit a parse tree produced by myCParser#MulDiv.
    def exitMulDiv(self, ctx:myCParser.MulDivContext):
        pass


    # Enter a parse tree produced by myCParser#AddSub.
    def enterAddSub(self, ctx:myCParser.AddSubContext):
        pass

    # Exit a parse tree produced by myCParser#AddSub.
    def exitAddSub(self, ctx:myCParser.AddSubContext):
        pass


    # Enter a parse tree produced by myCParser#double.
    def enterDouble(self, ctx:myCParser.DoubleContext):
        pass

    # Exit a parse tree produced by myCParser#double.
    def exitDouble(self, ctx:myCParser.DoubleContext):
        pass


    # Enter a parse tree produced by myCParser#int.
    def enterInt(self, ctx:myCParser.IntContext):
        pass

    # Exit a parse tree produced by myCParser#int.
    def exitInt(self, ctx:myCParser.IntContext):
        pass


    # Enter a parse tree produced by myCParser#Neg.
    def enterNeg(self, ctx:myCParser.NegContext):
        pass

    # Exit a parse tree produced by myCParser#Neg.
    def exitNeg(self, ctx:myCParser.NegContext):
        pass


    # Enter a parse tree produced by myCParser#arrayitem.
    def enterArrayitem(self, ctx:myCParser.ArrayitemContext):
        pass

    # Exit a parse tree produced by myCParser#arrayitem.
    def exitArrayitem(self, ctx:myCParser.ArrayitemContext):
        pass


    # Enter a parse tree produced by myCParser#function.
    def enterFunction(self, ctx:myCParser.FunctionContext):
        pass

    # Exit a parse tree produced by myCParser#function.
    def exitFunction(self, ctx:myCParser.FunctionContext):
        pass


    # Enter a parse tree produced by myCParser#AND.
    def enterAND(self, ctx:myCParser.ANDContext):
        pass

    # Exit a parse tree produced by myCParser#AND.
    def exitAND(self, ctx:myCParser.ANDContext):
        pass


    # Enter a parse tree produced by myCParser#char.
    def enterChar(self, ctx:myCParser.CharContext):
        pass

    # Exit a parse tree produced by myCParser#char.
    def exitChar(self, ctx:myCParser.CharContext):
        pass


    # Enter a parse tree produced by myCParser#structmember.
    def enterStructmember(self, ctx:myCParser.StructmemberContext):
        pass

    # Exit a parse tree produced by myCParser#structmember.
    def exitStructmember(self, ctx:myCParser.StructmemberContext):
        pass


    # Enter a parse tree produced by myCParser#Judge.
    def enterJudge(self, ctx:myCParser.JudgeContext):
        pass

    # Exit a parse tree produced by myCParser#Judge.
    def exitJudge(self, ctx:myCParser.JudgeContext):
        pass


    # Enter a parse tree produced by myCParser#mType.
    def enterMType(self, ctx:myCParser.MTypeContext):
        pass

    # Exit a parse tree produced by myCParser#mType.
    def exitMType(self, ctx:myCParser.MTypeContext):
        pass


    # Enter a parse tree produced by myCParser#mArray.
    def enterMArray(self, ctx:myCParser.MArrayContext):
        pass

    # Exit a parse tree produced by myCParser#mArray.
    def exitMArray(self, ctx:myCParser.MArrayContext):
        pass


    # Enter a parse tree produced by myCParser#mVoid.
    def enterMVoid(self, ctx:myCParser.MVoidContext):
        pass

    # Exit a parse tree produced by myCParser#mVoid.
    def exitMVoid(self, ctx:myCParser.MVoidContext):
        pass


    # Enter a parse tree produced by myCParser#mStruct.
    def enterMStruct(self, ctx:myCParser.MStructContext):
        pass

    # Exit a parse tree produced by myCParser#mStruct.
    def exitMStruct(self, ctx:myCParser.MStructContext):
        pass


    # Enter a parse tree produced by myCParser#structMember.
    def enterStructMember(self, ctx:myCParser.StructMemberContext):
        pass

    # Exit a parse tree produced by myCParser#structMember.
    def exitStructMember(self, ctx:myCParser.StructMemberContext):
        pass


    # Enter a parse tree produced by myCParser#arrayItem.
    def enterArrayItem(self, ctx:myCParser.ArrayItemContext):
        pass

    # Exit a parse tree produced by myCParser#arrayItem.
    def exitArrayItem(self, ctx:myCParser.ArrayItemContext):
        pass


    # Enter a parse tree produced by myCParser#func.
    def enterFunc(self, ctx:myCParser.FuncContext):
        pass

    # Exit a parse tree produced by myCParser#func.
    def exitFunc(self, ctx:myCParser.FuncContext):
        pass


    # Enter a parse tree produced by myCParser#strlenFunc.
    def enterStrlenFunc(self, ctx:myCParser.StrlenFuncContext):
        pass

    # Exit a parse tree produced by myCParser#strlenFunc.
    def exitStrlenFunc(self, ctx:myCParser.StrlenFuncContext):
        pass


    # Enter a parse tree produced by myCParser#atoiFunc.
    def enterAtoiFunc(self, ctx:myCParser.AtoiFuncContext):
        pass

    # Exit a parse tree produced by myCParser#atoiFunc.
    def exitAtoiFunc(self, ctx:myCParser.AtoiFuncContext):
        pass


    # Enter a parse tree produced by myCParser#printfFunc.
    def enterPrintfFunc(self, ctx:myCParser.PrintfFuncContext):
        pass

    # Exit a parse tree produced by myCParser#printfFunc.
    def exitPrintfFunc(self, ctx:myCParser.PrintfFuncContext):
        pass


    # Enter a parse tree produced by myCParser#scanfFunc.
    def enterScanfFunc(self, ctx:myCParser.ScanfFuncContext):
        pass

    # Exit a parse tree produced by myCParser#scanfFunc.
    def exitScanfFunc(self, ctx:myCParser.ScanfFuncContext):
        pass


    # Enter a parse tree produced by myCParser#getsFunc.
    def enterGetsFunc(self, ctx:myCParser.GetsFuncContext):
        pass

    # Exit a parse tree produced by myCParser#getsFunc.
    def exitGetsFunc(self, ctx:myCParser.GetsFuncContext):
        pass


    # Enter a parse tree produced by myCParser#selfDefinedFunc.
    def enterSelfDefinedFunc(self, ctx:myCParser.SelfDefinedFuncContext):
        pass

    # Exit a parse tree produced by myCParser#selfDefinedFunc.
    def exitSelfDefinedFunc(self, ctx:myCParser.SelfDefinedFuncContext):
        pass


    # Enter a parse tree produced by myCParser#argument.
    def enterArgument(self, ctx:myCParser.ArgumentContext):
        pass

    # Exit a parse tree produced by myCParser#argument.
    def exitArgument(self, ctx:myCParser.ArgumentContext):
        pass


    # Enter a parse tree produced by myCParser#mID.
    def enterMID(self, ctx:myCParser.MIDContext):
        pass

    # Exit a parse tree produced by myCParser#mID.
    def exitMID(self, ctx:myCParser.MIDContext):
        pass


    # Enter a parse tree produced by myCParser#mINT.
    def enterMINT(self, ctx:myCParser.MINTContext):
        pass

    # Exit a parse tree produced by myCParser#mINT.
    def exitMINT(self, ctx:myCParser.MINTContext):
        pass


    # Enter a parse tree produced by myCParser#mDOUBLE.
    def enterMDOUBLE(self, ctx:myCParser.MDOUBLEContext):
        pass

    # Exit a parse tree produced by myCParser#mDOUBLE.
    def exitMDOUBLE(self, ctx:myCParser.MDOUBLEContext):
        pass


    # Enter a parse tree produced by myCParser#mCHAR.
    def enterMCHAR(self, ctx:myCParser.MCHARContext):
        pass

    # Exit a parse tree produced by myCParser#mCHAR.
    def exitMCHAR(self, ctx:myCParser.MCHARContext):
        pass


    # Enter a parse tree produced by myCParser#mSTRING.
    def enterMSTRING(self, ctx:myCParser.MSTRINGContext):
        pass

    # Exit a parse tree produced by myCParser#mSTRING.
    def exitMSTRING(self, ctx:myCParser.MSTRINGContext):
        pass


    # Enter a parse tree produced by myCParser#mLIB.
    def enterMLIB(self, ctx:myCParser.MLIBContext):
        pass

    # Exit a parse tree produced by myCParser#mLIB.
    def exitMLIB(self, ctx:myCParser.MLIBContext):
        pass



del myCParser