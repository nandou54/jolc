
tokens  = (
  ''
)

# TOKENS
t_REVALUAR  = r'Evaluar'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_PTCOMA    = r';'

# IGNORED
t_ignore = "\w\t"


def t_newline(t):
  r'\n+'
  t.lexer.lineno += t.value.count("\n")

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

# LEXICAL ANALYZER
import ply.lex as lex
lexer = lex.lex()

# Precedence
precedence = (
  ('left','MAS','MENOS'),
  ('left','POR','DIVIDIDO'),
  ('right','UMENOS'),
  )

# Productions
def p_instrucciones_lista(t):
    '''instrucciones    : instruccion instrucciones
                        | instruccion '''

def p_instrucciones_evaluar(t):
    'instruccion : REVALUAR CORIZQ expresion CORDER PTCOMA'
    print('El valor de la expresión es: ' + str(t[3]))

def p_expresion_binaria(t):
  '''expresion : expresion MAS expresion
                | expresion MENOS expresion
                | expresion POR expresion
                | expresion DIVIDIDO expresion'''
  if t[2] == '+'  : t[0] = t[1] + t[3]
  elif t[2] == '-': t[0] = t[1] - t[3]
  elif t[2] == '*': t[0] = t[1] * t[3]
  elif t[2] == '/': t[0] = t[1] / t[3]

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = -t[2]

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_number(t):
    '''expresion    : ENTERO
                    | DECIMAL'''
    t[0] = t[1]

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()
