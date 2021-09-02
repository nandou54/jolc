import copy
from .analyzer import parse
from .core import Environment, SemanticError, getOutput, getErrors, getSymbols, envs, functions, loops, reset
from .core import RESERVED_FUNCTIONS, BINARY_OPERATIONS, UNARY_OPERATIONS, BINARY_OPERATION_RESULTS, UNARY_OPERATION_RESULTS
from .symbols import Expression, Value, Assignment, StructAssignment, ArrayAssignment, Function, Struct, Call, Access, If, Else, While, For, Return, Break, Continue
from .symbols import T_SENTENCE, EXECUTABLE_SENTENCE
from .helper import graphAST

def interpret(input):
  reset()
  globalEnv = Environment()
  envs.append(globalEnv)

  res = parse(input)
  INS = res['ast']

  for ins in INS:
    if type(ins) is Function: exFunction(ins, globalEnv)
  newINS = []
  for ins in INS:
    if type(ins) is not Function: newINS.append(ins)

  exInstructions(newINS, globalEnv)

  # res['ast'] = graphAST(res['ast'])
  res['output'] = getOutput()
  res['errors'] += getErrors()
  res['symbols'] = getSymbols()
  return res

def exInstructions(INS:T_SENTENCE, env:Environment):
  for ins in INS:
    if type(ins) in EXECUTABLE_SENTENCE:
      result = executables(ins, env)
      if not result: continue
      ins = result

    if type(ins) is Return:
      if len(functions)==0: return SemanticError(ins, 'Sentencia return fuera de una función')
      if ins.ex: ins.ex = exExpression(ins.ex, env)
    elif type(ins) is Break:
      if len(loops)==0: return SemanticError(ins, 'Sentencia break fuera de un ciclo')
    elif type(ins) is Continue:
      if len(loops)==0: return SemanticError(ins, 'Sentencia continue fuera de un ciclo')
    return ins
def exExpression(ex:Expression, env:Environment) -> Value:
  if type(ex) is Call: return exCall(ex, env)
  if type(ex) is Access: return exAccess(ex, env)
  if ex.type=='id':
    if len(ex.value)==1:
      id = env.getGlobalSymbol(ex.value[0].value)
      if not id: return SemanticError(ex, "No se ha declarado '{}'".format(ex.value[0].value))
      if id.type=='Nothing': return SemanticError(ex, "No se le asignó un valor a '{}'".format(ex.value[0].value))
      return id
    else:
      struct = env.getGlobalSymbol(ex.value[0].value)
      if not struct: return SemanticError(ex, "No se ha declarado '{}'".format(ex.value[0].value))

      attribute = None
      for i in range(1, len(ex.value)):
        if attribute: struct = attribute.value
        if type(struct.value) is not Struct: return SemanticError(ex, "La variable '{}' no es un struct".format(struct.value.id.value))
        attribute = struct.value.getAttribute(ex.value[i].value)
        if not attribute: return SemanticError(ex, "No existe el atributo '{}'".format(ex.value[i].value))
      return attribute.value
  if ex.type=='array':
    for i in range(len(ex.value)):
      newValue = exExpression(ex.value[i], env)
      if not newValue: return SemanticError(ex, "No se pudo crear el array")
      ex.value[i] = newValue
    return ex
  if type(ex) is Value: return ex

  l = exExpression(ex.left, env) if ex.left else None
  r = exExpression(ex.right, env) if ex.right else None

  if not l: return SemanticError(ex, "No se pudo realizar la operación '{}'".format(ex.type))

  unaryOperation = ex.type in UNARY_OPERATIONS.keys()

  if unaryOperation:
    try: returnType = UNARY_OPERATION_RESULTS[ex.type][l.type]
    except: return SemanticError(ex, "No se pudo aplicar '{}' a '{}' y '{}'".format(ex.type, l.type, r.type))
  else:
    if not r: return SemanticError(ex, "No se pudo realizar la operación '{}'".format(ex.type))

    if ex.type == 'rango':
      if l.type!='int64' or r.type!='int64': return SemanticError(ex, "Se esperaba un int64 en el rango")
      if l.value>=r.value: return SemanticError(ex, "El rango no es válido")

      ex.l = l
      ex.r = r
      return ex

    try: returnType = BINARY_OPERATION_RESULTS[ex.type][l.type][r.type]
    except: return SemanticError(ex, "No se pudo aplicar '{}' a '{}' y '{}'".format(ex.type, l.type, r.type))

  if unaryOperation: newValue = Value(ex.ln, ex.col, UNARY_OPERATIONS[ex.type](l), returnType)
  else: newValue = Value(ex.ln, ex.col, BINARY_OPERATIONS[ex.type](l, r), returnType)
  return newValue

def exAssignment(sen:Assignment, env:Environment):
  value = Value(sen.ln, sen.col, None, 'Nothing')
  targetEnv = env

  if sen.scope:
    if env.id=='global': return SemanticError(sen, "No se puede asignar un scope en el entorno global")
    if env.getLocalSymbol(sen.id.value): return SemanticError(sen, "Ya existe una variable '{}' en este entorno".format(sen.id.value))

    if sen.scope=='local':
      targetEnv.declareSymbol(sen.id.value, value)
    else:
      while True:
        targetEnv = env.parent
        if targetEnv.id=='global': break
      env.declareSymbol(sen.id.value, targetEnv.getLocalSymbol(sen.id.value))
  else:
    if env.getGlobalSymbol(sen.id.value):
      while True:
        if targetEnv.getLocalSymbol(sen.id.value): break
        targetEnv = env.parent

  if sen.ex:
    value = exExpression(sen.ex, env)
    if not value: return SemanticError(sen, 'No se pudo realizar la asignación')
    if sen.type and sen.type!=value.type: return SemanticError(sen, 'No se puede asignar un valor {} a una variable {}'.format(value.type, sen.type))

  targetEnv.declareSymbol(sen.id.value, value)

def exStructAssignment(sen:StructAssignment, env:Environment):
  struct = env.getGlobalSymbol(sen.id[0].value)
  if not struct: return SemanticError(sen, "No se ha declarado '{}'".format(sen.id[0].value))

  attribute = None
  for i in range(1, len(sen.id)):
    if attribute: struct = attribute.value
    if type(struct.value) is not Struct: return SemanticError(sen, "La variable '{}' no es un struct".format(sen.id[0].value))
    if not struct.value.mutable: return SemanticError(sen, "No se puede modificar el struct inmutable '{}'".format(struct.value.id.value))

    attribute = struct.value.getAttribute(sen.id[i].value)
    if not attribute: return SemanticError(sen, "No existe el atributo '{}'".format(sen.id[i].value))

    if i==len(sen.id)-1:
      ex = exExpression(sen.ex, env)
      if not ex: return SemanticError(sen, "No se pudo asignar el valor al struct")
      if attribute.type and attribute.type!=ex.type: "No se puede asignar un valor {} al atributo ({})".format(ex.type, attribute.type)

      attribute.value = ex

def exArrayAssignment(sen:ArrayAssignment, env:Environment):
  currentValue = env.getGlobalSymbol(sen.id.value)
  if not currentValue: return SemanticError(sen, "No se ha declarado el array '{}'".format(sen.id.value))

  for i in range(len(sen.index)):
    ex = sen.index[i]
    if currentValue.type!='array': return SemanticError(sen, "Se esperaba un array")

    index = exExpression(ex, env)
    if not index: return SemanticError(sen, "No se pudo acceder al array con el índice dado")
    if index.type!='int64': return SemanticError(sen, "Se esperaba un valor int64 para acceder al array '{}'".format(sen.id.value))
    if index.value<1 or index.value>len(currentValue.value): return SemanticError(sen, "No se pudo acceder al array '{}' ({}) en la posición {}".format(sen.id.value, len(currentValue.value), index.value))

    if i==len(sen.index)-1:
      newValue = exExpression(sen.ex, env)
      if not newValue: return SemanticError(sen, "No se pudo asignar el valor dado")
      currentValue.value[index.value-1] = newValue
    else:
      currentValue = currentValue.value[index.value-1]
      if not currentValue: return SemanticError(sen, "No se pudo acceder al array con el índice '{}'".format(index.value))

  return currentValue

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

def exCall(sen:Call, env:Environment):
  values = []

  for expression in sen.expressions:
    id = exExpression(expression, env)
    if not id: return SemanticError(sen, "No se pudo ejecutar la llamada de '{}'".format(sen.id.value))
    values.append(id)

  if sen.id.value in RESERVED_FUNCTIONS.keys():
    if not values: return SemanticError(sen, "No se pudo ejecutar la función '{}' con ningún parámetro".format(sen.id.value))

    return RESERVED_FUNCTIONS[sen.id.value](values)

  id = env.getGlobalSymbol(sen.id.value)
  if not id: return SemanticError(sen, "No se declaró '{}'".format(sen.id.value))
  if type(id) is Function:
    if len(values)!=len(id.parameters): return SemanticError(sen, "La función '{}' recibe {} parámetros".format(sen.id.value, len(id.parameters)))

    newEnv = Environment(env.id+"$"+sen.id.value, env)
    envs.append(newEnv)

    for i in range(len(id.parameters)):
      newEnv.declareSymbol(id.parameters[i].value, values[i])

    functions.append(sen.id.value)
    result = exInstructions(id.ins, newEnv)
    functions.pop()
    if type(result) is Return: return result.ex
    return result
  elif type(id) is Struct:
    if len(values)!=len(id.attributes): return SemanticError(sen, "El struct '{}' necesita {} atributos".format(sen.id.value, len(id.attributes)))

    struct = copy.deepcopy(id)
    for i in range(len(struct.attributes)):
      attribute = struct.attributes[i]
      if attribute.type and attribute.type!=values[i].type:
        return SemanticError(sen, "No se puede asignar un valor {} al atributo '{}' ({})".format(values[i].type, attribute.id.value, attribute.type))
      attribute.value = values[i]

    newValue = Value(sen.ln, sen.col, struct, struct.id.value)
    return newValue
  else: return SemanticError(sen, "No se puede llamar la variable '{}'".format(sen.id.value))

def exAccess(sen:Access, env:Environment):
  currentValue = env.getGlobalSymbol(sen.id.value)
  if not currentValue: return SemanticError(sen, "No se ha declarado el array '{}'".format(sen.id.value))

  for ex in sen.index:
    if currentValue.type!='array': return SemanticError(sen, "Se esperaba un array")

    index = exExpression(ex, env)
    if not index: return SemanticError(sen, "No se pudo acceder al array con el índice dado")
    if index.type not in ['int64', 'rango']: return SemanticError(sen, "Se esperaba un valor int64 o un rango para acceder al array '{}'".format(sen.id.value))
    if index.type=='int64':
      if index.value<1 or index.value>len(currentValue.value): return SemanticError(sen, "No se pudo acceder al array ({}) en la posición {}".format(len(currentValue.value), index.value))
      currentValue = currentValue.value[index.value-1]
      if not currentValue: return SemanticError(sen, "No se pudo acceder al array con el índice '{}'".format(index.value))
    else:
      if index.l.value<1 or index.r.value>len(currentValue.value):
        return SemanticError(sen, "No se pudo acceder al array ({}) con el rango {}:{}".format(len(currentValue.value), index.l.value, index.r.value))
      currentValue = copy.deepcopy(currentValue)
      currentValue.value = currentValue.value[index.l.value-1:index.r.value]

  return currentValue

def exIf(sen:If, env:Environment):
  condition = exExpression(sen.ex, env)
  if not condition: return SemanticError(sen, 'No se pudo ejecutar la sentencia if')
  if condition.type != 'bool': return SemanticError(sen, 'Se esperaba una condición en la sentencia if')

  newEnv = Environment(env.id + '#if({},{})'.format(sen.ln, sen.col), env)

  if condition.value: return exInstructions(sen.ins, newEnv)
  elif sen.elseif:
    if type(sen.elseif) is Else: return exInstructions(sen.elseif.ins, newEnv)
    else: return exIf(sen.elseif, env)

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

    if not result: continue

    if type(result) is Return:
      loops.pop()
      return result
    elif type(result) is Break:
      loops.pop()
      return
    elif type(result) is Continue: continue

def exFor(sen:For, env:Environment):
  loops.append('for')

  iterable = exExpression(sen.ex, env)
  if not iterable: return SemanticError(sen, 'No se pudo ejecutar la sentencia for')
  if iterable.type not in ['string', 'array', 'rango']: return SemanticError(sen, "No se puede iterar sobre un valor {}".format(iterable.type))

  if iterable.type=='rango':
    val = []
    for num in range(iterable.l.value, iterable.r.value+1):
      val.append(Value(iterable.ln, iterable.col, num, 'int64'))
    iterable = Value(iterable.ln, iterable.col, val, 'array')

  for value in iterable.value:
    newEnv = Environment(env.id+'#for({},{})'.format(sen.ln, sen.col), env)

    if iterable.type!='array':
      value = Value(sen.ln, sen.col, value, 'string')
    newEnv.declareSymbol(sen.id.value, value)
    result = exInstructions(sen.ins, newEnv)

    if not result: continue

    if type(result) is Return:
      loops.pop()
      return result
    elif type(result) is Break:
      loops.pop()
      return
    elif type(result) is Continue: continue

def executables(sen, env):
  T = type(sen)
  if T is Assignment: return exAssignment(sen, env)
  if T is StructAssignment: return exStructAssignment(sen, env)
  if T is ArrayAssignment: return exArrayAssignment(sen, env)
  if T is Function: return exFunction(sen, env)
  if T is Struct: return exStruct(sen, env)
  if T is Call: return exCall(sen, env)
  if T is Access: return exAccess(sen, env)
  if T is If: return exIf(sen, env)
  if T is While: return exWhile(sen, env)
  if T is For: return exFor(sen, env)
