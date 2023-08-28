import sys

class Token:
    def __init__(self, value, type):
        self.type = type
        self.value = value

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

            else:
                raise ValueError(f"Unexpected character: {current_char}")
        else:
            self.next = Token("", "EOF")

class Parser:
    tokenizer = None
    
    def parseExpression(self):
        result = self.parseTerm()

        if self.tokenizer.next is not None and self.tokenizer.next.type not in ["PLUS", "MINUS", "EOF"]:
            raise ValueError("Unexpected token: " + self.tokenizer.next.value)

        while self.tokenizer.next.type in ["PLUS", "MINUS"]:
            operator = self.tokenizer.next.value
            self.tokenizer.selectNext()

            operand = self.parseTerm()

            if operator == "+":
                result += operand
            elif operator == "-":
                result -= operand

        return result

    def parseTerm(self):
        result = self.parseFactor()

        while self.tokenizer.next.type in ["MULT", "DIV"]:
            operator = self.tokenizer.next.value
            self.tokenizer.selectNext()

            operand = self.parseFactor()

            if operator == "*":
                result *= operand
            elif operator == "/":
                if operand == 0:
                    raise ValueError("Division by zero")
                result //= operand

        return result
    
    def parseFactor(self):
        if self.tokenizer.next.type == "INT":
            result = self.tokenizer.next.value
            self.tokenizer.selectNext()
            return result
        else:
            raise ValueError("Expected INT in factor")
    
    def run(self, code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        return self.parseExpression()

if __name__ == "__main__":
    p = Parser()
    teste = p.run(sys.argv[1])
    print(teste)
