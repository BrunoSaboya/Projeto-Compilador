from Token import Token
import re

EOF = "End of File"
INT = "INTEGER"
STR = "STRING"

class Tokenizer:

    specialWords = ['Println', 'Scanln', 'if', 'for', 'else', 'var', 'int', 'string', 'func', 'return']

    def __init__(self, source, next=None, position=0):
        self.source = str(source)
        self.next = next
        self.position = position

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token(value="EOF", type="EOF")
            return

        while self.position < len(self.source):
            if self.position >= len(self.source):
                self.next = Token(" ", "EOF")
                return
            if re.match("[0-9]", self.source[self.position]):
                number = ""
                while self.position < len(self.source):
                    if re.match(r"[0-9]", self.source[self.position]):
                        number += self.source[self.position]
                        self.position += 1
                    else:
                        self.next = Token(value=int(number), type="NUMBER")
                        return
                self.next = Token(value=int(val), type="NUMBER")
                return
            elif self.source[self.position] == '"':
                string_value = ""
                self.position += 1
                while self.position < len(self.source):
                    if self.source[self.position] != '"':
                        string_value += self.source[self.position]
                        self.position += 1
                    else:
                        self.position += 1
                        self.next = Token(value=str(string_value), type="STRING")
                        return
                raise Exception("String errada")
            elif self.source[self.position] == "+":
                self.next = Token(value=self.source[self.position], type="PLUS")
                self.position += 1
                return
            elif self.source[self.position] == "-":
                self.next = Token(value=self.source[self.position], type="MINUS")
                self.position += 1
                return
            elif self.source[self.position] == "*":
                self.next = Token(value=self.source[self.position], type="MULTIPLY")
                self.position += 1
                return
            elif self.source[self.position] == "/":
                self.next = Token(value=self.source[self.position], type="DIVIDE")
                self.position += 1
                return
            elif self.source[self.position] == "(":
                self.next = Token(value=self.source[self.position], type="OPEN_PAR")
                self.position += 1
                return
            elif self.source[self.position] == ")":
                self.next = Token(value=self.source[self.position], type="CLOSE_PAR")
                self.position += 1
                return
            elif self.source[self.position] == "{":
                self.next = Token(value=self.source[self.position], type="OPEN_BRACE")
                self.position += 1
                return
            elif self.source[self.position] == "}":
                self.next = Token(value=self.source[self.position], type="CLOSE_BRACE")
                self.position += 1
                return
            elif self.source[self.position] == "\n":
                self.next = Token(value=self.source[self.position], type="BREAKLINE")
                self.position += 1
                return
            elif self.source[self.position] == ";":
                self.next = Token(value=self.source[self.position], type="SEMICOLUMN")
                self.position += 1
                return
            elif self.source[self.position] == ",":
                self.next = Token(value=self.source[self.position], type="COMMA")
                self.position += 1
                return
            elif re.match(
                "[a-zA-Z]", self.source[self.position]
            ):
                val = ""
                while self.position < len(self.source) and re.match(
                    r"[a-zA-Z1-9_]", self.source[self.position]
                ):
                    val += self.source[self.position]
                    self.position += 1
                if val == "Println":
                    self.next = Token(value=str(val), type="PRINTLN")
                elif val == "Scanln":
                    self.next = Token(value=str(val), type="SCANLN")
                elif val == "if":
                    self.next = Token(value=str(val), type="IF")
                elif val == "else":
                    self.next = Token(value=str(val), type="ELSE")
                elif val == "for":
                    self.next = Token(value=str(val), type="FOR")
                elif val == "return":
                    self.next = Token(value=str(val), type="RETURN")
                elif val == "func":
                    self.next = Token(value=str(val), type="FUNC")
                elif val == "var":
                    self.next = Token(value=str(val), type="VAR")
                elif val == "int":
                    self.next = Token(value=str(val), type="T_INT")
                elif val == "string":
                    self.next = Token(value=str(val), type="T_STRING")
                else:
                    self.next = Token(value=str(val), type="IDENTIFIER")
                return
            elif self.source[self.position] == ">":
                self.next = Token(value=self.source[self.position], type="GREATER")
                self.position += 1
                return
            elif self.source[self.position] == "<":
                self.next = Token(value=self.source[self.position], type="LESS")
                self.position += 1
                return
            elif self.source[self.position] == "!":
                self.next = Token(value=self.source[self.position], type="NOT")
                self.position += 1
                return
            elif self.source[self.position] == ".":
                self.next = Token(value=self.source[self.position], type="CONCAT")
                self.position += 1
                return
            elif self.source[self.position] == "|":
                self.position += 1
                if self.source[self.position] == "|":
                    self.next = Token(value=self.source[self.position], type="OR")
                    self.position += 1
                    return
                else:
                    raise Exception("| nn eh valido, tentar ||")
            elif self.source[self.position] == "=":  # Checking if is =
                self.position += 1
                if self.source[self.position] == "=":  # Checking if is ==
                    self.next = Token(value=self.source[self.position], type="COMPARE")
                    self.position += 1
                else:
                    self.next = Token(value=self.source[self.position - 1], type="ASSIGN")
                return
            elif self.source[self.position] == "&":  # Checking if is &&
                self.position += 1
                if self.source[self.position] == "&":
                    self.next = Token(value=self.source[self.position], type="AND")
                    self.position += 1
                    return
                else:
                    raise Exception("& nn eh valido, tentar &&")
            elif self.source[self.position] == " ":  # jumping spaces
                self.position += 1
                continue
            else:
                raise Exception("nao eh token")
