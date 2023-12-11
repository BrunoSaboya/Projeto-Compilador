from Tokenizer import *
from Token import Token

class SymbolTable:
    def __init__(self):
        self.symbol_table = dict()

    def set(self, identifier, value):
        if identifier not in self.symbol_table.keys():
            raise Exception("n declarada")
        else:
            if (type(value[0]) == FuncDec):
                self.symbol_table[identifier] = value 
            elif (self.symbol_table[identifier][1] == value[1]):
                self.symbol_table[identifier] = value                
            else:
                raise Exception("tipagem diferentes")
            
    def get(self, identifier):
        try:
            return self.symbol_table[identifier]
        except:
            raise Exception(f"{identifier} n existe")
        
    def assing(self, identifier, type):
        if identifier in self.symbol_table.keys():
            raise Exception("variavel ja existe")
        else:
            self.symbol_table[identifier] = (None,type)
    
class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, table: SymbolTable):
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
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        var = self.children[0].evaluate(table,funcTable)
        if (var[1] == "int"):  
            if self.value == "+":
                return (1 * var[0] , var[1])
            elif self.value == "-":
                return (-1 * var[0],var[1])
            elif self.value == "!":
                return (not (var[0]), var[1])
            else:
                raise Exception("Erro")
        else:
            raise Exception("Erro")

class IntVal(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        return (self.value,"int")
    
class NoOp(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        pass
    
class StringVal(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        return (self.value,"string")
    
class Assigment(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        table.set(self.children[0].value, self.children[1].Evaluate(table,funcTable))

class Identifier(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        return table.get(self.value)

class Block(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        for node in self.children:
            if type(node) == ReturnFunc:
                guarda = node.evaluate(table,funcTable)
                return guarda
            node.evaluate(table,funcTable)

class PrintLn(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        print(self.children[0].evaluate(table,funcTable)[0])
        
class ScanLn(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        return (int(input()),"int")

class If(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        if self.children[0].evaluate(table,funcTable)[0]:
            self.children[1].evaluate(table,funcTable)
        elif len(self.children) > 2:
            self.children[2].evaluate(table,funcTable)

class For(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        self.children[0].evaluate(table,funcTable)
        while self.children[1].evaluate(table,funcTable)[0]:            
            self.children[2].evaluate(table,funcTable)
            self.children[3].evaluate(table,funcTable)
            
class VarDec(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        table.assing(self.children[0],self.value)
        if len(self.children)>1:
            a = self.children[1].evaluate(table,funcTable)
            table.set(self.children[0],a)

class ReturnFunc(Node):
    def evaluate(self, table: SymbolTable,funcTable: SymbolTable):
        return self.children[0].evaluate(table,funcTable)
         
class FuncDec(Node):
    def Evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        table.assing(self.value[0],self.value[1])
        funcTable.assing(self.value[0],self.value[1])
        funcTable.assing(self.value[0],(self,self.value[1]))
    
class FuncCall(Node):
    def evaluate(self, table: SymbolTable, funcTable: SymbolTable):
        decnode,type = funcTable.get(self.value)
        local_ST = SymbolTable()
        i = 1
        while i < len(decnode.children) - 1:
            decnode.children[i].evaluate(local_ST,funcTable)
            local_ST.set(decnode.children[i].children[0],self.children[i-1].evaluate(table,funcTable))
            i+=1
            
        a = decnode.children[-1].evaluate(local_ST,funcTable)
        return a
        