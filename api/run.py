import json
from interpreter.analyzer import lexer as lex, parse
from interpreter.main import interpret

INPUT = r'''
print("testing");
'''

LEXER = True
PARSER = True
INTERPRETER = True

# LEXER
if LEXER:
  print('=== LEXER ===')
  lex.input(INPUT)
  for tok in lex:
    print(tok)

# PARSER
if PARSER:
  print('=== PARSER ===')
  res = parse(INPUT)
  try:
    print(json.dumps(res, indent=2))
  except:
    print(res)

# INTERPRETER
if INTERPRETER:
  print('=== INTERPRETER ===')
  res = interpret(INPUT)

  print('\n'.join(res['output']))

  with open('./test.dot', 'w') as dot:
    dot.write(res['ast'])
  try:
    print(json.dumps(res['errors'], indent=2))
  except:
    print(res['errors'])
