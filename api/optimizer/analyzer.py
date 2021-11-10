from api.ply.yacc import yacc
from api.ply.lex import lex

from api.optimizer.symbols import Assignment, Call, Expression, Function, Goto, Id, If, Library, Number, Return, String, Tag, Wrapper, operations

INPUT = ''
errors = []

def getColumn(t):
  global INPUT
  line_start = INPUT.rfind('\n', 0, t.lexpos)+1
  return (t.lexpos-line_start)+1

def parse(input):
  global INPUT
  global errors

  for _ in range(10):
    index = input.find('\n')
    input = input[index+1:]

  INPUT = input
  lexer.lineno = 10

  ast = parser.parse(input)

  if ast is None: ast = []
  return {'ast': ast, 'output': '', 'reports': []}

reserved = (
  'func',
  'return',
  'goto',
  'if'
)

tokens = (
  'parA',
  'parB',
  'corA',
  'corB',
  'llaveA',
  'llaveB',
  'id',
  'number',
  'string',
  'mas',
  'menos',
  'asterisco',
  'barra',
  'modulo',
  'igual',
  'mayor',
  'menor',
  'mayor_igual',
  'menor_igual',
  'igualacion',
  'diferenciacion',
  'punto',
  'coma',
  'puntoycoma',
  'dospuntos'
) + reserved

# Lexemas ignorados
t_ignore                       =  ' \t'
t_ignore_comentario            = r'//.*'
t_ignore_comentario_multilinea = r'/\*([\s\S]*?)\*/\s*'

t_parA           = r'\('
t_parB           = r'\)'
t_corA           = r'\['
t_corB           = r'\]'
t_llaveA           = r'{'
t_llaveB           = r'}'
t_mas            = r'\+'
t_menos          = r'-'
t_asterisco      = r'\*'
t_barra          = r'/'
t_modulo         = r'%'
t_mayor_igual    = r'>='
t_mayor          = r'>'
t_menor_igual    = r'<='
t_menor          = r'<'
t_igualacion     = r'=='
t_diferenciacion = r'!='
t_punto          = r'\.'
t_coma           = r','
t_igual          = r'='
t_puntoycoma     = r';'
t_dospuntos      = r':'

def t_id(t):
  r'[a-zA-Z_][a-zA-Z_0-9!]*'
  if t.value in reserved: t.type = t.value
  return t

def t_number(t):
  r'\d+(\.\d+)?'
  value = 0

  try:
    value = float(t.value)
  except ValueError:
    print("Float64 value too big: %d", t.value)

  t.value = Number(t.lineno, getColumn(t), value)
  return t

def t_string(t):
  r'".*"'
  t.value = String(t.lineno, getColumn(t), t.value)
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno+=len(t.value)

def t_error(t):
  # error = LexicalError(t.lineno, getColumn(t), "No se pudo reconocer el lexema '%s'" % t.value)
  # errors.append(error)
  print('no reconocido: ', t.value)
  t.lexer.skip(1)

# Precedencia de menos a más
precedence = (
  ('left','igualacion','diferenciacion'),
  ('left','menor','menor_igual','mayor','mayor_igual'),
  ('left','mas','menos'),
  ('left','asterisco','barra','modulo'),
  ('right','op_negacion'),
  ('nonassoc','op_agrupacion')
)

# Producciones
def p_FUNCTIONS(p):
  '''
  FUNCTIONS : FUNCTIONS F
            | F
  '''
  if len(p)==3:
    p[0] = p[1]
    p[0].append(p[2])
  else:
    p[0] = [p[1]]

def p_F(p):
  '''
  F : func id parA parB llaveA INS llaveB
  '''
  id, INS = p[2], p[6]

  function = Function(p.lexer.lineno, getColumn(p.lexer), id, INS)

  for ins in INS:
    ins.owner = function

  p[0] = function

def p_INS(p):
  '''
  INS : INS I
      | I
  '''
  if len(p)==3:
    p[0] = p[1]
    p[0].append(p[2])
  else:
    p[0] = [p[1]]

def p_I(p):
  '''
  I : ASIGNACION puntoycoma
    | ETIQUETA
    | GOTO puntoycoma
    | IF
    | LLAMADA puntoycoma
    | RETURN puntoycoma
    | LIBRARY puntoycoma
  '''
  p[0] = p[1]

def p_E(p):
  '''
  E : E mas E
    | E menos E
    | E asterisco E
    | E barra E
    | E modulo E
    | menos E                   %prec op_negacion
    | E mayor E
    | E menor E
    | E mayor_igual E
    | E menor_igual E
    | E igualacion E
    | E diferenciacion E
    | parA E parB               %prec op_agrupacion
    | LIBRARY
    | number
    | ID
    | string
  '''
  if len(p)==2:
    p[0] = p[1]
    return

  if p[1]=='(':
    p[0] = p[2]
    return

  unary, l, r, type = False, None, None, None

  if len(p)==4:
    l = p[1]
    r = p[3]
    type = operations[p[2]]
  else:
    unary = True
    l = p[2]
    type = 'negacion'

  p[0] = Expression(p.lexer.lineno, getColumn(p.lexer), unary, type, l, r)

def p_ASIGNACION(p):
  '''
  ASIGNACION : ID igual E
  '''
  id, expression = p[1], p[3]
  p[0] = Assignment(p.lexer.lineno, getColumn(p.lexer), id, expression)

def p_ID(p):
  '''
  ID  : id
      | id corA ID corB
      | id parA ID parB
  '''
  if len(p)==2:
    p[0] = Id(p.lexer.lineno, getColumn(p.lexer), p[1])
    return

  id, type = p[1], 'access' if p[2]=='[' else 'call'

  wrapper = Wrapper(p.lexer.lineno, getColumn(p.lexer), id, type)
  p[0] = p[3]
  p[0].wrappers.append(wrapper)

def p_ETIQUETA(p):
  '''
  ETIQUETA : id dospuntos
  '''
  id = p[1]
  p[0] = Tag(p.lexer.lineno, getColumn(p.lexer), id)

def p_GOTO(p):
  '''
  GOTO : goto id
  '''
  tag = p[2]
  p[0] = Goto(p.lexer.lineno, getColumn(p.lexer), tag)

def p_LLAMADA(p):
  '''
  LLAMADA : id parA parB
  '''
  id = p[1]
  p[0] = Call(p.lexer.lineno, getColumn(p.lexer), id)

def p_IF(p):
  '''
  IF : if parA E parB llaveA GOTO llaveB
  '''
  expression, goto = p[3], p[6]
  p[0] = If(p.lexer.lineno, getColumn(p.lexer), expression, goto)

def p_RETURN(p):
  '''
  RETURN : return
  '''
  p[0] = Return(p.lexer.lineno, getColumn(p.lexer))

def p_LIBRERIA(p):
  '''
  LIBRARY : id punto id parA PARS parB
  '''
  parameters = ','.join(p[5])
  lexeme = f'{p[1]}.{p[3]}({parameters})'
  p[0] = Library(p.lexer.lineno, getColumn(p.lexer), lexeme)

def p_PARS(p):
  '''
  PARS  : PARS coma P
        | P
  '''
  if len(p)==4:
    p[0] = p[1]
    p[0].append(p[3])
  else:
    p[0] = [p[1]]

def p_P(p):
  '''
  P : E
  '''
  ex = str(p[1])
  p[0] = ex

def p_error(p):
  if p:
    if type(p.value) in [str, int, float, bool]: msg = "Sintaxis no válida cerca de '{}' ({})" .format(p.value, p.type)
    else: msg = "Sintáxis no válida en {}".format(p.type)
    # error = SyntacticError(p.lineno, getColumn(p), msg)
  # else:
    # error = SyntacticError(0, 0, "Ninguna instrucción válida")

  # errors.append(error)

lexer = lex()
parser = yacc()
