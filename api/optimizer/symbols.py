class Function:
  def __init__(self, ln, col, id, ins):
    self.ln = ln
    self.col = col
    self.id = id
    self.ins = ins

class Expression:
  def __init__(self, ln, col, unary, type, left, right):
    self.ln = ln
    self.col = col
    self.unary = unary
    self.type = type
    self.left:Expression = left
    self.right:Expression = right
    self.owner = None

  def __str__(self):
    return f'{self.left}{operators[self.type]}{self.right}'

class Number:
  def __init__(self, ln, col, value):
    self.ln = ln
    self.col = col
    self.value = value

  def __str__(self):
    return str(self.value)

class String:
  def __init__(self, ln, col, value):
    self.ln = ln
    self.col = col
    self.value = value

  def __str__(self):
    return self.value

class Id:
  def __init__(self, ln, col, value):
    self.ln = ln
    self.col = col
    self.value = value
    self.wrappers = []

  def __str__(self):
    s = self.value
    for w in self.wrappers:
      s = w.id + f'({s})' if w.type=='call' else f'[{s}]'
    return s

class Wrapper:
  def __init__(self, ln, col, id, type):
    self.ln = ln
    self.col = col
    self.id = id
    self.type = type

class Assignment:
  def __init__(self, ln, col, id, ex):
    self.ln = ln
    self.col = col
    self.id = id
    self.ex:Expression = ex
    self.owner = None
    self.deleted = False

  def __str__(self):
    return f'{self.id}={self.ex};'

class Tag:
  def __init__(self, ln, col, id):
    self.ln = ln
    self.col = col
    self.id = id
    self.owner = None
    self.deleted = False

  def __str__(self):
    return f'{self.id}:'

class Goto:
  def __init__(self, ln, col, tag):
    self.ln = ln
    self.col = col
    self.tag = tag
    self.owner = None
    self.deleted = False

  def __str__(self):
    return f'goto {self.tag};'

class Call:
  def __init__(self, ln, col, id):
    self.ln = ln
    self.col = col
    self.id = id
    self.owner = None

  def __str__(self):
    return f'{self.id}();'

class If:
  def __init__(self, ln, col, ex, goto):
    self.ln = ln
    self.col = col
    self.ex = ex
    self.goto = goto
    self.owner = None
    self.deleted = False

  def __str__(self):
    return f'if({self.ex}){{{self.goto}}}'

class Return:
  def __init__(self, ln, col):
    self.ln = ln
    self.col = col
    self.owner = None

  def __str__(self):
    return 'return;'

class Library:
  def __init__(self, ln, col, lexeme):
    self.ln = ln
    self.col = col
    self.lexeme = lexeme
    self.owner = None

  def __str__(self):
    return f'{self.lexeme};'

operations = {
  '+':'suma',
  '-':'resta',
  '*':'multiplicacion',
  '/':'division',
  '%':'modulo',
  '<':'menor',
  '<=':'menor_igual',
  '>':'mayor',
  '>=':'mayor_igual',
  '==':'igualacion',
  '!=':'diferenciacion'
}

operators = {
  'suma':'+',
  'resta':'-',
  'multiplicacion':'*',
  'division':'/',
  'modulo':'%',
  'menor':'<',
  'menor_igual':'<=',
  'mayor':'>',
  'mayor_igual':'>=',
  'igualacion':'==',
  'diferenciacion':'!='
}
