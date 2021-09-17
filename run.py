INPUT = r'''print(2);'''

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
