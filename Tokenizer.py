class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    
    special_words = ["Println", "Scanln", "if", "else", "for", "var", "int", "string", "func", "return"]

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position] == " ":
            self.position += 1
        
        if self.position == len(self.source):
            self.next = Token("EOF", "")
           
        elif self.position != len(self.source):
            if self.source[self.position].isdigit():
                number = ""

                while self.position < len(self.source) and self.source[self.position].isdigit():
                    number += self.source[self.position]
                    self.position += 1
                self.next = Token("INT", int(number))

            elif self.source[self.position] == "*":
                self.next = Token("TIMES", "*")
                self.position += 1
            
            elif self.source[self.position] == "/":
                self.next = Token("DIV", "/")
                self.position += 1

            elif self.source[self.position] == "+":
                self.next = Token("PLUS", "+")
                self.position += 1
            
            elif self.source[self.position] == "-":
                self.next = Token("MINUS", "-")
                self.position += 1
            
            elif self.source[self.position] == "(":
                self.next = Token("OPEN_PAR", "(")
                self.position += 1
            
            elif self.source[self.position] == ")":
                self.next = Token("CLOSE_PAR", ")")
                self.position += 1
            
            elif self.source[self.position] == "\n":
                self.next = Token("BREAKLINE", "\n")
                self.position += 1
            
            elif self.source[self.position] == "=":
                if self.source[self.position + 1] == "=":
                    self.next = Token("COMPARE", "==")
                    self.position += 2
                else:
                    self.next = Token("EQUAL", "=")
                    self.position += 1
            
            elif self.source[self.position] == "&":
                if self.source[self.position + 1] == "&":
                    self.next = Token("AND", "&")
                    self.position += 2
                else:
                    raise TypeError("Erro")
            
            elif self.source[self.position] == "|":
                if self.source[self.position + 1] == "|":
                    self.next = Token("OR", "|")
                    self.position += 2
                else:
                    raise TypeError("Erro")

            elif self.source[self.position] == ">":
                self.next = Token("GREATER", ">")
                self.position += 1
            
            elif self.source[self.position] == "<":
                self.next = Token("LESS", "<")
                self.position += 1
            
            elif self.source[self.position] == "!":
                self.next = Token("NOT", "!")
                self.position += 1
            
            elif self.source[self.position] == ";":
                self.next = Token("SEMICOLON", ";")
                self.position += 1
            
            elif self.source[self.position] == "{":
                self.next = Token("OPEN_BRACE", "{")
                self.position += 1
            
            elif self.source[self.position] == "}":
                self.next = Token("CLOSE_BRACE", "}")
                self.position += 1
            
            elif self.source[self.position] == ".":
                self.next = Token("CONCAT", ".")
                self.position += 1
            
            elif self.source[self.position] == ",":
                    self.next = Token("COMMA", self.source[self.position])
                    self.position += 1
            
            elif self.source[self.position] == '"': 
                string = ""
                self.position += 1
                while self.position < len(self.source) and self.source[self.position] != '"':
                    string += self.source[self.position]
                    self.position += 1
                if self.source[self.position] == '"':
                    self.position += 1
                    self.next = Token("STRING", string)
                    
                else:
                    raise TypeError("Erro")

            elif self.source[self.position].isalpha():
                id = ""
                while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                    id += self.source[self.position]
                    self.position += 1
                
                if id == "Println":
                    self.next = Token("Println", id)
                elif id == "Scanln":
                    self.next = Token("Scanln", id)
                elif id == "if":
                    self.next = Token("if", id)
                elif id == "else":
                    self.next = Token("else", id)
                elif id == "for":
                    self.next = Token("for", id)
                elif id == "var":
                    self.next = Token("var", id)
                elif id == "int":
                    self.next = Token("type", id)
                elif id == "string":
                    self.next = Token("type", id)
                elif id == "func":
                    self.next = Token("func", id)
                elif id == "return":
                    self.next = Token("return", id)
                else:
                    self.next = Token("ID", id)

            elif self.source[self.position].isspace():
                self.position += 1
                self.selectNext()
            
            else:
                raise TypeError("Erro")
        else:
            raise ValueError("Erro")