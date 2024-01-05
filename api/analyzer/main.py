from ply.yacc import yacc
from ply.lex import lex

from symbols import Assignment, Expression, Value, Function, Struct, Attribute, Call, If, Else, While, For, Break, Continue, Return, Error
from symbols import operations

INPUT = ''
errors = []

def LexicalError(ln, col, description):
  return Error(ln, col, 'Léxico', description)

def SyntacticError(ln, col, description):
  return Error(ln, col, 'Sintáctico', description)

def getColumn(t):
  global INPUT
  line_start = INPUT.rfind('\n', 0, t.lexpos)+1
  return (t.lexpos-line_start)+1

def parse(input):
  global INPUT
  global errors

  INPUT = input
  errors = []
  lexer.lineno = 1

  ast = parser.parse(input, lexer)

  if ast is None: ast = []
  return {'ast':ast, 'errors':errors, 'output':'', 'symbols':[]}

reserved = (
  'Nothing',
  'Int64',
  'Float64',
  'Bool',
  'Char',
  'String',
  'struct',
  'local',
  'global',
  'function',
  'end',
  'if',
  'elseif',
  'else',
  'while',
  'for',
  'break',
  'continue',
  'return',
  'mutable',
  'in'
)

tokens = (
  'id',
  'parA',
  'parB',
  'corA',
  'corB',
  'llaveA',
  'llaveB',
  'int64',
  'float64',
  'bool',
  'char',
  'string',
  'mas',
  'menos',
  'asterisco',
  'barra',
  'caret',
  'modulo',
  'igual',
  'mayor',
  'menor',
  'mayor_igual',
  'menor_igual',
  'igualacion',
  'diferenciacion',
  'or',
  'and',
  'not',
  'punto',
  'coma',
  'dospuntos',
  'tipo',
  'interrog',
  'puntoycoma'
) + reserved

states = (
  ('string','exclusive'),
  ('expresion','inclusive')
)

# Lexemas ignorados
t_ignore                       =  ' \t\r'
t_ignore_comentario            = r'[#].*'
t_ignore_comentario_multilinea = r'[#]=([^=]|[\r\n]|(=+([^#])))*=+[#]'
t_string_ignore = ""
t_expresion_ignore = t_ignore

t_parA           = r'\('
t_parB           = r'\)'
t_corA           = r'\['
t_corB           = r'\]'
t_mas            = r'\+'
t_menos          = r'-'
t_asterisco      = r'\*'
t_barra          = r'/'
t_caret          = r'\^'
t_modulo         = r'%'
t_mayor_igual    = r'>='
t_mayor          = r'>'
t_menor_igual    = r'<='
t_menor          = r'<'
t_igualacion     = r'=='
t_diferenciacion = r'!='
t_or             = r'\|\|'
t_and            = r'&&'
t_not            = r'!'
t_punto          = r'\.'
t_coma           = r','
t_igual          = r'='
t_tipo           = r'::'
t_interrog       = r'\?'
t_dospuntos      = r':'
t_puntoycoma     = r';'

def t_begin_string(t):
  r'"'
  t.lexer.push_state('string')
  t.lexer.nothingRecognized = True

def t_string_string(t):
  r'[^"\n{]+'
  value, valueType = t.value, 'string'
  t.value = Value(t.lineno, getColumn(t), value, valueType)
  t.lexer.nothingRecognized = False
  return t

def t_string_llaveA(t):
  r'\{'
  t.lexer.nothingRecognized = False
  t.lexer.push_state('expresion')
  return t

def t_string_end(t):
  r'"'
  t.lexer.pop_state()

  if t.lexer.nothingRecognized:
    value, valueType = '', 'string'
    t.value = Value(t.lineno, getColumn(t), value, valueType)
    t.type = valueType
    return t


def t_expresion_llaveB(t):
  r'\}'
  t.lexer.pop_state()
  return t

def t_float64(t):
  r'\d+\.\d+'
  value, valueType = 0, 'float64'

  try:
    value = float(t.value)
  except ValueError:
    print("Float64 value too big: %d", t.value)

  t.value = Value(t.lineno, getColumn(t), value, valueType)
  return t

def t_int64(t):
  r'\d+'
  value, valueType = 0, 'int64'

  try:
    value = int(t.value)
  except ValueError:
    print("Int64 value too big: %d", t.value)

  t.value = Value(t.lineno, getColumn(t), value, valueType)
  return t

def t_bool(t):
  r'(true)|(false)'
  value, valueType = t.value=='true', 'bool'
  t.value = Value(t.lineno, getColumn(t), value, valueType)
  return t

def t_char(t):
  r"'[^'\n]'"
  value, valueType = t.value[1], 'char'
  t.value = Value(t.lineno, getColumn(t), value, valueType)
  return t

def t_Nothing(t):
  r'nothing'
  t.value = Value(t.lineno, getColumn(t), None, 'nothing')
  return t

def t_id(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  if t.value in reserved: t.type = t.value
  else: t.value = Value(t.lineno, getColumn(t), t.value, 'id')
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno+=len(t.value)

def t_error(t):
  error = LexicalError(t.lineno, getColumn(t), "No se pudo reconocer el lexema '%s'" % t.value)
  errors.append(error)
  t.lexer.skip(1)

t_string_error = t_error
t_expresion_error = t_error

# Precedencia de menos a más
precedence = (
  ('left','op_rango'),
  ('right','op_ternaria'),
  ('left','or'),
  ('left','and'),
  ('left','igualacion','diferenciacion'),
  ('left','menor','menor_igual','mayor','mayor_igual'),
  ('left','mas','menos'),
  ('left','asterisco','barra','modulo'),
  ('right','caret'),
  ('right','op_negacion','not'),
  ('left','op_llamada'),
  ('left','op_acceso'),
  ('nonassoc','op_agrupacion')
)

# Producciones
def p_INS(p):
  '''
  INS : INS I puntoycoma
      | I puntoycoma
  '''
  if len(p)==4:
    p[0] = p[1]
    p[0].append(p[2])
  else:
    p[0] = [p[1]]

def p_INS_error(p):
  '''
  INS : INS error puntoycoma
      | error puntoycoma
  '''
  p[0] = p[1] if len(p)==4 else []

def p_I(p):
  '''
  I : ASIGNACION
    | FUNCION
    | STRUCT
    | LLAMADA
    | IF
    | WHILE
    | FOR
    | BREAK
    | CONTINUE
    | RETURN
  '''
  p[0] = p[1]

def p_BLOQUE(p):
  '''
  BLOQUE  : INS end
  '''
  p[0] = p[1]

def p_BLOQUE_ABIERTO(p):
  '''
  BLOQUE_ABIERTO  : INS
  '''
  p[0] = p[1]

def p_TIPO(p):
  '''
  TIPO  : Int64
        | Float64
        | Bool
        | Char
        | String
  '''
  p[0] = p[1].lower()

def p_SCOPE(p):
  '''
  SCOPE : local
        | global
  '''
  p[0] = p[1]

def p_ASIGNACION(p):
  '''
  ASIGNACION  : ID igual ASIGNACION_VALOR
              | SCOPE id igual ASIGNACION_VALOR
              | SCOPE id
  '''
  id, expression, scope, type = None, None, None, None

  if len(p)==4:
    id = p[1]
    expression = p[3]['expression']
    type = p[3]['type']
  else:
    scope = p[1]
    id = p[2]
    if len(p)==5:
      expression = p[4]['expression']
      type = p[4]['type']

  p[0] = Assignment(p.lexer.lineno, getColumn(p.lexer), id, expression, scope, type)

def p_ASIGNACION_VALOR(p):
  '''
  ASIGNACION_VALOR  : E
                    | E tipo TIPO
  '''
  expression, type = p[1], None
  if len(p)==4: type = p[3]

  p[0] = {'expression':expression, 'type':type}

def p_ID(p):
  '''
  ID  : ID punto id
      | ID corA E corB
      | id
  '''
  if len(p)>2:
    l, r = p[1], p[3]
    type = 'chain' if p[2]=='.' else 'access'

    expression = Expression(p.lexer.lineno, getColumn(p.lexer), False, type, l, r)
    p[0] = expression
  else: p[0] = p[1]

def p_FUNCION(p):
  '''
  FUNCION : function id parA PAR parB BLOQUE
          | function id parA parB BLOQUE
  '''
  id, parameters, types, instructions = p[2], [], [], p[5]

  if len(p)==7:
    parameters = p[4]['parameters']
    types = p[4]['types']
    instructions = p[6]

  p[0] = Function(p.lexer.lineno, getColumn(p.lexer), id, parameters, types, instructions)

def p_PAR(p):
  '''
  PAR : PAR coma P
      | P
  '''
  if len(p)==4:
    p[0] = p[1]
    parameter = p[3]
    p[0]['parameters'].append(parameter['id'])
    p[0]['types'].append(parameter['type'])
  else:
    parameter = p[1]
    p[0] = {'parameters':[parameter['id']], 'types':[parameter['type']]}

def p_P(p):
  '''
  P : id
    | id tipo TIPO
  '''
  type = p[3] if len(p)==4 else None
  p[0] = {'id':p[1], 'type':type}

def p_STRUCT(p):
  '''
  STRUCT  : struct id ATR end
          | mutable struct id ATR end
  '''
  mutable, id, attributes = False, p[2], p[3]

  if len(p)==6:
    mutable = True
    id = p[3]
    attributes = p[4]

  p[0] = Struct(p.lexer.lineno, getColumn(p.lexer), id, mutable, attributes)

def p_ATR(p):
  '''
  ATR : ATR A
      | A
  '''
  if len(p)==3:
    p[0] = p[1]
    p[0].append(p[2])
  else: p[0] = [p[1]]

def p_A(p):
  '''
  A : id tipo TIPO puntoycoma
    | id puntoycoma
  '''
  id, tipo = p[1], None

  if len(p)==5:
    tipo = p[3]

  p[0] = Attribute(p.lexer.lineno, getColumn(p.lexer), id, tipo)

def p_EXP(p):
  '''
  EXP : EXP coma E
      | E
  '''
  if len(p)==4:
    p[0] = p[1]
    p[0].append(p[3])
  else: p[0] = [p[1]]

def p_E(p):
  '''
  E : E mas E
    | E menos E
    | E asterisco E
    | E barra E
    | E caret E
    | E modulo E
    | menos E                     %prec op_negacion
    | E mayor E
    | E menor E
    | E mayor_igual E
    | E menor_igual E
    | E igualacion E
    | E diferenciacion E
    | E or E
    | E and E
    | not E
    | E interrog E dospuntos E  %prec op_ternaria
    | ID                        %prec op_acceso
    | parA E parB               %prec op_agrupacion
    | LLAMADA                   %prec op_llamada
    | RANGO                     %prec op_rango
    | ARREGLO
    | int64
    | float64
    | bool
    | char
    | STRING
    | Nothing
  '''
  if len(p)==2:
    p[0] = p[1]
    return

  if p[1]=='(':
    p[0] = p[2]
    return

  unary, l, r, expressionType = False, None, None, None

  if len(p)==6:
    unary = p[1]
    l = p[3]
    r = p[5]
    expressionType = 'ternary'
  elif len(p)==4:
    l = p[1]
    r = p[3]
    expressionType = operations[p[2]]
  else:
    unary = True
    l = p[2]
    expressionType = 'negacion' if p[1]=='-' else 'not'

  p[0] = Expression(p.lexer.lineno, getColumn(p.lexer), unary, expressionType, l, r)

def p_STRING(p):
  '''
  STRING  : STRING S
          | S
  '''
  if len(p)==3:
    p[0] = p[1]
    p[0].value.append(p[2])
  else:
    value = Value(p.lexer.lineno, getColumn(p.lexer), [p[1]], 'string')
    p[0] = value

def p_S(p):
  '''
  S : string
    | llaveA E llaveB
  '''
  p[0] = p[1] if len(p)==2 else p[2]

def p_ARREGLO(p):
  '''
  ARREGLO : corA EXP corB
          | corA corB
  '''
  value = []
  if len(p)==4: value = p[2]
  p[0] = Value(p.lexer.lineno, getColumn(p.lexer), value, 'array')

def p_LLAMADA(p):
  '''
  LLAMADA : id parA EXP parB
          | id parA parB
  '''
  id, expressions = p[1], []

  if len(p)==5:
    expressions = p[3]

  p[0] = Call(p.lexer.lineno, getColumn(p.lexer), id, expressions)

def p_IF(p):
  '''
  IF  : if E BLOQUE
      | if E BLOQUE_ABIERTO ELSE
      | if E BLOQUE_ABIERTO ELSEIF
  '''
  expression, instructions, elseif = p[2], p[3], None

  if len(p)==5:
    elseif = p[4]

  p[0] = If(p.lexer.lineno, getColumn(p.lexer), expression, instructions, elseif)

def p_ELSEIF(p):
  '''
  ELSEIF  : elseif E BLOQUE
          | elseif E BLOQUE_ABIERTO ELSEIF
          | elseif E BLOQUE_ABIERTO ELSE
  '''
  expression, instructions, elseif = p[2], p[3], None

  if len(p)==5:
    elseif = p[4]

  p[0] = If(p.lexer.lineno, getColumn(p.lexer), expression, instructions, elseif)

def p_ELSE(p):
  '''
  ELSE : else BLOQUE
  '''
  instructions = p[2]
  p[0] = Else(p.lexer.lineno, getColumn(p.lexer), instructions)

def p_WHILE(p):
  '''
  WHILE : while E BLOQUE
  '''
  expression, instructions = p[2], p[3]
  p[0] = While(p.lexer.lineno, getColumn(p.lexer), expression, instructions)

def p_FOR(p):
  '''
  FOR : for id in E BLOQUE
  '''
  id, expression, instructions = p[2], p[4], p[5]
  p[0] = For(p.lexer.lineno, getColumn(p.lexer), id, expression, instructions)

def p_RANGO(p):
  '''
  RANGO : E dospuntos E
        | dospuntos
  '''
  izq, der = None, None
  if len(p)==4:
    izq, der = p[1], p[3]
  p[0] = Expression(p.lexer.lineno, getColumn(p.lexer), False, 'range', izq, der)

def p_BREAK(p):
  '''
  BREAK : break
  '''
  p[0] = Break(p.lexer.lineno, getColumn(p.lexer))

def p_CONTINUE(p):
  '''
  CONTINUE : continue
  '''
  p[0] = Continue(p.lexer.lineno, getColumn(p.lexer))

def p_RETURN(p):
  '''
  RETURN  : return E
          | return
  '''
  expression = p[2] if len(p)==3 else None
  p[0] = Return(p.lexer.lineno, getColumn(p.lexer), expression)

def p_error(p):
  if p:
    if type(p.value) in [str, int, float, bool]: msg = "Sintaxis no válida cerca de '{}' ({})" .format(p.value, p.type)
    else: msg = "Sintáxis no válida en {}".format(p.type)
    error = SyntacticError(p.lineno, getColumn(p), msg)
  else:
    error = SyntacticError(0, 0, "Ninguna instrucción válida")

  errors.append(error)

lexer = lex()
parser = yacc()
