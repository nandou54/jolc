from traceback import print_exc

from api.analyzer.main import parse
from api.symbols import Expression, Value, Assignment, Function, Struct, Call, If, Else, While, For, Return, Break, Continue
from api.symbols import T_SENTENCE, EXECUTABLE_SENTENCE

from .core import getOutput, getTemps, BINARY_OPERATIONS, UNARY_OPERATIONS
from .core import reset, Label, Temp, ApplicationError
# from .core import RESERVED_FUNCTIONS, BINARY_OPERATIONS, UNARY_OPERATIONS, BINARY_OPERATION_RESULTS, UNARY_OPERATION_RESULTS

def translate(input):
  reset()

  res = parse(input)
  INS = res['ast']

  output = getOutput()

  try:
    NEW_INS = [ins for ins in INS if type(ins) is not Function]
    ins_output = exInstructions(NEW_INS)

    output += getTemps()
    output += 'func main(){\nfmt.Println("running")\n'
    output += ins_output
    output += '}\n'

    for ins in INS:
      if type(ins) is Function: output += exFunction(ins)
  except:
    print_exc()
    ApplicationError('Error en la traducción a C3D')

  res['output'] = output
  return res

def exInstructions(INS:T_SENTENCE):
  return '\n'.join(execute(ins) for ins in INS)

def exExpression(ex:Expression):
  if type(ex) is Call: return exCall(ex)
  if ex.type=='array':
    # for i in range(len(ex.value)):
    #   newValue = exExpression(ex.value[i])
    #   if not newValue: return SemanticError(ex, "No se pudo crear el array")
    #   ex.value[i] = newValue
    return ex
  if ex.type=='access': return exAccess(ex)
  if ex.type=='chain': return exChain(ex)
  if ex.type=='range': return exRange(ex)
  if ex.type=='ternary': return exTernary(ex)
  if ex.type=='id': return exId(ex)
  if ex.type=='string': return exString(ex)
  if type(ex) is Value: return Temp(ex.value)

  left_temp = exExpression(ex.left) if ex.left else None
  right_temp = exExpression(ex.right) if ex.right else None

  return (UNARY_OPERATIONS[ex.type](left_temp)
         if ex.unary
         else BINARY_OPERATIONS[ex.type](left_temp, right_temp))

def exString(ex):
  s = ''

def exId(ex):
  s = ''

def exCall(sen:Call):
  s = ''

def exAccess(ex:Expression):
  s = ''

def exChain(ex:Expression, output, assignment = False):
  s = ''

def exRange(ex:Expression):
  s = ''

def exTernary(ex:Expression):
  s = ''

def exAssignment(sen:Assignment):
  s = ''
  result = exExpression(sen.ex)
  s += result.output
  return s

def exFunction(sen:Function):
  s = ''
  # return s

def exStruct(sen:Struct):
  s = ''

def exIf(sen:If):
  s = ''

  condition = exExpression(sen.ex)
  s += condition.output

  s += condition.printTrueTags()
  s += exInstructions(sen.ins)

  escape_label = Label()
  s += f'goto {escape_label}\n'
  s += condition.printFalseTags()

  if type(sen.elseif) is Else:
    s += exInstructions(sen.elseif.ins)
    s += f'goto {escape_label}\n'
  elif type(sen.elseif) is If:
    s += exIf(sen.elseif)

  s += f'{escape_label}:\n'
  return s

def exWhile(sen:While):
  s = ''

def exFor(sen:For):
  s = ''

def execute(sen):
  T = type(sen)
  if T is Assignment: return exAssignment(sen)
  # if T is Function: return exFunction(sen)
  # if T is Struct: return exStruct(sen)
  # if T is Call: return exCall(sen)
  if T is If: return exIf(sen)
  # if T is While: return exWhile(sen)
  # if T is For: return exFor(sen)
  return '// {} not supported\n'.format(sen.type)
