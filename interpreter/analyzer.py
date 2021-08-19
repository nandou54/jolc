from interpreter.symbols import *

tokens = (
  'id',
  'parentesis_A',
  'parentesis_B',
  'corchete_A',
  'corchete_B',
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
  'puntoycoma',
  # reservadas
  'nothing',
  'tipo_int64',
  'tipo_float64',
  'tipo_bool',
  'tipo_char',
  'tipo_string',
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

t_parentesis_A   = r'\('
t_parentesis_B   = r'\)'
t_corchete_A     = r'\['
t_corchete_B     = r'\]'
t_id             = r'[a-zA-Z_][a-zA-Z_0-9]*'
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
t_dospuntos      = r':'
t_puntoycoma     = r';'
t_tipo_int64     = r'Int64'
t_tipo_float64   = r'Float64'
t_tipo_bool      = r'Bool'
t_tipo_char      = r'Char'
t_tipo_string    = r'String'
t_struct         = r'struct'
t_local          = r'local'
t_global         = r'global'
t_function       = r'function'
t_end            = r'end'
t_if             = r'if'
t_elseif         = r'elseif'
t_else           = r'else'
t_while          = r'while'
t_for            = r'for'
t_break          = r'break'
t_continue       = r'continue'
t_return         = r'return'
t_mutable        = r'mutable'
t_in             = r'in'

def t_comentario(t):
    r'\#.*'

def t_comentario_multilinea(t):
     r'\#=([^=]|[\r\n]|(=+([^#])))*=+\#'

def t_nothing(t):
    r'Nothing'
    valor, tipo = None, 'nothing'

    t.value = Expresion(False, False, valor, None, tipo)
    return t

def t_int64(t):
    r'\d+'
    valor, tipo = 0, 'int64'

    try:
        valor = int(t.value)
    except ValueError:
        print("Int64 value too big: %d", t.value)

    t.value = Expresion(False, False, valor, None, tipo)
    return t

def t_float64(t):
    r'\d+\.\d+'
    valor, tipo = 0, 'float64'

    try:
        valor = float(t.value)
    except ValueError:
        print("Float64 value too big: %d", t.value)

    t.value = Expresion(False, False, valor, None, tipo)
    return t

def t_bool(t):
    r'(true)|(false)'
    valor, tipo = bool(t.value), 'bool'

    t.value = Expresion(False, False, valor, None, tipo)
    return t

def t_char(t):
    r'\'[a-zA-Z0-9]\''
    valor, tipo = t.value[1], 'char'

    t.value = Expresion(False, False, valor, None, tipo)
    return t

def t_string(t):
    r'"[a-zA-Z0-9]*"'
    valor, tipo = t.value[1:-1], 'string'

    t.value = Expresion(False, False, valor, None, tipo)
    return t


# Caracteres ignorados
t_ignore = "\t "

def t_newline(t):
  r'\n+'
  t.lexer.lineno += t.value.count("\n")

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)


# Analizador léxico
from interpreter.ply.lex import lex
lexer = lex()


# Precedencia de más a menos
precedence = (
  ('nonassoc','op_agrupacion'),
  ('left','op_acceso_arreglo'),
  ('left','op_llamada'),
  ('right','op_negacion','not'),
  ('right','caret'),
  ('left','asterisco','barra','modulo'),
  ('left','mas','menos'),
  ('left','menor','menor_igual','mayor','mayor_igual'),
  ('left','igualacion','diferenciacion'),
  ('left','and'),
  ('left','or')
)


# Producciones
def p_INS(p):
    '''
    INS : INS I puntoycoma
        | I puntoycoma
    '''
    if len(p)==4:
        p[0] = p[1]
        p[0].insert(p[2], -1)
    else: p[0] = [p[1]]
    print(p)

def p_I(p):
    '''
    I   : ASIGNACION
        | FUNCION
        | STRUCT
        | LLAMADA
        | IF
        | WHILE
        | FOR
        | BREAK
        | CONTINUE
        | RETURN
        | error puntoycoma
    '''
    p[0] = p[1]

def p_BLOQUE(p):
    '''
    BLOQUE  : INS end
            | end
    '''
    p[0] = None if p[1]=='end' else p[1]

def p_TIPO(p):
    '''
    TIPO    : tipo_int64
            | tipo_float64
            | tipo_bool
            | tipo_char
            | tipo_string
    '''
    p[0] = p[1]

def p_ASIGNACION(p):
    '''
    ASIGNACION  : ID igual ASIGNACION_VALOR
                | global id igual ASIGNACION_VALOR
                | global id
                | local id igual ASIGNACION_VALOR
                | local id
    '''
    scope, id, expresion, tipo = None, None, None, None

    if p[1] in ['global', 'local']:
        scope = p[1]
        id = [p[2]]
        if len(p) > 3:
            expresion = p[4]['expresion']
            tipo = p[4]['tipo']
    else:
        id = p[1]
        expresion = p[3]['expresion']
        tipo = p[3]['tipo']

    p[0] = Asignacion(scope, id, expresion, tipo)

def p_ASIGNACION_VALOR(p):
    '''
    ASIGNACION_VALOR    : E
                        | E tipo TIPO
    '''
    expresion, tipo = p[1], None

    if len(p)>2: 
        tipo = p[3]

    p[0] = {'expresion':expresion, 'tipo':tipo}

def p_FUNCION(p):
    '''
    FUNCION : function id parentesis_A PAR parentesis_B BLOQUE
            | function id parentesis_A parentesis_B BLOQUE
    '''
    id, parametros = p [2], []

    if len(p) == 7:
        parametros = p[5]

    p[0] = Funcion(id, parametros)

def p_PAR(p):
    '''
    PAR : PAR coma P
        | P
    '''
    if len(p)==4:
        p[0] = p[1]
        p[0].insert(p[3], -1)
    else: p[0] = [p[1]]

def p_P(p):
    '''
    P : id
    '''
    p[0] = p[1]

def p_STRUCT(p):
    '''
    STRUCT  : struct id ATR end
            | mutable struct id ATR end
    '''
    mutable, id, atributos = False, p[2], p[3]

    if len(p)>5:
        id = p[3]
        atributos = p[4]

    p[0] = Struct(mutable, id, atributos)

def p_ATR(p):
    '''
    ATR : ATR A
        | A
    '''
    if len(p)==4:
        p[0] = p[1]
        p[0].insert(p[2], -1)
    else: p[0] = [p[1]]

def p_A(p):
    '''
    A   : id tipo TIPO puntoycoma
        | id puntoycoma
    '''
    id, tipo = p[1], None

    if len(p)>3:
        tipo = p[2]

    p[0] = Atributo((id, tipo))

def p_EXP(p):
    '''
    EXP : EXP coma E
        | E
    '''
    if len(p)==4:
        p[0] = p[1]
        p[0].insert(p[2], -1)
    else: p[0] = [p[1]]

def p_E(p):
    '''
    E   : E mas E
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
        | parentesis_A E parentesis_B %prec op_agrupacion
        | LLAMADA                     %prec op_llamada
        | ACCESO_ARREGLO              %prec op_acceso_arreglo
        | ARREGLO
        | ID
        | int64
        | float64
        | bool
        | char
        | string
        | nothing
    '''
    if len(p)==2:
        p[0] = p[1]
        return

    if p[1]=='(':
        p[0] = p[2]
        return

    operable, unaria, izq, der, tipo = True, False, None, None, None

    if len(p)>3:
        izq = p[1]
        der = p[3]
        tipo = operaciones[p[2]]
    else:
        unaria = True
        izq = p[2]
        tipo = operaciones[p[1]]

    p[0] = Expresion(operable, unaria, izq, der, tipo)

def p_ARREGLO(p):
    '''
    ARREGLO : corchete_A EXP corchete_B
            | corchete_A corchete_B
    '''
    izq = p[2]
    p[0] = Expresion(False, False, izq, None, 'array' )

def p_LLAMADA(p):
    '''
    LLAMADA : id parentesis_A EXP parentesis_B
            | id parentesis_A parentesis_B
    '''
    id, expresiones = p[1], []

    if len(p)==5:
        expresiones = p[3]

    p[0] = Llamada(id, expresiones)

def p_ACCESO_ARREGLO(p):
    '''
    ACCESO_ARREGLO : id corchete_A E corchete_B
    '''
    id, expresion = p[1], p[3]
    p[0] = Acceso_arreglo(id, expresion)

def p_ID(p):
    '''
    ID : ID punto id
        | id
    '''
    if len(p)==4:
        p[0] = p[1]
        p[0].insert(p[3], -1)
    else: p[0] = [p[1]]

def p_IF(p):
    '''
    IF : if E BLOQUE
        | if E BLOQUE ELSEIF
        | if E BLOQUE ELSE
    '''
    expresion, instrucciones, elseif = p[2], p[3], None

    if len(p)==5:
        elseif = p[4]

    p[0] = If(expresion, instrucciones, elseif)

def p_ELSEIF(p):
    '''
    ELSEIF  : elseif E BLOQUE
            | elseif E BLOQUE ELSEIF
            | elseif E BLOQUE ELSE
    '''
    expresion, instrucciones, elseif = p[2], p[3], None

    if len(p)==5:
        elseif = p[4]

    p[0] = If(expresion, instrucciones, elseif)

def p_ELSE(p):
    '''
    ELSE : else BLOQUE
    '''
    instrucciones = p[2]
    p[0] = Else(instrucciones)

def p_WHILE(p):
    '''
    WHILE : while E BLOQUE
    '''
    expresion, instrucciones = p[2], p[3]
    p[0] = While(expresion, instrucciones)

def p_FOR(p):
    '''
    FOR : for id in E BLOQUE
        | for id in RANGO BLOQUE
    '''
    id, expresion, instrucciones = p[2], p[4], p[5]
    p[0] = For(id, expresion, instrucciones)

def p_RANGO(p):
    '''
    RANGO : E dospuntos E
    '''
    izq, der = p[1], p[3]
    p[0] = Expresion(False, False, izq, der, 'rango')

def p_BREAK(p):
    '''
    BREAK : break
    '''
    p[0] = Break()

def p_CONTINUE(p):
    '''
    CONTINUE : continue
    '''
    p[0] = Continue()

def p_RETURN(p):
    '''
    RETURN  : return E
            | return
    '''
    expresion = None

    if len(p)==3:
        expresion = p[2]

    p[0] = Return(expresion)

def p_error(p):
    print("Error sintáctico en ''")
    print(p)

from interpreter.ply.yacc import yacc
parser = yacc()

# TODO: array de errores (linea, columna, tipo, descripcion)
errores:list = [] 

def parse(input):
    ast = parser.parse(input)
    return {'ast':ast, 'simbolos':[], 'errores':errores, 'output':[]}


# f = open("api\input.txt", "r")
# input = f.read()
# result = parser.parse(input)
