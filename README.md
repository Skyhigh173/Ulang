# Ulang

A (slow) programming language interpreter in Python.

`main.py` playground requires `rich` module. You can edit it.

**W.I.P error messages**

## How to lex

> main.py
```py
from src.parse.lex import ULex

l = ULex('your code here')
l.run()

print(l.tokens) # list of tokens
```

## How to parse

> main.py
```py
from src.parse.lex import ULex
from src.parse.parse import UParse

l = ULex('your code here')
p = UParse(l.run())

print(p.mulstatement(reqBrc = False))  # AST tree
```
