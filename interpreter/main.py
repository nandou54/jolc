from .core import *
from .analyzer import parse
from .symbols import SemanticError


def interpret(input):
  global errors, output, symbols
  global functions, loops, envs, globalEnv

  errors.clear()
  output.clear()
  symbols.clear()

  functions.clear()
  loops.clear()
  envs.clear()

  globalEnv = Environment()
  envs.append(globalEnv)

  res = parse(input)
  INS = res['ast'].copy()
  errors = res['errors']

  for instruction in INS:
    if instruction['i_type']=='function': exFunction(instruction, globalEnv)

  INS = list(filter(lambda instruction: instruction['i_type'!='function']), INS)

  exInstructions(INS, globalEnv)

  res['errors'] = errors
  res['output'] = output
  res['symbols'] = symbols

  return res


def exInstructions(instrucciones, env:Environment):
  for instruccion in instrucciones:
    if instruccion['i'] in executables.keys():
      res = executables[instruccion['i']](instruccion, env)

def exExpression(ins, env:Environment):
  pass

def exAssignment(ins, env:Environment):
  if env.getLocalSymbol(ins['id']): return print('La variable %s ya ha sido declarada', )

  value = None

  if ins['expresion'] != None:
    pass

def exFunction(ins, env:Environment):
  if ins['id'] in RESERVED_FUNCTIONS:
    return SemanticError(ins, 'Semántico')

def exStruct(ins, env:Environment):
  pass

def exCall(ins, env:Environment):
  pass

def exAccess(ins, env:Environment):
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

executables = {
  'asignacion':exAssignment,
  'funcion':exFunction,
  'struct':exStruct,
  'llamada':exCall,
  'acceso':exAccess,
  'if':exIf,
  'else':exElse,
  'while':exWhile, 
  'for':exFor,
  'break':exBreak,
  'continue':exContinue,
  'return':exReturn
}
