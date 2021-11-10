import json
import os
from api.analyzer.main import lexer, parse
from api.interpreter.main import interpret
from api.translator.main import translate
from api.optimizer.eyehole import optimize as optimize_eyehole
from api.optimizer.blocks import optimize as optimize_blocks

INPUT = r'''
x=5;
print(x+x);
'''

LEXER = False
PARSER = False
INTERPRETER = False
TRANSLATOR = False
OPTIMIZER_EYEHOLE = True
OPTIMIZER_BLOCKS = False

if LEXER:
  print('=== LEXER ===')
  lexer.input(INPUT)
  for tok in lexer:
    print(tok)

if PARSER:
  print('=== PARSER ===')
  res = parse(INPUT)
  try:
    print(json.dumps(res, indent=2, ensure_ascii=False))
  except:
    print(res)

if INTERPRETER:
  print('=== INTERPRETER ===')
  res = interpret(INPUT)

  print('\n'.join(res['output']))
  try:
    print(json.dumps(res['errors'], indent=2))
  except:
    print(res['errors'])

if TRANSLATOR:
  print('=== TRANSLATOR ===')
  res = translate(INPUT)
  output = res['output']

  with open('./test.go', 'w') as file:
    file.write(output)
  print(output)

  print('= GO OUTPUT =')
  os.system('go run ./test.go')
  print()
  try:
    print(json.dumps(res['errors'], indent=2, ensure_ascii=False))
  except:
    print(res['errors'])

if OPTIMIZER_EYEHOLE:
  print('=== OPTIMIZER BY EYEHOLE ===')

  with open('./test.go', 'r') as file:
    content = file.read()
    res = optimize_eyehole(content)

if OPTIMIZER_BLOCKS:
  print('=== OPTIMIZER BY BLOCKS ===')

  with open('./test.go', 'r') as file:
    content = file.read()
    res = optimize_blocks(content)
