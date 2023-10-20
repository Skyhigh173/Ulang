from ..defs import Token, TokenType
from ..errors import UError
class Gen:
    type dss = dict[str, str]

    @staticmethod
    def nop() -> dss:
        return {'type': Gen._nop}
    _nop = 'nop'

    @staticmethod
    def mulstatement(stmt: list[dss]) -> dss:
        return {'type': Gen._mulstatement, 'statements': stmt}
    _mulstatement = 'mulstmt'

    @staticmethod
    def constant_value(t: Token) -> dss:
        return {'type': Gen._constant_value, 'xtype': t.type, 'value': t.value}
    _constant_value = 'constv'
    
    @staticmethod
    def bin_expression(l: dss, op: Token, r: dss) -> dss:
        return {'type': Gen._bin_expression, 'left': l, 'oper': op.value, 'right': r}
    _bin_expression = 'binexpr'
    
    @staticmethod
    def dot_expression(obj: dss, attr: Token) -> dss:
        if (attr.type != TokenType.idnt): UError.SyntaxErr(attr.value, 'idnt', '', '')
        return {'type': Gen._dot_expression, 'object': obj, 'attr': attr.value}
    _dot_expression = 'dotexpr'
    
    @staticmethod
    def call_func(obj: dss, args: dss) -> dss:
        return {'type': Gen._call_func, 'object': obj, 'arguments': args}
    _call_func = 'callfunc'
    
    @staticmethod
    def separater_list(ls: list[dss]) -> dss:
        return {'type': Gen._separater_list, 'list': ls}
    _separater_list = 'seplist'

    @staticmethod
    def var_stmt(obj: dss, expr: dss) -> dss:
        return {'type': Gen._var_stmt, 'object': obj, 'expr': expr}
    _var_stmt = 'varstmt'

    @staticmethod
    def prefix(oper: Token, expr: dss) -> dss:
        if (oper.type != TokenType.oper): UError.SyntaxErr(oper.value, 'operator', '', '')
        return {'type': Gen._prefix, 'oper': oper.value, 'expr': expr}
    _prefix = 'prefix'

    @staticmethod
    def ifelse_stmt(expr: dss, if_stmt: dss, else_stmt: dss) -> dss:
        return {'type': Gen._ifelse_stmt, 'expr': expr, 'if': if_stmt, 'else': else_stmt}
    _ifelse_stmt = 'ifelsestmt'

    @staticmethod
    def repeat_stmt(expr: dss, stmt: dss) -> dss:
        return {'type': Gen._repeat_stmt, 'expr': expr, 'statement': stmt}
    _repeat_stmt = 'repeatstmt'