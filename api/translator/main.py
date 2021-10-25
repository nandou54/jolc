from traceback import print_exc

from api.analyzer.main import parse
from api.symbols import Expression, Value, Assignment, Function, Struct, Call, If, Else, While, For, Return, Break, Continue
from api.symbols import T_SENTENCE, EXECUTABLE_SENTENCE

from .core import RESERVED_FUNCTIONS, Environment, SemanticError, addFunction, addTemp, getEnv, getFunction, getOutput, getTemps, BINARY_OPERATIONS, UNARY_OPERATIONS
from .core import reset, Label, Temp, ApplicationError
# from .core import RESERVED_FUNCTIONS, BINARY_OPERATIONS, UNARY_OPERATIONS, BINARY_OPERATION_RESULTS, UNARY_OPERATION_RESULTS

def translate(input):
  reset()
  mainEnv = Environment('main')

  res = parse(input)
  INS = res['ast']

  output = getOutput()

  try:
    NEW_INS = [ins for ins in INS if type(ins) is not Function]
    func_output = '\n\n'.join(trFunction(ins, mainEnv) for ins in INS if type(ins) is Function)
    ins_output = trInstructions(NEW_INS, mainEnv)

    output += getTemps()
    output += 'func main(){\n'
    output += ins_output
    output += '}\n\n'
    output += func_output

  except:
    print_exc()
    ApplicationError('Error en la traducción a C3D')

  res['output'] = output
  return res

def trInstructions(INS:T_SENTENCE, env:Environment):
  return '\n'.join(execute(ins, env) for ins in INS)

def trExpression(ex:Expression, env:Environment):
  if type(ex) is Call: return trCall(ex, env)
  if ex.type=='array':
    # for i in range(len(ex.value)):
    #   newValue = exExpression(ex.value[i])
    #   if not newValue: return SemanticError(ex, "No se pudo crear el array")
    #   ex.value[i] = newValue
    return ex
  if ex.type=='access': return trAccess(ex, env)
  if ex.type=='chain': return trChain(ex, env)
  if ex.type=='range': return trRange(ex, env)
  if ex.type=='ternary': return trTernary(ex, env)
  if ex.type=='id':
    if env.getSymbolPosition(ex.value) is None:
      return SemanticError(ex, f"No se declaró '{ex.value}'")

    pos_temp = Temp()
    val_temp = Temp()

    s = f'{pos_temp}=p+{env.getSymbolPosition(ex.value)} // posicion de variable {ex.value}\n'
    s += f'{val_temp}=stack[int({pos_temp})] // valor de variable {ex.value}\n'

    val_temp.output = s
    return val_temp

    # return trId(ex, env)
  if ex.type=='string': return trString(ex, env)
  if type(ex) is Value: return Temp(ex.value)

  left_temp = trExpression(ex.left, env) if ex.left else None
  right_temp = trExpression(ex.right, env) if ex.right else None

  return (UNARY_OPERATIONS[ex.type](left_temp)
         if ex.unary
         else BINARY_OPERATIONS[ex.type](left_temp, right_temp))

def trString(ex, env:Environment):
  s = ''

def trId(ex, env:Environment):
  s = ''

def trCall(sen:Call, env:Environment):
  s = ''
  values = []

  for expression in sen.expressions:
    tempBase = trExpression(expression, env)
    if not tempBase:
      return SemanticError(sen, f"No se pudo realizar la llamda a '{sen.id}'")
    values.append(tempBase)

  if sen.id.value in RESERVED_FUNCTIONS.keys():
    for value in values:
      s += value.output
    s += RESERVED_FUNCTIONS[sen.id.value](values)
    return s

  function = getFunction(sen.id.value)
  if not function: return SemanticError(sen, f"No se declaró '{sen.id.value}'")
  if type(function) is Function:
    if len(values)!=len(function.parameters):
      return SemanticError(sen, f"La función '{sen.id.value}' recibe {len(function.parameters)} parámetros")

    newEnv = getEnv(sen.id.value)

    tempBase = Temp()
    s += f'{tempBase}=p+{newEnv.base-env.base} // base de la nueva funcion\n'
    for i in range(len(function.parameters)):
      temp = Temp()
      parameter = function.parameters[i]

      s += f'{temp}={tempBase}+{env.getSymbolPosition(parameter)} // posicion de parametro {parameter}\n'
      s += values[i].output
      s += f'stack[int({temp})] // asignacion de parametro {parameter}\n'

    s += f'{sen.id.value}()\n'
    return s

def trAccess(ex:Expression, env:Environment):
  s = ''

def trChain(ex:Expression, output, assignment = False):
  s = ''

def trRange(ex:Expression, env:Environment):
  s = ''

def trTernary(ex:Expression, env:Environment):
  s = ''

def trAssignment(sen:Assignment, env:Environment):
  s = ''
  env.declareSymbol(sen.id.value)

  if sen.ex:
    pos_temp = Temp()
    res_temp = trExpression(sen.ex, env)

    s += f'{pos_temp}=p+{env.getSymbolPosition(sen.id.value)} // posicion de variable {sen.id.value}\n'
    s += res_temp.output

    s += f'stack[int({pos_temp})]={res_temp}'
    # s += f'{sen.id.value}={result.value}\n'
  # else:
    # s += f'{sen.id.value}=0\n'

  return s

def trFunction(sen:Function, env:Environment):
  if sen.id.value in RESERVED_FUNCTIONS.keys():
    return SemanticError(sen, f"El id '{sen.id.value}' está reservado")

  if env.id!='global':
    return SemanticError(sen, 'Solo se pueden declarar funciones en el entorno global')

  if getFunction(sen.id.value):
    return SemanticError(sen, f"No se puede redeclarar '{sen.id.value}'")

  addFunction(sen)

  s = f'func {sen.id.value}(){{\n'

  newEnv = Environment(sen.id.value, env)

  for parameter in sen.parameters:
    newEnv.declareSymbol(parameter)

  newEnv.declareSymbol('return')

  s += trInstructions(sen.ins, newEnv)

  s += 'return\n}'
  return s

def trStruct(sen:Struct, env:Environment):
  s = ''

def trIf(sen:If, env:Environment):
  s = ''

  condition = trExpression(sen.ex, env)
  s += condition.output
  s += condition.printTrueTags()

  newEnv = Environment(f'{env.id}#if({sen.ln}, {sen.col})', env)
  s += trInstructions(sen.ins, newEnv)

  escape_label = Label()
  s += f'goto {escape_label}\n'
  s += condition.printFalseTags()

  if type(sen.elseif) is Else:
    s += trInstructions(sen.elseif.ins, newEnv)
    s += f'goto {escape_label}\n'
  elif type(sen.elseif) is If:
    s += trIf(sen.elseif, env)

  s += f'{escape_label}:\n'
  return s

def trWhile(sen:While, env:Environment):
  s = ''

def trFor(sen:For, env:Environment):
  s = ''

def execute(sen, env:Environment):
  T = type(sen)
  if T is Assignment: return trAssignment(sen, env)
  # if T is Function: return trFunction(sen, env)
  # if T is Struct: return trStruct(sen, env)
  if T is Call: return trCall(sen, env)
  if T is If: return trIf(sen, env)
  # if T is While: return trWhile(sen, env)
  # if T is For: return trFor(sen, env)
  return f'***** {type(sen)} not supported\n'
