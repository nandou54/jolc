from math import log10 as __log10, log as __log, sin as __sin, cos as __cos, tan as __tan, sqrt as __sqrt, trunc as __trunc
from .symbols import Value, _Error

output = ''
errors = []
symbols = []

envs = []
functions = []
loops = []

def getOutput(): return output

def getErrors(): return errors

def getSymbols(): return symbols

def reset():
  global output

  errors.clear()
  output = ''
  symbols.clear()

  functions.clear()
  loops.clear()
  envs.clear()

def SemanticError(ins, description):
  errors.append(_Error(ins.ln, ins.col, 'Semántico', description))

class Environment():
  def __init__(self, id = 'global', parent = None) -> None:
    self.id = id
    self.parent = parent
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

def _print(values):
  global output
  string = ''

  for value in values:
    string+=_tostring(value.value)+' '

  string = string[0:-1]

  output+=string

def _println(values):
  global output
  string = ''

  for value in values:
    if value.type in ['int64', 'float64', 'bool', 'string', 'char']:
      string+=value.value
    else:
      string+=_string(value).value

    string+=''

  output+=string+'\n'

def _log10(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'log10' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'log10' recibe un valor numérico")

  newValue = ex.copy()
  newValue.type = 'float64'
  newValue.value = __log10(newValue.value)
  return newValue

def _log(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'log' recibe dos parámetros")

  base, ex = values[0], values[1]
  if base.type not in ['int64', 'float64'] or ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'log' recibe dos valores numéricos")

  newValue = ex.copy()
  newValue.type = 'float64'
  newValue.value = __log(newValue.value, base.value)
  return newValue

def _sin(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'sin' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'sin' recibe un valor numérico")

  newValue = ex.copy()
  newValue.type = 'float64'
  newValue.value = __sin(newValue.value)
  return newValue

def _cos(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'cos' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'cos' recibe un valor numérico")

  newValue = ex.copy()
  newValue.type = 'float64'
  newValue.value = __cos(newValue.value)
  return newValue

def _tan(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'tan' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'tan' recibe un valor numérico")

  newValue = ex.copy()
  newValue.type = 'float64'
  newValue.value = __tan(newValue.value)
  return newValue

def _sqrt(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'sqrt' recibe un parámetro")

  ex = values[0]
  if ex.type not in ['int64', 'float64']:
    return SemanticError(ex, "La función nativa 'sqrt' recibe un valor numérico")

  newValue = ex.copy()
  newValue.type = 'float64'
  newValue.value = __sqrt(newValue.value)
  return newValue

def _parse():
  pass

def _trunc(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'trunc' recibe un parámetro")

  ex = values[0]
  if ex.type!='float64':
    return SemanticError(ex, "La función nativa 'trunc' recibe un valor float64")

  newValue = ex.copy()
  newValue.type = 'int64'
  newValue.value = int(newValue.value)
  return newValue

def _float(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'float' recibe un parámetro")

  ex = values[0]
  if ex.type!='int64':
    return SemanticError(ex, "La función nativa 'trunc' recibe un valor int64")

  newValue = ex.copy()
  newValue.type = 'float64'
  newValue.value = float(newValue.value)
  return newValue

def _tostring(val):
  if type(val) is list:
    for i in range(len(val)-1):
      val[i] = _tostring(val)
  return str(val)

def _string(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'string' recibe un parámetro")

  newValue = values[0].copy()
  newValue.type = 'string'
  newValue.value = _tostring(newValue.value)
  return newValue

def _uppercase(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'uppercase' recibe un parámetro")

  ex = values[0]
  if ex.type!='string':
    return SemanticError(ex, "La función nativa 'uppercase' recibe un valor string")

  newValue = ex.copy()
  newValue.value = newValue.value.upper()
  return newValue

def _lowercase(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'lowercase' recibe un parámetro")

  ex = values[0]
  if ex.type!='string':
    return SemanticError(ex, "La función nativa 'lowercase' recibe un valor string")

  newValue = ex.copy()
  newValue.value = newValue.value.upper()
  return newValue

def _typeof(values):
  if len(values)>1: return SemanticError(values[0], "La función nativa 'typeof' recibe un parámetro")

  ex = values[0]
  value = ex.copy()
  value.value = value.type
  value.type = 'string'
  return value

def _push(values):
  if len(values)>2: return SemanticError(values[0], "La función nativa 'push' recibe dos parámetros")

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
  if len(values)>1: return SemanticError(values[0], "La función nativa 'sin' recibe un parámetro")

  arr = values[0]
  if arr.type!='array':
    return SemanticError(arr, "La función nativa 'length' recibe un array")

  value = arr.copy()
  value.type = 'int64'
  value.value = len(arr.value)
  return value

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
  'or':{
    'bool':'bool'
  }
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

OPERATIONS = {
  'suma': _suma,
  'resta':_resta,
  'multiplicacion':_multiplicacion,
  'division':_division,
  'modulo':_modulo,
  'potencia':_potencia,
  'negacion':_negacion,
  'menor':_menor,
  'menor_igual':_menor_igual,
  'mayor':_mayor,
  'mayor_igual':_mayor_igual,
  'igualacion':_igualacion,
  'diferenciacion':_diferenciacion,
  'or':_or,
  'and':_and,
  'not':_not
}
