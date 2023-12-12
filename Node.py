from Tokenizer import *
from abc import ABC, abstractmethod

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod

    def evaluate(self, symbol_table):
        pass

class SymbolTable:
    def __init__(self) -> None:
        self.symbol_table = {}

    def getter(self, ident):
        if ident in self.symbol_table:
            return self.symbol_table[ident]
        else:
            raise TypeError("Erro")
    
    def setter(self, id, value):
        if value[0] == self.symbol_table[id][0]:
            if id in self.symbol_table:
                self.symbol_table[id] = value
            else:
                raise TypeError("Error: Variable not declared")
        else:
            raise TypeError("Error: Type mismatch")
    
    def create(self, id, type):
        if id not in self.symbol_table:
            self.symbol_table[id] = (type, None)
        else:
            raise TypeError("Error: Variable already declared")  

class FuncTable():
    func_table = {}

    def getter(id):
        if id in FuncTable.func_table:
            return FuncTable.func_table[id]
        else:
            raise TypeError("Erro")
    
    def setter(id, value):
        if value[0] == FuncTable[id][0]:
            if id in FuncTable.func_table:
                FuncTable.func_table[id] = value
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")
            
    def create(id, type, node):
        if id in FuncTable.func_table:
            raise TypeError("Erro")
        else:
            FuncTable.func_table[id] = (node, type)

class Block(Node):
    def evaluate(self, symbol_table):
        for child in self.children:
            if isinstance(child, Return):
                return child.evaluate(symbol_table)
            child.evaluate(symbol_table)

class Program(Node):
    def evaluate(self, symbol_table):
        for child in self.children:
            if isinstance(child, Return):
                return child.evaluate(symbol_table)
            child.evaluate(symbol_table)

class Print(Node):
    def evaluate(self, symbol_table):
        print(self.children[0].evaluate(symbol_table)[1])

class Identifier(Node):
    def evaluate(self, symbol_table):
        return symbol_table.getter(self.value)

class Assignment(Node): 
    def evaluate(self, symbol_table):
        symbol_table.setter(self.children[0].value, self.children[1].evaluate(symbol_table))

class BinOp(Node):
    def evaluate(self, symbol_table):
        left = self.children[0].evaluate(symbol_table)
        right = self.children[1].evaluate(symbol_table)
        if self.value == "+" and left[0] == right[0] and left[0] == "int":
            return (left[0], left[1] + right[1])
        
        elif self.value == "-" and left[0] == right[0] and left[0] == "int":
            return (left[0], left[1] - right[1])
        
        elif self.value == "*" and left[0] == right[0] and left[0] == "int":
            return (left[0], left[1] * right[1])
        
        elif self.value == "/" and left[0] == right[0] and left[0] == "int":
            return (left[0], left[1] // right[1])
        
        elif self.value == "==" and left[0] == right[0]:
            return (left[0], int(left[1] == right[1]))
        
        elif self.value == ">" and left[0] == right[0]:
            return (left[0], int(left[1] > right[1]))
        
        elif self.value == "<" and left[0] == right[0]:
            return (left[0], int(left[1] < right[1]))
        
        elif self.value == "&&" and left[0] == right[0] and left[0] == "int":
            return (left[0], int(left[1] and right[1]))
        
        elif self.value == "||" and left[0] == right[0] and left[0] == "int":
            return (left[0], int(left[1] or right[1]))
        
        elif self.value == ".":
            return ("string", str(left[1]) + str(right[1]))
        else:
            raise TypeError("Erro")

class UnOp(Node):
    def evaluate(self, symbol_table):
        left = self.children[0].evaluate(symbol_table)
        if self.value == "+" and left[0] == "int":
            return ("int", left[1])
        elif self.value == "-" and left[0] == "int":
            return ("int", -left[1])
        elif self.value == "!" and left[0] == "int":
            return ("int", int(not left[1]))

class IntVal(Node):
    def evaluate(self, symbol_table):
        return ("int", self.value)

class NoOp(Node):
    def evaluate(self, symbol_table):
        pass

class Scanln(Node):
    def evaluate(self, symbol_table):
        return ("int", int(input()))

class If(Node):
    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table):
            self.children[1].evaluate(symbol_table)
        elif len(self.children) == 3:
            self.children[2].evaluate(symbol_table)

class For(Node):
    def evaluate(self, symbol_table):
        self.children[0].evaluate(symbol_table)
        while self.children[1].evaluate(symbol_table)[1]:
            self.children[3].evaluate(symbol_table)
            self.children[2].evaluate(symbol_table)

class VarDec(Node):
    def evaluate(self, symbol_table):
        if len(self.children) == 2:
            symbol_table.create(self.children[0].value, self.value)
            symbol_table.setter(self.children[0].value, self.children[1].evaluate(symbol_table))
        else:
            symbol_table.create(self.children[0].value, self.value)

class FuncDec(Node):
    def evaluate(self, symbol_table):
        func_name = self.children[0].children[0].value
        func_type = self.children[0].value
        FuncTable.create(id=func_name, type=func_type, node=self)
    
class FuncCall(Node):
    def evaluate(self, symbol_table):
        func_name = self.value
        func_node, type = FuncTable.getter(func_name)
        func_st = SymbolTable()
        for i in range(len(self.children)):
            func_node.children[i+1].evaluate(func_st)
            func_st.setter(func_node.children[i+1].children[0].value, self.children[i].evaluate(symbol_table))
        
        ret_block = func_node.children[-1].evaluate(func_st)
        if ret_block is not None:
            if type == ret_block[0]:
                return ret_block
            else:
                raise TypeError("Erro")

class StrVal(Node):
    def evaluate(self, symbol_table):
        return ("string", self.value)

class Return(Node):
    def evaluate(self, symbol_table):
        return self.children[0].evaluate(symbol_table)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value