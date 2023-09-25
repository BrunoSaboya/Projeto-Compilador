import sys

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

class Node:
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

class PrePro:
    @staticmethod
    def filter(code):
        i = 0
        while i < len(code) - 1:
            if code[i] == '/' and code[i + 1] == '/':
                code = code[:i]
                break
            i += 1
        return code

class BinOp(Node):
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
            raise Exception('Invalid operator')

class UnOp(Node):
    def evaluate(self):
        if self.value == '+':
            return self.children[0].evaluate()
        elif self.value == '-':
            return -self.children[0].evaluate()
        else:
            raise Exception('Invalid operator')

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
        elif char.isdigit():
            number = ''
            while char.isdigit():
                number += char
                if self.position >= len(self.source):
                    break
                char = self.source[self.position]
                if char.isdigit():
                    self.position += 1
                elif char.isspace() or char in ['+', '-', '*', '/', '(', ')']:
                    break
                else:
                    raise Exception(f"Unexpected character 1 {char}")
            self.next = Token(int(number), 'NUMBER')
        else:
            raise Exception(f"Unexpected character 2 {char}")

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.current = self.tokenizer.next

    def parseFactor(self):
        sign = 1
        #print(f"Parsing factor: {self.current.value}, {self.current.type}")

        if self.current.type == "OPERATOR" and self.current.value in ['+', '-']:
            if self.current.value == '-':
                sign = -1
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            unary_operator = '+' if sign == 1 else '-'
            #print(f"Unary operator: {unary_operator}")
            return UnOp(unary_operator, [self.parseFactor()])

        if self.current.type == 'NUMBER':
            value = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            #print(f"Number value: {value}")
            return IntVal(value)

        if self.current.type == "PARENTHESIS" and self.current.value == '(':
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            node = self.parseExpression()
            if self.current.type == "PARENTHESIS" and self.current.value == ')':
                self.tokenizer.selectNext()
                self.current = self.tokenizer.next
                unary_operator = '+' if sign == 1 else '-'
                #print(f"Closing parenthesis with unary operator: {unary_operator}")
                return UnOp(unary_operator, [node])
            else:
                raise Exception('Expected closing parenthesis')

        if self.current.type == "PARENTHESIS" and self.current.value == ')':
            raise Exception("Unmatched or unexpected closing parenthesis")

        raise Exception('Invalid factor')

    def parseTerm(self):
        result = self.parseFactor()
        #print(f"Parsing term: {result.value}")

        while self.current.type == 'OPERATOR' and self.current.value in ['*', '/']:
            operator = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            result = BinOp(operator, [result, self.parseFactor()])
            #print(f"Operator: {operator}")

        return result

    def parseExpression(self):
        result = self.parseTerm()
        #print(f"Parsing expression: {result.value}")

        while self.current.type == 'OPERATOR' and self.current.value in ['+', '-']:
            operator = self.current.value
            self.tokenizer.selectNext()
            self.current = self.tokenizer.next
            result = BinOp(operator, [result, self.parseTerm()])
            #print(f"Operator: {operator}")

        return result

    @staticmethod
    def run(code):
        code = PrePro().filter(code)
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
        with open(sys.argv[1], "r") as myfile:
            data = myfile.read().replace('\n', '')
        ast_root = Parser.run(data)
        result = ast_root.evaluate()
        print(result)
    except Exception as e:
        print(str(e), file=sys.stderr)

if __name__ == "__main__":
    main()
