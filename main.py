import sys

class Token:
    def __init__(self, type, value):
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

    @staticmethod
    def parseExpression():

        if Parser.tokenizer.next.type == "INT":
            result = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()

            while Parser.tokenizer.next.type in ["PLUS", "MINUS"]:
                if Parser.tokenizer.next.value == "+":
                    Parser.tokenizer.selectNext()

                    if Parser.tokenizer.next.type == "INT":
                        result += Parser.tokenizer.next.value
                        Parser.tokenizer.selectNext()
                    else:
                        raise ValueError("Expected INT after +")
                elif Parser.tokenizer.next.value == "-":
                    Parser.tokenizer.selectNext()

                    if Parser.tokenizer.next.type == "INT":
                        result -= Parser.tokenizer.next.value
                        Parser.tokenizer.selectNext()
                    else:
                        raise ValueError("Expected INT after -")
                else:
                    raise ValueError("Expected + or - operator")

            return result
        else:
            raise ValueError("Expected INT at the beginning of expression")

    @staticmethod
    def run(code):
        tokenizer = Tokenizer(code)
        parser = Parser(tokenizer)

        result = parser.parseExpression()

        if parser.tokenizer.next is not None:
            raise SyntaxError("Parsing não completado. Token inválido ou não esperado.")

        return result

if __name__ == "__main__":
    p = Parser()
    teste = p.run(sys.argv[1])
    print(teste)