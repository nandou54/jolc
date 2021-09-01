import json

INPUT = '''
println("Funciones nativas aritmeticas");
# log(base, numero)
println(log(2, 4));     # 2.0
println(log(9, 135));   # 2.2324867603589635
# log10()
println(log10(2000));   # 3.3010299956639813
println(log10(512));    # 2.709269960975831
# trigonometricas
println(sin(67/360*2*3.14));    # 0.9202730580752193
println(cos(67/360*2*3.14));    # 0.39127675446016985
println(tan(67/360*2*3.14));    # 2.351974778938468
# sqrt
println(sqrt(2^4));     # 4.0
println(sqrt(1258));    # 35.4682957019364

println("Operaciones con cadenas");
println("para" * "caidismo");   # paracaidismo
println("Holaaa"^5);    # HolaaaHolaaaHolaaaHolaaaHolaaa
# println("Hola Mundo!"[begin:5] * "Auxiliar" * "Auxiliar"[2:end]);    # Hola Auxiliar
# println(length("Esto no sé cuanto mide"));  # 22
println(uppercase("mayuscula"));    # MAYUSCULA
println(lowercase("MINUSCULA"));    # minuscula
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
    try:
      print(json.dumps(res['output'], indent=2))
      print(json.dumps(res['errors'], indent=2))
    except:
      print(res['output'])
      print(res['errors'])

run(INPUT, lexer, parser, interpreter)
