class Token:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token("EOF", "EOF")
            return

        if self.position < len(self.source):
            char = self.source[self.position]

            if char == "\n":
                self.next = Token("BREAKLINE", "\n")
                self.position += 1
            elif char.isspace():
                self.position += 1
                self.selectNext()
            elif char == "+":
                self.next = Token("PLUS", "+")
                self.position += 1
            elif char == "-":
                self.next = Token("MINUS", "-")
                self.position += 1
            elif char == "*":
                self.next = Token("MULT", "*")
                self.position += 1
            elif char == "/":
                self.next = Token("DIV", "/") 
                self.position += 1
            elif char == "(":
                self.next = Token("OPEN_PAR", "(") 
                self.position += 1                
            elif char == ")":
                self.next = Token("CLOSE_PAR", ")") 
                self.position += 1
            elif char == "=":
                if self.source[self.position+1] == "=":
                    self.next = Token("COMPARE", "==")
                    self.position += 2
                else:
                    self.next = Token("EQUAL", "=") 
                    self.position += 1                    
            elif char == ">":
                self.next = Token("GREATER", ">") 
                self.position += 1                    
            elif char == "<":
                self.next = Token("LESS", "<") 
                self.position += 1                    
            elif char == "|":
                self.next = Token("OR", "||") 
                self.position += 2                    
            elif char == "&":
                self.next = Token("AND", "&&") 
                self.position += 2                    
            elif char == "!":
                self.next = Token("NOT", "!") 
                self.position += 1                    
            elif char == "{":
                self.next = Token("OPEN_BRACE", "{")
                self.position += 1       
            elif char == "}":
                self.next = Token("CLOSE_BRACE", "}") 
                self.position += 1                     
            elif char == ";":
                self.next = Token("SEMICOLUMN", ";") 
                self.position += 1                
            elif char == ".":
                self.next = Token("CONCAT", ".") 
                self.position += 1
            elif char == ",":
                self.next = Token("COMMA", ",") 
                self.position += 1
            elif char.isdigit():
                value = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    value += self.source[self.position]
                    self.position += 1
                self.next = Token("INT", int(value))
            elif char == '"':
                identifier = char
                self.position += 1
                char = self.source[self.position]
                while self.position < len(self.source) and char != '"':
                    identifier += char
                    self.position += 1
                    char = self.source[self.position]
                if char == '"':
                    identifier += char
                    self.position += 1
                    identifier = identifier.strip('"')
                    self.next = Token("STRING", identifier)
                else:
                    raise SyntaxError("String mal formada: aspa dupla de fechamento faltando")
            elif char.isalpha() or char == "_":
                identifier = ""
                while self.position < len(self.source) and (char.isalnum() or char == "_"):
                    identifier += char
                    self.position += 1
                    if self.position < len(self.source):
                        char = self.source[self.position]                        
                if identifier == "Println":
                    self.next = Token("PRINTLN", "Println")                        
                elif identifier == "Scanln":
                    self.next = Token("SCANLN", "Scanln")                        
                elif identifier == "if": 
                    self.next = Token("IF", "if")                        
                elif identifier == "else":
                    self.next = Token("ELSE", "else")                        
                elif identifier == "for":
                    self.next = Token("FOR", "for")                        
                elif identifier == "var":
                    self.next = Token("VAR", "var")                        
                elif identifier == "int":
                    self.next = Token("TYPE", "int")      
                elif identifier == "string":
                    self.next = Token("TYPE", "string")
                elif identifier == "func":
                    self.next = Token("FUNC", "func")                        
                elif identifier == "return":
                    self.next = Token("RETURN", "func")
                else:
                    self.next = Token("IDENTIFIER", identifier)
            else:
                raise SyntaxError("Identificador inválido")