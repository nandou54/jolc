from symbols import Error

INITIAL_OUTPUT = '''package main
import "fmt"
var stack [1000]float64 // stack
var heap [1000]float64  // heap
var P,H int64         // pointers

'''

output = INITIAL_OUTPUT
temps = []
errors = []

label_counter = 1
temp_counter = 1

def reset():
  global output, label_counter, temp_counter
  output = INITIAL_OUTPUT
  label_counter = temp_counter = 1

  temps.clear()
  errors.clear()

def getOutput():
  return output

def getTemps():
  return 'var ' + ','.join(temps) + ' float64\n\n'

def getErrors():
  return errors

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
      temps.append(self.value)
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

def SemanticError(sen, description):
  errors.append(Error(sen.ln, sen.col, 'Semántico', description))

def ApplicationError(description):
  errors.append(Error(1, 1, 'Aplicación', description))

def _suma(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t} = {l} + {r}\n'
  return t

def _resta(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t} = {l} - {r}\n'
  return t

def _multiplicacion(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t} = {l} * {r}\n'
  return t

def _division(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t} = {l} / {r}\n'
  return t

def _modulo(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t} = {l} % {r}\n'
  return t

def _potencia(l:Temp, r:Temp):
  t = Temp()

  t.getOutput(l, r)
  t.output += f'{t} = {l} ^ {r}\n'
  return t

def _negacion(l:Temp):
  t = Temp()

  t.getOutput(l)
  t.output += f'{t} = -{l}\n'
  return t

def _menor(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l} < {r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _menor_igual(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l} <= {r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _mayor(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l} > {r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _mayor_igual(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l} >= {r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _igualacion(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l} == {r}){{goto {true_tag}}}\ngoto {false_tag}\n'
  return t

def _diferenciacion(l:Temp, r:Temp):
  t = Temp('')
  true_tag = Label()
  false_tag = Label()

  t.true_tags.append(true_tag)
  t.false_tags.append(false_tag)

  t.getOutput(l, r)
  t.output += f'if ({l} != {r}){{goto {true_tag}}}\ngoto {false_tag}\n'
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
