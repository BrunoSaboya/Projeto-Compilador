import sys

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    def evaluate(self, sym_table):
        pass

class PrePro:
    @staticmethod
    def filter(code):
        i = 0
        filtered_code = ""
        
        while i < len(code):
            # If a comment starts
            if i < len(code) - 1 and code[i] == '/' and code[i + 1] == '/':
                # Skip till end of line or end of string
                while i < len(code) and code[i] != '\n':
                    i += 1
            else:
                filtered_code += code[i]
                i += 1
        
        return filtered_code

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
        else:
            raise Exception('Invalid operator')

        return result

class UnOp(Node):
    def evaluate(self, sym_table):
        if self.value == '+':
            return self.children[0].evaluate(sym_table)
        elif self.value == '-':
            return -self.children[0].evaluate(sym_table)
        else:
            raise Exception('Invalid operator')

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, sym_table):
        return int(self.value)

class NoOp(Node):
    def evaluate(self, sym_table):
        pass

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def set(self, identifier, value):
        self.symbols[identifier] = value

    def get(self, identifier):
        if identifier in self.symbols:
            return self.symbols[identifier]
        else:
            raise Exception(f"'{identifier}' not found in the symbol table")

class Assignment(Node):
    def evaluate(self, sym_table):
        identifier = self.value
        value = self.children[0].evaluate(sym_table)
        sym_table.set(identifier, value)
        return value

class Identifier(Node):
    def evaluate(self, sym_table):
        return sym_table.get(self.value)

class Block(Node):
    def evaluate(self, sym_table):
        last_result = None
        for child in self.children:
            last_result = child.evaluate(sym_table)
        return last_result

class Print(Node):
    def evaluate(self, sym_table):
        val = self.children[0].evaluate(sym_table)
        print(val)

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.selectNext()

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token(None, 'EOF')
            return

        char = self.source[self.position]
        self.position += 1

        if char in ['+', '-', '*', '/']:
            self.next = Token(char, 'OPERATOR')
        elif char in ['(', ')']:
            self.next = Token(char, 'PARENTHESIS')
        elif char == '\n':
            self.next = Token(char, 'BREAKLINE')
        elif char == '=':
            self.next = Token(char, 'EQUALS')
        elif char.isdigit():
            number = ''
            while char.isdigit():
                number += char
                if self.position >= len(self.source):
                    break
                char = self.source[self.position]
                if char.isdigit():
                    self.position += 1
                elif char.isspace() or char in ['+', '-', '*', '/', '(', ')'] or char.isalpha() or char == '_':
                    break
                else:
                    raise Exception(f"Unexpected character 1 {char}")
            
            self.next = Token(int(number), 'NUMBER')
        elif char.isalpha():
            identifier = ''
            while char.isalnum() or char == '_':
                identifier += char
                if self.position >= len(self.source):
                    break
                char = self.source[self.position]
                if char.isalnum() or char == '_':
                    self.position += 1
                else:
                    break
            if identifier == 'Println':
                self.next = Token(identifier, 'PRINTLN')
            else:
                self.next = Token(identifier, 'IDENTIFIER')
        else:
            raise Exception(f"Unexpected character 2 {char}")

class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current = self.tokenizer.next

    def parseFactor(self):
        if self.current.type == "OPERATOR" and self.current.value in ['+', '-']:
            unary_operator = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            return UnOp(unary_operator, [self.parseFactor()])
        elif self.current.type == 'NUMBER':
            value = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            return IntVal(value)
        elif self.current.type == "PARENTHESIS" and self.current.value == '(':
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            node = self.parseExpression()
            if self.current.type == "PARENTHESIS" and self.current.value == ')':
                self.tokenizer.selectNext()
                self.current = self.tokenizer.next
                return node
            else:
                raise Exception('Expected closing parenthesis')
        elif self.current.type == "IDENTIFIER":
            node = Identifier(self.current.value)
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            return node
        raise Exception('Invalid factor')

    def parseTerm(self):
        result = self.parseFactor()
        while self.current.type == 'OPERATOR' and self.current.value in ['*', '/']:
            operator = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            result = BinOp(operator, [result, self.parseFactor()])
        return result

    def parseExpression(self):
        result = self.parseTerm()
        while self.current.type == 'OPERATOR' and self.current.value in ['+', '-']:
            operator = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            result = BinOp(operator, [result, self.parseTerm()])
        return result

    def parseStatement(self):
        if self.current.type == "IDENTIFIER":
            var_name = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            if self.current.value == "=":
                self.tokenizer.selectNext()
                self.current = self.tokenizer.next
                expr = self.parseExpression()
                return Assignment(var_name, [expr])
            else:
                raise Exception(f"Unexpected token after identifier: {self.current.value}")
        if self.current.value == "Println":
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            expr = self.parseExpression()
            return Print(None, [expr])
        if self.current.type == "NUMBER":
            raise Exception("Invalid statement")
        else:
            return self.parseExpression()

    def parseBlock(self):
        children = []
        while self.current.type != 'EOF':
            statement = self.parseStatement()
            children.append(statement)
            if self.current.type == 'BREAKLINE':
                self.tokenizer.selectNext()
                self.current = self.tokenizer.next
        return Block(None, children)

    @staticmethod
    def run(code):
        code = PrePro().filter(code)
        tokenizer = Tokenizer(code)
        parser = Parser(tokenizer)
        result = parser.parseBlock()
        if parser.current.type != 'EOF':
            raise Exception(f'Invalid expression, stopped at {parser.current.value} of type {parser.current.type}')
        return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py '<expression>'", file=sys.stderr)
        return
    try:
        with open(sys.argv[1], "r") as myfile:
            data = myfile.read()
        ast_root = Parser.run(data)
        sym_table = SymbolTable()
        ast_root.evaluate(sym_table)
    except Exception as e:
        print(str(e), file=sys.stderr)

if __name__ == "__main__":
    main()
