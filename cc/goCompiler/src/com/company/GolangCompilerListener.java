package com.company;

import com.company.gen.GolangListener;
import com.company.gen.GolangParser;
import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.tree.ErrorNode;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeProperty;
import org.antlr.v4.runtime.tree.TerminalNode;

import java.util.*;


public class GolangCompilerListener implements GolangListener {
    private List<String> structVars = new ArrayList<>();
    private int numReg = 0;
    private int intReg = 0;

    private StringBuilder stringBuilder = new StringBuilder();

    // Для генерации функций
    private HashMap<String, String> goToParVars = new HashMap<>();
    private StringBuilder functionBodyBuilder = new StringBuilder();
    private ParseTreeProperty<String> nodeToValue = new ParseTreeProperty<>();
    private List<String> imports = new ArrayList<>();

    private StringBuilder parrotImports = new StringBuilder();
    private List<LoopStatement> loops = new ArrayList<>();
    private boolean inLoop = false;

    private List<IfStatement> ifs = new ArrayList<>();
    private boolean inIf = false;

    private List<String> prepares = new ArrayList<>();

    private boolean inForClause = false;

    private boolean inStructDeclare = false;

    private List<StructStatement> structStatementList = new ArrayList<>();

    class StructStatement {
        String name;
        List<String> attrs = new ArrayList<>();
        String varName;

        StructStatement() {
            this.varName = "$P" + numReg;
            numReg++;
        }

        String getStructDefenition() {
            StringBuilder ret = new StringBuilder(varName + " = newclass \'" + name + "\'\n");

            for (String s: attrs) {
                ret.append("addattribute ").append(varName).append(", \'").append(s).append("\'\n");
            }

            return ret.toString();
        }
    }


    class LoopStatement {
        String name;
        String counter;
        String startValue;
        String tempNum;
        String tempValueBody;
        String funcBody;
        String conditionParam;

        LoopStatement() {
            int leftLimit = 97; // letter 'a'
            int rightLimit = 122; // letter 'z'
            int targetStringLength = 10;
            Random random = new Random();
            StringBuilder buffer = new StringBuilder(targetStringLength);
            for (int i = 0; i < targetStringLength; i++) {
                int randomLimitedInt = leftLimit + (int)
                        (random.nextFloat() * (rightLimit - leftLimit + 1));
                buffer.append((char) randomLimitedInt);
            }
            this.name = buffer.toString();
            this.tempNum = "$P"+numReg;
            tempValueBody = tempNum + " = new \"Integer\"\n";
            numReg++;
        }

        void addTemp(String temp) {
            tempValueBody += tempNum + " = " + temp + "\n";
        }

        String getParrotLoop() {
            return name + "_init:\n" +
                    "    .local pmc " + counter + "\n" +
                    "    " + counter + " = box " + startValue + "\n" +
                    "\n" +
                    "  " + name + "_test:\n" +
                    tempValueBody +
                    "    if " + counter + " "+conditionParam + " " + tempNum + " goto " + name + "_body\n" +
                    "    goto " + name + "_end\n" +
                    "\n" +
                    "  "+name+"_body:\n" +
                    "    "+ funcBody +"\n" +
                    "\n" +
                    "  " + name + "_continue:\n" +
                    "    inc "+counter+"\n" +
                    "    goto "+name+"_test\n" +
                    "\n" +
                    "  "+name+"_end:\n";
        }
    }

    class IfStatement {
        String ifBody;
        String elseBody;
        String condition;
        String conditionName;
        String compare;
        String name;
        IfStatement() {
            int leftLimit = 97; // letter 'a'
            int rightLimit = 122; // letter 'z'
            int targetStringLength = 10;
            Random random = new Random();
            StringBuilder buffer = new StringBuilder(targetStringLength);
            for (int i = 0; i < targetStringLength; i++) {
                int randomLimitedInt = leftLimit + (int)
                        (random.nextFloat() * (rightLimit - leftLimit + 1));
                buffer.append((char) randomLimitedInt);
            }
            this.name = buffer.toString();
            this.conditionName = "$P" + intReg;
            intReg++;
        }

        String getParrotFor() {
            if (elseBody == null) {
                elseBody = "";
            }
            return conditionName + " = " + condition + "\n" +
                    "if " + conditionName + " " + compare + " goto " + name + "_do_it\n" +
                    elseBody + "\n" +
                    "goto " + name + "_dont_do_it\n" +
                    name + "_do_it:\n" +
                    ifBody + "\n" +
                    name + "_dont_do_it:";
        }
    }

    GolangCompilerListener() {
    }

    private void processForward(ParseTree ctx) {
        ParseTree childValue = ctx.getChild(0);
        String value = this.nodeToValue.get(childValue);
        this.nodeToValue.put(ctx, value);
    }

    private void processChilds(ParseTree ctx) {
        StringBuilder value = new StringBuilder();
        for (int i = 0; i < ctx.getChildCount(); i++) {
            ParseTree child = ctx.getChild(i);
            String childValue = this.nodeToValue.get(child);
            if (childValue == null) {
                childValue = child.getText();
            }
            value.append(childValue);
            value.append(" ");
        }
        this.nodeToValue.put(ctx, value.toString());
    }

    String result() {
        StringBuilder ret = new StringBuilder();
        for (String line: stringBuilder.toString().split("\n")) {
            ret.append(line.trim()).append("\n");
        }
        return ret.toString();
    }

    @Override
    public void enterSourceFile(GolangParser.SourceFileContext ctx) {

    }

    @Override
    public void exitSourceFile(GolangParser.SourceFileContext ctx) {
        stringBuilder.append("\n");
        stringBuilder.append(parrotImports.toString());
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
        imports.add(packageName);
        parrotImports.append(".include \"stdlib/");
        parrotImports.append(packageName);
        parrotImports.append(".pir\"\n");
    }

    @Override
    public void exitImportPath(GolangParser.ImportPathContext ctx) {

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
            if (inLoop && loops.get(loops.size() - 1).counter == null) {
                newParVar = varName;
            }
            goToParVars.put(varName, newParVar);
            numReg++;
        }

    }

    @Override
    public void enterExpressionList(GolangParser.ExpressionListContext ctx) {

    }

    @Override
    public void exitExpressionList(GolangParser.ExpressionListContext ctx) {
        StringBuilder value = new StringBuilder();

        ParseTree childValue = ctx.getChild(0);
        value.append(this.nodeToValue.get(childValue));
        this.nodeToValue.put(ctx, value.toString());
    }

    @Override
    public void enterTypeDecl(GolangParser.TypeDeclContext ctx) {
        this.structStatementList.add(new StructStatement());
        this.inStructDeclare = true;
    }

    @Override
    public void exitTypeDecl(GolangParser.TypeDeclContext ctx) {
        inStructDeclare = false;
    }

    @Override
    public void enterTypeSpec(GolangParser.TypeSpecContext ctx) {

    }

    @Override
    public void exitTypeSpec(GolangParser.TypeSpecContext ctx) {
        if (inStructDeclare) {
            structStatementList.get(structStatementList.size() - 1).name = ctx.getChild(0).getText();
        }
    }

    @Override
    public void enterFunctionDecl(GolangParser.FunctionDeclContext ctx) {

    }

    @Override
    public void exitFunctionDecl(GolangParser.FunctionDeclContext ctx) {

        StringBuilder funcText = new StringBuilder();

        String funcName = ctx.getChild(1).getText();
        funcText.append(".sub ");
        funcText.append(funcName);
        funcText.append("\n");
        if ("main".equals(funcName)) {
            for (StructStatement structStatement: structStatementList) {
                funcText.append(structStatement.getStructDefenition());
            }
        }
        funcText.append("\n");
        funcText.append(functionBodyBuilder.toString());
        functionBodyBuilder = new StringBuilder();
        funcText.append(".end");
        funcText.append("\n");

        if ("main".equals(funcName)) {
            funcText.append(stringBuilder.toString());
            stringBuilder = funcText;
        } else {
            stringBuilder.append(funcText.toString());
        }
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
        if(inIf) {
            this.nodeToValue.put(ctx, this.nodeToValue.get(ctx.getChild(1)));
        }  else if (inLoop) {
            loops.get(loops.size()-1).funcBody = nodeToValue.get(ctx.getChild(1));
        }
        else {
                String statementValue = this.nodeToValue.get(ctx.getChild(1));
                this.functionBodyBuilder.append(statementValue);
        }
    }

    @Override
    public void enterStatementList(GolangParser.StatementListContext ctx) {

    }

    @Override
    public void exitStatementList(GolangParser.StatementListContext ctx) {
        this.processChilds(ctx);
    }

    @Override
    public void enterStatement(GolangParser.StatementContext ctx) {

    }

    @Override
    public void exitStatement(GolangParser.StatementContext ctx) {
        this.processForward(ctx);
    }

    @Override
    public void enterSimpleStmt(GolangParser.SimpleStmtContext ctx) {

    }

    @Override
    public void exitSimpleStmt(GolangParser.SimpleStmtContext ctx) {
        this.processForward(ctx);
    }

    @Override
    public void enterExpressionStmt(GolangParser.ExpressionStmtContext ctx) {

    }

    @Override
    public void exitExpressionStmt(GolangParser.ExpressionStmtContext ctx) {
        this.processForward(ctx);
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
        StringBuilder shorDeclaration = new StringBuilder();
        for (String prep: this.prepares) {
            shorDeclaration.append(prep).append("\n");
        }
        prepares.clear();
        String leftPart = ctx.getChild(0).getText();
        String varName = this.goToParVars.get(leftPart);
        if (varName == null) {
            varName = this.nodeToValue.get(ctx.getChild(0));
        }

        String rightPart = this.nodeToValue.get(ctx.getChild(2));
        if (rightPart.contains("[")) {
            shorDeclaration.append("$P").append(numReg).append(" = ").append(rightPart).append("\n");
            rightPart = "$P" + numReg;
            numReg++;
        }
        // Если справа нет переменных
        boolean needBox = true;
        for (String var: this.goToParVars.values()) {
            if (rightPart.contains(var)) {
                needBox = false;
                break;
            }
        }
        if (needBox) {
            rightPart = " = box " + rightPart;
        } else {
            rightPart = " = " + rightPart;
        }


        for (String str: structVars) {
            if (varName.contains(str)) {
                String tempVar = "$P" + numReg;
                numReg++;
                if (rightPart.contains("nil")) {
                    shorDeclaration.append("null ").append(tempVar).append("\n");
                } else {
                    shorDeclaration.append(tempVar).append(rightPart).append("\n");
                }
                shorDeclaration.append("setattribute ").append(varName).append(", ").append(tempVar);
                this.nodeToValue.put(ctx, shorDeclaration.toString());
                return;
            }
        }
        shorDeclaration.append(varName);
        shorDeclaration.append(rightPart);
        shorDeclaration.append("\n");
        this.nodeToValue.put(ctx, shorDeclaration.toString());
    }

    @Override
    public void enterAssign_op(GolangParser.Assign_opContext ctx) {

    }

    @Override
    public void exitAssign_op(GolangParser.Assign_opContext ctx) {

    }

    @Override
    public void enterShortVarDecl(GolangParser.ShortVarDeclContext ctx) {

    }

    @Override
    public void exitShortVarDecl(GolangParser.ShortVarDeclContext ctx) {
        StringBuilder shorDeclaration = new StringBuilder();
        for (String prep: this.prepares) {
            shorDeclaration.append(prep).append("\n");
        }
        prepares.clear();
        String leftPart = ctx.getChild(0).getText();
        String varName = this.goToParVars.get(leftPart);
        varName = varName.replace(" ", "");
        String rightPart = this.nodeToValue.get(ctx.getChild(2));

        if (inLoop && this.loops.get(this.loops.size() - 1).counter == null) {
            this.loops.get(this.loops.size() - 1).counter = leftPart;
            this.loops.get(this.loops.size() - 1).startValue = rightPart;
            return;
        }
        // Если справа нет переменных
        boolean needBox = true;
        for (String var: this.goToParVars.values()) {
            if (rightPart.contains(var)) {
                needBox = false;
                break;
            }
        }
        if (needBox) {
            rightPart = "box " + rightPart;
        }

        for (StructStatement structStatement: structStatementList) {
            if (rightPart.contains(structStatement.name)) {
                structVars.add(varName);
            }
        }

        shorDeclaration.append(varName);
        shorDeclaration.append(" = ");
        shorDeclaration.append(rightPart);
        shorDeclaration.append("\n");

        this.nodeToValue.put(ctx, shorDeclaration.toString());
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
        StringBuilder returnString = new StringBuilder();
        returnString.append(".return (");
        String returnValue = this.nodeToValue.get(ctx.getChild(1));
        returnString.append(returnValue);
        returnString.append(")");
        this.nodeToValue.put(ctx, returnString.toString());
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
        this.ifs.add(new IfStatement());
        this.inIf = true;
    }

    @Override
    public void exitIfStmt(GolangParser.IfStmtContext ctx) {
        int ifClassIndex = ifs.size() - 1;
        IfStatement ifSt = this.ifs.get(ifClassIndex);
        ifSt.ifBody = nodeToValue.get(ctx.getChild(2));
        ifSt.elseBody = nodeToValue.get(ctx.getChild(4));
        this.ifs.remove(ifClassIndex);
        if (this.ifs.size() == 0) {
            this.inIf = false;
        }
        this.nodeToValue.put(ctx, ifSt.getParrotFor());
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
        this.loops.add(new LoopStatement());
        this.inLoop = true;
    }

    @Override
    public void exitForStmt(GolangParser.ForStmtContext ctx) {
        int loopClassIndex = loops.size() - 1;
        LoopStatement loop = this.loops.get(loopClassIndex);
        this.loops.remove(loopClassIndex);
        if (this.loops.size() == 0) {
            this.inLoop = false;
        }
        this.nodeToValue.put(ctx, loop.getParrotLoop());
    }

    @Override
    public void enterForClause(GolangParser.ForClauseContext ctx) {
        this.inForClause = true;
    }

    @Override
    public void exitForClause(GolangParser.ForClauseContext ctx) {
        this.inForClause = false;
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
        String paramName = ctx.getChild(0).getText();
        functionBodyBuilder.append(".param pmc ").append(paramName).append("\n");
        this.goToParVars.put(paramName, paramName);
    }

    @Override
    public void enterOperand(GolangParser.OperandContext ctx) {

    }

    @Override
    public void exitOperand(GolangParser.OperandContext ctx) {
        this.processForward(ctx);
    }

    @Override
    public void enterLiteral(GolangParser.LiteralContext ctx) {

    }

    @Override
    public void exitLiteral(GolangParser.LiteralContext ctx) {
        this.processForward(ctx);
    }

    @Override
    public void enterBasicLit(GolangParser.BasicLitContext ctx) {

    }

    @Override
    public void exitBasicLit(GolangParser.BasicLitContext ctx) {
        String value = ctx.getText();
        this.nodeToValue.put(ctx, value);
    }

    @Override
    public void enterOperandName(GolangParser.OperandNameContext ctx) {

    }

    @Override
    public void exitOperandName(GolangParser.OperandNameContext ctx) {
        String value = ctx.getText();
        if (imports.contains(value)) {
            value = "";
        } else {
            value = this.goToParVars.get(value);
            if (value == null) {
                value = ctx.getText();
            }
        }
        this.nodeToValue.put(ctx, value);
        if (!this.goToParVars.containsKey(value)) {
            goToParVars.put(value, value);
        }
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
        String val = nodeToValue.get(ctx.getChild(1));
        if (val.equals("")) {
            this.processChilds(ctx);
        } else {
            nodeToValue.put(ctx, nodeToValue.get(ctx.getChild(1)));
        }
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
        if (ctx.getChildCount() != 2) {
            StringBuilder arr = new StringBuilder();
            arr.append("new \"ResizablePMCArray\"").append("\n");
            arr.append(nodeToValue.get(ctx.getChild(1)));
            nodeToValue.put(ctx, arr.toString());
            goToParVars.put("new", "new");
        } else {
            goToParVars.put("new", "new");
            nodeToValue.put(ctx, "");
        }
    }

    @Override
    public void enterElementList(GolangParser.ElementListContext ctx) {

    }

    @Override
    public void exitElementList(GolangParser.ElementListContext ctx) {
        StringBuilder val = new StringBuilder();
        for (int i = 0; i < ctx.getChildCount(); i=i+2) {
            int index = i / 2;
            val.append("$P").append(numReg-1).append("[").append(index).append("]")
                    .append(" = ").append(nodeToValue.get(ctx.getChild(i))).append("\n");
        }
        this.nodeToValue.put(ctx, val.toString());
    }

    @Override
    public void enterKeyedElement(GolangParser.KeyedElementContext ctx) {

    }

    @Override
    public void exitKeyedElement(GolangParser.KeyedElementContext ctx) {
        this.processForward(ctx);
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
        this.processForward(ctx);
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
        if (inStructDeclare) {
            structStatementList.get(structStatementList.size() - 1).attrs.add(ctx.getChild(0).getText());
        }
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
        StringBuilder value = new StringBuilder();

        // Заполнение атрибутов структуры
        String childValue = this.nodeToValue.get(ctx.getChild(0));
        if (childValue == null) {
            childValue = ctx.getChild(0).getText();
        }
        childValue = childValue.replaceAll(" ", "");
        if (structVars.contains(childValue) && ctx.getChildCount() == 2) {
            String field = this.nodeToValue.get(ctx.getChild(1));
            if (field == null) {
                field = ctx.getChild(1).getText();
            }
            field = field.replaceAll(" ", "");
            nodeToValue.put(ctx, childValue + ", \'" + field + "\'");
            return;
        }

        for (int i = 0; i < ctx.getChildCount(); i++) {
            ParseTree child = ctx.getChild(i);
            childValue = this.nodeToValue.get(child);
            if (childValue == null) {
                childValue = child.getText();
            }
            value.append(childValue);
            value.append(" ");
        }
        this.nodeToValue.put(ctx, value.toString());
    }

    @Override
    public void enterSelector(GolangParser.SelectorContext ctx) {

    }

    @Override
    public void exitSelector(GolangParser.SelectorContext ctx) {
        this.nodeToValue.put(ctx, ctx.getChild(1).getText());

    }

    @Override
    public void enterIndex(GolangParser.IndexContext ctx) {
    }

    public static boolean isInteger(String s) {
        boolean isValidInteger = false;
        try
        {
            Integer.parseInt(s);

            // s is a valid integer

            isValidInteger = true;
        }
        catch (NumberFormatException ex)
        {
            // s is not an integer
        }

        return isValidInteger;
    }

    @Override
    public void exitIndex(GolangParser.IndexContext ctx) {
        String indexVal = ctx.getChild(1).getText().replace("", " ").trim();
        String newVal = "$P" + numReg;
        numReg++;
        nodeToValue.put(ctx.getChild(1), newVal);
        String box = "box ";
        for (String var: this.goToParVars.values()) {
            if (indexVal.contains(var)) {
                box = "";
                break;
            }
        }
        if (isInteger(indexVal)) {
            box = "box ";
        }
        prepares.add(newVal + " = " + box + indexVal);
        this.processChilds(ctx);
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
        this.processChilds(ctx);
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
        if (inIf && ctx.getChildCount() == 3 && ctx.getChild(1).getText().equals("==")) {
            this.ifs.get(this.ifs.size() - 1).condition = this.nodeToValue.get(ctx.getChild(0));
            this.ifs.get(this.ifs.size() - 1).compare = "==" + this.nodeToValue.get(ctx.getChild(2));
            return;
        }
        if (inIf && ctx.getChildCount() == 3 && ctx.getChild(1).getText().equals(">")) {
            this.ifs.get(this.ifs.size() - 1).condition = this.nodeToValue.get(ctx.getChild(0));
            this.ifs.get(this.ifs.size() - 1).compare = ">" + this.nodeToValue.get(ctx.getChild(2));
            return;
        }
        if (inLoop && ctx.getChildCount() == 3 && !inIf && inForClause) {
            String child1 = nodeToValue.get(ctx.getChild(1));
            if (child1 == null)
                child1 = ctx.getChild(1).getText();
            String child2 = nodeToValue.get(ctx.getChild(2));
            if (child2 == null)
                child2 = ctx.getChild(2).getText();
            if (child1.equals("<") || child1.equals("==") ||child1.equals(">")) {
                this.loops.get(this.loops.size() - 1).conditionParam = child1;
                String box = "box ";
                for (String var: this.goToParVars.values()) {
                    if (child2.contains(var)) {
                        box = "";
                        break;
                    }
                }
                this.loops.get(this.loops.size() - 1).addTemp(box + child2);
            } else {
                this.loops.get(this.loops.size() - 1).addTemp(this.loops.get(this.loops.size() - 1).tempNum + " " + child1 + " " + child2);
            }
            return;
        }
        this.processChilds(ctx);
    }

    @Override
    public void enterUnaryExpr(GolangParser.UnaryExprContext ctx) {

    }

    @Override
    public void exitUnaryExpr(GolangParser.UnaryExprContext ctx) {
        if (ctx.getChild(0).getText().equals("&")) {
            nodeToValue.put(ctx, "new \""+nodeToValue.get(ctx.getChild(1)).replaceAll(" ", "")+"\"");
            return;
        }
        this.processForward(ctx);
    }

    @Override
    public void enterConversion(GolangParser.ConversionContext ctx) {

    }

    @Override
    public void exitConversion(GolangParser.ConversionContext ctx) {

    }

    @Override
    public void enterEos(GolangParser.EosContext ctx) {
        this.nodeToValue.put(ctx, "\n");
    }

    @Override
    public void exitEos(GolangParser.EosContext ctx) {

    }

    @Override
    public void visitTerminal(TerminalNode terminalNode) {
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
