from .errors import UError

class TokenType:
    eof  = 'eof'
    null = 'null'

    number    = 'number'
    string    = 'string'
    idnt      = 'idnt'
    boolean   = 'boolean'
    function  = 'function'
    object    = 'object'
    address   = 'address'

    keyword   = 'keyword'
    oper      = 'operator'
    paren     = 'parenthesis'
    sepr      = 'seperator'

# basically all data types
const_type: list[str] = [
    TokenType.number,
    TokenType.idnt,
    TokenType.boolean,
    TokenType.string
]

class Token:
    def __init__(self, tokenType, string):
        self.type:  str = tokenType
        self.value: str = string

    @property
    def is_eof(self) -> bool:
        return self.type == TokenType.eof
    
    @property
    def is_binexpr_end(self) -> bool:
        return (self.type == TokenType.paren) \
            or (self.type == TokenType.sepr)
    
    def is_keyword(self, x: str) -> bool:
        return self.type == TokenType.keyword and self.value == x
    
    def __repr__(self) -> str:
        if self.is_eof: return '{eof}'
        
        return f'{{{self.type}:{self.value}}}'
    
    def __eq__(self, x: 'Token') -> bool:
        return self.type == x.type and self.value == x.value
    
    def __neq__(self, x: 'Token') -> bool:
        return not self.__eq__(x)
    
    __str__ = __repr__

TOKEN_EOF = Token(TokenType.eof, '')

oper_prec: dict[str, int] = {
    # !unary (will not be compared in bin expr)
    # !will throw error when compared (str) > (ptp)
    '!': '',
    # !normal
    '=': 10, '+=': 10, '-=': 10, '*=': 10, '/=': 10,
    '||': 50, '&&': 55,
    '==': 60, '!=': 60,
    '>=': 60, '<=': 60,
    '>': 60, '<': 60,
    '&': 100, '|': 100,
    '+': 100, '-': 100,
    '*': 200, '/': 200,
    '**': 300,
}
oper_right: list[str] = ['**']

oper_list : list[str] = list(oper_prec.keys())
opert_list: list[str] = [x for x in oper_list if len(x) == 2]
sper_list : list[str] = [':',',',';','.']
paren_list: list[str] = ['(','{','[',')','}',']']
unary_list: list[str] = ['-','!']

rparen: list[str] = [')','}',']']

from string import ascii_letters
valid_idnt: str = ascii_letters + '_0123456789'

def get_oper_prec(x: Token) -> int:
    if (x.type != TokenType.oper) or (x.value not in oper_list): UError.SyntaxErr(x, 'operator', '', '')
    return oper_prec.get(x.value)

def get_oper_prec_greater(x:Token, ptp: int) -> (int, bool):
    prec: int = get_oper_prec(x)
    if (x.value in oper_right):
        return prec, prec >= ptp
    return prec, prec > ptp

keyword_list: list[str] = [
    'if', 'else',
    'var',
    'for', 'while', 'repeat'
]