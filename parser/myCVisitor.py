# Generated from myC.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .myCParser import myCParser
else:
    from myCParser import myCParser

# This class defines a complete generic visitor for a parse tree produced by myCParser.

class myCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by myCParser#prog.
    def visitProg(self, ctx:myCParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#include.
    def visitInclude(self, ctx:myCParser.IncludeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mStructDef.
    def visitMStructDef(self, ctx:myCParser.MStructDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#structParam.
    def visitStructParam(self, ctx:myCParser.StructParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mFunction.
    def visitMFunction(self, ctx:myCParser.MFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#params.
    def visitParams(self, ctx:myCParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#param.
    def visitParam(self, ctx:myCParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#funcBody.
    def visitFuncBody(self, ctx:myCParser.FuncBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#body.
    def visitBody(self, ctx:myCParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#block.
    def visitBlock(self, ctx:myCParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#initialBlock.
    def visitInitialBlock(self, ctx:myCParser.InitialBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#arrayInitBlock.
    def visitArrayInitBlock(self, ctx:myCParser.ArrayInitBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#structInitBlock.
    def visitStructInitBlock(self, ctx:myCParser.StructInitBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#assignBlock.
    def visitAssignBlock(self, ctx:myCParser.AssignBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#ifBlocks.
    def visitIfBlocks(self, ctx:myCParser.IfBlocksContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#ifBlock.
    def visitIfBlock(self, ctx:myCParser.IfBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#elifBlock.
    def visitElifBlock(self, ctx:myCParser.ElifBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#elseBlock.
    def visitElseBlock(self, ctx:myCParser.ElseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#condition.
    def visitCondition(self, ctx:myCParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#whileBlock.
    def visitWhileBlock(self, ctx:myCParser.WhileBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#forBlock.
    def visitForBlock(self, ctx:myCParser.ForBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#for1Block.
    def visitFor1Block(self, ctx:myCParser.For1BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#for3Block.
    def visitFor3Block(self, ctx:myCParser.For3BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#returnBlock.
    def visitReturnBlock(self, ctx:myCParser.ReturnBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#identifier.
    def visitIdentifier(self, ctx:myCParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#parens.
    def visitParens(self, ctx:myCParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#OR.
    def visitOR(self, ctx:myCParser.ORContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#string.
    def visitString(self, ctx:myCParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#MulDiv.
    def visitMulDiv(self, ctx:myCParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#AddSub.
    def visitAddSub(self, ctx:myCParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#double.
    def visitDouble(self, ctx:myCParser.DoubleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#int.
    def visitInt(self, ctx:myCParser.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#Neg.
    def visitNeg(self, ctx:myCParser.NegContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#arrayitem.
    def visitArrayitem(self, ctx:myCParser.ArrayitemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#function.
    def visitFunction(self, ctx:myCParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#AND.
    def visitAND(self, ctx:myCParser.ANDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#char.
    def visitChar(self, ctx:myCParser.CharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#structmember.
    def visitStructmember(self, ctx:myCParser.StructmemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#Judge.
    def visitJudge(self, ctx:myCParser.JudgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mType.
    def visitMType(self, ctx:myCParser.MTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mArray.
    def visitMArray(self, ctx:myCParser.MArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mVoid.
    def visitMVoid(self, ctx:myCParser.MVoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mStruct.
    def visitMStruct(self, ctx:myCParser.MStructContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#structMember.
    def visitStructMember(self, ctx:myCParser.StructMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#arrayItem.
    def visitArrayItem(self, ctx:myCParser.ArrayItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#func.
    def visitFunc(self, ctx:myCParser.FuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#strlenFunc.
    def visitStrlenFunc(self, ctx:myCParser.StrlenFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#atoiFunc.
    def visitAtoiFunc(self, ctx:myCParser.AtoiFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#printfFunc.
    def visitPrintfFunc(self, ctx:myCParser.PrintfFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#scanfFunc.
    def visitScanfFunc(self, ctx:myCParser.ScanfFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#getsFunc.
    def visitGetsFunc(self, ctx:myCParser.GetsFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#selfDefinedFunc.
    def visitSelfDefinedFunc(self, ctx:myCParser.SelfDefinedFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#argument.
    def visitArgument(self, ctx:myCParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mID.
    def visitMID(self, ctx:myCParser.MIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mINT.
    def visitMINT(self, ctx:myCParser.MINTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mDOUBLE.
    def visitMDOUBLE(self, ctx:myCParser.MDOUBLEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mCHAR.
    def visitMCHAR(self, ctx:myCParser.MCHARContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mSTRING.
    def visitMSTRING(self, ctx:myCParser.MSTRINGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by myCParser#mLIB.
    def visitMLIB(self, ctx:myCParser.MLIBContext):
        return self.visitChildren(ctx)



del myCParser