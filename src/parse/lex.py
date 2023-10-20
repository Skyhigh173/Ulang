from ..defs import *

from typing import LiteralString

class ULex:
    def __init__(self, text):
        self.text: str = text
        self.tlen: int = len(text)
        self.lin = 1
        self.col = 0
        self.ptr = -1
        
        self.tokens: list[Token] = []
    
    def reset(self):
        'reset the state of lexer'
        self.lin = 1
        self.col = 0
        self.ptr = -1

        self.tokens = []
    
    def run(self) -> list[Token]:
        'scan tokens'
        self.reset()
        t: Token = self.__scan()
        
        while not t.is_eof:
            self.tokens.append(t)
            t = self.__scan()
        
        return self.tokens
    
    @property
    def pos(self) -> str:
        return f'(at line {self.lin}, col {self.col})'
    
    def __access(self, pos) -> str:
        if (pos >= self.tlen):
            return TokenType.eof
        return self.text[pos]
    
    def __get(self, pos=None) -> str:
        return self.__access(self.ptr)
    
    def __peek(self) -> str:
        return self.__access(self.ptr+1)
    
    def __next(self) -> str:
        # check if out of bound
        if (self.ptr >= self.tlen):
            return TokenType.eof
        
        # increment ptr
        self.ptr += 1
        self.col += 1

        # get char
        char: str = self.__get()
        if (char == '\n'):
            self.lin += 1
            self.col = 0
        return char
    
    def __skip(self) -> str:
        char: str = self.__next()

        while (char in [' ', '\n', '\r', '\t']):
            char = self.__next()
        
        return char
    
    def __scan(self) -> Token:
        char: str = self.__skip()

        # eof
        if (char == TokenType.eof):
            return TOKEN_EOF

        # operators
        if (char in oper_list):
            return Token(TokenType.oper, self.__scan_oper(char))
        
        # numbers
        if (char.isdigit()):
            return Token(TokenType.number, self.__scan_number(char))
        
        # parens
        if (char in paren_list):
            return Token(TokenType.paren, char)
        
        # sepr
        if (char in sper_list):
            return Token(TokenType.sepr, char)
        
        # idnt
        if (char in valid_idnt):
            idnt: str = self.__scan_idnt(char)
            if (idnt in keyword_list):
                return Token(TokenType.keyword, idnt)
            return Token(TokenType.idnt, idnt)
        
        UError.SyntaxErr(char, 'other', self.pos, '')

    def __scan_number(self, char: str) -> str:
        # rule:
        # [digits] (. [digits]) (e (+|-) [digits])

        def match(m) -> bool:
            nonlocal char

            if (self.__peek() == m):
                char += m
                self.__next()
                return True
            return False
        
        def digit():
            nonlocal char

            c: str = self.__next()

            while (c.isdigit()):
                char += c
                c = self.__next()
            
            self.ptr -= 1

        digit()
        if match('.'):
            digit()
        if match('e'):
            if not match('-'): match('+')
            digit()
        
        return char
    
    def __scan_idnt(self, char: str) -> str:
        
        c: str = self.__next()
        while c in valid_idnt:
            char += c
            c = self.__next()
            
        self.ptr -= 1
        return char

    def __scan_oper(self, char: str) -> str:
        c: str = char + self.__peek()
        if c in opert_list:
            self.__next()
            return c
        return char