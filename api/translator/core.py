from copy import deepcopy
from api.symbols import Error, Struct

INITIAL_OUTPUT = '''package main
import "fmt"
var stack [1000]float64 // stack
var heap [1000]float64  // heap
var P, H int64          // pointers

'''

output = INITIAL_OUTPUT
errors = []
temps = []

envs = []

label_counter = 1
temp_counter = 1

def addTemp(temp):
  temps.append(temp)

def reset():
  global output, label_counter, temp_counter
  output = INITIAL_OUTPUT
  label_counter = temp_counter = 1

  errors.clear()
  temps.clear()
  envs.clear()


def getOutput():
  return output

def getTemps():
  return 'var ' + ','.join(temps) + ' float64\n\n'

def getErrors():
  return errors

def SemanticError(sen, description):
  errors.append(Error(sen.ln, sen.col, 'Semántico', description))

def ApplicationError(description):
  errors.append(Error(1, 1, 'Aplicación', description))

class Environment():
  def __init__(self, id = 'global', parent = None):
    self.id = id
    self.parent:Environment = parent
    self.symbols = {}
    envs.append(self)

  def declareSymbol(self, id, value):
    self.symbols[id] = value

  def getLocalSymbol(self, id):
    if id not in self.symbols.keys(): return None
    return self.symbols[id]

  def getGlobalSymbol(self, id):
    tempEnv = self
    while tempEnv:
      if tempEnv.getLocalSymbol(id):
        return tempEnv.getLocalSymbol(id)
      tempEnv = tempEnv.parent
    return None

  def getParentEnvById(self, id):
    tempEnv = self
    while tempEnv:
      if tempEnv.getLocalSymbol(id):
        return tempEnv
      tempEnv = tempEnv.parent
    return None

class Label:
  def __init__(self):
    global label_counter
    self.value = f'L{label_counter}'
    label_counter += 1

  def __str__(self):
    return self.value

class Temp:
  def __init__(self, value = None):
    if value != None:
      self.value = str(value)
    else:
      global temp_counter, temps
      self.value = f't{temp_counter}'
      addTemp(self.value)
      temp_counter += 1

    self.output = ''
    self.true_tags = []
    self.false_tags = []

  def __str__(self):
    return self.value

  def getOutput(self, *args):
    for t in args: self.output += t.output

  def printTrueTags(self):
    return ''.join(str(tag) + ':\n' for tag in self.true_tags)

  def printFalseTags(self):
    return ''.join(str(tag) + ':\n' for tag in self.false_tags)

def _print(temps):
  return '\n'.join(f'fmt.Print({temp})' for temp in temps)

def _println(temps):
  return '\n'.join(f'fmt.Println({temp})' for temp in temps)

def _log10(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'log10' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'log10' recibe un valor numérico")

  newValue = deepcopy(ex)
  newValue.type = 'float64'
  # newValue.value = log10(newValue.value)
  return newValue

def _log(values):
  if len(values)!=2: return SemanticError(values[0], "La función nativa 'log' recibe dos parámetros")

  base, ex = values[0], values[1]
  if base.type not in ['int64', 'float64'] or ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'log' recibe dos valores numéricos")

  newValue = deepcopy(ex)
  newValue.type = 'float64'
  # newValue.value = log(newValue.value, base.value)
  return newValue

def _sin(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'sin' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'sin' recibe un valor numérico")

  newValue = deepcopy(ex)
  newValue.type = 'float64'
  # newValue.value = sin(newValue.value)
  return newValue

def _cos(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'cos' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'cos' recibe un valor numérico")

  newValue = deepcopy(ex)
  newValue.type = 'float64'
  # newValue.value = cos(newValue.value)
  return newValue

def _tan(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'tan' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'tan' recibe un valor numérico")

  newValue = deepcopy(ex)
  newValue.type = 'float64'
  # newValue.value = tan(newValue.value)
  return newValue

def _sqrt(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'sqrt' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'sqrt' recibe un valor numérico")

  newValue = deepcopy(ex)
  newValue.type = 'float64'
  # newValue.value = sqrt(newValue.value)
  return newValue

def _parse(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'typeof' recibe un parámetro")

  ex = values[0]
  if ex.type!='string':
    return SemanticError(ex, "La función nativa 'parse' recibe un valor string")

  newValue = deepcopy(ex)
  try:
    newValue.value = int(newValue.value)
    newValue.type = 'int64'
  except ValueError:
    try:
      newValue.value = float(newValue.value)
      newValue.type = 'float64'
    except ValueError: return SemanticError(ex, "No se pudo parsear el string dado")

  return newValue

def _trunc(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'trunc' recibe un parámetro")

  ex = values[0]
  if ex.type!='float64':
    return SemanticError(ex, "La función nativa 'trunc' recibe un valor float64")

  newValue = deepcopy(ex)
  newValue.type = 'int64'
  newValue.value = int(newValue.value)
  return newValue

def _float(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'float' recibe un parámetro")

  ex = values[0]
  if ex.type!='int64':
    return SemanticError(ex, "La función nativa 'trunc' recibe un valor int64")

  newValue = deepcopy(ex)
  newValue.type = 'float64'
  newValue.value = float(newValue.value)
  return newValue

def unnest(val):
  if type(val) is list:
    for i in range(len(val)):
      val[i] = unnest(val[i].value)
  elif type(val) is Struct:
    d = {'struct': val.id.value}
    for a in val.attributes:
      d[a.id.value] = unnest(a.value.value)
    val = d
  return val

def _string(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'string' recibe un parámetro")

  newValue = deepcopy(values[0])
  newValue.value = str(unnest(newValue.value))
  newValue.type = 'string'
  return newValue

def _uppercase(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'uppercase' recibe un parámetro")

  ex = values[0]
  if ex.type!='string':
    return SemanticError(ex, "La función nativa 'uppercase' recibe un valor string")

  newValue = deepcopy(ex)
  newValue.value = newValue.value.upper()
  return newValue

def _lowercase(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'lowercase' recibe un parámetro")

  ex = values[0]
  if ex.type!='string':
    return SemanticError(ex, "La función nativa 'lowercase' recibe un valor string")

  newValue = deepcopy(ex)
  newValue.value = newValue.value.lower()
  return newValue

def _typeof(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'typeof' recibe un parámetro")

  ex = values[0]
  value = deepcopy(ex)
  value.value = value.type
  value.type = 'string'
  return value

def _push(values):
  if len(values)!=2: return SemanticError(values[0], "La función nativa 'push' recibe dos parámetros")

  arr, ex = values[0], values[1]
  if arr.type!='array':
    return SemanticError(arr, "La función nativa 'push' recibe un array")
  arr.value.append(ex)

def _pop(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'pop' recibe un parámetro")

  arr = values[0]
  if arr.type!='array':
    return SemanticError(arr, "La función nativa 'pop' recibe un array")

  return arr.value.pop()

def _length(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'length' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['string', 'array']:
    return SemanticError(ex, "La función nativa 'length' recibe un string o un array")

  newValue = deepcopy(ex)
  newValue.type = 'int64'
  newValue.value = len(ex.value)
  return newValue

RESERVED_FUNCTIONS = {
  'print': _print,
  'println': _println,
  'log10': _log10,
  'log': _log,
  'sin': _sin,
  'cos': _cos,
  'tan': _tan,
  'sqrt': _sqrt,
  'parse': _parse,
  'trunc': _trunc,
  'float': _float,
  'string': _string,
  'uppercase': _uppercase,
  'lowercase': _lowercase,
  'typeof': _typeof,
  'push!': _push,
  'pop!': _pop,
  'length': _length
}

def _suma(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t}={l}+{r}\n'
  return t

def _resta(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t}={l}-{r}\n'
  return t

def _multiplicacion(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t}={l}*{r}\n'
  return t

def _division(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t}={l}/{r}\n'
  return t

def _modulo(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t}={l}%{r}\n'
  return t

def _potencia(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t}={l}^{r}\n'
  return t

def _negacion(l:Temp):
  t = Temp()

  t.getOutput(l)
  t.output += f'{t}=-{l}\n'
  return t

def _menor(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l}<{r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _menor_igual(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l}<={r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _mayor(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l}>{r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _mayor_igual(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l}>={r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _igualacion(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l}=={r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _diferenciacion(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l}!={r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _or(l:Temp, r:Temp):
  t = Temp('')
  t.getOutput(l)

  t.true_tags = l.true_tags + r.true_tags
  t.false_tags = r.false_tags

  t.output += l.printFalseTags()
  t.getOutput(r)
  return t

def _and(l:Temp, r:Temp):
  t = Temp('')
  t.getOutput(l)

  t.true_tags = r.true_tags
  t.false_tags = l.false_tags + r.false_tags

  t.output += l.printTrueTags()
  t.getOutput(r)
  return t

def _not(l:Temp):
  temp_tags = l.true_tags
  l.true_tags = l.false_tags
  l.false_tags = temp_tags

BINARY_OPERATIONS = {
  'suma': _suma,
  'resta':_resta,
  'multiplicacion':_multiplicacion,
  'division':_division,
  'modulo':_modulo,
  'potencia':_potencia,
  'menor':_menor,
  'menor_igual':_menor_igual,
  'mayor':_mayor,
  'mayor_igual':_mayor_igual,
  'igualacion':_igualacion,
  'diferenciacion':_diferenciacion,
  'or':_or,
  'and':_and
}

UNARY_OPERATIONS = {
  'negacion':_negacion,
  'not':_not
}
