INPUT = r'''
#################################################
#   Las demás reglas se le preguntará al estudiante
#   sobre como las implemento, se revisará código y
#   se probarán archivos que estos hayan probado
#   para hacer esta sección
#################################################

# Regla 4
if true && true
    println(true);
else
    println(false);
end;

# # Regla 5 o 3
# if 5 > 2
#     println(true);
# else
#     println(false);
# end;

# # Regla 7
# var1 = 4 + 0;
# var1 = (var1 - 0) * 20;
# var1 = (var1 - 10 * 5) * 1;
# var1 = var1 / 1;

# # Regla 8
# var1 = 4 * 2;
# var1 = var1 * 2;
# var1 = var1 * 0;
# var1 = 0 / var1;
'''

LEXER = False
PARSER = False
INTERPRETER = False
TRANSLATOR = False
OPTIMIZER_EYEHOLE = True
OPTIMIZER_BLOCKS = False

import json
import os
from api.analyzer.main import lexer, parse
from api.interpreter.main import interpret
from api.translator.main import translate
from api.optimizer.eyehole import optimize as optimize_eyehole
from api.optimizer.blocks import optimize as optimize_blocks

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
    print(json.dumps(res['errors'], indent=2, ensure_ascii=False))
  except:
    print(res['errors'])

if TRANSLATOR:
  print('=== TRANSLATOR ===')
  res = translate(INPUT)
  output = res['output']

  with open('./test.go', 'w') as file:
    file.write(output)

  # print(output)
  print(json.dumps(res['errors'], indent=2, ensure_ascii=False))
  # print(json.dumps(res['symbols'], indent=2, ensure_ascii=False))

if OPTIMIZER_EYEHOLE:
  print('=== OPTIMIZER BY EYEHOLE ===')

  res = {}
  with open('./test.go', 'r') as file:
    content = file.read()
    res = optimize_eyehole(content)
    # print(res['output'])
    print(json.dumps(res['reports'], indent=2, ensure_ascii=False))

  with open('./test.go', 'w') as file:
    file.write(res['output'])

if OPTIMIZER_BLOCKS:
  print('=== OPTIMIZER BY BLOCKS ===')

  res = {}
  with open('./test.go', 'r') as file:
    content = file.read()
    res = optimize_blocks(content)
    # print(res['output'])
    print(json.dumps(res['reports'], indent=2, ensure_ascii=False))

  with open('./test.go', 'w') as file:
    file.write(res['output'])

if TRANSLATOR or OPTIMIZER_BLOCKS or OPTIMIZER_EYEHOLE:
  print('= GO OUTPUT =')
  os.system('go run ./test.go')
  print()
