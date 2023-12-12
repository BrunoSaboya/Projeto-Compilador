import sys
import re
from Node import *
from Tokenizer import *

class PrePro:
    def filter(code):
        code = code.split("\n")
        for i in range(len(code)):
            if "//" in code[i]:
                code[i] = code[i].split("//")[0]
        code = "\n".join(code)
        return code
    
class Parser:

    tokenizer = None

    def parseProgram():
        result = Block("", [])
        while Parser.tokenizer.next.type != "EOF":
            while Parser.tokenizer.next.type == "BREAKLINE":
                Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "EOF":
                result.children.append(Parser.parseDeclaration())
        result.children.append(FuncCall("main", []))
        return result
    
    def parseFactor():
        result = None 
        if Parser.tokenizer.next.type == "INT":
            result = IntVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            return result
        
        elif Parser.tokenizer.next.type == "STRING":
            result = StrVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            return result
        
        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.selectNext()
            result = UnOp("+", [Parser.parseFactor()])
            return result
        
        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.selectNext()
            result = UnOp("-", [Parser.parseFactor()])
            return result
        
        elif Parser.tokenizer.next.type == "NOT":
            Parser.tokenizer.selectNext()
            result = UnOp("!", [Parser.parseFactor()])
            return result
        
        elif Parser.tokenizer.next.type == "OPEN_PAR":
            Parser.tokenizer.selectNext()
            result = Parser.parseBoolExpression()
            if Parser.tokenizer.next.type == "CLOSE_PAR":
                Parser.tokenizer.selectNext()
                return result
        
        elif Parser.tokenizer.next.type == "ID":
            id = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                result = FuncCall(id, [])
                while Parser.tokenizer.next.type != "CLOSE_PAR":
                    result.children.append(Parser.parseBoolExpression())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                    else:
                        break
                if Parser.tokenizer.next.type == "CLOSE_PAR":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise TypeError("Erro")
            else:
                result = Identifier(id, [])
                return result
        
        elif Parser.tokenizer.next.type == "Scanln":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                result = Scanln("Scanln", [])
                if Parser.tokenizer.next.type == "CLOSE_PAR":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")
            
    def parseTerm():
        result = Parser.parseFactor()
        while Parser.tokenizer.next.type == "TIMES" or Parser.tokenizer.next.type == "DIV":
            if Parser.tokenizer.next.type == "TIMES":
                Parser.tokenizer.selectNext()
                result = BinOp("*", [result, Parser.parseFactor()])
            elif Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.selectNext()
                result = BinOp("/", [result, Parser.parseFactor()])

        return result
    
    def parseExpression():
        result = Parser.parseTerm()
        while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS" or Parser.tokenizer.next.type == "CONCAT":
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                result = BinOp("+", [result, Parser.parseTerm()])
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                result = BinOp("-", [result, Parser.parseTerm()])
            elif Parser.tokenizer.next.type == "CONCAT":
                Parser.tokenizer.selectNext()
                result = BinOp(".", [result, Parser.parseTerm()])    
        return result
    
    def parseStatement():
        result = None
        if Parser.tokenizer.next.type == "BREAKLINE":
            Parser.tokenizer.selectNext()
            return NoOp("NoOp", [])
        
        elif Parser.tokenizer.next.type == "ID":
            ident = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.selectNext()
                result = Assignment("=", [ident, Parser.parseBoolExpression()])
                if Parser.tokenizer.next.type == "BREAKLINE":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise TypeError("Erro")
                
            elif Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                result = FuncCall(ident.value, [])
                while Parser.tokenizer.next.type != "CLOSE_PAR":
                    result.children.append(Parser.parseBoolExpression())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                    else:
                        break
                if Parser.tokenizer.next.type == "CLOSE_PAR":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "BREAKLINE":
                        Parser.tokenizer.selectNext()
                        return result
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro")
        
        elif Parser.tokenizer.next.type == "if":
            Parser.tokenizer.selectNext()
            condition = Parser.parseBoolExpression()
            if_block = Parser.parseBlock()
            if Parser.tokenizer.next.type == "else":
                Parser.tokenizer.selectNext()
                else_block = Parser.parseBlock()
                result = If("if", [condition, if_block, else_block])
            else:
                result = If("if", [condition, if_block])
            if Parser.tokenizer.next.type == "BREAKLINE":
                Parser.tokenizer.selectNext()
                return result
        
        elif Parser.tokenizer.next.type == "for":
            Parser.tokenizer.selectNext()
            atribution = Parser.parseAssigments()
            if Parser.tokenizer.next.type == "SEMICOLON":
                Parser.tokenizer.selectNext()
                condition = Parser.parseBoolExpression()
                if Parser.tokenizer.next.type == "SEMICOLON":
                    Parser.tokenizer.selectNext()
                    increment = Parser.parseAssigments()
                    block = Parser.parseBlock()
                    result = For("for", [atribution, condition, increment, block])
            if Parser.tokenizer.next.type == "BREAKLINE":
                Parser.tokenizer.selectNext()
                return result
            else:
                raise TypeError("Erro")
        
        elif Parser.tokenizer.next.type == "var":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "ID":
                ident = Identifier(Parser.tokenizer.next.value, [])
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "type":
                    type = Parser.tokenizer.next.value
                    result = VarDec(type, [ident])
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "EQUAL":
                        Parser.tokenizer.selectNext()
                        result.children.append(Parser.parseBoolExpression())
                    if Parser.tokenizer.next.type == "BREAKLINE":
                        Parser.tokenizer.selectNext()
                        return result
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")
        
        elif Parser.tokenizer.next.type == "Println":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                result = Print("Println", [Parser.parseBoolExpression()])
                if Parser.tokenizer.next.type == "CLOSE_PAR":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "BREAKLINE":
                        Parser.tokenizer.selectNext()
                        return result
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro")
            
        elif Parser.tokenizer.next.type == "return":
            Parser.tokenizer.selectNext()
            resultado = Return("return", [Parser.parseBoolExpression()])
            if Parser.tokenizer.next.type == "BREAKLINE":
                Parser.tokenizer.selectNext()
                return resultado
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")

    def parseBlock():
        if Parser.tokenizer.next.type == "OPEN_BRACE":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "BREAKLINE":
                Parser.tokenizer.selectNext()
                result = Block("", [])
                while Parser.tokenizer.next.type != "CLOSE_BRACE":
                    result.children.append(Parser.parseStatement())
                if Parser.tokenizer.next.type == "CLOSE_BRACE":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise TypeError("Erro")
    
    def parseRelExpression():
        result = Parser.parseExpression()

        while Parser.tokenizer.next.type == "COMPARE" or Parser.tokenizer.next.type == "GREATER" or Parser.tokenizer.next.type == "LESS":
            if Parser.tokenizer.next.type == "COMPARE":
                Parser.tokenizer.selectNext()
                result = BinOp("==", [result, Parser.parseExpression()])
            elif Parser.tokenizer.next.type == "GREATER":
                Parser.tokenizer.selectNext()
                result = BinOp(">", [result, Parser.parseExpression()])
            elif Parser.tokenizer.next.type == "LESS":
                Parser.tokenizer.selectNext()
                result = BinOp("<", [result, Parser.parseExpression()])
        
        return result
    
    def parseBoolTerm():
        result = Parser.parseRelExpression()
        while Parser.tokenizer.next.type == "AND":
            Parser.tokenizer.selectNext()
            result = BinOp("&&", [result, Parser.parseRelExpression()])
        
        return result

    def parseBoolExpression():
        result = Parser.parseBoolTerm()
        while Parser.tokenizer.next.type == "OR":
            Parser.tokenizer.selectNext()
            result = BinOp("||", [result, Parser.parseBoolTerm()])
        
        return result
    
    def parseAssigments():
        if Parser.tokenizer.next.type == "ID":
            id = Parser.tokenizer.next.value
            id_node = Identifier(id, [])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.selectNext()
                parseBoolExpression = Parser.parseBoolExpression()
                return Assignment("=",[id_node, parseBoolExpression])
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                result = FuncCall(id_node, [])
                while Parser.tokenizer.next.type != "CLOSE_PAR":
                    result.children.append(Parser.parseBoolExpression())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                    else:
                        break
                if Parser.tokenizer.next.type == "CLOSE_PAR":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "BREAKLINE":
                        Parser.tokenizer.selectNext()
                        return result
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")       
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")
    
    def parseDeclaration():
        parameters = []
        
        if Parser.tokenizer.next.type == "func":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "ID":
                func_name = Parser.tokenizer.next.value
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "OPEN_PAR":
                    Parser.tokenizer.selectNext()
                    while Parser.tokenizer.next.type == "ID":
                        variable_name = Parser.tokenizer.next.value
                        Parser.tokenizer.selectNext()
                        variable_type = Parser.tokenizer.next.value
                        Parser.tokenizer.selectNext()
                        parameters.append((variable_type, variable_name))
                        if Parser.tokenizer.next.type == "COMMA":
                            Parser.tokenizer.selectNext()
                        else:
                            break

                    if Parser.tokenizer.next.type == "CLOSE_PAR":
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == "type":
                            func_type = Parser.tokenizer.next.value
                            Parser.tokenizer.selectNext()
                            result = FuncDec(None, [VarDec(func_type, [Identifier(func_name, [])])])
                            if len(parameters) > 0:
                                for i in range(len(parameters)):
                                    result.children.append(VarDec(parameters[i][0], [Identifier(parameters[i][1], [])]))
                            result.children.append(Parser.parseBlock())

                            if Parser.tokenizer.next.type == "BREAKLINE":
                                Parser.tokenizer.selectNext()
                            else:
                                raise TypeError("Erro")
                            return result
                        else:
                            raise TypeError("Erro")
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")

    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        result = Parser.parseProgram()
        if Parser.tokenizer.next.type == "EOF":
            return result
        else:
            raise TypeError("Erro")


if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        codigo = file.read()
        codigo = PrePro.filter(codigo) + "\n"

    run = Parser.run(codigo)
    symbol_table = SymbolTable()
    run.evaluate(symbol_table)
