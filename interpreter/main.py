from interpreter.analyzer import parse
from interpreter.core import *

output:list = []
errores:list = []
simbolos:list = []

entorno_global = Entorno()


def interpret(input):
  res = parse(input)

  return res

INPUT = '''
x = 9;
'''

def exInstrucciones(instrucciones, env):
  for instruccion in instrucciones:
    if instruccion['i'] in ejecutables.keys():
      res = ejecutables[instruccion['i']](instruccion, env)

def exExpresion(_expresion, env):
  pass

def exAsignacion(_asignacion, env):
  pass

def exFuncion(_funcion, env):
  pass

def exStruct(_struct, env):
  pass

def exLlamada(_llamada, env):
  pass

def exAcceso(_acceso, env):
  pass

def exIf(_if, env):
  pass

def exElse(_else, env):
  pass

def exWhile(_while, env):
  pass

def exFor(_for, env):
  pass

def exBreak(env):
  pass

def exContinue(env):
  pass

def exReturn(_return, env):
  pass


ejecutables = {
  'asignacion':exAsignacion,
  'funcion':exFuncion,
  'struct':exStruct,
  'llamada':exLlamada,
  'acceso':exAcceso,
  'if':exIf,
  'else':exElse,
  'while':exWhile, 
  'for':exFor,
  'break':exBreak,
  'continue':exContinue,
  'return':exReturn
}

# result = interpret(INPUT)
# print(result['ast'])
