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

    def __repr__(self):
        return "<" + self.value + ",".join(self.children) + ">"


class BinOp(Node):
    def evaluate(self, sym_table):
        left = self.children[0].evaluate(sym_table)
        right = self.children[1].evaluate(sym_table)
        # print(left, right)

        if self.value == '+':
            if left[1] != right[1] or left[1] != 'int':
                raise SyntaxError("Erro de BinOp +")
            return (self.children[0].evaluate(sym_table)[0] + self.children[1].evaluate(sym_table)[0], "int")
        elif self.value == '-':
            if left[1] != right[1] or left[1] != 'int':
                raise SyntaxError("Erro de BinOp -")
            return (self.children[0].evaluate(sym_table)[0] - self.children[1].evaluate(sym_table)[0], "int")
        elif self.value == '*':
            if left[1] != right[1] or left[1] != 'int':
                raise SyntaxError("Erro de BinOp *")
            return (self.children[0].evaluate(sym_table)[0] * self.children[1].evaluate(sym_table)[0], "int")
        elif self.value == '/':
            if left[1] != right[1] or left[1] != 'int':
                raise SyntaxError("Erro de BinOp /")
            return (self.children[0].evaluate(sym_table)[0] // self.children[1].evaluate(sym_table)[0], "int")
        elif self.value == '==':
            if left[1] != right[1]:
                raise SyntaxError("Erro de BinOp ==")
            return (int(self.children[0].evaluate(sym_table)[0] == self.children[1].evaluate(sym_table)[0]), "int")
        elif self.value == '&&':
            if left[1] != right[1] or left[1] != 'int':
                raise SyntaxError("Erro de BinOp &&")
            return (int(self.children[0].evaluate(sym_table)[0] and self.children[1].evaluate(sym_table)[0]), "int")
        elif self.value == '||':
            if left[1] != right[1] or left[1] != 'int':
                raise SyntaxError("Erro de BinOp ||")
            return (int(self.children[0].evaluate(sym_table)[0] or self.children[1].evaluate(sym_table)[0]), "int")
        elif self.value == '>':
            return (int(self.children[0].evaluate(sym_table)[0] > self.children[1].evaluate(sym_table)[0]), "int")
        elif self.value == '<':
            return (int(self.children[0].evaluate(sym_table)[0] < self.children[1].evaluate(sym_table)[0]), "int")
        elif self.value == '.':
            return (str(self.children[0].evaluate(sym_table)[0]) + str(self.children[1].evaluate(sym_table)[0]), "string")
        
class UnOp(Node):
    def evaluate(self, sym_table):
        if self.value == '+':
            return (self.children[0].evaluate(sym_table)[0], 'int')
        elif self.value == '-':
            return (-self.children[0].evaluate(sym_table)[0], 'int')
        elif self.value == '!':
            return (not self.children[0].evaluate(sym_table)[0], 'int')

class SymbolTable:
    def __init__(self):
        self.symbol_table = {}

    def set(self, identifier, value):
        if value[1] != self.symbol_table[identifier][1]:
            raise SyntaxError("Erro de tipos") 
        self.symbol_table[identifier] = value

    def get(self, identifier):
        # print(self.symbol_table)
        return self.symbol_table[identifier]
        
    def assing(self, identifier, value):
        if identifier in self.symbol_table.keys():
            raise SyntaxError(f"'{identifier}' already exists in the symbol table")
        else:
            self.symbol_table[identifier] = value

class FuncTable:
    def __init__(self):
        self.func_table = {}

    def setfunc(self, identifier, value):
        if value[1] != self.func_table[identifier][1]:
            raise SyntaxError("Erro de tipos")
        self.func_table[identifier] = value

    def getfunc(self, identifier):
        return self.func_table[identifier]

class IntVal(Node):
    def evaluate(self, sym_table):
        return (int(self.value), "int")
    
class NoOp(Node):
    def evaluate(self, sym_table):
        pass
    
class StringVal(Node):
    def evaluate(self, sym_table):
        return (self.value, "string")

class Assignment(Node):
    def evaluate(self, sym_table):
        
        sym_table.set(self.children[0].value, self.children[1].evaluate(sym_table))
        

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
        print(self.children[0].evaluate(sym_table)[0])
        return 0

class ScanLn(Node):
    def evaluate(self, sym_table):
        return (int(input()), "int")

class If(Node):
    def evaluate(self, sym_table):
        if self.children[0].evaluate(sym_table):
            self.children[1].evaluate(sym_table)
        elif len(self.children) == 3:
            self.children[2].evaluate(sym_table)
        
class For(Node):
    def evaluate(self, sym_table):
        self.children[0].evaluate(sym_table)
        while self.children[1].evaluate(sym_table)[0]:
            self.children[3].evaluate(sym_table)
            self.children[2].evaluate(sym_table)

class VarDec(Node):
    def evaluate(self, sym_table):
        if len(self.children) == 1:
            if self.value == 'int':
                sym_table.assing(self.children[0].value, (0, self.value))
            elif self.value == 'string':
                sym_table.assing(self.children[0].value, ("", self.value))
        else:
            sym_table.assing(self.children[0].value, (self.children[1].evaluate(sym_table)[0], self.value))

class ReturnFunc(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, sym_table):
        return self.children[0].evaluate(sym_table)
    
class FuncDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, sym_table):
        functionName = self.children[0].value
        functionValue = self

        if len(self.children) != 3:
            raise Exception('Error in function declaration')
        FuncTable.setfunc(functionName, (functionValue, self.value))

class FuncCall(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, sym_table):
        funcObj = FuncTable.getfunc(self.value)

        if len(funcObj.children) != len(self.children)+2:
            raise Exception('Error in function call')
        localSymTable = SymbolTable()

        for i in range(len(self.children)):
            funcObj.children[i+1].evaluate(localSymTable)
            localSymTable.set(funcObj.children[i+1].value, self.children[i].evaluate(localSymTable))
        return self.children[-1].evaluate(localSymTable)

class Tokenizer:

    specialWords = ['Println', 'Scanln', 'if', 'for', 'else', 'var', 'int', 'string', 'func', 'return']

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
                    self.position += 1
                elif self.source[self.position] == ",":
                    self.next = Token(self.source[self.position], "COMMA")
                    self.position += 1
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
                            self.next = Token(identifier, "TYPE")
                        elif identifier == "func":
                            self.next = Token(identifier, "FUNC")
                        elif identifier == "return":
                            self.next = Token(identifier, "RETURN")
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
            identifier = Identifier(Parser.tokenizer.next.value, [])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                if not Parser.tokenizer.next.type == "CLOSE_PAR":
                    args = []
                    args.append(Parser.parseBoolExpression())
                    while Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                        arg = Parser.parseBoolExpression()
                        args.append(arg)
                    if Parser.tokenizer.next.type == "CLOSE_PAR":
                        Parser.tokenizer.selectNext()
                        result = FuncCall(identifier.value, args)
                        return result
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")
            else:
                return identifier
                
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
                result = BinOp("*", [result, Parser.parseFactor()])
            elif Parser.tokenizer.next.type == "DIVIDE":
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
                Parser.tokenizer.selectNext()
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
                    tipo = Parser.tokenizer.next.value
                    varDec = VarDec(Parser.tokenizer.next.value, [identificador])
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "ASSIGN":
                        Parser.tokenizer.selectNext()
                        resultado = VarDec(tipo, [identificador, Parser.parseBoolExpression()])
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
        elif Parser.tokenizer.next.type == "RETURN":
            Parser.tokenizer.selectNext()
            resultado = ReturnFunc("return", [Parser.parseBoolExpression()])
            if Parser.tokenizer.next.type == "BREAKLINE":
                Parser.tokenizer.selectNext()
                return resultado
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
        while Parser.tokenizer.next.value == "AND":
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
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                if not Parser.tokenizer.next.type == "CLOSE_PAR":
                    args = []
                    args.append(Parser.parseBoolExpression())
                    while Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                        arg = Parser.parseBoolExpression()
                        args.append(arg)
                    if Parser.tokenizer.next.type == "CLOSE_PAR":
                        Parser.tokenizer.selectNext()
                        result = FuncCall(identifier.value, args)
                        return result
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")
            elif Parser.tokenizer.next.type == "ASSIGN":
                Parser.tokenizer.selectNext()
                result = Assignment("=", [identifier, Parser.parseBoolExpression()])
                return result
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro") 
        
    def parseDeclaration():
        if Parser.tokenizer.next.type == "FUNC":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "IDENTIFIER":
                funcName = Identifier(Parser.tokenizer.next.value, [])
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "OPEN_PAR":
                    Parser.tokenizer.selectNext()
                    args = []
                    if Parser.tokenizer.next.type == "CLOSE_PAR":
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == "TYPE":
                            funcType = Parser.tokenizer.next.value
                            block = Parser.parseBlock()
                            Parser.tokenizer.selectNext()
                            if Parser.tokenizer.next.type == "BREAKLINE":
                                Parser.tokenizer.selectNext()
                                return FuncDec(funcName.value, [VarDec(funcType, [funcName]) + args + [block]])
                    elif Parser.tokenizer.next.type == "IDENTIFIER":
                        parametro = Parser.tokenizer.next.value
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == "TYPE":
                            tipo = Parser.tokenizer.next.value
                            args.append(VarDec(tipo, [Identifier(parametro, [])]))
                            Parser.tokenizer.selectNext()
                            while Parser.tokenizer.next.type == "COMMA":
                                Parser.tokenizer.selectNext()
                                if Parser.tokenizer.next.type == "IDENTIFIER":
                                    parametro = Parser.tokenizer.next.value
                                    Parser.tokenizer.selectNext()
                                    if Parser.tokenizer.next.type == "TYPE":
                                        tipo = Parser.tokenizer.next.value
                                        args.append(VarDec(tipo, [Identifier(parametro, [])]))
                                        Parser.tokenizer.selectNext()
                                    else:
                                        raise TypeError("Erro")
                                else:
                                    raise TypeError("Erro")
                            if Parser.tokenizer.next.type == "CLOSE_PAR":
                                Parser.tokenizer.selectNext()
                                if Parser.tokenizer.next.type == "TYPE":
                                    funcType = Parser.tokenizer.next.value
                                    block = Parser.parseBlock()
                                    Parser.tokenizer.selectNext()
                                    if Parser.tokenizer.next.type == "BREAKLINE":
                                        return FuncDec(funcName.value, [VarDec(funcType, [funcName]) + args + [block]])

        
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
        code = file.read()+"\n"
        code = PrePro.filter(code)
    symbol_table = SymbolTable()
    run = Parser.run(code)
    run.evaluate(symbol_table)