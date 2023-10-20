from ..defs import *
from .lex import ULex
from .gen import *
from collections import deque
dss = Gen.dss

class UParse:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.tklen: int = len(tokens)
        self.ptr = -1

    def _match(self, type: str, value: str):
        t: Token = self._forward()
        if (t.type != type or t.value != value):
            UError.SyntaxErr(t.value, Token(type, value), '', '')

    def _match_opt(self, type: str, value: str) -> bool:
        t: Token = self._forward()
        if (t.type != type or t.value != value):
            self._backward()
            return False
        return True
    
    def _matcht(self, x: Token): self._match(x.type, x.value)
    def _matcht_opt(self, x: Token) -> bool: return self._match_opt(x.type, x.value)

    def _matchkey(self, x: str): self._match(TokenType.keyword, x)
    def stmt_end(self):
        t: Token = self._forward()
        if (t.type != TokenType.sepr or t.value != ';'):
            UError.semiColonErr('')
        

    def _backward(self) -> Token:
        self.ptr -= 1
        return self._get()
    
    def _forward(self) -> Token:
        self.ptr += 1
        return self._get()
    
    def _peek(self) -> Token:
        if (self.ptr + 1 >= self.tklen): return TOKEN_EOF
        return self.tokens[self.ptr + 1]
    
    def _get(self) -> Token:
        if (self.ptr >= self.tklen): return TOKEN_EOF
        return self.tokens[self.ptr]

    def separater_list(self, kind_value: str, kind_type = TokenType.paren) -> dss:
        MATCH = Token(kind_type, kind_value)

        # test if it is an empty sep list
        if (self._forward() == MATCH):
            return Gen.separater_list([])
        self._backward()
        
        COMMA = Token(TokenType.sepr, ',')
        datas: list[dss] = []
        while 1:
            datas.append(self.bin_expression())

            if not self._matcht_opt(COMMA):
                # not a comma, the loop breaks
                break
        self._matcht(MATCH)
        return Gen.separater_list(datas)
    
    def primary_expression(self) -> dss:
        'expression without basic operators, but contains prefix & postfix'
        t: Token = self._peek()
        if (t.type == TokenType.oper and t.value in unary_list):
            # _forward() is same as t but required
            return Gen.prefix(self._forward(), self.primary_expression())
        return self.atom()
    
    def atom(self) -> dss:
        'expression without basic operators'
        # dot notation & call & colon syntax parsing

        stack: deque[Token] = []
        while 1:
            t: Token = self._forward()

            # const data types
            if (t.type in const_type):
                stack.append
                stack.append(Gen.constant_value(t))
            
            # dot expression with idnt
            elif (t.type == TokenType.sepr and t.value == '.'):
                t = self._forward()
                stack.append(Gen.dot_expression(stack.pop(), t))
            
            # call funcs or brc
            elif (t.type == TokenType.paren and t.value == '('):
                # is it a normal paren or a call node?
                if len(stack) == 0:
                    # it is a normal paren
                    t = self.bin_expression(0)
                    self._match(TokenType.paren, ')')
                    stack.append(t)
                else:
                    # it is call node
                    args: list[dss] = self.separater_list(')')
                    stack.append(Gen.call_func(stack.pop(), args))

            else:
                self._backward()
                break

        if (len(stack) != 1):
            UError.SyntaxErr('atom', 'TODO', '', '')
        return stack.pop()
    
    def bin_expression(self, ptp: int = 0) -> dss:
        'expression'
        # pratt parser
        left: dss = self.primary_expression()
        prec: int = 0
        isGt: bool = False

        oper: Token = self._forward()
        if (oper.is_eof):
            return left
        if (oper.is_binexpr_end):
            self._backward()
            return left

        prec, isGt = get_oper_prec_greater(oper, ptp)
        while (isGt):
            right: dss = self.bin_expression(prec)
            left = Gen.bin_expression(left, oper, right)

            oper = self._forward()
            if (oper.is_eof): return left
            if (oper.is_binexpr_end): break

            prec, isGt = get_oper_prec_greater(oper, ptp)
        
        self._backward() # put back oper
        return left

    def var_statement(self) -> dss:
        # todo - type declar
        self._matchkey('var')
        # use atom to allow a.b.c = d.e
        # without prefix & postfix
        idnt: dss = self.atom()
        self._match(TokenType.oper, '=')

        expr: dss = self.bin_expression()
        self.stmt_end()
        return Gen.var_stmt(idnt, expr)
    
    def paren_stmt(self) -> dss:
        self._match(TokenType.paren, '(')
        expr: dss = self.bin_expression()
        self._match(TokenType.paren, ')')
        return expr

    def ifelse_statement(self) -> dss:
        self._matchkey('if')

        expr: dss = self.paren_stmt()
        if_: dss = self.statement()
        else_:dss = Gen.nop()

        if (self._peek().is_keyword('else')):
            self._forward()
            else_ = self.statement()
        return Gen.ifelse_stmt(expr, if_, else_)

    def repeat_statement(self) -> dss:
        self._matchkey('repeat')
        expr: dss = self.paren_stmt()
        stmt: dss = self.statement()
        return Gen.repeat_stmt(expr, stmt)
    
    def mulstatement(self, reqBrc = True) -> dss:
        if reqBrc: self._match(TokenType.paren, '{')
        stmts: list[dss] = []
        stmt: dss = self.statement()
        while (stmt['type'] != Gen._nop):
            stmts.append(stmt)
            stmt = self.statement()
        if reqBrc: self._match(TokenType.paren, '}')
        return Gen.mulstatement(stmts)

    def statement(self) -> dss:
        # for special syntax only.
        # e.g. if, for, function, return
        # others go in bin expr

        t: Token = self._peek()

        if t.is_keyword('var'):
            return self.var_statement()
        
        elif t.is_keyword('if'):
            return self.ifelse_statement()
        
        elif t.is_keyword('repeat'):
            return self.repeat_statement()
        
        elif t.is_eof or t.type == TokenType.sepr:
            return Gen.nop()
        
        elif t.type == TokenType.paren and t.value in rparen:
            return Gen.nop()
        
        elif t.type == TokenType.paren and t.value == '{':
            return self.mulstatement()
        
        else:
            expr: dss = self.bin_expression(0)
            self.stmt_end()
            return expr