import json
import os
from api.analyzer.main import lexer, parse
from api.interpreter.main import interpret
from api.translator.main import translate

INPUT = r'''
s = length("quepex bro");
print(s);
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

  with open('./test.go', 'w') as file:
    file.write(res['output'])
  print(res['output'])

  # os.system('go fmt ./test.go')

  # with open('./test.go', 'r') as file:
  #   print(file.read())

  print('= GO OUTPUT =')
  os.system('go run ./test.go')
  print()
  try:
    print(json.dumps(res['errors'], indent=2, ensure_ascii=False))
  except:
    print(res['errors'])
