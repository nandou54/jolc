import copy
from math import log10, log, sin, cos, tan, sqrt
from .symbols import Function, Struct, Value, _Error

output = ''
errors = []
symbols = []

envs = []
functions = []
loops = []

def getOutput():
  return output.strip().split('\n') if output else []

def getErrors(): return errors

d:dict={}

def getSymbols():
  symbols = []
  for env in envs:
    for id, value in env.symbols.items():
      valueType, parameters, attributes = 'no aplica', 'no aplica', 'no aplica'

      if type(value) is Value:
        symbolType = 'Variable'
        valueType = value.type
      elif type(value) is Function:
        symbolType = 'Función'
        parameters = ', '.join([parameter.value for parameter in value.parameters])
      else:
        symbolType = 'Struct'
        attributes = ', '.join([attribute.id.value for attribute in value.attributes])

      symbol = [
        value.ln,
        value.col,
        env.id,
        id,
        valueType,
        parameters,
        attributes,
        symbolType
      ]
      symbols.append(symbol)
  return symbols

def reset():
  global output

  output = ''
  errors.clear()
  symbols.clear()

  functions.clear()
  loops.clear()
  envs.clear()

def SemanticError(sen, description):
  errors.append(_Error(sen.ln, sen.col, 'Semántico', description))

class Environment():
  def __init__(self, id = 'global', parent = None):
    self.id = id
    self.parent:Environment = parent
    self.symbols = {}

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

def _print(values):
  global output
  string = ''
  for value in values:
    string+=_string([value]).value+' '
  output+=string[0:-1]

def _println(values):
  global output
  string = ''
  for value in values:
    string+=_string([value]).value+' '
  output+=string[0:-1]+'\n'

def _log10(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'log10' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'log10' recibe un valor numérico")

  newValue = copy.deepcopy(ex)
  newValue.type = 'float64'
  newValue.value = log10(newValue.value)
  return newValue

def _log(values):
  if len(values)!=2: return SemanticError(values[0], "La función nativa 'log' recibe dos parámetros")

  base, ex = values[0], values[1]
  if base.type not in ['int64', 'float64'] or ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'log' recibe dos valores numéricos")

  newValue = copy.deepcopy(ex)
  newValue.type = 'float64'
  newValue.value = log(newValue.value, base.value)
  return newValue

def _sin(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'sin' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'sin' recibe un valor numérico")

  newValue = copy.deepcopy(ex)
  newValue.type = 'float64'
  newValue.value = sin(newValue.value)
  return newValue

def _cos(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'cos' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'cos' recibe un valor numérico")

  newValue = copy.deepcopy(ex)
  newValue.type = 'float64'
  newValue.value = cos(newValue.value)
  return newValue

def _tan(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'tan' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'tan' recibe un valor numérico")

  newValue = copy.deepcopy(ex)
  newValue.type = 'float64'
  newValue.value = tan(newValue.value)
  return newValue

def _sqrt(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'sqrt' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'sqrt' recibe un valor numérico")

  newValue = copy.deepcopy(ex)
  newValue.type = 'float64'
  newValue.value = sqrt(newValue.value)
  return newValue

def _parse(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'typeof' recibe un parámetro")

  ex = values[0]
  if ex.type!='string':
    return SemanticError(ex, "La función nativa 'parse' recibe un valor string")

  newValue = copy.deepcopy(ex)
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
  if len(values)>1: return SemanticError(values[0], "La función nativa 'trunc' recibe un parámetro")

  ex = values[0]
  if ex.type!='float64':
    return SemanticError(ex, "La función nativa 'trunc' recibe un valor float64")

  newValue = copy.deepcopy(ex)
  newValue.type = 'int64'
  newValue.value = int(newValue.value)
  return newValue

def _float(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'float' recibe un parámetro")

  ex = values[0]
  if ex.type!='int64':
    return SemanticError(ex, "La función nativa 'trunc' recibe un valor int64")

  newValue = copy.deepcopy(ex)
  newValue.type = 'float64'
  newValue.value = float(newValue.value)
  return newValue

def unnest(val):
  if type(val) is list:
    for i in range(len(val)):
      val[i] = unnest(val[i].value)
  elif type(val) is Struct:
    d = dict()
    d['struct']=val.id.value
    for a in val.attributes:
      d[a.id.value] = unnest(a.value.value)
    val = d
  return val

def _string(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'string' recibe un parámetro")

  newValue = copy.deepcopy(values[0])
  newValue.value = str(unnest(newValue.value))
  newValue.type = 'string'
  return newValue

def _uppercase(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'uppercase' recibe un parámetro")

  ex = values[0]
  if ex.type!='string':
    return SemanticError(ex, "La función nativa 'uppercase' recibe un valor string")

  newValue = copy.deepcopy(ex)
  newValue.value = newValue.value.upper()
  return newValue

def _lowercase(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'lowercase' recibe un parámetro")

  ex = values[0]
  if ex.type!='string':
    return SemanticError(ex, "La función nativa 'lowercase' recibe un valor string")

  newValue = copy.deepcopy(ex)
  newValue.value = newValue.value.lower()
  return newValue

def _typeof(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'typeof' recibe un parámetro")

  ex = values[0]
  value = copy.deepcopy(ex)
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
  if len(values)>1: return SemanticError(values[0], "La función nativa 'pop' recibe un parámetro")

  arr = values[0]
  if arr.type!='array':
    return SemanticError(arr, "La función nativa 'pop' recibe un array")

  value = arr.value.pop()
  return value

def _length(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'length' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['string', 'array']:
    return SemanticError(ex, "La función nativa 'length' recibe un string o un array")

  newValue = copy.deepcopy(ex)
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
  'push': _push,
  'pop': _pop,
  'length': _length
}

def _suma(l:Value, r:Value):
  return l.value+r.value

def _resta(l:Value, r:Value):
  return l.value-r.value

def _multiplicacion(l:Value, r:Value):
  if l.type=='string': return l.value+r.value
  else: return l.value*r.value

def _division(l:Value, r:Value):
  return l.value/r.value

def _modulo(l:Value, r:Value):
  return l.value%r.value

def _potencia(l:Value, r:Value):
  if l.type=='string': return l.value*r.value
  else: return l.value**r.value

def _negacion(l:Value):
  return -l.value

def _menor(l:Value, r:Value):
  return l.value<r.value

def _menor_igual(l:Value, r:Value):
  return l.value<=r.value

def _mayor(l:Value, r:Value):
  return l.value>r.value

def _mayor_igual(l:Value, r:Value):
  return l.value>=r.value

def _igualacion(l:Value, r:Value):
  return l.value==r.value

def _diferenciacion(l:Value, r:Value):
  return l.value!=r.value

def _or(l:Value, r:Value):
  return l.value or r.value

def _and(l:Value, r:Value):
  return l.value and r.value

def _not(l:Value):
  return not l.value

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

BINARY_OPERATION_RESULTS = {
  'suma':{
    'int64':{
      'int64':'int64',
      'float64':'float64'
    },
    'float64':{
      'int64':'float64',
      'float64':'float64'
    }
  },
  'resta':{
    'int64':{
      'int64':'int64',
      'float64':'float64'
    },
    'float64':{
      'int64':'float64',
      'float64':'float64'
    }
  },
  'multiplicacion':{
    'int64':{
      'int64':'int64',
      'float64':'float64'
    },
    'float64':{
      'int64':'float64',
      'float64':'float64'
    },
    'string':{
      'string':'string'
    }
  },
  'division':{
    'int64':{
      'int64':'float64',
      'float64':'float64'
    },
    'float64':{
      'int64':'float64',
      'float64':'float64'
    }
  },
  'modulo':{
    'int64':{
      'int64':'int64',
      'float64':'float64'
    },
    'float64':{
      'int64':'float64',
      'float64':'float64'
    }
  },
  'potencia':{
    'int64':{
      'int64':'int64',
      'float64':'float64'
    },
    'float64':{
      'int64':'float64',
      'float64':'float64'
    },
    'string':{
      'int64':'string'
    }
  },
  'menor':{
    'int64':{
      'int64':'bool',
      'float64':'bool'
    },
    'float64':{
      'int64':'bool',
      'float64':'bool'
    },
    'bool':{
      'bool':'bool'
    },
    'string':{
      'string':'bool'
    }
  },
  'menor_igual':{
    'int64':{
      'int64':'bool',
      'float64':'bool'
    },
    'float64':{
      'int64':'bool',
      'float64':'bool'
    },
    'bool':{
      'bool':'bool'
    },
    'string':{
      'string':'bool'
    }
  },
  'mayor':{
    'int64':{
      'int64':'bool',
      'float64':'bool'
    },
    'float64':{
      'int64':'bool',
      'float64':'bool'
    },
    'bool':{
      'bool':'bool'
    },
    'string':{
      'string':'bool'
    }
  },
  'mayor_igual':{
    'int64':{
      'int64':'bool',
      'float64':'bool'
    },
    'float64':{
      'int64':'bool',
      'float64':'bool'
    },
    'bool':{
      'bool':'bool'
    },
    'string':{
      'string':'bool'
    }
  },
  'igualacion':{
    'int64':{
      'int64':'bool',
      'float64':'bool'
    },
    'float64':{
      'int64':'bool',
      'float64':'bool'
    },
    'bool':{
      'bool':'bool'
    },
    'string':{
      'string':'bool'
    }
  },
  'diferenciacion':{
    'int64':{
      'int64':'bool',
      'float64':'bool'
    },
    'float64':{
      'int64':'bool',
      'float64':'bool'
    },
    'bool':{
      'bool':'bool'
    },
    'string':{
      'string':'bool'
    }
  },
  'and':{
    'bool':{
      'bool':'bool'
    }
  },
  'or':{
    'bool':{
      'bool':'bool'
    }
  }
}

UNARY_OPERATION_RESULTS = {
  'negacion':{
    'int64':'int64',
    'float64':'float64'
  },
  'not':{
    'bool':'bool'
  }
}
