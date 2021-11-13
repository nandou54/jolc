import json
import os
from api.analyzer.main import lexer, parse
from api.interpreter.main import interpret
from api.translator.main import translate
from api.optimizer.eyehole import optimize as optimize_eyehole
from api.optimizer.blocks import optimize as optimize_blocks

INPUT = r'''
function fact(a)
  if a > 0
    return a*fact(a-1);
  end;
  return 1;
end;

x = fact(3);
println(x);
'''

LEXER = False
PARSER = False
INTERPRETER = False
TRANSLATOR = True
OPTIMIZER_EYEHOLE = False
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
  print(json.dumps(res['errors'], indent=2, ensure_ascii=False))
  # print(json.dumps(res['symbols'], indent=2, ensure_ascii=False))

if OPTIMIZER_EYEHOLE:
  print('=== OPTIMIZER BY EYEHOLE ===')

  res = {}
  with open('./test.go', 'r') as file:
    content = file.read()
    res = optimize_eyehole(content)
    print(res['output'])
    print(json.dumps(res['reports'], indent=2, ensure_ascii=False))

  with open('./test.go', 'w') as file:
    file.write(res['output'])

if OPTIMIZER_BLOCKS:
  print('=== OPTIMIZER BY BLOCKS ===')

  res = {}
  with open('./test.go', 'r') as file:
    content = file.read()
    res = optimize_blocks(content)
    print(res['output'])
    print(json.dumps(res['reports'], indent=2, ensure_ascii=False))

  with open('./test.go', 'w') as file:
    file.write(res['output'])

if TRANSLATOR or OPTIMIZER_BLOCKS or OPTIMIZER_EYEHOLE:
  print('= GO OUTPUT =')
  os.system('go run ./test.go')
  print()
