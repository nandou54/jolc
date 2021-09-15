INPUT = r'''
function swap(i, j, arr) 
    temp = arr[i]::Int64;
    arr[i] = arr[j];
    arr[j] = temp;
end;

function bubbleSort(arr)
    for i in 0:(length(arr) - 1)
        for j in 1:(length(arr) - 1)
            if(arr[j] > arr[j + 1])
                swap(j, j+1, arr);
            end;
        end;
    end;
end;

function insertionSort(arr) 

    for i in 1:length(arr)
        j = i;
        temp = arr[i];
        while(j > 1)
            if arr[j - 1] <= temp
                continue;
            end;

            arr[j] = arr[j-1];
            j = j - 1;
        end;
        arr[j] = temp;
    end;

end;

arreglo = [32,7*3,7,89,56,909,109,2,9,9874^0,44,3,820*10,11,8*0+8,10];
bubbleSort(arreglo);
println("BubbleSort => ",arreglo);

arreglo = [32,7*3,7,89,56,909,109,2,9,9874^0,44,3,820*10,11,8*0+8,10];
arreglo[1] = arreglo[2] - 21+4;
insertionSort(arreglo);
print("InsertionSort => ",arreglo);
'''

lexer = False
parser = False
interpreter = True

def run(INPUT, lexer=False, parser=False, interpreter=False):
  # LEXER
  if lexer:
    from interpreter.analyzer import lexer as lex
    print('=== LEXER ===')
    lex.input(INPUT)
    for tok in lex:
        print(tok)

  import json
  # PARSER
  if parser:
    from interpreter.analyzer import parse
    print('=== PARSER ===')
    res = parse(INPUT)
    try:
      print(json.dumps(res, indent=2))
    except:
      print(res)

  # INTERPRETER
  if interpreter:
    from interpreter.main import interpret
    print('=== INTERPRETER ===')
    res = interpret(INPUT)

    print('\n'.join(res['output']))

    dot = open('./test.dot', 'w')
    dot.write(res['ast'])
    dot.close()
    try:
    #   print(json.dumps(res['ast'], indent=2))
      print(json.dumps(res['errors'], indent=2))
    except:
    #   print(res['ast'])
      print(res['errors'])

run(INPUT, lexer, parser, interpreter)
