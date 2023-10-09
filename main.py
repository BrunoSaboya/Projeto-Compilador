import sys
from abc import ABC, abstractmethod

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    @abstractmethod
    
    def evaluate(self, st):
        pass

class PrePro: 
    
    def filter(code):
        code = code.split("\n")
        for i in range(len(code)):
            if "//" in code[i]:
                code[i] = code[i].split("//")[0]
        code = "\n".join(code)
        return code
    
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
        else:
            raise Exception('Invalid operator')

        return result
        
class UnOp(Node):
    def evaluate(self, sym_table):
        if self.value == "+":
            return +self.children[0].evaluate(sym_table)
        elif self.value == "-":
            return -self.children[0].evaluate(sym_table)
        elif self.value == "!":
            return not self.children[0].evaluate(sym_table)
        
class IntVal(Node):
    def evaluate(self, sym_table):
        return self.value
    
class NoOp(Node):
    def evaluate(self, sym_table):
        pass
    
class Symbol_Table:
    symbol_table = {}

    def get(self, ident):
        if ident in self.symbol_table:
            return self.symbol_table[ident]
        else:
            raise NameError(f"'{ident}' not found in the symbol table")
        
    def set(self, identifier, value):
        self.symbol_table[identifier] = value

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

class Println(Node):
    def evaluate(self, sym_table):
        print(self.children[0].evaluate(sym_table))

class Scanln(Node):
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
    
class Tokenizer:

    specialWords = ['Println', 'Scanln', 'if', 'for', 'else']

    def __init__(self, source : str):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        blank = True
        while blank:
            blank = False
            if self.position == len(self.source):
                self.next = Token("EOF", "")
            elif self.position != len(self.source):
                if self.source[self.position].isdigit():
                    number = ""
                    while self.position < len(self.source) and self.source[self.position].isdigit():
                        number += self.source[self.position]
                        self.position += 1
                    self.next = Token("NUMBER", int(number))
                elif self.source[self.position] == "+":
                    self.next = Token("PLUS", self.source[self.position])
                    self.position += 1
                elif self.source[self.position] == "-":
                    self.next = Token("MINUS", self.source[self.position])
                    self.position += 1
                elif self.source[self.position] == "*":
                    self.next = Token("MULTIPLY", self.source[self.position])
                    self.position += 1
                elif self.source[self.position] == "/":
                    self.next = Token("DIVIDE", self.source[self.position])
                    self.position += 1
                elif self.source[self.position] == "(":
                    self.next = Token("OPEN_PAR", self.source[self.position])
                    self.position += 1                
                elif self.source[self.position] == ")":
                    self.next = Token("CLOSE_PAR", self.source[self.position])
                    self.position += 1
                elif self.source[self.position] == "=":
                    if self.source[self.position+1] == "=":
                        self.next = Token("EQUALS", "==")
                        self.position += 2
                    else:
                        self.next = Token("ASSIGN", self.source[self.position])
                        self.position += 1
                elif self.source[self.position] == "\n":
                    self.next = Token("BREAKLINE", self.source[self.position])
                    self.position += 1
                elif self.source[self.position] == "|":
                    if self.source[self.position+1] == "|":  
                        self.next = Token("OR", "||")
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
                    self.next = Token("GREATER", self.source[self.position])
                    self.position += 1                
                elif self.source[self.position] == "<":
                    self.next = Token("LESS", self.source[self.position])
                    self.position += 1                
                elif self.source[self.position] == "!":
                    self.next = Token("NOT", self.source[self.position])
                    self.position += 1
                elif self.source[self.position] == "{":
                    self.next = Token("OPEN_BRACE", self.source[self.position])
                    self.position += 1
                elif self.source[self.position] == "}":
                    self.next = Token("CLOSE_BRACE", self.source[self.position])
                    self.position += 1
                elif self.source[self.position] == ";":
                    self.next = Token("SEMICOLUMN", self.source[self.position])
                    self.position += 1
                elif self.source[self.position].isalpha():
                    identifier = ""
                    while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                        identifier += self.source[self.position]
                        self.position += 1
                    if identifier in Tokenizer.specialWords:
                        if identifier == "Println":    
                            self.next = Token("PRINTLN", identifier)
                        elif identifier == "if":
                            self.next = Token("IF", identifier)
                        elif identifier == "else":
                            self.next = Token("ELSE", identifier)
                        elif identifier == "for":
                            self.next = Token("FOR", identifier)
                        elif identifier == "Scanln":
                            self.next = Token("SCANLN", identifier)
                    else:
                        self.next = Token("IDENTIFIER", identifier) 
                elif self.source[self.position].isspace(): 
                    blank = True
                    self.position += 1
                else:
                    raise TypeError("Erro")
            else:
                raise ValueError("Erro")
        
class Parser:

    tokenizer = None

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
                resultado = Scanln("Scanln", [])
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
        resultado = Parser.parseFactor()
        while Parser.tokenizer.next.type == "MULTIPLY" or Parser.tokenizer.next.type == "DIVIDE":
            if Parser.tokenizer.next.type == "MULTIPLY":
                Parser.tokenizer.selectNext()
                resultado = BinOp("*", [resultado, Parser.parseFactor()])            
            elif Parser.tokenizer.next.type == "DIVIDE":
                Parser.tokenizer.selectNext()
                resultado = BinOp("/", [resultado, Parser.parseFactor()])         
        return resultado
    
    def parseExpression():
        resultado = Parser.parseTerm()

        while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS":
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                resultado = BinOp("+", [resultado, Parser.parseTerm()])
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                resultado = BinOp("-", [resultado, Parser.parseTerm()])           
        return resultado
    
    def parseStatement():
        resultado = None
        if Parser.tokenizer.next.type == "BREAKLINE":
            Parser.tokenizer.selectNext()
            return NoOp("NoOp", [])
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
                resultado = Println("Println", [Parser.parseBoolExpression()])
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
            if Parser.tokenizer.next.type == "SEMICOLUMN":
                Parser.tokenizer.selectNext()
                resultado.children.append(Parser.parseBoolExpression())
                if Parser.tokenizer.next.type == "SEMICOLUMN":
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
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")
        
    def parseRelExpression():
        expression = Parser.parseExpression()
        while Parser.tokenizer.next.type == "EQUALS" or Parser.tokenizer.next.type == "GREATER" or Parser.tokenizer.next.type == "LESS":
            if Parser.tokenizer.next.type == "EQUALS":
                Parser.tokenizer.selectNext()
                expression = BinOp("==", [expression, Parser.parseExpression()])
            elif Parser.tokenizer.next.type == "GREATER":
                Parser.tokenizer.selectNext()
                expression = BinOp(">", [expression, Parser.parseExpression()])
            elif Parser.tokenizer.next.type == "LESS":
                Parser.tokenizer.selectNext()
                expression = BinOp("<", [expression, Parser.parseExpression()])
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
            if Parser.tokenizer.next.type == "ASSIGN":
                Parser.tokenizer.selectNext()
                result = Assignment("=", [identifier, Parser.parseBoolExpression()])
                return result
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")
            
    def parseProgram():
        result = Block("Block", [])
        while Parser.tokenizer.next.type != "EOF":
            result.children.append(Parser.parseStatement())
        return result
    
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        result = Parser.parseProgram()
        if Parser.tokenizer.next.type == "EOF":
            return result
        else:
            raise TypeError("Erro")   

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        code = file.read()
        code = PrePro.filter(code)
    symbol_table = Symbol_Table()    
    run = Parser.run(code)
    run.evaluate(symbol_table)