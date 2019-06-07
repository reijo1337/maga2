package com.company;

import com.company.gen.GolangLexer;
import com.company.gen.GolangParser;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.tree.ParseTreeWalker;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        String source = "src/examples/array.go";
        String[] sourceParts = source.split("/");
        String filename = sourceParts[sourceParts.length - 1].split("\\.")[0];
        List<Token> tokens = new ArrayList<>();
        GolangLexer lexer;
        GolangParser parser;
        CharStream charStream;
        try {
            charStream = CharStreams.fromFileName(source);
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        lexer = new GolangLexer(charStream);
        Token token = lexer.nextToken();

        while (token.getType() != GolangLexer.EOF) {
            tokens.add(token);
            token = lexer.nextToken();
        }

        lexer.reset();
        lexer.setLine(0);
        lexer._tokenStartCharPositionInLine = 0;

        //получили дерево
        CommonTokenStream tokenStream = new CommonTokenStream(lexer);
        parser = new GolangParser(tokenStream);
        GolangParser.SourceFileContext sourceFileContext = parser.sourceFile();

        //делаем обход дерева
        ParseTreeWalker parseTreeWalker = new ParseTreeWalker();
        GolangCompilerListener golangCompilerListener = new GolangCompilerListener();

        parseTreeWalker.walk(golangCompilerListener, sourceFileContext);

        System.out.println(golangCompilerListener.result());
        try (PrintWriter out = new PrintWriter("pirbook/"+ filename + ".pir")) {
            out.println(golangCompilerListener.result());
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
}
