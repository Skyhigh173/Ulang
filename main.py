from src.parse.lex import ULex
from src.parse.parse import UParse
import rich, json

while 1:
    t = ''
    l = ' '
    while (l != ''):
        l = input('>>> ')
        t += l
    
    c = ULex(t)
    p = UParse(c.run())
    rich.print(c.tokens)
    rich.print_json(json.dumps(p.mulstatement(False)))