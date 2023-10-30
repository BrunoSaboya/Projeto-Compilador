import sys
import re
from abc import ABC, abstractmethod

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

class PrePro:
    def filter(code):
        code = code.split("\n")
        for i in range(len(code)):
            if "//" in code[i]:
                code[i] = code[i].split("//")[0]
        code = "\n".join(code)
        return code

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self, sym_table):
        pass


class BinOp(Node):
    def evaluate(self, sym_table):
        left = self.children[0].evaluate(sym_table)
        right = self.children[1].evaluate(sym_table)

        if self.value == '+':
            result = left + right
        elif self.value == '-':
            result = left - right
        elif self.value == '*':
            result = left * right
        elif self.value == '/':
            result = left // right
        elif self.value == '>':
            result = left > right
        elif self.value == '<':
            result = left < right
        elif self.value == '==':
            result = left == right
        elif self.value == '&&':
            result = left and right
        elif self.value == '!':
            result = not right
        elif self.value == '||':
            result = left or right
        elif self.value == '.':
            result = str(left) + str(right)
        else:
            raise Exception('Invalid operator')

        return result

class UnOp(Node):
    def evaluate(self, sym_table):
        if self.value == '+':
            return +self.children[0].evaluate(sym_table)
        elif self.value == '-':
            return -self.children[0].evaluate(sym_table)
        elif self.value == '!':
            return not self.children[0].evaluate(sym_table)
        else:
            raise Exception('Invalid operator')

class SymbolTable:
    symbol_table = {}

    def set(self, identifier, value):
        self.symbol_table[identifier] = value

    def get(self, identifier):
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]
        else:
            raise Exception(f"'{identifier}' not found in the symbol table")
        
    def assing(self, identifier, value):
        if identifier in self.symbol_table:
            raise Exception(f"'{identifier}' already exists in the symbol table")
        else:
            self.symbol_table[identifier] = value

class IntVal(Node):
    def evaluate(self, sym_table):
        return self.value
    
class NoOp(Node):
    def evaluate(self, sym_table):
        pass
    
class StringVal(Node):
    def evaluate(self, sym_table):
        return self.value

class Assignment(Node):
    def evaluate(self, sym_table):
        return sym_table.set(self.children[0].value, self.children[1].evaluate(sym_table))

class Identifier(Node):
    def evaluate(self, sym_table):
        return sym_table.get(self.value)

class Block(Node):
    def evaluate(self, sym_table):
        for child in self.children:
            child.evaluate(sym_table)

class Program(Node):
    def evaluate(self, sym_table):
        for child in self.children:
            child.evaluate(sym_table)

class PrintLn(Node):
    def evaluate(self, sym_table):
        val = self.children[0].evaluate(sym_table)
        print(val)

class ScanLn(Node):
    def evaluate(self, sym_table):
        return int(input())

class If(Node):
    def evaluate(self, sym_table):
        if self.children[0].evaluate(sym_table):
            self.children[1].evaluate(sym_table)
        elif len(self.children) == 3:
            self.children[2].evaluate(sym_table)
        
class For(Node):
    def evaluate(self, sym_table):
        self.children[0].evaluate(sym_table)
        while self.children[1].evaluate(sym_table):
            self.children[3].evaluate(sym_table)
            self.children[2].evaluate(sym_table)

class VarDec(Node):
    def evaluate(self, sym_table):
        if (len(self.children)) == 1:
            if self.value == 'int':
                sym_table.assing(self.children[0].value, 0)
            elif self.value == 'string':
                sym_table.assing(self.children[0].value, "")
        else:
            sym_table.assing(self.children[0].value, self.children[1].evaluate(sym_table))

class Tokenizer:

    specialWords = ['Println', 'Scanln', 'if', 'for', 'else', 'var', 'int', 'string']

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        blank = True
        while blank:
            blank = False
            if self.position == len(self.source):
                self.next = Token("", "EOF")
            elif self.position != len(self.source):
                if self.source[self.position].isdigit():
                    while self.position < len(self.source) and self.source[self.position].isdigit():
                        number = ""
                        number += self.source[self.position]
                        self.position += 1
                    self.next = Token(int(number), "NUMBER")
                elif self.source[self.position] == "+":
                    self.next = Token(self.source[self.position], "PLUS")
                    self.position += 1
                elif self.source[self.position] == "-":
                    self.next = Token(self.source[self.position], "MINUS")
                    self.position += 1
                elif self.source[self.position] == "*":
                    self.next = Token(self.source[self.position], "MULTIPLY")
                    self.position += 1
                elif self.source[self.position] == "/":
                    self.next = Token(self.source[self.position], "DIVIDE")
                    self.position += 1
                elif self.source[self.position] == "(":
                    self.next = Token(self.source[self.position], "OPEN_PAR")
                    self.position += 1                
                elif self.source[self.position] == ")":
                    self.next = Token(self.source[self.position], "CLOSE_PAR")
                    self.position += 1
                elif self.source[self.position] == ".":
                    self.next = Token(self.source[self.position], "CONCAT")
                elif self.source[self.position] == '"':
                    identifier = self.source[self.position]
                    self.position += 1
                    current_char = self.source[self.position]

                    while self.position < len(self.source) and current_char != '"':
                        identifier += current_char
                        self.position += 1
                        current_char = self.source[self.position]

                    if current_char == '"':
                        identifier += current_char
                        self.position += 1
                        identifier = identifier.strip('"')
                        self.next = Token(identifier, "STRING")
                    else:
                        raise SyntaxError("Erro de string mal formada")
                elif self.source[self.position] == "=":
                    if self.source[self.position+1] == "=":
                        self.next = Token("==", "EQUALS")
                        self.position += 2
                    else:
                        self.next = Token(self.source[self.position], "ASSIGN")
                        self.position += 1
                elif self.source[self.position] == "\n":
                    self.next = Token(self.source[self.position], "BREAKLINE")
                    self.position += 1
                elif self.source[self.position] == "|":
                    if self.source[self.position+1] == "|":  
                        self.next = Token("||", "OR")
                        self.position += 2
                    else:
                        raise TypeError("Erro")
                elif self.source[self.position] == "&":
                    if self.source[self.position+1] == "&":  
                        self.next = Token("AND", "&&")
                        self.position += 2
                    else:
                        raise TypeError("Erro")
                elif self.source[self.position] == ">":
                    self.next = Token(self.source[self.position], "GREATER")
                    self.position += 1                
                elif self.source[self.position] == "<":
                    self.next = Token(self.source[self.position], "LESS")
                    self.position += 1                
                elif self.source[self.position] == "!":
                    self.next = Token(self.source[self.position], "NOT")
                    self.position += 1
                elif self.source[self.position] == "{":
                    self.next = Token(self.source[self.position], "OPEN_BRACE")
                    self.position += 1
                elif self.source[self.position] == "}":
                    self.next = Token(self.source[self.position], "CLOSE_BRACE")
                    self.position += 1
                elif self.source[self.position] == ";":
                    self.next = Token(self.source[self.position], "SEMICOLON")
                    self.position += 1
                elif self.source[self.position].isalpha():
                    identifier = ""
                    while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                        identifier += self.source[self.position]
                        self.position += 1
                    if identifier in Tokenizer.specialWords:
                        if identifier == "Println":    
                            self.next = Token(identifier, "PRINTLN")
                        elif identifier == "if":
                            self.next = Token(identifier, "IF")
                        elif identifier == "else":
                            self.next = Token(identifier, "ELSE")
                        elif identifier == "for":
                            self.next = Token(identifier, "FOR")
                        elif identifier == "Scanln":
                            self.next = Token(identifier, "SCANLN")
                        elif identifier == "var":
                            self.next = Token(identifier, "VAR")
                        elif identifier == "int":
                            self.next = Token(identifier, "TYPE")
                        elif identifier == "string":
                            self.next = Token(identifier, "STRING")
                    else:
                        self.next = Token(identifier, "IDENTIFIER")
                elif self.source[self.position].isspace(): 
                    blank = True
                    self.position += 1
                else:
                    raise TypeError("Erro")
            else:
                raise ValueError("Erro")
            
class Parser:
    
    tokenizer = None
        
    def parseProgram():
        result = Program("", [])
        while Parser.tokenizer.next.type != "EOF":
            result.children.append(Parser.parseStatement())
        return result
    
    def parseFactor():
        resultado = None
        if Parser.tokenizer.next.type == "NUMBER":
            resultado = IntVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            return resultado
        
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            resultado = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            return resultado
        
        elif Parser.tokenizer.next.type == "STRING":
            resultado = StringVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            return resultado
        
        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.selectNext()
            resultado = UnOp("+", [Parser.parseFactor()])
            return resultado
        
        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.selectNext()
            resultado = UnOp("-", [Parser.parseFactor()])
            return resultado
        
        elif Parser.tokenizer.next.type == "NOT":
            Parser.tokenizer.selectNext()
            resultado = UnOp("!", [Parser.parseFactor()])
            return resultado
        
        elif Parser.tokenizer.next.type == "OPEN_PAR":
            Parser.tokenizer.selectNext()
            resultado = Parser.parseBoolExpression()
            if Parser.tokenizer.next.type == "CLOSE_PAR":
                Parser.tokenizer.selectNext()
                return resultado
            else:
                raise TypeError("Erro")
        elif Parser.tokenizer.next.type == "SCANLN":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                resultado = ScanLn("Scanln", [])
                if Parser.tokenizer.next.type == "CLOSE_PAR":
                    Parser.tokenizer.selectNext()
                    return resultado
                else:
                    raise TypeError("Erro")           
            else:
                raise TypeError("Erro")
        
        else:
            raise TypeError("Erro")
    
    def parseTerm():
        result = Parser.parseFactor()
        while Parser.tokenizer.next.type == "MULTIPLY" or Parser.tokenizer.next.type == "DIVIDE":
            if Parser.tokenizer.next.type == "MULTIPLY":
                Parser.tokenizer.selectNext()
                result = BinOp(None, [result, Parser.parseFactor()])
            elif Parser.tokenizer.next.type == "DIVIDE":
                Parser.tokenizer.selectNext()
                result = BinOp(None, [result, Parser.parseFactor()])
        return result
    
    def parseExpression():
        result = Parser.parseTerm()
        while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS" or Parser.tokenizer.next.type == "CONCAT":
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                result = BinOp(None, [result, Parser.parseTerm()])
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                result = BinOp(None, [result, Parser.parseTerm()])
            elif Parser.tokenizer.next.type == "CONCAT":
                Parser.tokenizer.selectNext()
                result = BinOp(None, [result, Parser.parseTerm()])  
        return result
        
    def parseStatement():
        resultado = None
        if Parser.tokenizer.next.type == "BREAKLINE":
            Parser.tokenizer.selectNext()
            return NoOp(None, [])
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            identificador = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "ASSIGN":
                Parser.tokenizer.selectNext()
                resultado = Assignment("=", [identificador, Parser.parseBoolExpression()])
                if Parser.tokenizer.next.type == "BREAKLINE":
                    Parser.tokenizer.selectNext()
                    return resultado
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro")
            
        elif Parser.tokenizer.next.type == "PRINTLN":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                resultado = PrintLn("PrintLn", [Parser.parseBoolExpression()])
                if Parser.tokenizer.next.type == "CLOSE_PAR":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "BREAKLINE":
                        Parser.tokenizer.selectNext()
                        return resultado
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro")
        elif Parser.tokenizer.next.type == "IF":
            Parser.tokenizer.selectNext()
            resultado = If("if", [Parser.parseBoolExpression()])
            resultado.children.append(Parser.parseBlock())
            if Parser.tokenizer.next.type == "ELSE":
                Parser.tokenizer.selectNext()
                resultado.children.append(Parser.parseBlock())
            if Parser.tokenizer.next.type == "BREAKLINE":
                Parser.tokenizer.select_next()
                return resultado
            else:
                raise TypeError("Erro")
        elif Parser.tokenizer.next.type == "FOR":
            Parser.tokenizer.selectNext()
            resultado = For("for", [Parser.parseAssignment()])
            if Parser.tokenizer.next.type == "SEMICOLON":
                Parser.tokenizer.selectNext()
                resultado.children.append(Parser.parseBoolExpression())
                if Parser.tokenizer.next.type == "SEMICOLON":
                    Parser.tokenizer.selectNext()
                    resultado.children.append(Parser.parseAssignment())
                    resultado.children.append(Parser.parseBlock())
                    if Parser.tokenizer.next.type == "BREAKLINE":
                        Parser.tokenizer.selectNext()
                        return resultado
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro")
        elif Parser.tokenizer.next.type == "VAR":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "IDENTIFIER":
                identificador = Identifier(Parser.tokenizer.next.value, [])
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "TYPE":
                    varDec = VarDec("var", [identificador])
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "ASSIGN":
                        Parser.tokenizer.selectNext()
                        resultado = VarDec("var", [identificador, Parser.parseBoolExpression()])
                        if Parser.tokenizer.next.type == "BREAKLINE":
                            Parser.tokenizer.selectNext()
                            return resultado
                        else:
                            raise TypeError("Erro")
                    elif Parser.tokenizer.next.type == "BREAKLINE":
                        Parser.tokenizer.selectNext()
                        return varDec
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")

    def parseBlock():
        result = Block("Block", [])
        if Parser.tokenizer.next.type == "OPEN_BRACE":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "BREAKLINE":
                Parser.tokenizer.selectNext()
                while Parser.tokenizer.next.type != "CLOSE_BRACE":
                    result.children.append(Parser.parseStatement())
                Parser.tokenizer.selectNext()
                return result
            else:
                raise TypeError("Expected breakline")
        else:
            raise TypeError("Expected opening brace")
    
    def parseRelExpression():
        expression = Parser.parseExpression()

        while Parser.tokenizer.next.type == "EQUALS" or Parser.tokenizer.next.type == "GREATER" or Parser.tokenizer.next.type == "LESS":
            if Parser.tokenizer.next.type == "EQUALS":
                Parser.tokenizer.selectNext()
                return BinOp("==", [expression, Parser.parseExpression()])
            elif Parser.tokenizer.next.type == "GREATER":
                Parser.tokenizer.selectNext()
                return BinOp(">", [expression, Parser.parseExpression()])
            elif Parser.tokenizer.next.type == "LESS":
                Parser.tokenizer.selectNext()
                return BinOp("<", [expression, Parser.parseExpression()])
        
        return expression

    def parseBoolTerm():
        expression = Parser.parseRelExpression()
        while Parser.tokenizer.next.type == "AND":
            Parser.tokenizer.selectNext()
            expression = BinOp("&&", [expression, Parser.parseRelExpression()])
        return expression   
    
    def parseBoolExpression():
        expression = Parser.parseBoolTerm()
        while Parser.tokenizer.next.type == "OR":
            Parser.tokenizer.selectNext()
            expression = BinOp("||", [expression, Parser.parseBoolTerm()])
        return expression

    def parseAssignment():
        if Parser.tokenizer.next.type == "IDENTIFIER":
            identifier = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.selectNext()
                result = Assignment("=", [identifier, Parser.parseBoolExpression()])
                return result
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
        code = file.read()
        code = PrePro.filter(code)
    symbol_table = SymbolTable()
    run = Parser.run(code)
    run.evaluate(symbol_table)