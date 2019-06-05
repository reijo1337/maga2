package com.company;

import com.company.gen.GolangListener;
import com.company.gen.GolangParser;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ErrorNode;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeProperty;
import org.antlr.v4.runtime.tree.TerminalNode;

import java.io.ByteArrayOutputStream;
import java.util.*;


public class GolangCompilerListener implements GolangListener {
    private ParseTreeProperty<Integer> intValues = new ParseTreeProperty<>();
    private ParseTreeProperty<Float> _floatValues = new ParseTreeProperty<>();
    private ParseTreeProperty<String> _stringValues = new ParseTreeProperty<>();
    private ParseTreeProperty<String> _whichValues = new ParseTreeProperty<>();

    private List<ByteArrayOutputStream> stackOutputStream = new ArrayList<>();
    private Hashtable<String, ByteArrayOutputStream> functionDefinitionStreams = new Hashtable<>();

    private Hashtable<Token, String> tokenStringHashtable = new Hashtable<>();

    private int numReg = 0;

    private StringBuilder stringBuilder = new StringBuilder();

    // Для генерации функций
    private HashMap<String, String> goToParVars = new HashMap<>();
    private StringBuilder functionBodyBuilder = new StringBuilder();
    private HashMap<String, String> nodeToValue = new HashMap<>();

    GolangCompilerListener() {
    }

    String result() {
        return stringBuilder.toString();
    }

    @Override
    public void enterSourceFile(GolangParser.SourceFileContext ctx) {

    }

    @Override
    public void exitSourceFile(GolangParser.SourceFileContext ctx) {

    }

    @Override
    public void enterPackageClause(GolangParser.PackageClauseContext ctx) {

    }

    @Override
    public void exitPackageClause(GolangParser.PackageClauseContext ctx) {

    }

    @Override
    public void enterImportDecl(GolangParser.ImportDeclContext ctx) {

    }

    @Override
    public void exitImportDecl(GolangParser.ImportDeclContext ctx) {

    }

    @Override
    public void enterImportSpec(GolangParser.ImportSpecContext ctx) {

    }

    @Override
    public void exitImportSpec(GolangParser.ImportSpecContext ctx) {

    }

    @Override
    public void enterImportPath(GolangParser.ImportPathContext ctx) {
        String packageName = ctx.getChild(0).getText();
        packageName = packageName.replaceAll("\"", "");
        stringBuilder.append(".include \"stdlib/");
        stringBuilder.append(packageName);
        stringBuilder.append(".pir\"");
    }

    @Override
    public void exitImportPath(GolangParser.ImportPathContext ctx) {
        stringBuilder.append("\n");
    }

    @Override
    public void enterTopLevelDecl(GolangParser.TopLevelDeclContext ctx) {
        stringBuilder.append("\n");

    }

    @Override
    public void exitTopLevelDecl(GolangParser.TopLevelDeclContext ctx) {

    }

    @Override
    public void enterDeclaration(GolangParser.DeclarationContext ctx) {

    }

    @Override
    public void exitDeclaration(GolangParser.DeclarationContext ctx) {

    }

    @Override
    public void enterConstDecl(GolangParser.ConstDeclContext ctx) {

    }

    @Override
    public void exitConstDecl(GolangParser.ConstDeclContext ctx) {

    }

    @Override
    public void enterConstSpec(GolangParser.ConstSpecContext ctx) {

    }

    @Override
    public void exitConstSpec(GolangParser.ConstSpecContext ctx) {

    }

    @Override
    public void enterIdentifierList(GolangParser.IdentifierListContext ctx) {

    }

    @Override
    public void exitIdentifierList(GolangParser.IdentifierListContext ctx) {
        String varName = ctx.getChild(0).getText();
        if (!goToParVars.containsKey(varName)) {
            String newParVar = "$P" + numReg;
            goToParVars.put(varName, newParVar);
            numReg++;
        }

    }

    @Override
    public void enterExpressionList(GolangParser.ExpressionListContext ctx) {

    }

    @Override
    public void exitExpressionList(GolangParser.ExpressionListContext ctx) {

    }

    @Override
    public void enterTypeDecl(GolangParser.TypeDeclContext ctx) {

    }

    @Override
    public void exitTypeDecl(GolangParser.TypeDeclContext ctx) {

    }

    @Override
    public void enterTypeSpec(GolangParser.TypeSpecContext ctx) {

    }

    @Override
    public void exitTypeSpec(GolangParser.TypeSpecContext ctx) {

    }

    @Override
    public void enterFunctionDecl(GolangParser.FunctionDeclContext ctx) {
        String funcName = ctx.getChild(1).getText();
        stringBuilder.append(".sub ");
        stringBuilder.append(funcName);
        stringBuilder.append("\n");
    }

    @Override
    public void exitFunctionDecl(GolangParser.FunctionDeclContext ctx) {
        for(Map.Entry<String, String> entry : goToParVars.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();

            System.out.println(key + "->" + value);
        }
        stringBuilder.append(".end");
        stringBuilder.append("\n");
    }

    @Override
    public void enterFunction(GolangParser.FunctionContext ctx) {

    }

    @Override
    public void exitFunction(GolangParser.FunctionContext ctx) {

    }

    @Override
    public void enterMethodDecl(GolangParser.MethodDeclContext ctx) {

    }

    @Override
    public void exitMethodDecl(GolangParser.MethodDeclContext ctx) {

    }

    @Override
    public void enterReceiver(GolangParser.ReceiverContext ctx) {

    }

    @Override
    public void exitReceiver(GolangParser.ReceiverContext ctx) {

    }

    @Override
    public void enterVarDecl(GolangParser.VarDeclContext ctx) {

    }

    @Override
    public void exitVarDecl(GolangParser.VarDeclContext ctx) {

    }

    @Override
    public void enterVarSpec(GolangParser.VarSpecContext ctx) {

    }

    @Override
    public void exitVarSpec(GolangParser.VarSpecContext ctx) {

    }

    @Override
    public void enterBlock(GolangParser.BlockContext ctx) {

    }

    @Override
    public void exitBlock(GolangParser.BlockContext ctx) {

    }

    @Override
    public void enterStatementList(GolangParser.StatementListContext ctx) {

    }

    @Override
    public void exitStatementList(GolangParser.StatementListContext ctx) {

    }

    @Override
    public void enterStatement(GolangParser.StatementContext ctx) {

    }

    @Override
    public void exitStatement(GolangParser.StatementContext ctx) {

    }

    @Override
    public void enterSimpleStmt(GolangParser.SimpleStmtContext ctx) {

    }

    @Override
    public void exitSimpleStmt(GolangParser.SimpleStmtContext ctx) {

    }

    @Override
    public void enterExpressionStmt(GolangParser.ExpressionStmtContext ctx) {

    }

    @Override
    public void exitExpressionStmt(GolangParser.ExpressionStmtContext ctx) {

    }

    @Override
    public void enterSendStmt(GolangParser.SendStmtContext ctx) {

    }

    @Override
    public void exitSendStmt(GolangParser.SendStmtContext ctx) {

    }

    @Override
    public void enterIncDecStmt(GolangParser.IncDecStmtContext ctx) {

    }

    @Override
    public void exitIncDecStmt(GolangParser.IncDecStmtContext ctx) {

    }

    @Override
    public void enterAssignment(GolangParser.AssignmentContext ctx) {

    }

    @Override
    public void exitAssignment(GolangParser.AssignmentContext ctx) {

    }

    @Override
    public void enterAssign_op(GolangParser.Assign_opContext ctx) {

    }

    @Override
    public void exitAssign_op(GolangParser.Assign_opContext ctx) {

    }

    @Override
    public void enterShortVarDecl(GolangParser.ShortVarDeclContext ctx) {
        System.out.println(ctx.getClass().getSimpleName());

    }

    @Override
    public void exitShortVarDecl(GolangParser.ShortVarDeclContext ctx) {
        StringBuilder shorDeclaration = new StringBuilder();
        String leftPart = ctx.getChild(0).getText();
        String varName = this.goToParVars.get(leftPart);
        String rightPart = this.nodeToValue.get(ctx.getChild(2).getText());
        this.functionBodyBuilder.append(leftPart);
        this.functionBodyBuilder.append(" = ");
        this.functionBodyBuilder.append(rightPart);
        this.functionBodyBuilder.append("\n");
    }

    @Override
    public void enterEmptyStmt(GolangParser.EmptyStmtContext ctx) {

    }

    @Override
    public void exitEmptyStmt(GolangParser.EmptyStmtContext ctx) {

    }

    @Override
    public void enterLabeledStmt(GolangParser.LabeledStmtContext ctx) {

    }

    @Override
    public void exitLabeledStmt(GolangParser.LabeledStmtContext ctx) {

    }

    @Override
    public void enterReturnStmt(GolangParser.ReturnStmtContext ctx) {

    }

    @Override
    public void exitReturnStmt(GolangParser.ReturnStmtContext ctx) {

    }

    @Override
    public void enterBreakStmt(GolangParser.BreakStmtContext ctx) {

    }

    @Override
    public void exitBreakStmt(GolangParser.BreakStmtContext ctx) {

    }

    @Override
    public void enterContinueStmt(GolangParser.ContinueStmtContext ctx) {

    }

    @Override
    public void exitContinueStmt(GolangParser.ContinueStmtContext ctx) {

    }

    @Override
    public void enterGotoStmt(GolangParser.GotoStmtContext ctx) {

    }

    @Override
    public void exitGotoStmt(GolangParser.GotoStmtContext ctx) {

    }

    @Override
    public void enterFallthroughStmt(GolangParser.FallthroughStmtContext ctx) {

    }

    @Override
    public void exitFallthroughStmt(GolangParser.FallthroughStmtContext ctx) {

    }

    @Override
    public void enterDeferStmt(GolangParser.DeferStmtContext ctx) {

    }

    @Override
    public void exitDeferStmt(GolangParser.DeferStmtContext ctx) {

    }

    @Override
    public void enterIfStmt(GolangParser.IfStmtContext ctx) {

    }

    @Override
    public void exitIfStmt(GolangParser.IfStmtContext ctx) {

    }

    @Override
    public void enterSwitchStmt(GolangParser.SwitchStmtContext ctx) {

    }

    @Override
    public void exitSwitchStmt(GolangParser.SwitchStmtContext ctx) {

    }

    @Override
    public void enterExprSwitchStmt(GolangParser.ExprSwitchStmtContext ctx) {

    }

    @Override
    public void exitExprSwitchStmt(GolangParser.ExprSwitchStmtContext ctx) {

    }

    @Override
    public void enterExprCaseClause(GolangParser.ExprCaseClauseContext ctx) {

    }

    @Override
    public void exitExprCaseClause(GolangParser.ExprCaseClauseContext ctx) {

    }

    @Override
    public void enterExprSwitchCase(GolangParser.ExprSwitchCaseContext ctx) {

    }

    @Override
    public void exitExprSwitchCase(GolangParser.ExprSwitchCaseContext ctx) {

    }

    @Override
    public void enterTypeSwitchStmt(GolangParser.TypeSwitchStmtContext ctx) {

    }

    @Override
    public void exitTypeSwitchStmt(GolangParser.TypeSwitchStmtContext ctx) {

    }

    @Override
    public void enterTypeSwitchGuard(GolangParser.TypeSwitchGuardContext ctx) {

    }

    @Override
    public void exitTypeSwitchGuard(GolangParser.TypeSwitchGuardContext ctx) {

    }

    @Override
    public void enterTypeCaseClause(GolangParser.TypeCaseClauseContext ctx) {

    }

    @Override
    public void exitTypeCaseClause(GolangParser.TypeCaseClauseContext ctx) {

    }

    @Override
    public void enterTypeSwitchCase(GolangParser.TypeSwitchCaseContext ctx) {

    }

    @Override
    public void exitTypeSwitchCase(GolangParser.TypeSwitchCaseContext ctx) {

    }

    @Override
    public void enterTypeList(GolangParser.TypeListContext ctx) {

    }

    @Override
    public void exitTypeList(GolangParser.TypeListContext ctx) {

    }

    @Override
    public void enterSelectStmt(GolangParser.SelectStmtContext ctx) {

    }

    @Override
    public void exitSelectStmt(GolangParser.SelectStmtContext ctx) {

    }

    @Override
    public void enterCommClause(GolangParser.CommClauseContext ctx) {

    }

    @Override
    public void exitCommClause(GolangParser.CommClauseContext ctx) {

    }

    @Override
    public void enterCommCase(GolangParser.CommCaseContext ctx) {

    }

    @Override
    public void exitCommCase(GolangParser.CommCaseContext ctx) {

    }

    @Override
    public void enterRecvStmt(GolangParser.RecvStmtContext ctx) {

    }

    @Override
    public void exitRecvStmt(GolangParser.RecvStmtContext ctx) {

    }

    @Override
    public void enterForStmt(GolangParser.ForStmtContext ctx) {

    }

    @Override
    public void exitForStmt(GolangParser.ForStmtContext ctx) {

    }

    @Override
    public void enterForClause(GolangParser.ForClauseContext ctx) {

    }

    @Override
    public void exitForClause(GolangParser.ForClauseContext ctx) {

    }

    @Override
    public void enterRangeClause(GolangParser.RangeClauseContext ctx) {

    }

    @Override
    public void exitRangeClause(GolangParser.RangeClauseContext ctx) {

    }

    @Override
    public void enterGoStmt(GolangParser.GoStmtContext ctx) {

    }

    @Override
    public void exitGoStmt(GolangParser.GoStmtContext ctx) {

    }

    @Override
    public void enterType(GolangParser.TypeContext ctx) {

    }

    @Override
    public void exitType(GolangParser.TypeContext ctx) {

    }

    @Override
    public void enterTypeName(GolangParser.TypeNameContext ctx) {

    }

    @Override
    public void exitTypeName(GolangParser.TypeNameContext ctx) {

    }

    @Override
    public void enterTypeLit(GolangParser.TypeLitContext ctx) {

    }

    @Override
    public void exitTypeLit(GolangParser.TypeLitContext ctx) {

    }

    @Override
    public void enterArrayType(GolangParser.ArrayTypeContext ctx) {

    }

    @Override
    public void exitArrayType(GolangParser.ArrayTypeContext ctx) {

    }

    @Override
    public void enterArrayLength(GolangParser.ArrayLengthContext ctx) {

    }

    @Override
    public void exitArrayLength(GolangParser.ArrayLengthContext ctx) {

    }

    @Override
    public void enterElementType(GolangParser.ElementTypeContext ctx) {

    }

    @Override
    public void exitElementType(GolangParser.ElementTypeContext ctx) {

    }

    @Override
    public void enterPointerType(GolangParser.PointerTypeContext ctx) {

    }

    @Override
    public void exitPointerType(GolangParser.PointerTypeContext ctx) {

    }

    @Override
    public void enterInterfaceType(GolangParser.InterfaceTypeContext ctx) {

    }

    @Override
    public void exitInterfaceType(GolangParser.InterfaceTypeContext ctx) {

    }

    @Override
    public void enterSliceType(GolangParser.SliceTypeContext ctx) {

    }

    @Override
    public void exitSliceType(GolangParser.SliceTypeContext ctx) {

    }

    @Override
    public void enterMapType(GolangParser.MapTypeContext ctx) {

    }

    @Override
    public void exitMapType(GolangParser.MapTypeContext ctx) {

    }

    @Override
    public void enterChannelType(GolangParser.ChannelTypeContext ctx) {

    }

    @Override
    public void exitChannelType(GolangParser.ChannelTypeContext ctx) {

    }

    @Override
    public void enterMethodSpec(GolangParser.MethodSpecContext ctx) {

    }

    @Override
    public void exitMethodSpec(GolangParser.MethodSpecContext ctx) {

    }

    @Override
    public void enterFunctionType(GolangParser.FunctionTypeContext ctx) {

    }

    @Override
    public void exitFunctionType(GolangParser.FunctionTypeContext ctx) {

    }

    @Override
    public void enterSignature(GolangParser.SignatureContext ctx) {

    }

    @Override
    public void exitSignature(GolangParser.SignatureContext ctx) {

    }

    @Override
    public void enterResult(GolangParser.ResultContext ctx) {

    }

    @Override
    public void exitResult(GolangParser.ResultContext ctx) {

    }

    @Override
    public void enterParameters(GolangParser.ParametersContext ctx) {

    }

    @Override
    public void exitParameters(GolangParser.ParametersContext ctx) {

    }

    @Override
    public void enterParameterList(GolangParser.ParameterListContext ctx) {

    }

    @Override
    public void exitParameterList(GolangParser.ParameterListContext ctx) {

    }

    @Override
    public void enterParameterDecl(GolangParser.ParameterDeclContext ctx) {

    }

    @Override
    public void exitParameterDecl(GolangParser.ParameterDeclContext ctx) {

    }

    @Override
    public void enterOperand(GolangParser.OperandContext ctx) {

    }

    @Override
    public void exitOperand(GolangParser.OperandContext ctx) {
        String childValue = ctx.getChild(0).getText();
        String value = this.nodeToValue.get(childValue);
        this.nodeToValue.put(ctx.getClass().getSimpleName(), value);
    }

    @Override
    public void enterLiteral(GolangParser.LiteralContext ctx) {

    }

    @Override
    public void exitLiteral(GolangParser.LiteralContext ctx) {
        String childValue = ctx.getChild(0).getText();
        String value = this.nodeToValue.get(childValue);
        this.nodeToValue.put(ctx.getClass().getSimpleName(), value);
    }

    @Override
    public void enterBasicLit(GolangParser.BasicLitContext ctx) {

    }

    @Override
    public void exitBasicLit(GolangParser.BasicLitContext ctx) {
        String value = ctx.getText();
        this.nodeToValue.put(ctx.getClass().getSimpleName(), value);
    }

    @Override
    public void enterOperandName(GolangParser.OperandNameContext ctx) {

    }

    @Override
    public void exitOperandName(GolangParser.OperandNameContext ctx) {

    }

    @Override
    public void enterQualifiedIdent(GolangParser.QualifiedIdentContext ctx) {

    }

    @Override
    public void exitQualifiedIdent(GolangParser.QualifiedIdentContext ctx) {

    }

    @Override
    public void enterCompositeLit(GolangParser.CompositeLitContext ctx) {

    }

    @Override
    public void exitCompositeLit(GolangParser.CompositeLitContext ctx) {

    }

    @Override
    public void enterLiteralType(GolangParser.LiteralTypeContext ctx) {

    }

    @Override
    public void exitLiteralType(GolangParser.LiteralTypeContext ctx) {

    }

    @Override
    public void enterLiteralValue(GolangParser.LiteralValueContext ctx) {

    }

    @Override
    public void exitLiteralValue(GolangParser.LiteralValueContext ctx) {

    }

    @Override
    public void enterElementList(GolangParser.ElementListContext ctx) {

    }

    @Override
    public void exitElementList(GolangParser.ElementListContext ctx) {

    }

    @Override
    public void enterKeyedElement(GolangParser.KeyedElementContext ctx) {

    }

    @Override
    public void exitKeyedElement(GolangParser.KeyedElementContext ctx) {

    }

    @Override
    public void enterKey(GolangParser.KeyContext ctx) {

    }

    @Override
    public void exitKey(GolangParser.KeyContext ctx) {

    }

    @Override
    public void enterElement(GolangParser.ElementContext ctx) {

    }

    @Override
    public void exitElement(GolangParser.ElementContext ctx) {

    }

    @Override
    public void enterStructType(GolangParser.StructTypeContext ctx) {

    }

    @Override
    public void exitStructType(GolangParser.StructTypeContext ctx) {

    }

    @Override
    public void enterFieldDecl(GolangParser.FieldDeclContext ctx) {

    }

    @Override
    public void exitFieldDecl(GolangParser.FieldDeclContext ctx) {

    }

    @Override
    public void enterAnonymousField(GolangParser.AnonymousFieldContext ctx) {

    }

    @Override
    public void exitAnonymousField(GolangParser.AnonymousFieldContext ctx) {

    }

    @Override
    public void enterFunctionLit(GolangParser.FunctionLitContext ctx) {

    }

    @Override
    public void exitFunctionLit(GolangParser.FunctionLitContext ctx) {

    }

    @Override
    public void enterPrimaryExpr(GolangParser.PrimaryExprContext ctx) {

    }

    @Override
    public void exitPrimaryExpr(GolangParser.PrimaryExprContext ctx) {
        String childValue = ctx.getChild(0).getText();
        String value = this.nodeToValue.get(childValue);
        this.nodeToValue.put(ctx.getClass().getSimpleName(), value);
    }

    @Override
    public void enterSelector(GolangParser.SelectorContext ctx) {

    }

    @Override
    public void exitSelector(GolangParser.SelectorContext ctx) {

    }

    @Override
    public void enterIndex(GolangParser.IndexContext ctx) {

    }

    @Override
    public void exitIndex(GolangParser.IndexContext ctx) {

    }

    @Override
    public void enterSlice(GolangParser.SliceContext ctx) {

    }

    @Override
    public void exitSlice(GolangParser.SliceContext ctx) {

    }

    @Override
    public void enterTypeAssertion(GolangParser.TypeAssertionContext ctx) {

    }

    @Override
    public void exitTypeAssertion(GolangParser.TypeAssertionContext ctx) {

    }

    @Override
    public void enterArguments(GolangParser.ArgumentsContext ctx) {

    }

    @Override
    public void exitArguments(GolangParser.ArgumentsContext ctx) {

    }

    @Override
    public void enterMethodExpr(GolangParser.MethodExprContext ctx) {

    }

    @Override
    public void exitMethodExpr(GolangParser.MethodExprContext ctx) {

    }

    @Override
    public void enterReceiverType(GolangParser.ReceiverTypeContext ctx) {

    }

    @Override
    public void exitReceiverType(GolangParser.ReceiverTypeContext ctx) {

    }

    @Override
    public void enterExpression(GolangParser.ExpressionContext ctx) {

    }

    @Override
    public void exitExpression(GolangParser.ExpressionContext ctx) {
        for (int i = 0; i < ctx.getChildCount(); i++) {
            String childValue = ctx.getChild(0).getText();
            String value = this.nodeToValue.get(childValue);
        }
        this.nodeToValue.put(ctx.getClass().getSimpleName(), "");
    }

    @Override
    public void enterUnaryExpr(GolangParser.UnaryExprContext ctx) {

    }

    @Override
    public void exitUnaryExpr(GolangParser.UnaryExprContext ctx) {
        String childValue = ctx.getChild(0).getText();
        String value = this.nodeToValue.get(childValue);
        this.nodeToValue.put(ctx.getClass().getSimpleName(), value);
    }

    @Override
    public void enterConversion(GolangParser.ConversionContext ctx) {

    }

    @Override
    public void exitConversion(GolangParser.ConversionContext ctx) {

    }

    @Override
    public void enterEos(GolangParser.EosContext ctx) {

    }

    @Override
    public void exitEos(GolangParser.EosContext ctx) {

    }

    @Override
    public void visitTerminal(TerminalNode terminalNode) {
        Token symbol = terminalNode.getSymbol();
        String symbolText = symbol.getText();
        switch(symbol.getType())
        {
            case GolangParser.INT_LIT:
                intValues.put(terminalNode, Integer.valueOf(symbolText));
                _whichValues.put(terminalNode, "Integer");
                break;
            case GolangParser.FLOAT_LIT:
                _floatValues.put(terminalNode, Float.valueOf(symbolText));
                _whichValues.put(terminalNode, "Float");
                break;
            case GolangParser.STRING_LIT:
                symbolText = symbolText.replaceAll("\"$", "");
                symbolText = symbolText.replaceAll("^\"", "");
                symbolText = symbolText.replaceAll("\'$", "");
                symbolText = symbolText.replaceAll("^\'", "");
                _stringValues.put(terminalNode, symbolText);
                _whichValues.put(terminalNode, "String");
                break;
            case GolangParser.IDENTIFIER:
                _stringValues.put(terminalNode, symbolText);
                _whichValues.put(terminalNode, "Dynamic");
                break;
        }
    }

    @Override
    public void visitErrorNode(ErrorNode errorNode) {

    }

    @Override
    public void enterEveryRule(ParserRuleContext parserRuleContext) {

    }

    @Override
    public void exitEveryRule(ParserRuleContext parserRuleContext) {

    }
}
