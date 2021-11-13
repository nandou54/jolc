import json
import os
from api.analyzer.main import lexer, parse
from api.interpreter.main import interpret
from api.translator.main import translate
from api.optimizer.eyehole import optimize as optimize_eyehole
from api.optimizer.blocks import optimize as optimize_blocks

INPUT = r'''
function StringFunction()

    str1 = "Sale Compiladores 2"::String;

    println("FUNCIONES STRING:");
    println("Concatenacion:");
    println(str1 * " C3D - segundo Proyecto");
    # println("UpperCase:");
    # println(uppercase(str1));
    # println("LowerCase:");
    # println(lowercase(str1 * " SI SALE"));

    println("Concatenacion + :");
    println("string * string");
    println(str1 * " C3D - segundo Proyecto");
    # println("string * numero entero");
    # println("entero = " * string(125));
    # println("string * numero decimal");
    # println("decimal = " * string(45.3246));
    # println("decimal = " * string(176/3));
end;

function testambito()
    # numberstring= string(100) * "Usac"::String;
    # stringnumber= "Usac" * string(2500)::String;
    stringstring= "Universidad" * " San Carlos"::String;
    println(numberstring);
    println(stringnumber);
    println(stringstring);
end;

# function todas(parametro::String)
#     println(uppercase(lowercase(parametro)));
# end;

StringFunction();
testambito();
# todas("hoy ganO compi2");
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

  # with open('./test.go', 'w') as file:
  #   file.write(res['output'])

if OPTIMIZER_BLOCKS:
  print('=== OPTIMIZER BY BLOCKS ===')

  res = {}
  with open('./test.go', 'r') as file:
    content = file.read()
    res = optimize_blocks(content)
    print(res['output'])
    print(json.dumps(res['reports'], indent=2, ensure_ascii=False))

  # with open('./test.go', 'w') as file:
  #   file.write(res['output'])

if TRANSLATOR or OPTIMIZER_BLOCKS or OPTIMIZER_EYEHOLE:
  print('= GO OUTPUT =')
  os.system('go run ./test.go')
  print()
