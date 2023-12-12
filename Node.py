from Tokenizer import *
from Token import Token

class SymbolTable:
    def __init__(self):
        self.table = {}

    def setter(self, key, value):
        if value[1] != self.table[key][1]:
            print(value)
            raise SyntaxError("Tipo não combina: "+value[1]+"!="+self.table[key][1]) 
        self.table[key] = value
        
    def getter(self, key):
        return self.table[key]
    
    def create(self, key, value):
        if key in self.table.keys():
            raise SyntaxError("Essa variável já existe")
        else:
            self.table[key] = value

class FuncTable:
    def __init__(self):
        self.table = {}

    def setter(self, key, value):
        self.table[key] = value
        
    def getter(self, key):
        return self.table[key]
    
class Node:
    def __init__(self, value, children):
        self.value = value 
        self.children = children

    def evaluate(self, symbol_table):
        pass

class BinOp(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        left = self.children[0].evaluate(table,funcTable)
        right = self.children[1].evaluate(table,funcTable)
        
        if self.value == ".":
            return (str(left[0])+str(right[0]),"string")
        
        if left[1] == right[1]:
            if self.value == "+":
                return (left[0] + right[0],"int")
            elif self.value == "-":
                return (left[0] - right[0],"int")
            if self.value == "*":
                return (left[0] * right[0],"int")
            elif self.value == "/":
                return (left[0] // right[0],"int")
            elif self.value == "||":
                return (int(left[0] | right[0]),"int")
            elif self.value == "&&":
                return (int(left[0] & right[0]),"int")
            elif self.value == "==":
                return (int(left[0] == right[0]),"int")
            elif self.value == ">":
                return (int(left[0] > right[0]),"int")
            elif self.value == "<":
                return (int(left[0] < right[0]),"int")
            else:
                raise Exception("Erro")
        else:
            raise Exception("Erro")

class UnOp(Node):
    def evaluate(self, symbol_table):
        if self.value == "+":
            return (self.children[0].evaluate(symbol_table)[0], "int")
        elif self.value == "!":
            return (not self.children[0].evaluate(symbol_table)[0], "int")
        else:
            return (-self.children[0].evaluate(symbol_table)[0], "int")

class IntVal(Node):
    def evaluate(self, symbol_table):
        return (int(self.value), "int")
    
class NoOp(Node):
    def evaluate(self, symbol_table):
        pass
    
class StrVal(Node):
    def evaluate(self, symbol_table):
        return (self.value, "string")
    
class Assigment(Node):
    def evaluate(self, symbol_table):
        symbol_table.setter(self.children[0].value, self.children[1].evaluate(symbol_table))

class Identifier(Node):
    def evaluate(self, symbol_table):
        return symbol_table.getter(self.value)
    
class Block(Node):
    def evaluate(self, symbol_table):
        for child in self.children:
            if isinstance(child, ReturnNode):
                return child.evaluate(symbol_table)

class PrintLn(Node):
    def evaluate(self, symbol_table):
        print(self.children[0].evaluate(symbol_table)[0])
        
class ScanLn(Node):
    def evaluate(self, symbol_table):
        return (int(input()), "int")

class If(Node):
    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table)[0]:
            self.children[1].evaluate(symbol_table)
        elif len(self.children)>2:
            self.children[2].evaluate(symbol_table)

class For(Node):
    def evaluate(self, symbol_table):
        self.children[0].evaluate(symbol_table)
        while self.children[1].evaluate(symbol_table)[0]:
            self.children[3].evaluate(symbol_table)
            self.children[2].evaluate(symbol_table)
            
class VarDec(Node):
    def evaluate(self, symbol_table):
        if len(self.children) == 1:
            if self.value == "int":
                symbol_table.create(self.children[0].value, (0, self.value))
            elif self.value == "string":
                symbol_table.create(self.children[0].value, ("", self.value))
            
        else:
            tipo = self.children[1].evaluate(symbol_table)
            if self.value != tipo[1]:
                raise SyntaxError("Tipo errado")
            symbol_table.create(self.children[0].value, (tipo[0], self.value))

class ReturnNode(Node):
    def evaluate(self, symbol_table):
        return self.children[0].evaluate(symbol_table)
         
class FuncDec(Node):
    def evaluate(self, symbol_table):
        FuncTable.setter(self.children[0].children[0].value, (self, self.children[0].value))
 
class FuncCall(Node):
    def evaluate(self, symbol_table):
        call = FuncTable.getter(self.value)
        
        if len(call[0].children) != len(self.children)+2:
            raise SyntaxError("Número de argumentos errados")
        
        nst = SymbolTable()
        for i in range(len(self.children)):
            call[0].children[i+1].evaluate(nst)
            nst.setter(call[0].children[i+1].children[0].value, self.children[i].evaluate(symbol_table))
        
        result = call[0].children[-1].evaluate(nst)
        
        if result is not None:
            if call[1] != result[1]:
                raise SyntaxError("Tipo de função errado")
            else:
                return result