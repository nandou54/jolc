from .analyzer import parse
from .core import Environment, SemanticError, getOutput, getErrors, getSymbols, envs, functions, loops, reset
from .core import RESERVED_FUNCTIONS, OPERATIONS, BINARY_OPERATION_RESULTS, UNARY_OPERATION_RESULTS
from .symbols import Expression, Value, Assignment, StructAssignment, ArrayAssignment, Function, Struct, Call, Access, If, Else, While, For, Return, Break, Continue
from .symbols import T_SENTENCE, EXECUTABLE_SENTENCE

def interpret(input):
  reset()
  globalEnv = Environment()
  envs.append(globalEnv)

  res = parse(input)
  INS = res['ast'].copy()

  for ins in INS:
    if type(ins) is Function: exFunction(ins, globalEnv)

  INS = list(filter(lambda instruction: type(ins) is not Function, INS))

  exInstructions(INS, globalEnv)

  res['output'] = getOutput()
  res['errors'].append(getErrors())
  res['symbols'] = getSymbols()
  return res

def exInstructions(INS:T_SENTENCE, env:Environment):
  for ins in INS:
    if type(ins) in EXECUTABLE_SENTENCE:
      fun = executables(type(ins))
      result = fun(ins, env)
      if not result: continue
      ins = result

    if type(ins) is Return:
      if len(functions)==0: return SemanticError(ins, 'Sentencia return fuera de una función')
      if ins.ex: ins.ex = exExpression(ins.ex, env)
      return ins

    elif type(ins) is Break:
      if len(loops)>0:
        return ins
      SemanticError(ins, 'Sentencia break fuera de un ciclo')
    elif type(ins) is Continue:
      if len(loops)>0:
        return ins
      SemanticError(ins, 'Sentencia continue fuera de un ciclo')

def exExpression(ex:Expression, env:Environment) -> Value:
  if type(ex) is Call: return exCall(ex, env)
  if type(ex) is Access: return exAccess(ex, env)
  if ex.type=='id':
    id = env.getGlobalSymbol(ex.value)
    return id if id else SemanticError(ex, "No se ha declarado '{}'".format(ex.value))
  if ex.type=='array':
    for i in range(len(ex.value)):
      newValue = exExpression(ex.value[i], env)
      if not newValue: return SemanticError(ex, "No se pudo crear el arreglo")
      ex.value[i] = newValue
    return ex
  if type(ex) is Value: return ex

  l = exExpression(ex.left, env) if ex.left else None
  r = exExpression(ex.right, env) if ex.right else None

  if not l: return SemanticError(ex, "No se pudo realizar la operación '{}'".format(ex.type))

  if ex.type == 'rango': return ex
  elif ex.type in BINARY_OPERATION_RESULTS.keys():
    if not r: return SemanticError(ex, "No se pudo realizar la operación '{}'".format(ex.type))
    returnType = BINARY_OPERATION_RESULTS[ex.type][l.type][r.type]
  else:
    returnType = UNARY_OPERATION_RESULTS[ex.type][l.type]

  if not returnType: return SemanticError(ex, "No se pudo aplicar '{}' a '{}' y '{}'".format(ex.type, l.type, r.type))

  newValue = Value(ex.ln, ex.col, OPERATIONS[ex.type](l, r), returnType)
  return newValue

def exAssignment(sen:Assignment, env:Environment):
  value = None

  if sen.scope:
    if sen.scope=='local':
      pass
    else:
      pass
      # original = env.getGlobalSymbol()

  if sen.ex:
    value = exExpression(sen.ex, env)

    if not value: return SemanticError(sen, 'No se pudo realizar la asignación')

    if sen.type and sen.type!=value.type: return SemanticError(sen, 'No se puede asignar un valor {} a una variable {}'.format(value.type, sen.type))

  env.declareSymbol(sen.id.value, value)

def exStructAssignment(sen:StructAssignment, env:Environment):
  pass

def exArrayAssignment(sen:ArrayAssignment, env:Environment):
  pass

def exFunction(sen:Function, env:Environment):
  if sen.id.value in RESERVED_FUNCTIONS.keys():
    return SemanticError(sen, 'El id ({}) de la función está reservado'.format(sen.id.value))

  if env.id!='global':
    return SemanticError(sen, 'Solo se pueden declarar funciones en el entorno global')

  if env.getGlobalSymbol(sen.id.value):
    return SemanticError(sen, 'La función {} ya ha sido declarada'.format(sen.id.value))

  env.declareSymbol(sen.id.value, sen)

def exStruct(sen:Struct, env:Environment):
  pass

def exCall(sen:Call, env:Environment):
  values = []

  for expression in sen.expressions:
    value = exExpression(expression, env)
    if not value: return SemanticError(sen, "No se pudo ejecutar la llamada de '{}'".format(sen.id.value))
    values.append(value)

  if sen.id.value in RESERVED_FUNCTIONS.keys():
    if not values: return SemanticError(sen, "No se pudo ejecutar la función '{}' con ningún parámetro".format(sen.id.value))

    return RESERVED_FUNCTIONS[sen.id.value](values)

  function = env.getGlobalSymbol(sen.id.value)
  if not function: return SemanticError(sen, "No se encontró la función '{}'".format(sen.id.value))

  if len(values)!=len(function.parameters): return SemanticError(sen, "La función '{}' recibe {} parámetros".format(sen.id.value, len(function.parameters)))

  newEnv = Environment(env.id+"$"+sen.id.value, env)
  envs.append(newEnv)
  functions.append(sen.id.value)

  result = exInstructions(function.ins, newEnv)
  functions.pop()
  return result

def exAccess(sen:Access, env:Environment):
  array = env.getGlobalSymbol(sen.id.value)
  if not array: return SemanticError(sen, "No se ha declarado la lista '{}'".format(sen.id.value))

  index = exExpression(sen.expression, env)
  if not index: return SemanticError(sen, "No se pudo acceder a la lista '{}'".format(sen.id.value))

  if index.type!='int64': return SemanticError(sen, "Se esperaba un valor int64 para acceder a la lista '{}'".format(sen.id.value))

  if index.value<1 or index.value>len(array.value): return SemanticError(sen, "No se pudo acceder a la lista '{}' ({}) en la posición {}".format(sen.id.value, len(sen.value), index.value))

  return array.value[index.value-1]

def exIf(sen:If, env:Environment):
  condition = exExpression(sen.ex, env)

  if not condition: return SemanticError(sen, 'No se pudo ejecutar la sentencia if')

  if condition.type != 'Bool': return SemanticError(sen, 'Se esperaba una condición en la sentencia if')

  newEnv = Environment(env.id + '#if({},{})'.format(sen.ln, sen.col), env)

  if condition.value: return exInstructions(sen.ins, newEnv)
  elif sen.elseif:
    if type(sen.elseif) is Else: return exInstructions(sen.elseif.ins, newEnv)
    else: return exIf(sen.elseif, env)

def exWhile(sen:While, env:Environment):
  loops.append('while')

  while True:
    condition = exExpression(sen.expression, env)

    if not condition:
      loops.pop()
      return SemanticError(sen, 'No se pudo ejecutar la sentencia while')

    if condition.type!='Bool':
      loops.pop()
      return SemanticError(sen, 'Se esperaba una condición en la sentencia while')

    if not condition.value:
      loops.pop()
      return

    newEnv = Environment(env.id+'#while({},{})'.format(sen.ln, sen.col), env)

    result = exInstructions(sen.ins, newEnv)

    if not result: continue

    if type(result) is Return:
      loops.pop()
      return result
    elif type(result) is Break:
      loops.pop()
      return
    elif type(result) is Continue: continue

# TODO: for loop
def exFor(ins:For, env:Environment):
  pass

def executables(T):
  if T is Assignment: return exAssignment
  if T is StructAssignment: return exStructAssignment
  if T is ArrayAssignment: return exArrayAssignment
  if T is Function: return exFunction
  if T is Struct: return exStruct
  if T is Call: return exCall
  if T is Access: return exAccess
  if T is If: return exIf
  if T is While: return exWhile
  if T is For: return exFor
