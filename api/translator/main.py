from traceback import print_exc

from api.analyzer.main import parse
from api.interpreter.core import BINARY_OPERATION_RESULTS, UNARY_OPERATION_RESULTS
from api.symbols import Expression, Value, Assignment, Function, Struct, Call, If, Else, While, For, Return, Break, Continue
from api.symbols import T_SENTENCE

from .core import RESERVED_FUNCTIONS, Environment, SemanticError, addFunction, getFunction, getTemps, BINARY_OPERATIONS, UNARY_OPERATIONS
from .core import getHeaderOutput, reset, getOutput, errors, Label, Temp, ApplicationError

def translate(input):
  global errors
  reset()
  output = getOutput()

  mainEnv = Environment('main')

  res = parse(input)
  INS = res['ast']

  try:
    FUNC_INS = [ins for ins in INS if type(ins) is Function]
    NEW_INS = [ins for ins in INS if type(ins) is not Function]

    process_functions(FUNC_INS)
    func_output = '\n\n'.join(trFunction(ins, mainEnv) for ins in FUNC_INS)

    ins_output = trInstructions(NEW_INS, mainEnv)

    output += getHeaderOutput()
    output += getTemps()
    output += 'func main(){\n'
    output += ins_output
    output += '}\n\n'
    output += func_output

  except:
    print_exc()
    ApplicationError('Error en la traducción a C3D')

  res['output'] = output
  res['errors'] += errors
  return res

def process_functions(INS):
  def get_assignments(INS):
    for sen in INS:
      if type(sen) is Assignment:
        newEnv.declareSymbol(sen.id.value)
      elif hasattr(sen, 'ins'):
        get_assignments(sen.ins)

  for sen in INS:
    newEnv = Environment(sen.id.value, False)

    for parameter in sen.parameters:
      newEnv.declareSymbol(parameter.value)

    get_assignments(sen.ins)
    newEnv.declareSymbol('return')
    sen.env = newEnv
    addFunction(sen)

def trInstructions(INS:T_SENTENCE, env:Environment):
  return '\n'.join(
    f'// ***** iniciando {type(ins).__name__} *****\n' +
    execute(ins, env) +
    f'// ***** terminando {type(ins).__name__} *****\n'
    for ins in INS)

def trExpression(ex:Expression, env:Environment):
  if type(ex) is Call: return trCall(ex, env)
  # if ex.type=='array':
    # for i in range(len(ex.value)):
    #   newValue = exExpression(ex.value[i])
    #   if not newValue: return SemanticError(ex, "No se pudo crear el array")
    #   ex.value[i] = newValue
    # return ex
  # if ex.type=='access': return trAccess(ex, env)
  # if ex.type=='chain': return trChain(ex, env)
  # if ex.type=='range': return trRange(ex, env)
  # if ex.type=='ternary': return trTernary(ex, env)
  if ex.type=='id':
    if env.getSymbol(ex.value) is None:
      return SemanticError(ex, f"No se declaró '{ex.value}'")

    symbol = env.getSymbol(ex.value)
    pos_temp = Temp()
    val_temp = Temp()

    s = f'{pos_temp}=p+{symbol}; // posicion de variable {ex.value}\n'
    s += f'{val_temp}=stack[int({pos_temp})]; // valor de variable {ex.value}\n'

    val_temp.type = symbol.type
    val_temp.output = s
    return val_temp
  if ex.type=='string':
    val_temp = Temp(None, ex.type)
    val_temp.output = f'{val_temp}=h; // inicio de string\n'

    value = ex.value[0].value

    for c in value:
      val_temp.output += f'heap[int(h)]={ord(c)}; // {c}\n'
      val_temp.output += f'h=h+1;\n'

    val_temp.output += f'heap[int(h)]=34; // fin de string\n'
    val_temp.output += f'h=h+1;\n'
    return val_temp
  if ex.type=='char': return Temp(ord(ex.value), ex.type)
  if type(ex) is Value: return Temp(ex.value, ex.type)

  l = trExpression(ex.left, env) if ex.left else None
  r = trExpression(ex.right, env) if ex.right else None

  if not l: return SemanticError(ex, "No se pudo realizar la operación '{}'".format(ex.type))

  if ex.unary:
    try: returnType = UNARY_OPERATION_RESULTS[ex.type][l.type]
    except: return SemanticError(ex, "No se pudo aplicar '{}' a '{}' y '{}'".format(ex.type, l.type, r.type))
  else:
    if not r: return SemanticError(ex, "No se pudo realizar la operación '{}'".format(ex.type))
    if ex.type in ['igualacion', 'diferenciacion']: returnType = 'bool'
    else:
      try: returnType = BINARY_OPERATION_RESULTS[ex.type][l.type][r.type]
      except: return SemanticError(ex, "No se pudo aplicar '{}' a '{}' y '{}'".format(ex.type, l.type, r.type))

  result_temp = (UNARY_OPERATIONS[ex.type](l)
    if ex.unary
    else BINARY_OPERATIONS[ex.type](l, r))
  result_temp.type = returnType
  return result_temp

def trId(ex, env:Environment):
  s = ''

def trCall(sen:Call, env:Environment):
  s = ''
  values = []

  for expression in sen.expressions:
    temp_base = trExpression(expression, env)
    if not temp_base:
      return SemanticError(sen, f"No se pudo realizar la llamada a '{sen.id}'")
    values.append(temp_base)

  if sen.id.value in RESERVED_FUNCTIONS.keys():
    for value in values: s += value.output
    t = RESERVED_FUNCTIONS[sen.id.value](values)
    t.output = s+t.output
    return t

  function = getFunction(sen.id.value)

  if not function: return SemanticError(sen, f"No se declaró '{sen.id.value}'")

  if type(function) is Function:
    if len(values)!=len(function.parameters):
      return SemanticError(sen, f"La función '{sen.id.value}' recibe {len(function.parameters)} parámetros")

    new_env = Environment(sen.id.value)

    for id, symbol in function.env.symbols.items():
      new_env.declareSymbol(id, symbol.type)

    temp_base = Temp()
    new_base = new_env.base-env.base
    s += f'{temp_base}=p+{new_base}; // base de la nueva funcion\n'
    for i in range(len(function.parameters)):
      temp_par_pos = Temp()
      parameter = function.parameters[i].value

      s += values[i].output
      s += f'{temp_par_pos}={temp_base}+{new_env.getSymbol(parameter)}; // posicion de parametro {parameter}\n'
      s += f'stack[int({temp_par_pos})]={values[i]}; // asignacion de parametro {parameter}\n'

    s += f'p=p+{new_base}; // cambio de entorno\n'
    s += f'{sen.id.value}();\n'

    temp_pos = Temp()
    temp_return = Temp()

    s += f'{temp_pos}=p+{new_env.getSymbol("return")}; // posicion de valor de retorno de {sen.id.value}\n'
    s += f'{temp_return}=stack[int({temp_pos})]; // valor de retorno de {sen.id.value}\n'
    s += f'p=p-{new_base}; // regreso de entorno\n'

    temp_return.type = new_env.getSymbol('return').type
    temp_return.output = s
    return temp_return

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
  env.declareSymbol(sen.id.value, sen.type or 'int64')

  if not sen.ex: return s

  pos_temp = Temp()
  res_temp = trExpression(sen.ex, env)
  if not res_temp: return SemanticError(sen, 'No se pudo realizar la asignación')
  if sen.type and sen.type!=res_temp.type: return SemanticError(sen, f'No se puede asignar un valor {res_temp.type} a una variable {sen.type}')

  env.declareSymbol(sen.id.value, res_temp.type)

  s += f'{pos_temp}=p+{env.getSymbol(sen.id.value)}; // posicion de variable {sen.id.value}\n'
  s += res_temp.output
  s += f'stack[int({pos_temp})]={res_temp}; // asignacion de variable {sen.id.value}\n'
  return s

def trFunction(sen:Function, env:Environment):
  if sen.id.value in RESERVED_FUNCTIONS.keys():
    return SemanticError(sen, f"El id '{sen.id.value}' está reservado")

  if env.id!='main':
    return SemanticError(sen, 'Solo se pueden declarar funciones en el entorno global')

  s = f'func {sen.id.value}(){{\n'

  newEnv = getFunction(sen.id.value).env

  s += trInstructions(sen.ins, newEnv)
  s += f'goto {newEnv.escape_label}; // goto para evitar error de go\n'
  s += f'{newEnv.escape_label}: // etiqueta de retorno\n'
  s += 'return;\n}'
  return s

def trReturn(sen:Return, env:Environment):
  s = ''
  if sen.ex:
    t_position = Temp()
    t_return = trExpression(sen.ex, env)
    s_return = env.getSymbol('return')
    s_return.setType(t_return.type)

    s += f'{t_position}=p+{s_return}; // posicion de retorno\n'
    s += t_return.output
    s += f'stack[int({t_position})]={t_return}; // valor de retorno\n'
    s += f'goto {env.escape_label};\n'
  return s

def trStruct(sen:Struct, env:Environment):
  s = ''

def trIf(sen:If, env:Environment):
  s = ''

  condition = trExpression(sen.ex, env)
  s += condition.output
  s += condition.printTrueTags()

  s += trInstructions(sen.ins, env)

  escape_label = Label()
  s += f'goto {escape_label};\n'
  s += condition.printFalseTags()

  if type(sen.elseif) is Else:
    s += trInstructions(sen.elseif.ins, env)
    s += f'goto {escape_label};\n'
  elif type(sen.elseif) is If:
    s += trIf(sen.elseif, env)

  s += f'{escape_label}:\n'
  return s

def trWhile(sen:While, env:Environment):
  s = ''

  loop_label = Label()
  s += f'{loop_label}:\n'

  condition = trExpression(sen.ex, env)
  s += condition.output
  s += condition.printTrueTags()

  s += trInstructions(sen.ins, env)

  s += f'goto {loop_label};\n'
  s += condition.printFalseTags()
  return s

def trFor(sen:For, env:Environment):
  s = ''

def execute(sen, env:Environment):
  try:
    T = type(sen)
    if T is Assignment: return trAssignment(sen, env)
    # if T is Struct: return trStruct(sen, env)
    if T is Call: return trCall(sen, env).output
    if T is Return: return trReturn(sen, env)
    if T is If: return trIf(sen, env)
    if T is While: return trWhile(sen, env)
    # if T is For: return trFor(sen, env)
  except: SemanticError(sen, f'Error al ejecutar {T.__name__}')
