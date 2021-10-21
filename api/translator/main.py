import copy
from ..analyzer import parse
from ..symbols import Expression, Value, Assignment, Function, Struct, Call, If, Else, While, For, Return, Break, Continue
from ..symbols import T_SENTENCE, EXECUTABLE_SENTENCE

# from .core import, SemanticError, ApplicationError, getOutput, getErrors, getSymbols, envs, functions, loops, reset
# from .core import RESERVED_FUNCTIONS, BINARY_OPERATIONS, UNARY_OPERATIONS, BINARY_OPERATION_RESULTS, UNARY_OPERATION_RESULTS

def translate(input):
  # reset()

  res = parse(input)
  INS = res['ast']

  import traceback
  try:
    exInstructions(INS, None)
  except:
    traceback.print_exc()
    # ApplicationError('Error en la ejecución del código')

  # res['output'] = getOutput()
  return res

def exInstructions(INS:T_SENTENCE, env):
  for ins in INS:
    if type(ins) in EXECUTABLE_SENTENCE:
      result = execute(ins, env)
      if not result or type(result) is Value: continue
      ins = result

    if type(ins) is Return:
      ins = copy.deepcopy(ins)
      ins.ex = exExpression(ins.ex, env)

    return ins

def exExpression(ex:Expression, env):
  pass

def exString(ex, env):
  pass

def exId(ex, env):
  pass

def exCall(sen:Call, env):
  pass

def exAccess(ex:Expression, env):
  pass

def exChain(ex:Expression, env, assignment = False):
  pass

def exRange(ex:Expression, env):
  pass

def exTernary(ex:Expression, env):
  pass

def exAssignment(sen:Assignment, env):
  pass

def exFunction(sen:Function, env):
  pass

def exStruct(sen:Struct, env):
  pass

def exIf(sen:If, env):
  pass

def exWhile(sen:While, env):
  pass

def exFor(sen:For, env):
  pass

def execute(sen, env):
  T = type(sen)
  if T is Assignment: return exAssignment(sen, env)
  if T is Function: return exFunction(sen, env)
  if T is Struct: return exStruct(sen, env)
  if T is Call: return exCall(sen, env)
  if T is If: return exIf(sen, env)
  if T is While: return exWhile(sen, env)
  if T is For: return exFor(sen, env)
