INPUT = r'''
x = 1::Int64;
y = 1::Int64;
println("---------------------------------");
println("Tablas de multiplicar con While");
println("---------------------------------");
while (x <= 10)
    while (y <= 10)
        print(x);
        print("x");
        print(y);
        print("=");
        println(x * y);
        global y = y + 1;
    end;
    println("-----------------------------");
    global x = x + 1;
    global y = 1;
end;

println("---------------------------------");
println("  Tablas de multiplicar con For");
println("---------------------------------");

for i in 1:10
    for j in 1:10
        print(i);
        print("x");
        print(j);
        print("=");
        println(i * j);
    end;
    println("--------------------------");
end;

iteraciones = 10::Int64;
temporal = 0::Int64;

while (temporal <= iteraciones)
    numero = temporal::Int64;
    if numero <= 0
        print("Factorial de ");
        print(temporal);
        println(" = 0");
        global temporal = temporal + 1;
        continue;
    end;
    factorial = 1::Int64;
    while (numero > 1)
        factorial = factorial * numero;
        numero = numero - 1;
    end;
    print("Factorial de ");
    print(temporal);
    print(" = ");
    println(factorial);
    temporal = temporal + 1;
end;

for i in 0:9

    output = "";
    for j in 0:(10 - i)
        output = output * " ";
    end;

    for k in 0:i 
        output = output * "* ";
    end;
    println(output);

end;
'''

LEXER = False
PARSER = False
INTERPRETER = False
TRANSLATOR = False
OPTIMIZER_EYEHOLE = False
OPTIMIZER_BLOCKS = True

import json
import os
from analyzer.main import lexer, parse
from interpreter.main import interpret
from translator.main import translate
from optimizer.eyehole import optimize as optimize_eyehole
from optimizer.blocks import optimize as optimize_blocks

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
