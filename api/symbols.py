from datetime import datetime as _datetime
from typing import List, Type

class Assignment:
  def __init__(self, ln, col, id, ex, scope, type):
    self.ln = ln
    self.col = col
    self.id = id
    self.ex:Expression = ex
    self.scope = scope
    self.type = type

class Function:
  def __init__(self, ln, col, id, parameters, types, ins):
    self.ln = ln
    self.col = col
    self.id = id
    self.parameters = parameters
    self.types = types
    self.ins:T_SENTENCE = ins
    self.env = None

class Struct:
  def __init__(self, ln, col, id, mutable, attributes):
    self.ln = ln
    self.col = col
    self.id = id
    self.mutable = mutable
    self.attributes:Type[List[Attribute]] = attributes

  def getAttribute(self, id):
    for a in self.attributes:
      if a.id.value==id: return a
    return None

class Attribute:
  def __init__(self, ln, col, id, type):
    self.ln = ln
    self.col = col
    self.id = id
    self.type = type
    self.value = None

class Expression:
  def __init__(self, ln, col, unary, expressionType, left, right):
    self.ln = ln
    self.col = col
    self.unary = unary
    self.type = expressionType
    self.left:Expression = left
    self.right:Expression = right

class Value:
  def __init__(self, ln, col, value, type):
    self.ln = ln
    self.col = col
    self.value = value
    self.type = type

class Call:
  def __init__(self, ln, col, id, expressions):
    self.ln = ln
    self.col = col
    self.id = id
    self.expressions = expressions

class If:
  def __init__(self, ln, col, ex, ins, elseif):
    self.ln = ln
    self.col = col
    self.ex:Expression = ex
    self.ins:T_SENTENCE = ins
    self.elseif = elseif

class Else:
  def __init__(self, ln, col, ins):
    self.ln = ln
    self.col = col
    self.ins:T_SENTENCE = ins

class While:
  def __init__(self, ln, col, ex, ins):
    self.ln = ln
    self.col = col
    self.ex:Expression = ex
    self.ins:T_SENTENCE = ins

class For:
  def __init__(self, ln, col, id, ex, ins):
    self.ln = ln
    self.col = col
    self.id = id
    self.ex:Expression = ex
    self.ins:T_SENTENCE = ins

class Break:
  def __init__(self, ln, col):
    self.ln = ln
    self.col = col

class Continue:
  def __init__(self, ln, col):
    self.ln = ln
    self.col = col

class Return:
  def __init__(self, ln, col, ex):
    self.ln = ln
    self.col = col
    self.ex:Expression = ex

EXECUTABLE_SENTENCE = [Assignment, Function, Struct, Call, If, While, For]

SENTENCE = EXECUTABLE_SENTENCE + [Break, Continue, Return]

T_SENTENCE = type(SENTENCE)

def Error(ln, col, type, description):
  time = _datetime.today().strftime('%d/%m/%Y %H:%M:%S')
  return [time, ln, col, type, description]

operations = {
  '+':'suma',
  '-':'resta',
  '*':'multiplicacion',
  '/':'division',
  '%':'modulo',
  '^':'potencia',
  '<':'menor',
  '<=':'menor_igual',
  '>':'mayor',
  '>=':'mayor_igual',
  '==':'igualacion',
  '!=':'diferenciacion',
  '&&':'and',
  '||':'or'
  }
