import sys

class Token:
    def __init__(self, value, type):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source.replace(" ", "").strip()
        self.position = 0
        self.next = None
    
    def selectNext(self):
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

            else:
                raise ValueError(f"Unexpected character: {current_char}")
        else:
            self.next = Token("", "EOF")

class Parser:

    tokenizer = None

    
    def parseExpression(self):

        if self.tokenizer.next.type == "INT":
            result = self.tokenizer.next.value
            self.tokenizer.selectNext()

            while self.tokenizer.next.type in ["PLUS", "MINUS"]:
                if self.tokenizer.next.value == "+":
                    self.tokenizer.selectNext()

                    if self.tokenizer.next.type == "INT":
                        result += self.tokenizer.next.value
                        self.tokenizer.selectNext()
                    else:
                        raise ValueError("Expected INT after +")
                elif self.tokenizer.next.value == "-":
                    self.tokenizer.selectNext()

                    if self.tokenizer.next.type == "INT":
                        result -= self.tokenizer.next.value
                        self.tokenizer.selectNext()
                    else:
                        raise ValueError("Expected INT after -")
                else:
                    raise ValueError("Expected + or - operator")

            return result
        else:
            raise ValueError("Expected INT at the beginning of expression")

    
    def run(self, code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        return self.parseExpression()

if __name__ == "__main__":
    p = Parser()
    teste = p.run(sys.argv[1])
    print(teste)