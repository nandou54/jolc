import json
from interpreter.analyzer import lexer, parse

INPUT = '''
x = accesoo[5];
'''

# lexer.input(INPUT)
# for tok in lexer:
#     print(tok)

res = parse(INPUT)
prettyAST = json.dumps(res["ast"], indent=2)
prettyErrors = json.dumps(res["errors"], indent=2)
print(prettyAST)
print(prettyErrors)
