from interpreter.analyzer import parse
from interpreter.core import *


def interpret(input):
  output.clear()
  errors.clear()
  symbols.clear()

  res = parse(input)

  return res


def exInstrucciones(instrucciones, env:Environment):
  for instruccion in instrucciones:
    if instruccion['i'] in ejecutables.keys():
      res = ejecutables[instruccion['i']](instruccion, env)

def exExpresion(ins, env:Environment):
  pass

def exAsignacion(ins, env:Environment):
  if env.getLocalSymbol(ins['id']): return print('La variable %s ya ha sido declarada', )

  value = None

  if ins['expresion'] != None:
    pass


def exFuncion(ins, env:Environment):
  pass

def exStruct(ins, env:Environment):
  pass

def exLlamada(ins, env:Environment):
  pass

def exAcceso(ins, env:Environment):
  pass

def exIf(ins, env:Environment):
  pass

def exElse(ins, env:Environment):
  pass

def exWhile(ins, env:Environment):
  pass

def exFor(ins, env:Environment):
  pass

def exBreak(env:Environment):
  pass

def exContinue(env:Environment):
  pass

def exReturn(_return, env:Environment):
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
