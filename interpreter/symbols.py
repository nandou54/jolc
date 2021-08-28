from datetime import datetime as _datetime

def Assignment(ln, col, scope, id, expression, type):
  return {"ln":ln, "col":col, 'i_type':'assignment', 'scope':scope, 'id':id, 'expression':expression, 'type':type}

def Assignment_Struct(ln, col, id, expression):
  return {"ln":ln, "col":col, 'i_type':'assignment_struct', 'id':id, 'expression':expression}

def Assignment_Array(ln, col, id, index, expression):
  return {"ln":ln, "col":col, 'i_type':'assignment_array', 'id':id, 'index':index, 'expression':expression}

def Function(ln, col, id, parameters, instructions):
  return {"ln":ln, "col":col, 'i_type':'function', 'id':id, 'parameters':parameters, 'instructions':instructions}

def Struct(ln, col, mutable, id, attributes):
  return {"ln":ln, "col":col, 'i_type':'struct', 'mutable':mutable, 'id':id, 'attributes':attributes}

def Attribute(ln, col, id, type):
  return {"ln":ln, "col":col, 'id':id, 'type':type}

def Expression(ln, col, operable, unary, l, r, type):
  return {"ln":ln, "col":col, 'i_type':'expression', 'operable':operable, 'unary':unary, 'type':type, 'l':l, 'r':r}

def Call(ln, col, id, expressions):
  return {"ln":ln, "col":col, 'i_type':'call', 'id':id, 'expressions':expressions}

def Access(ln, col, id, expression):
  return {"ln":ln, "col":col, 'i_type':'access', 'id':id, 'expression':expression}

def If(ln, col, expression, instructions, elseif):
  return {"ln":ln, "col":col, 'i_type':'if', 'expression':expression, 'instructions':instructions, 'elseif':elseif}

def Else(ln, col, instructions):
  return {"ln":ln, "col":col, 'i_type':'else', 'instructions':instructions}

def While(ln, col, expression, instructions):
  return {"ln":ln, "col":col, 'i_type':'while', 'expression':expression, 'instructions':instructions}

def For(ln, col, id, expression, instructions):
  return {"ln":ln, "col":col, 'i_type':'for', 'id':id, 'expression':expression, 'instructions':instructions}

def Break(ln, col):
  return {"ln":ln, "col":col, 'i_type':'break'}

def Continue(ln, col):
  return {"ln":ln, "col":col, 'i_type':'continue'}

def Return(ln, col, expression):
  return {"ln":ln, "col":col, 'i_type':'return', 'expression':expression}

def LexicalError(ln, col, description):
  return _Error(ln, col, 'Léxico', description)

def SyntacticError(ln, col, description):
  return _Error(ln, col, 'Sintáctico', description)

def SemanticError(ins, description):
  return _Error(ins['ln'], ins['col'], 'Semántico', description)

def _Error(ln, col, type, description):
  time = _datetime.today().strftime('%d/%m/%Y %H:%M:%S.%f')
  return {"ln":ln, "col":col, "type":type, "description":description, "time":time}

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
  '!':'not',
  '&&':'and',
  '||':'or',
  }
