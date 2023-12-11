import sys
import re
import string
from Node import *
from Token import Token
from Tokenizer import *


with open(sys.argv[1], 'r') as f:
    input = f.read()


class PrePro:
    def __init__(self, source):
        self.source = source

    def filter(self):
        with open(self.source, "r") as input_file:
            code = input_file.read()

        code = re.sub(r"//.*", "", code)

        lines = code.split("\n")

        if re.search(r"\d\s+\d", code):
            raise Exception("Nao separar numeros com espaco")
        
        code = "\n".join([line.lstrip("\t") for line in lines])
        
        return code
    

class ParserError(Exception):
    pass


class Parser:
    tokens = None

    def parseProgram(self):
        childrens = []
        while self.tokens.next.type != EOF:
            childrens.append(self.parseDeclaration())
            while self.tokens.next.type == '\n':
                self.tokens.selectNext()
        return childrens
    
    def parseFactor(self):
        node = 0
        if self.tokens.next.type == "NUMBER":
            node = IntVal(self.tokens.next.value, [])
            self.tokens.selectNext()
            if self.tokens.next.type == "NUMBER":
                raise Exception("codigo incorreto")
            
        elif self.tokens.next.type == "STRING":
            node = StringVal(self.tokens.next.value, [])
            self.tokens.selectNext()
        elif self.tokens.next.type == "IDENTIFIER":
            identifier_name = self.tokens.next.value
            self.tokens.selectNext()
            if self.tokens.next.type == "OPEN_PAR":
                self.tokens.selectNext()
                nodes = []
                if self.tokens.next.type == "COMMA":
                    raise Exception("codigo incorreto")
                
                while self.tokens.next.type != "CLOSE_PAR":
                    nodes.append(self.parseBoolExpression())
                    if self.tokens.next.type == "COMMA":
                        self.tokens.selectNext()
                        nodes.append(self.parseBoolExpression())
                
                self.tokens.selectNext()
                node = FuncCall(identifier_name,nodes)
            else:
                node = Identifier(identifier_name, [])
        elif self.tokens.next.type == "PLUS":
            self.tokens.selectNext()
            node = UnOp("+", [self.parseFactor()])
        elif self.tokens.next.type == "MINUS":
            self.tokens.selectNext()
            node = UnOp("-", [self.parseFactor()])
        elif self.tokens.next.type == "NOT":
            self.tokens.selectNext()
            node = UnOp("!", [self.parseFactor()])
        elif self.tokens.next.type == "OPEN_PAR":
            self.tokens.selectNext()
            node = self.parseBoolExpression()
            if self.tokens.next.type == "CLOSE_PAR":
                self.tokens.selectNext()
            else:
                raise Exception("codigo incorreto")
        elif self.tokens.next.type == "SCANLN":
            self.tokens.selectNext()
            if self.tokens.next.type == "OPEN_PAR":
                self.tokens.selectNext()
                node = ScanLn("Scanln", [])
                if self.tokens.next.type != "CLOSE_PAR":
                    raise Exception("codigo incorreto")
                self.tokens.selectNext()
        else:
            raise Exception("codigo incorreto")

        return node

    def parseTerm(self):
        node = self.parseFactor()
        while self.tokens.next.type == "MULTIPLY" or self.tokens.next.type == "DIVIDE":
            if self.tokens.next.type == "MULTIPLY":
                self.tokens.selectNext()
                node = BinOp("*", [node, self.parseFactor()])
            elif self.tokens.next.type == "DIVIDE":
                self.tokens.selectNext()
                node = BinOp("/", [node, self.parseFactor()])
            else:
                raise Exception("codigo incorreto")

        return node
    
    def parseExpression(self):
        node = self.parseTerm()
        while self.tokens.next.type == "PLUS" or self.tokens.next.type == "MINUS" or self.tokens.next.type == "CONCAT":
            if self.tokens.next.type == "PLUS":
                self.tokens.selectNext()
                node = BinOp("+", [node, self.parseTerm()])
            elif self.tokens.next.type == "MINUS":
                self.tokens.selectNext()
                node = BinOp("-", [node, self.parseTerm()])
            elif self.tokens.next.type == "CONCAT":
                self.tokens.selectNext()
                node = BinOp(".", [node, self.parseTerm()])

        if self.tokens.next.type == INT or self.tokens.next.type == STR:
            raise Exception("codigo incorreto")

        return node
    
    def parseStatement(self):
        if self.tokens.next.type == "IDENTIFIER":
            identifier_name = self.tokens.next.value
            variable = Identifier(identifier_name, [])
            self.tokens.selectNext()
            if self.tokens.next.type == "ASSIGN":
                self.tokens.selectNext()
                variable = Assigment("=", [variable, self.parseBoolExpression()])
            elif self.tokens.next.type == "OPEN_PAR":
                self.tokens.selectNext()
                nodes = []                
                if self.tokens.next.type == "COMMA":
                    raise Exception("codigo incorreto")
                
                while self.tokens.next.type != "CLOSE_PAR":
                    nodes.append(self.parseBoolExpression())
                    if self.tokens.next.type == "COMMA":
                        self.tokens.selectNext()
                        nodes.append(self.parseBoolExpression())
                self.tokens.selectNext()        
                variable = FuncCall(identifier_name,nodes)
            else:
                raise Exception("operacao nn suportada")
        elif self.tokens.next.type == "PRINTLN":
            self.tokens.selectNext()
            if self.tokens.next.type == "OPEN_PAR":
                self.tokens.selectNext()
                variable = PrintLn("PrintLn", [self.parseBoolExpression()])
                if self.tokens.next.type == "CLOSE_PAR":
                    self.tokens.selectNext()
                    if self.tokens.next.type == "BREAKLINE" or self.tokens.next.type == EOF:
                        self.tokens.selectNext()
                    else:
                        raise Exception("codigo incorreto")
                else:
                    raise Exception("codigo incorreto")
        elif self.tokens.next.type == "VAR":
            self.tokens.selectNext()
            if self.tokens.next.type == "IDENTIFIER":
                name = self.tokens.next.value
                self.tokens.selectNext()
                if self.tokens.next.type in ["T_INT", "T_STRING"]:
                    tipo = self.tokens.next.type
                    self.tokens.selectNext()
                    if self.tokens.next.type == "ASSIGN":
                        self.tokens.selectNext()
                        variable = VarDec(tipo, [name, self.parseBoolExpression()])
                    elif self.tokens.next.type == EOF or self.tokens.next.type == "BREAKLINE":
                        variable = VarDec(tipo, [name])
                        self.tokens.selectNext()
                    else:
                        raise Exception("codigo incorreto")
        elif self.tokens.next.type == "IF":
            self.tokens.selectNext()
            condition_node = self.parseBoolExpression()
            node = self.parseBlock()
            if self.tokens.next.type == "BREAKLINE" or self.tokens.next.type == EOF:
                variable = If("if", [condition_node, node])
            else:
                if self.tokens.next.type == "ELSE":
                    self.tokens.selectNext()
                    variable = If("if", [condition_node, node, self.parseBlock()])
                    if self.tokens.next.type == "BREAKLINE":
                        self.tokens.selectNext()
                    else:
                        raise Exception("codigo incorreto")
                else:
                    raise Exception("codigo incorreto")
        elif self.tokens.next.type == "FOR":
            self.tokens.selectNext()
            if self.tokens.next.type == "IDENTIFIER":
                variable = Identifier(self.tokens.next.value, [])
                self.tokens.selectNext()
                if self.tokens.next.type == "ASSIGN":
                    self.tokens.selectNext()
                    a = Assigment("=", [variable, self.parseBoolExpression()])
                    if self.tokens.next.type == "SEMICOLUMN":
                        self.tokens.selectNext()
                        b = self.parseBoolExpression()
                        if self.tokens.next.type == "SEMICOLUMN":
                            self.tokens.selectNext()
                            if self.tokens.next.type == "IDENTIFIER":
                                variable = Identifier(self.tokens.next.value, [])
                                self.tokens.selectNext()
                                if self.tokens.next.type == "ASSIGN":
                                    self.tokens.selectNext()
                                    c = Assigment(
                                        "=", [variable, self.parseBoolExpression()]
                                    )  # for increment
                                    block = self.parseBlock()
                                    variable = For("if", [a, b, block, c])
                                    if (
                                        self.tokens.next.type == "BREAKLINE"
                                        or self.tokens.next.type == EOF
                                    ):
                                        self.tokens.selectNext()
                                    else:
                                        raise Exception("codigo incorreto")
                                else:
                                    raise Exception("operacao nn suportada")
                            else:
                                raise Exception(
                                    "for assignment ; condition; expression {block}"
                                )
                        else:
                            raise Exception(
                                "for assignment ; condition; expression {block}"
                            )
                    else:
                        raise Exception(
                            "for assignment ; condition; expression {block}"
                        )
                else:
                    raise Exception("for assignment ; condition; expression {block}")
        elif self.tokens.next.type == "RETURN":
            self.tokens.selectNext()
            variable = ReturnFunc("return",[self.parseBoolExpression()])
        elif self.tokens.next.type == "BREAKLINE":
            self.tokens.selectNext()
            variable = NoOp("NoOp", [])
        else:
            raise Exception("codigo incorreto")

        return variable

    def parseBlock(self):
        childrens = []
        if self.tokens.next.type == "OPEN_BRACE":
            self.tokens.selectNext()
            if self.tokens.next.type == "BREAKLINE":
                self.tokens.selectNext()
                while self.tokens.next.type != "CLOSE_BRACE":
                    node = self.parseStatement()
                    childrens.append(node)
                self.tokens.selectNext()
                if self.tokens.next.type not in ["BREAKLINE",EOF,"ELSE"]:
                    raise Exception("espaço necessario")
            else:
                raise Exception("codigo incorreto")
        master = Block("Block", childrens)
        return master
    
    def parseRelExpression(self):
        node = self.parseExpression()
        while self.tokens.next.type == "COMPARE" or self.tokens.next.type == "GREATER" or self.tokens.next.type == "LESS":
            if self.tokens.next.type == "COMPARE":
                self.tokens.selectNext()
                node = BinOp("==", [node, self.parseExpression()])
            elif self.tokens.next.type == "GREATER":
                self.tokens.selectNext()
                node = BinOp(">", [node, self.parseExpression()])
            elif self.tokens.next.type == "LESS":
                self.tokens.selectNext()
                node = BinOp("<", [node, self.parseExpression()])

        if self.tokens.next.type == INT:
            raise Exception("codigo incorreto")

        return node
    
    def parseBoolTerm(self):
        node = self.parseRelExpression()
        while self.tokens.next.type == "AND":
            self.tokens.selectNext()
            node = BinOp("&&", [node, self.parseRelExpression()])

        if self.tokens.next.type == INT:
            raise Exception("codigo incorreto")
        return node

    def parseBoolExpression(self):
        node = self.parseBoolTerm()
        while self.tokens.next.type == "OR":
            self.tokens.selectNext()
            node = BinOp("||", [node, self.parseBoolTerm()])

        if self.tokens.next.type == INT:
            raise Exception("codigo incorreto")

        return node
    
    def parseDeclaration(self):
        argumentos = []
        if self.tokens.next.type == "FUNC":
            self.tokens.selectNext()
            if self.tokens.next.type == "IDENTIFIER":
                nome_funcao = self.tokens.next.value
                self.tokens.selectNext()
                if self.tokens.next.type == "OPEN_PAR":
                    self.tokens.selectNext()
                    if self.tokens.next.type == "COMMA":
                        raise Exception("virgula nn suportada")
                    
                    while self.tokens.next.type != "OPEN_PAR":
                        if self.tokens.next.type == "IDENTIFIER":
                            nome_argumento = self.tokens.next.value
                            self.tokens.selectNext()
                            if self.tokens.next.type in ["T_INT","T_STRING"]:
                                tipo_argumento = self.tokens.next.type
                                arg = VarDec(tipo_argumento, [nome_argumento])
                                argumentos.append(arg)
                                self.tokens.selectNext()
                            else:
                                raise Exception("declaracao incorreta")
                        elif self.tokens.next.type == "COMMA":
                            self.tokens.selectNext()
                            if self.tokens.next.type == "CLOSE_PAR":
                                raise Exception("parenteses nn suportado")
                        else:
                            raise Exception("codigo incorreto")
                    
                    self.tokens.selectNext()
                    if self.tokens.next.type in ["T_INT","T_STRING"]:
                        tipo_func = self.tokens.next.type
                        func_dec = VarDec(tipo_func, [nome_funcao])
                        argumentos.insert(0,func_dec)
                        self.tokens.selectNext()
                        argumentos.append(self.parseBlock())
                        variable = FuncDec((nome_funcao,tipo_func),argumentos)
                    else:
                        raise Exception("declaracao incorreta de funcao")
        return variable

    def run(self, code):
        filtered = PrePro(code).filter()
        identifier_table = SymbolTable()
        function_table = SymbolTable()
        self.tokens = Tokenizer(filtered)
        self.tokens.selectNext()
        list_of_nodes = self.parseProgram()
        if self.tokens.next.type == EOF:
            for node in list_of_nodes:
                node.evaluate(identifier_table,function_table)
                
            main_node = FuncCall('main',[])
            main_node.evaluate(identifier_table,function_table)
        else:
            raise Exception("codigo incorreto")


if __name__ == "__main__":
    chain = sys.argv[1]
    parser = Parser()
    final = parser.run(chain)
