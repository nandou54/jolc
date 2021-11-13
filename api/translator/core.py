from copy import deepcopy
from api.symbols import Error, Struct

def getHeaderOutput():
  s = 'package main;\n'

  if fmt_was_used or math_was_used:
    s += 'import (\n'
    if fmt_was_used: s += '"fmt"\n'
    if math_was_used: s += '"math"\n'
    s += ');\n'

  s += '''
var stack [1000]float64; // stack
var heap [1000]float64;  // heap
var p,h float64;         // pointers
'''
  return s

STACK_TOP = 0

output = ''
fmt_was_used = False
math_was_used = False

errors = []
temps = []

envs = []
functions = []

label_counter = 1
temp_counter = 1

def addTemp(temp):
  temps.append(temp)

def addFunction(function):
  functions.append(function)

def reset():
  global fmt_was_used, math_was_used, STACK_TOP, output, label_counter, temp_counter

  fmt_was_used = math_was_used = False

  STACK_TOP = 0
  output = ''
  label_counter = temp_counter = 1

  errors.clear()
  temps.clear()
  envs.clear()
  functions.clear()

def setMath():
  global math_was_used
  math_was_used = True

def setFmt():
  global fmt_was_used
  fmt_was_used = True

def getOutput():
  return output

def getErrors():
  return errors

def getSymbols():
  symbols = {"variables": [], "functions": [], "structs": []}
  for env in envs:
    for id, value in env.symbols.items():
      symbol = [env.id, 0, 0, id, value.type]
      symbols["variables"].append(symbol)
  for function in functions:
      symbol = ['global', function.ln, function.col, function.id.value, ', '.join(parameter.value for parameter in function.parameters)]
      symbols["functions"].append(symbol)

  return symbols

def getTemps():
  if len(temps)==0: return '\n'
  return 'var ' + ','.join(temps) + ' float64;\n\n'

def getFunction(id):
  for function in functions:
    if function.id.value==id: return function

def SemanticError(sen, description):
  if hasattr(sen, 'ln'):
    errors.append(Error(sen.ln, sen.col, 'Semántico', description))
  else:
    errors.append(Error(0, 0, 'Semántico', description))
  return ''

def ApplicationError(description):
  errors.append(Error(1, 1, 'Aplicación', description))

class Environment():
  def __init__(self, id = 'global', increment = True):
    self.id = id
    self.symbols = {}
    self.escape_label = None
    self.increment = increment

    if increment: envs.append(self)
    self.escape_label = Label()

    self.base = self.top = STACK_TOP
    self.length = 0

  def declareSymbol(self, id, type = 'int64'):
    if id in self.symbols.keys():
      self.symbols[id].setType(type)
    else:
      self.symbols[id] = Symbol(self.length, type)

      self.top += 1
      self.length += 1

      # if self.increment:
      global STACK_TOP
      STACK_TOP += 1

  def getSymbol(self, id):
    if id not in self.symbols.keys(): return None
    return self.symbols[id]

class Symbol():
  def __init__(self, position, type):
    self.position = position
    self.type = type
    self.location = 'heap' if type in ['string'] else 'stack'

  def __str__(self):
    return str(self.position)

  def setType(self, type):
    self.type = type
    self.location = 'heap' if type in ['string'] else 'stack'

class Label:
  def __init__(self):
    global label_counter
    self.value = f'L{label_counter}'
    label_counter += 1

  def __str__(self):
    return self.value

class Temp:
  def __init__(self, value = None, type = None):
    if value != None:
      self.value = value
      self.type = type
    else:
      global temp_counter, temps
      self.value = f't{temp_counter}'
      self.type = type
      addTemp(self.value)
      temp_counter += 1


    self.output = ''
    self.true_tags = []
    self.false_tags = []

  def __str__(self):
    return str(self.value)

  def setOutput(self, *args):
    for t in args: self.output += t.output

  def printTrueTags(self):
    return ''.join(str(tag) + ':\n' for tag in self.true_tags)

  def printFalseTags(self):
    return ''.join(str(tag) + ':\n' for tag in self.false_tags)

format_types = {
  'int64': '%d',
  'float64': '%f',
  'string': '%c',
  'char': '%c',
  'bool': '%t'
}

def _print(temps):
  setFmt()
  s = ''

  for temp in temps:
    if temp.type == 'float64':
      s += f'fmt.Printf("{format_types[temp.type]}", {temp});\n'
    elif temp.type == 'string':
      char_temp = Temp()
      loop_label = Label()
      true_label = Label()
      false_label = Label()

      s += f'{loop_label}:\n'
      s += f'{char_temp}=heap[int({temp})];\n'
      s += f'if({char_temp}!=34){{goto {true_label};}}\n'
      s += f'goto {false_label};\n'
      s += f'{true_label}:\n'
      s += f'fmt.Printf("%c", int({char_temp}));\n'
      s += f'{temp}={temp}+1;\n'
      s += f'goto {loop_label};\n'
      s += f'{false_label}:\n'
    else:
      s += f'fmt.Printf("{format_types[temp.type]}", int({temp}));\n'

  t = Temp('')
  t.output = s
  return t

def _println(temps):
  setFmt()
  s = ''

  for temp in temps:
    if temp.type == 'float64':
      s += f'fmt.Printf("{format_types[temp.type]}", {temp});\n'
    elif temp.type == 'string':
      char_temp = Temp()
      loop_label = Label()
      true_label = Label()
      false_label = Label()

      s += f'{loop_label}:\n'
      s += f'{char_temp}=heap[int({temp})];\n'
      s += f'if({char_temp}!=34){{goto {true_label};}}\n'
      s += f'goto {false_label};\n'
      s += f'{true_label}:\n'
      s += f'fmt.Printf("%c", int({char_temp}));\n'
      s += f'{temp}={temp}+1;\n'
      s += f'goto {loop_label};\n'
      s += f'{false_label}:\n'
    else:
      s += f'fmt.Printf("{format_types[temp.type]}", int({temp}));\n'
  s += 'fmt.Printf("%c", 10); // nueva linea\n'

  t = Temp('')
  t.output = s
  return t

def _log10(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'log10' recibe un parámetro")

  t = values[0]
  if t.type not in ['int64', 'float64']:
    return SemanticError(t, "La función nativa 'log10' recibe un valor numérico")

  setMath()

  t_result = Temp(None, 'float64')
  t_result.output = f'{t_result}=math.Log10({t});\n'
  return t_result

def _log(values):
  if len(values)!=2: return SemanticError(values[0], "La función nativa 'log' recibe dos parámetros")

  base, ex = values[0], values[1]
  if base.type not in ['int64', 'float64'] or ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'log' recibe dos valores numéricos")

  setMath()

  t_ex = Temp(None, 'float64')
  t_base = Temp(None, 'float64')
  t_result = Temp(None, 'float64')


  t_result.output = f'{t_ex}=math.Log10({ex});\n'
  t_result.output += f'{t_base}=math.Log10({base});\n'
  t_result.output += f'{t_result}={t_ex}/{t_base};\n'
  return t_result

def _sin(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'sin' recibe un parámetro")

  t = values[0]
  if t.type not in ['int64', 'float64']:
    return SemanticError(t, "La función nativa 'sin' recibe un valor numérico")

  setMath()

  t_result = Temp(None, 'float64')
  t_result.output = f'{t_result}=math.Sin({t});\n'
  return t_result

def _cos(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'cos' recibe un parámetro")

  t = values[0]
  if t.type not in ['int64', 'float64']:
    return SemanticError(t, "La función nativa 'cos' recibe un valor numérico")

  setMath()

  t_result = Temp(None, 'float64')
  t_result.output = f'{t_result}=math.Cos({t});\n'
  return t_result

def _tan(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'tan' recibe un parámetro")

  t = values[0]
  if t.type not in ['int64', 'float64']:
    return SemanticError(t, "La función nativa 'tan' recibe un valor numérico")

  setMath()

  t_result = Temp(None, 'float64')
  t_result.output = f'{t_result}=math.Tan({t});\n'
  return t_result

def _sqrt(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'sqrt' recibe un parámetro")

  t = values[0]
  if t.type not in ['int64', 'float64']:
    return SemanticError(t, "La función nativa 'sqrt' recibe un valor numérico")

  setMath()

  t_result = Temp(None, 'float64')
  t_result.output = f'{t_result}=math.Sqrt({t});\n'
  return t_result

def _parse(values):
  if len(values)!=1: return SemanticError(values[0], "La función nativa 'typeof' recibe un parámetro")

  t = values[0]
  if t.type!='string':
    return SemanticError(t, "La función nativa 'parse' recibe un valor string")

  setFmt()

  t_result = Temp(None, 'int64')
  char_temp = Temp()
  loop_label = Label()
  true_label = Label()
  false_label = Label()
  true_label_num = Label()
  true_label_num2 = Label()
  false_label_num = Label()

  s = f'{loop_label}:\n'
  s += f'{char_temp}=heap[int({t})];\n'
  s += f'if({char_temp}!=34){{goto {true_label};}}\n'
  s += f'goto {false_label};\n'
  s += f'{true_label}:\n'
  s += f'if({char_temp}>=48){{goto {true_label_num};}}\ngoto {false_label_num};\n'
  s += f'{true_label_num}:\n'
  s += f'if({char_temp}<=57){{goto {true_label_num2};}}\ngoto {false_label_num};\n'
  s += f'{true_label_num2}:\n'
  s += f'{char_temp}={char_temp}-48;\n'
  s += f'{t_result}={t_result}*10;\n'
  s += f'{t_result}={t_result}+{char_temp};\n'
  s += f'{t}={t}+1;\n'
  s += f'goto {loop_label};\n'
  s += f'{false_label_num}:\n'
  s += 'fmt.Printf("%c", 69);\n'
  s += 'fmt.Printf("%c", 114);\n'
  s += 'fmt.Printf("%c", 114);\n'
  s += 'fmt.Printf("%c", 111);\n'
  s += 'fmt.Printf("%c", 114);\n'
  s += f'{false_label}:\n'

  t_result.output = s
  return t_result

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

  t = Temp(None, 'string')

  s = f'{t}=h;\n'
  for c in ex.type:
    s += f'heap[int(h)]={ord(c)};\n'
    s += 'h=h+1;\n'

  s += 'heap[int(h)]=34;\n'
  s += 'h=h+1;\n'

  t.output = s
  return t

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

  if ex.type=='string':
    t = Temp(None, 'string')
    t_result = Temp(None, 'int64')

    char_temp = Temp()
    loop_label = Label()
    true_label = Label()
    false_label = Label()

    s = f'{t}={ex};\n'
    s += f'{loop_label}:\n'
    s += f'{char_temp}=heap[int({t})];\n'
    s += f'if({char_temp}!=34){{goto {true_label};}}\n'
    s += f'goto {false_label};\n'
    s += f'{true_label}:\n'
    s += f'{t_result}={t_result}+1;\n'
    s += f'{t}={t}+1;\n'
    s += f'goto {loop_label};\n'
    s += f'{false_label}:\n'

    t_result.output = s
    return t_result

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

  t.setOutput(l, r)
  t.output += f'{t}={l}+{r};\n'
  return t

def _resta(l:Temp, r:Temp):
  t = Temp()

  t.setOutput(l, r)
  t.output += f'{t}={l}-{r};\n'
  return t

def _multiplicacion(l:Temp, r:Temp):
  if l.type=='string':
    res_temp = Temp(None, 'string')
    res_temp.setOutput(l, r)
    char_temp = Temp()

    s = f'{res_temp}=h; // inicio de suma de string\n'

    for temp in [l, r]:
      loop_label = Label()
      true_label = Label()
      false_label = Label()

      s += f'{loop_label}:\n'
      s += f'{char_temp}=heap[int({temp})];\n'
      s += f'if({char_temp}!=34){{goto {true_label};}}\n'
      s += f'goto {false_label};\n'
      s += f'{true_label}:\n'
      s += f'heap[int(h)]={char_temp};\n'
      s += 'h=h+1;\n'
      s += f'{temp}={temp}+1;\n'
      s += f'goto {loop_label};\n'
      s += f'{false_label}:\n'

    s += 'heap[int(h)]=34; // fin de suma de string\n'
    s += 'h=h+1;\n'

    res_temp.output += s
    return res_temp

  t = Temp()
  t.setOutput(l, r)
  t.output += f'{t}={l}*{r};\n'
  return t

def _division(l:Temp, r:Temp):
  setFmt()

  t = Temp()
  t.setOutput(l, r)

  lt = Label()
  lf = Label()

  t.output += f'''if {t}!=0 {{goto {lt};}}
fmt.Printf("%c", 77);  //M
fmt.Printf("%c", 97);  //a
fmt.Printf("%c", 116); //t
fmt.Printf("%c", 104); //h
fmt.Printf("%c", 69);  //E
fmt.Printf("%c", 114); //r
fmt.Printf("%c", 114); //r
fmt.Printf("%c", 111); //o
fmt.Printf("%c", 114); //r
{t}=0
goto {lf};
{lt}:
{t}={l}/{r};
{lf}:
'''
  return t

def _modulo(l:Temp, r:Temp):
  setFmt()

  t = Temp()
  t.setOutput(l, r)

  lt = Label()
  lf = Label()

  t.output += f'''if {t}!=0 {{goto {lt};}}
fmt.Printf("%c", 77);  //M
fmt.Printf("%c", 97);  //a
fmt.Printf("%c", 116); //t
fmt.Printf("%c", 104); //h
fmt.Printf("%c", 69);  //E
fmt.Printf("%c", 114); //r
fmt.Printf("%c", 114); //r
fmt.Printf("%c", 111); //o
fmt.Printf("%c", 114); //r
{t}=0;
goto {lf};
{lt}:
{t}=float64(int({l})%int({r}));
{lf}:
'''
  return t

def _potencia(l:Temp, r:Temp):
  if l.type=='string':
    res_temp = Temp(None, 'string')
    res_temp.setOutput(l, r)
    char_temp = Temp()
    i = Temp()
    j = Temp()

    s = f'{res_temp}=h; // inicio de multiplicacion de string\n'

    loop_label_i = Label()
    true_label_i = Label()
    false_label_i = Label()
    loop_label_j = Label()
    true_label_j = Label()
    false_label_j = Label()

    s += f'{i}=0;\n'
    s += f'{loop_label_i}:\n'
    s += f'if({i}<{r}){{goto {true_label_i};}}\ngoto {false_label_i};\n'

    s += f'{true_label_i}:\n'
    s += f'{j}={l};\n'
    s += f'{loop_label_j}:\n'
    s += f'{char_temp}=heap[int({j})];\n'
    s += f'if({char_temp}!=34){{goto {true_label_j};}}\n'
    s += f'goto {false_label_j};\n'
    s += f'{true_label_j}:\n'
    s += f'heap[int(h)]={char_temp};\n'
    s += 'h=h+1;\n'
    s += f'{j}={j}+1;\n'
    s += f'goto {loop_label_j};\n'
    s += f'{false_label_j}:\n'

    s += f'{i}={i}+1;\n'
    s += f'goto {loop_label_i};\n'
    s += f'{false_label_i}:\n'

    s += 'heap[int(h)]=34; // fin de multiplicacion de string\n'
    s += 'h=h+1;\n'

    res_temp.output += s
    return res_temp

  t = Temp()
  t.setOutput(l, r)
  t.type = 'float64'
  limit = Temp()
  i = Temp()

  loop_label = Label()
  true_label = Label()
  false_label = Label()
  true_label_limit = Label()
  true_label_res = Label()
  false_label_res = Label()

  s = f'{t}=1; // first\n'
  s += f'{limit}={r};\n'
  s += f'{i}=0;\n'
  s += f'if({r}<0){{goto {true_label_limit};}}\ngoto {loop_label};\n'
  s += f'{true_label_limit}:\n'
  s += f'{limit}={limit}*-1;\n'
  s += f'{loop_label}:\n'
  s += f'if({i}<{limit}){{goto {true_label};}}\ngoto {false_label};\n'
  s += f'{true_label}:\n'
  s += f'{t}={t}*{l};\n'
  s += f'{i}={i}+1;\n'
  s += f'goto {loop_label};\n'
  s += f'{false_label}:\n'
  s += f'if({r}<0){{goto {true_label_res};}}\ngoto {false_label_res};\n'
  s += f'{true_label_res}:\n'
  s += f'{t}=1/{t};\n'
  s += f'{false_label_res}:\n'

  t.output += s
  return t

def _negacion(l:Temp):
  t = Temp()

  t.setOutput(l)
  t.output += f'{t}=-{l};\n'
  return t

def _menor(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.setOutput(l, r)
  t.output += f'if ({l}<{r}){{goto {true_tag};}}\ngoto {false_tag};\n'
  return t

def _menor_igual(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.setOutput(l, r)
  t.output += f'if ({l}<={r}){{goto {true_tag};}}\ngoto {false_tag};\n'
  return t

def _mayor(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.setOutput(l, r)
  t.output += f'if ({l}>{r}){{goto {true_tag};}}\ngoto {false_tag};\n'
  return t

def _mayor_igual(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.setOutput(l, r)
  t.output += f'if ({l}>={r}){{goto {true_tag};}}\ngoto {false_tag};\n'
  return t

def _igualacion(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.setOutput(l, r)
  t.output += f'if ({l}=={r}){{goto {true_tag};}}\ngoto {false_tag};\n'
  return t

def _diferenciacion(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.setOutput(l, r)
  t.output += f'if ({l}!={r}){{goto {true_tag};}}\ngoto {false_tag};\n'
  return t

def _or(l:Temp, r:Temp):
  t = Temp('')
  t.setOutput(l)

  t.true_tags = l.true_tags + r.true_tags
  t.false_tags = r.false_tags

  t.output += l.printFalseTags()
  t.setOutput(r)
  return t

def _and(l:Temp, r:Temp):
  t = Temp('')
  t.setOutput(l)

  t.true_tags = r.true_tags
  t.false_tags = l.false_tags + r.false_tags

  t.output += l.printTrueTags()
  t.setOutput(r)
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
