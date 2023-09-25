import sys

class Token:
    def __init__(self, value, type):
        self.type = type
        self.value = value

class Node:
    def __init__(self, value, children:list):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

class PreProcess:
    @staticmethod
    def filter(code):
        n = 0
        while n < len(code)-1:
            if code[n] == '/' and code[n+1] == '/':
                code = code[:n]
                break
            n += 1
        return code
    
class BinaryOp(Node):
    def evaluate(self):
        left = self.children[0].evaluate()
        right = self.children[1].evaluate()

        if self.value == '+':
            return left + right
        elif self.value == '-':
            return left - right
        elif self.value == '*':
            return left * right
        elif self.value == '/':
            return left // right
        else:
            raise Exception(f"Unexpected operator: {self.value}")

class UnaryOp(Node):
    def evaluate(self):
        if self.value == '+':
            return self.children[0].evaluate()
        elif self.value == '-':
            return -self.children[0].evaluate()
        else:
            raise Exception(f"Unexpected operator: {self.value}")  

class IntVal(Node):
    def evaluate(self):
        return int(self.value)

class NoOp(Node):
    def evaluate(self):
        pass 

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
    
    def skipSpaces(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1
    
    def selectNext(self):
        self.skipSpaces()
        
        if self.position < len(self.source):
            current_char = self.source[self.position]

            if current_char.isdigit():
                value = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    value += self.source[self.position]
                    self.position += 1
                self.next = Token(int(value), "INT")

            elif current_char == '+':
                self.next = Token("+", "PLUS")
                self.position += 1

            elif current_char == '-':
                self.next = Token("-", "MINUS")
                self.position += 1

            elif current_char == '*':
                self.next = Token("*", "MULT")
                self.position += 1

            elif current_char == '/':
                self.next = Token("/", "DIV")
                self.position += 1

            elif current_char == '(':
                self.next = Token("(", "OPENPAR")
                self.position += 1

            elif current_char == ')':
                self.next = Token(")", "CLOSEPAR")
                self.position += 1

            else:
                raise ValueError(f"Unexpected character: {current_char}")
        else:
            self.next = Token("", "EOF")

class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current = self.tokenizer.next
    
    def parseExpression(self):
        result = self.parseTerm()

        if self.current is not None and self.current.type not in ["PLUS", "MINUS", "EOF", "CLOSEPAR"]:
            raise ValueError("Unexpected token: " + self.current.value)

        while self.current.type in ["PLUS", "MINUS"]:
            operator = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            result = BinaryOp(operator, [result, self.parseTerm()])

        return result

    def parseTerm(self):
        result = self.parseFactor()

        while self.current.type in ["MULT", "DIV"]:
            operator = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            
            result = BinaryOp(operator, [result, self.parseFactor()])
            
        return result
    
    def parseFactor(self):

        sign = 1

        if self.current.type == "INT":
            result = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            return IntVal(result, [])
        
        if self.current.type in ["PLUS", "MINUS"]:
            if self.current.value == "-":
                sign = -1
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            unary_op = "+" if sign == 1 else "-"
            return UnaryOp(unary_op, [self.parseFactor()])
            
        if self.tokenizer.next and self.tokenizer.next.type == "OPENPAR":
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            result = self.parseExpression()
            if self.current.type == "CLOSEPAR":
                self.tokenizer.selectNext()
                self.current = self.tokenizer.next
                unary_operator = '+' if sign == 1 else '-'
                return UnaryOp(unary_operator, [result])
            else:
                raise ValueError("Expected closing parenthesis ')'")

        if self.current.value == "CLOSEPAR":
            raise ValueError("Unexpected closing parenthesis ')'")
        
        raise ValueError("Expected INT, '+', '-', '(', or operator")
        
    @staticmethod
    def run(code):
        code = PreProcess().filter(code)
        tokenizer = Tokenizer(code)
        parser = Parser(tokenizer)

        result = parser.parseExpression()

        if parser.current.type != 'EOF':
            raise Exception(f'Invalid expression, stopped at {parser.current.value} of type {parser.current.type}')

        return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py '<expression>'", file=sys.stderr)
        return
    try:
        with open (sys.argv[1], "r") as myfile:
            data=myfile.read().replace('\n', '')
        ast_root = Parser.run(data)
        result = ast_root.evaluate()
        print(result)
    except Exception as e:
        print(str(e), file=sys.stderr)

if __name__ == "__main__":
    main()
