import json
import os
from analyzer.main import lexer, parse
from interpreter.main import interpret
from translator.main import translate

INPUT = r'''
if 5==5
  x = 1 + 1;
elseif 6==6
  x = 100 + 100;
end;
'''

LEXER = False
PARSER = False
INTERPRETER = False
TRANSLATOR = True

if LEXER:
  print('=== LEXER ===')
  lexer.input(INPUT)
  for tok in lexer:
    print(tok)

if PARSER:
  print('=== PARSER ===')
  res = parse(INPUT)
  try:
    print(json.dumps(res, indent=2))
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

  with open('./test.go', 'w') as file:
    file.write(res['output'])

  os.system('go fmt ./test.go')

  with open('./test.go', 'r') as file:
    print(file.read())

  print('= GO OUTPUT =')
  os.system('go run ./test.go')

  try:
    print(json.dumps(res['errors'], indent=2))
  except:
    print(res['errors'])
