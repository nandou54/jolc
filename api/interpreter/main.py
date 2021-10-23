from copy import deepcopy
from traceback import print_exc

from api.analyzer.main import parse
from .grapher import graphAST
from api.symbols import Expression, Value, Assignment, Function, Struct, Call, If, Else, While, For, Return, Break, Continue
from api.symbols import T_SENTENCE, EXECUTABLE_SENTENCE

from .core import Environment, SemanticError, ApplicationError, getOutput, getErrors, getSymbols, envs, functions, loops, reset
from .core import RESERVED_FUNCTIONS, BINARY_OPERATIONS, UNARY_OPERATIONS, BINARY_OPERATION_RESULTS, UNARY_OPERATION_RESULTS

import sys
sys.setrecursionlimit(5000)
del sys

def interpret(input):
  reset()
  globalEnv = Environment()

  res = parse(input)
  INS = res['ast']

  for ins in INS:
    if type(ins) is Function: exFunction(ins, globalEnv)
  NEW_INS = [ins for ins in INS if type(ins) is not Function]

  try:
    exInstructions(NEW_INS, globalEnv)
  except:
    print_exc()
    ApplicationError('Error en la ejecución del código')

  try:
    res['ast'] = graphAST(res['ast'])
  except:
    print_exc()
    res['ast'] = graphAST([])
    ApplicationError('Error en la generación del dot')

  res['output'] = getOutput()
  res['symbols'] = getSymbols()
  res['errors'] += getErrors()
  return res

def exInstructions(INS:T_SENTENCE, env:Environment):
  for ins in INS:
    if type(ins) in EXECUTABLE_SENTENCE:
      result = execute(ins, env)
      if not result or type(result) is Value: continue
      ins = result

    if type(ins) is Return:
      if len(functions)==0:
        SemanticError(ins, 'Sentencia return fuera de una función')
        continue
      ins = deepcopy(ins)
      ins.ex = exExpression(ins.ex, env)
    if type(ins) is Break and len(loops)==0:
      SemanticError(ins, 'Sentencia break fuera de un ciclo')
      continue
    if type(ins) is Continue and len(loops)==0:
      SemanticError(ins, 'Sentencia continue fuera de un ciclo')
      continue
    return ins

def exExpression(ex:Expression, env:Environment) -> Value:
  if type(ex) is Call: return exCall(ex, env)
  if ex.type=='array':
    for i in range(len(ex.value)):
      newValue = exExpression(ex.value[i], env)
      if not newValue: return SemanticError(ex, "No se pudo crear el array")
      ex.value[i] = newValue
    return ex
  if ex.type=='access': return exAccess(ex, env)
  if ex.type=='chain': return exChain(ex, env)
  if ex.type=='range': return exRange(ex, env)
  if ex.type=='ternary': return exTernary(ex, env)
  if ex.type=='id': return exId(ex, env)
  if ex.type=='string': return exString(ex, env)
  if type(ex) is Value: return ex

  l = exExpression(ex.left, env) if ex.left else None
  r = exExpression(ex.right, env) if ex.right else None

  if not l: return SemanticError(ex, "No se pudo realizar la operación '{}'".format(ex.type))

  if ex.unary:
    try: returnType = UNARY_OPERATION_RESULTS[ex.type][l.type]
    except: return SemanticError(ex, "No se pudo aplicar '{}' a '{}' y '{}'".format(ex.type, l.type, r.type))
  else:
    if not r:
      if ex.type in ['or', 'and']: r = Value(ex.ln, ex.col, False, 'bool')
      else: return SemanticError(ex, "No se pudo realizar la operación '{}'".format(ex.type))
    if ex.type in ['igualacion', 'diferenciacion']: returnType = 'bool'
    else:
      try: returnType = BINARY_OPERATION_RESULTS[ex.type][l.type][r.type]
      except: return SemanticError(ex, "No se pudo aplicar '{}' a '{}' y '{}'".format(ex.type, l.type, r.type))

  if ex.unary: newValue = Value(ex.ln, ex.col, UNARY_OPERATIONS[ex.type](l), returnType)
  else: newValue = Value(ex.ln, ex.col, BINARY_OPERATIONS[ex.type](l, r), returnType)
  return newValue

def exString(ex, env:Environment):
  ex = deepcopy(ex)
  newValue = ''

  for val in ex.value:
    if type(val) is Value and type(val.value) is str: newValue+=val.value
    else:
      result = exExpression(val, env)
      if not result: return SemanticError(ex, 'No se pudo evaluar el string')

      result = RESERVED_FUNCTIONS['string']([result])
      newValue+=result.value

  ex.value = newValue
  return ex

def exId(ex, env:Environment):
  id = env.getGlobalSymbol(ex.value)
  if not id: return SemanticError(ex, "No se ha declarado '{}'".format(ex.value))
  if type(id) is Function:
    print("es funcion")
    return SemanticError(ex, 'Error al obtener una funcion')
  if type(id) is Struct: return SemanticError(ex, 'Error al obtener un struct')
  return id

def exCall(sen:Call, env:Environment):
  values = []

  for expression in sen.expressions:
    value = exExpression(expression, env)
    if not value: return SemanticError(sen, "No se pudo ejecutar la llamada de '{}'".format(sen.id.value))
    values.append(value)

  if sen.id.value in RESERVED_FUNCTIONS.keys():
    result = RESERVED_FUNCTIONS[sen.id.value](values)
    if not result: result = Value(sen.ln, sen.col, None, 'nothing')
    return result

  function = env.getGlobalSymbol(sen.id.value)
  if not function: return SemanticError(sen, "No se declaró '{}'".format(sen.id.value))
  if type(function) is Function:
    if len(values)!=len(function.parameters):
      return SemanticError(sen, "La función '{}' recibe {} parámetros".format(sen.id.value, len(function.parameters)))

    newEnv = Environment(env.id+"$"+sen.id.value, env)

    for i in range(len(function.parameters)):
      newEnv.declareSymbol(function.parameters[i].value, values[i])

    functions.append(sen.id.value)
    result = exInstructions(function.ins, newEnv)
    functions.pop()

    if not result: result = Return(sen.ln, sen.col, Value(sen.ln, sen.col, None, 'nothing'))
    return result.ex
  elif type(function) is Struct:
    if len(values)!=len(function.attributes): return SemanticError(sen, "El struct '{}' necesita {} atributos".format(sen.id.value, len(function.attributes)))

    struct = deepcopy(function)
    for i in range(len(struct.attributes)):
      attribute = struct.attributes[i]
      if attribute.type and attribute.type!=values[i].type:
        return SemanticError(sen, "No se puede asignar un valor {} al atributo '{}' ({})".format(values[i].type, attribute.id.value, attribute.type))
      attribute.value = values[i]
    return Value(sen.ln, sen.col, struct, struct.id.value)
  else: return SemanticError(sen, "No se puede llamar la variable '{}'".format(sen.id.value))

def exAccess(ex:Expression, env:Environment):
  expression = exExpression(ex.left, env)
  if not expression: return SemanticError(ex, "No se ha declarado el array")
  if expression.type not in ['string', 'array']: return SemanticError(ex, "Se esperaba un string o un array")

  index = exExpression(ex.right, env)
  if not index: return SemanticError(ex, "No se pudo acceder con el índice dado")
  if index.type not in ['int64', 'range']: return SemanticError(ex, "Se esperaba un valor int64 o un rango para acceder al array")

  if index.type=='int64':
    if index.value<1 or index.value>len(expression.value): return SemanticError(ex, "No se pudo acceder al array ({}) en la posición {}".format(len(expression.value), index.value))
    if expression.type=='string': expression.value = expression.value[index.value-1]
    else: expression = expression.value[index.value-1]
  else:
    expression = deepcopy(expression)
    if not index.left: return expression
    if index.left.value<1 or index.right.value>len(expression.value):
      return SemanticError(ex, "No se pudo acceder al array ({}) con el rango {}:{}".format(len(expression.value), index.left.value, index.right.value))
    expression.value = expression.value[index.left.value-1:index.right.value]

  return expression

def exChain(ex:Expression, env:Environment, assignment = False):
  struct = exExpression(ex.left, env)
  if not struct: return SemanticError(ex, "No se pudo acceder al atributo del struct")
  if type(struct.value) is not Struct: return SemanticError(ex, "Se esperaba un struct".format(struct.value.id.value))

  assignment = ex.unary
  if assignment and not struct.value.mutable: return SemanticError(ex, "No se puede modificar un struct inmutable")

  attribute = struct.value.getAttribute(ex.right.value)
  if not attribute: return SemanticError(ex, "No existe el atributo '{}'".format(ex.right.value))
  return attribute.value

def exRange(ex:Expression, env:Environment):
  if not ex.left: return ex

  l = exExpression(ex.left, env)
  r = exExpression(ex.right, env)

  if l.type!='int64' or r.type!='int64': return SemanticError(ex, "Se esperaba un int64 en el rango")
  if l.value>r.value: return SemanticError(ex, "El rango no es válido")

  ex.l, ex.r = l, r
  return ex

def exTernary(ex:Expression, env:Environment):
  condition = exExpression(ex.unary, env)
  if not condition: return SemanticError(ex, "No se pudo ejecutar la operación ternaria")
  if condition.type!='bool': return SemanticError(ex, "Se esperaba una condición")

  l = exExpression(ex.left, env)
  r = exExpression(ex.right, env)
  if condition.value:
    if not l: return SemanticError(ex, "No se pudo ejecutar la operación ternaria")
    return l
  else:
    if not r: return SemanticError(ex, "No se pudo ejecutar la operación ternaria")
    return r

def exAssignment(sen:Assignment, env:Environment):
  if sen.id.type=='id':
    value = Value(sen.ln, sen.col, None, 'nothing')
    targetEnv = env

    if sen.scope:
      if env.id=='global': return SemanticError(sen, "No se puede asignar un scope en el entorno global")
      if env.getLocalSymbol(sen.id.value): return SemanticError(sen, "Ya existe una variable '{}' en este entorno".format(sen.id.value))

      if sen.scope=='local':
        targetEnv.declareSymbol(sen.id.value, value)
      elif not env.getGlobalSymbol(sen.id.value): return SemanticError(sen, "No existe la variable '{}' en el entorno global".format(sen.id.value))
      else: targetEnv = env.getParentEnvById(sen.id.value)
      if not sen.ex: return
    elif env.getGlobalSymbol(sen.id.value):
      targetEnv = env.getParentEnvById(sen.id.value)

    if sen.ex:
      value = exExpression(sen.ex, env)
      if not value: return SemanticError(sen, 'No se pudo realizar la asignación')
      if sen.type and sen.type!=value.type: return SemanticError(sen, 'No se puede asignar un valor {} a una variable {}'.format(value.type, sen.type))
    targetEnv.declareSymbol(sen.id.value, deepcopy(value))
  else:
    inform(sen.id)
    id = exExpression(sen.id, env)
    if not id: return SemanticError(sen, 'No se pudo realizar la asignación')

    value = exExpression(sen.ex, env)
    if not value: return SemanticError(sen, 'No se pudo realizar la asignación')

    id.type = value.type
    id.value = value.value

def inform(ex):
  ex.unary = True
  if type(ex.left) is Expression: inform(ex.left)

def exFunction(sen:Function, env:Environment):
  if sen.id.value in RESERVED_FUNCTIONS.keys():
    return SemanticError(sen, "El id '{}' está reservado".format(sen.id.value))

  if env.id!='global':
    return SemanticError(sen, 'Solo se pueden declarar funciones en el entorno global')

  if env.getLocalSymbol(sen.id.value):
    return SemanticError(sen, "No se puede redeclarar '{}'".format(sen.id.value))

  env.declareSymbol(sen.id.value, sen)

def exStruct(sen:Struct, env:Environment):
  if sen.id.value in RESERVED_FUNCTIONS.keys():
    return SemanticError(sen, "El id '{}' está reservado".format(sen.id.value))

  if env.id!='global':
    return SemanticError(sen, 'Solo se pueden declarar struct en el entorno global')

  if env.getLocalSymbol(sen.id.value):
    return SemanticError(sen, "No se puede redeclarar '{}'".format(sen.id.value))

  env.declareSymbol(sen.id.value, sen)

def exIf(sen:If, env:Environment):
  condition = exExpression(sen.ex, env)
  if not condition: return SemanticError(sen, 'No se pudo ejecutar la sentencia if')
  if condition.type != 'bool': return SemanticError(sen, 'Se esperaba una condición en la sentencia if')

  newEnv = Environment(env.id + '#if({},{})'.format(sen.ln, sen.col), env)

  if condition.value: return exInstructions(sen.ins, newEnv)
  elif type(sen.elseif) is Else: return exInstructions(sen.elseif.ins, newEnv)
  elif type(sen.elseif) is If: return exIf(sen.elseif, env)

def exWhile(sen:While, env:Environment):
  loops.append('while')
  while True:
    condition = exExpression(sen.ex, env)

    if not condition:
      loops.pop()
      return SemanticError(sen, 'No se pudo ejecutar la sentencia while')

    if condition.type!='bool':
      loops.pop()
      return SemanticError(sen, 'Se esperaba una condición en la sentencia while')

    if not condition.value:
      loops.pop()
      return

    newEnv = Environment(env.id+'#while({},{})'.format(sen.ln, sen.col), env)
    result = exInstructions(sen.ins, newEnv)

    if type(result) is Return:
      loops.pop()
      return result
    elif type(result) is Break:
      loops.pop()
      return

def exFor(sen:For, env:Environment):
  iterable = exExpression(sen.ex, env)
  if not iterable: return SemanticError(sen, 'No se pudo ejecutar la sentencia for')
  if iterable.type not in ['string', 'array', 'range']: return SemanticError(sen, "No se puede iterar sobre un valor {}".format(iterable.type))

  if iterable.type=='range':
    if not iterable.left: return SemanticError(sen, "El rango del for no es válido")
    val = [
        Value(iterable.ln, iterable.col, num, 'int64')
        for num in range(iterable.l.value, iterable.r.value + 1)
    ]
    iterable = Value(iterable.ln, iterable.col, val, 'array')

  loops.append('for')
  for value in iterable.value:
    if iterable.type!='array': value = Value(sen.ln, sen.col, value, 'string')

    newEnv = Environment(env.id+'#for({},{})'.format(sen.ln, sen.col), env)
    newEnv.declareSymbol(sen.id.value, value)
    result = exInstructions(sen.ins, newEnv)

    if type(result) is Return:
      loops.pop()
      return result
    elif type(result) is Break:
      loops.pop()
      return

  loops.pop()

def execute(sen, env):
  T = type(sen)
  if T is Assignment: return exAssignment(sen, env)
  if T is Function: return exFunction(sen, env)
  if T is Struct: return exStruct(sen, env)
  if T is Call: return exCall(sen, env)
  if T is If: return exIf(sen, env)
  if T is While: return exWhile(sen, env)
  if T is For: return exFor(sen, env)
