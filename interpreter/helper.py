from .symbols import Assignment, Else, Expression, Function, Struct, Call, If, Value, While, For, Return, Break, Continue

def graphAST(parsed):
  s = '''digraph G {
		nodesep=0.4;
		ranksep=0.5;

    node__ [fontsize=13 fontname = "helvetica" label="Instrucciones"];'''

  s+=printInstructions(parsed, 'node__')
  s+='}'

  return s

def printInstructions(INS, backNode = ''):
  s = ''

  for sen in INS:
    node = nodeName(sen)
    s+=printNode(node, senType(sen))
    s+=linkNodes(backNode, node)

    if type(sen) in [Continue, Break]: continue

    s+=execute(sen, node)

  return s

def printNode(node, label):
  return '{} [fontsize=13 fontname = "helvetica" label="{}"];\n'.format(node, label)

def nodeName(sen, extra=''):
  return '{}_{}_{}_{}'.format(senType(sen), sen.ln, sen.col, extra)

def linkNodes(backNode, nextNode):
  return '{} -> {};\n'.format(backNode, nextNode)

def printExpression(ex:Expression, backNode):
  s = ''
  if not ex: return s

  node = nodeName(ex)
  s += linkNodes(backNode, node)

  if type(ex) is Call:
    s += printNode(node, 'Llamada')
    s += printCall(ex, node)
  elif ex.type=='id':
    s += printNode(node, 'ID\\n{}'.format(ex.value))
  elif ex.type=='array':
    s += printNode(node, 'Arreglo')
    for val in ex.value:
      valueNode = nodeName(val)
      s += printExpression(valueNode, val.value)
      s += linkNodes(node, valueNode)
  elif ex.type=='access':
    s += printNode(node, 'Acceso')
  elif ex.type=='chain':
    s += printNode(node, 'Chain')

    exNode = nodeName(ex, 'l')
    s += printNode(exNode, 'Izquierda')
    s += linkNodes(node, exNode)
    s += printExpression(ex.left, exNode)

    exNode = nodeName(ex, 'r')
    s += printNode(exNode, 'ID\\n{}'.format(ex.right.value))
    s += linkNodes(node, exNode)
  elif ex.type=='range':
    s += printNode(node, 'Rango')

    if ex.left:
      exNode = nodeName(ex, 'l')
      s += printNode(exNode, 'Izquierda')
      s += linkNodes(node, exNode)
      s += printExpression(ex.left, exNode)

      exNode = nodeName(ex, 'r')
      s += printNode(exNode, 'Índice')
      s += linkNodes(node, exNode)
      s += printExpression(ex.right, exNode)
    else:
      exNode = nodeName(ex, 'v')
      s += printNode(exNode, 'Vacío')
      s += linkNodes(node, exNode)

  elif ex.type=='ternary':
    s += printNode(node, 'Ternaria')

    exNode = nodeName(ex, 'con')
    s += printNode(exNode, 'Condición')
    s += linkNodes(node, exNode)
    s += printExpression(ex.left, exNode)

    exNode = nodeName(ex, 'l')
    s += printNode(exNode, 'Verdadero')
    s += linkNodes(node, exNode)
    s += printExpression(ex.left, exNode)

    exNode = nodeName(ex, 'r')
    s += printNode(exNode, 'Falso')
    s += linkNodes(node, exNode)
    s += printExpression(ex.right, exNode)
  elif ex.type=='string':
    s += printNode(node, 'string')
    for val in ex.value:
      valueNode = nodeName(val)
      if val.type=='string': printNode(valueNode, val.value)
      else: s += printExpression(val, valueNode)
      s += linkNodes(node, valueNode)
  elif type(ex) is Value:
    s += printNode(node, '<{}>\\n{}'.format(ex.type, ex.value))
  else:
    node = nodeName(ex)
    s += printNode(node, 'Operacion {}'.format(ex.type))

    exNode = nodeName(ex, 'l')
    s += printNode(exNode, 'Izquierda')
    s += linkNodes(node, exNode)
    s += printExpression(ex.left, exNode)

    if ex.right:
      exNode = nodeName(ex, 'r')
      s += printNode(exNode, 'Derecha')
      s += linkNodes(node, exNode)
      s += printExpression(ex.right, exNode)

  return s

def printAssignment(sen:Assignment, backNode):
  s = ''

  node = nodeName(sen, 'id')
  s += linkNodes(backNode, node)
  if sen.id.type=='id':
    s += printNode(node, 'ID\\n{}'.format(sen.id.value))
  else:
    s += printNode(node, 'ID')
    s += printExpression(sen.id, node)


  node = nodeName(sen, 'ex')
  s += printNode(node, 'Expresión')
  s += linkNodes(backNode, node)
  s += printExpression(sen.ex, node)

  if sen.scope:
    node = nodeName(sen, 'scope')
    s += printNode(node, 'Scope')
    s += linkNodes(backNode, node)

  if sen.type:
    node = nodeName(sen, 'type')
    s += printNode(node, 'Tipo')
    s += linkNodes(backNode, node)

  return s

def printFunction(sen:Function, backNode):
  s = ''

  node = nodeName(sen, 'id')
  s += printNode(node, 'ID\\n{}'.format(sen.id.value))
  s += linkNodes(backNode, node)

  if sen.parameters:

    node = nodeName(sen, 'par')
    s += printNode(node, 'Parámetros')
    s += linkNodes(backNode, node)

    for parameter in sen.parameters:
      parNode = nodeName(parameter)
      s += printNode(parNode, 'ID\\n{}'.format(parameter.value))
      s += linkNodes(node, parNode)

  node = nodeName(sen, 'ins')
  s += printNode(node, 'Instrucciones')
  s += linkNodes(backNode, node)
  s += printInstructions(sen.ins, node)

  return s

def printStruct(sen:Struct, backNode):
  s = ''

  node = nodeName(sen, 'id')
  s += printNode(node, 'ID\\n{}'.format(sen.id.value))
  s += linkNodes(backNode, node)

  node = nodeName(sen, 'mut')
  s += printNode(node, 'mutable' if sen.mutable else 'inmutable')
  s += linkNodes(backNode, node)

  node = nodeName(sen, 'atr')
  s += printNode(node, 'Atributos')
  s += linkNodes(backNode, node)

  for attribute in sen.attributes:
    atrNode = nodeName(attribute)
    s += printNode(atrNode, 'ID\\n{}'.format(attribute.id.value))
    s += linkNodes(node, atrNode)

    if attribute.type:
      typeNode = nodeName(attribute, 'tipo')
      s += printNode(typeNode, 'Tipo {}'.format(attribute.type))
      s += linkNodes(atrNode, typeNode)

  return s

def printCall(sen:Call, backNode):
  s = ''

  node = nodeName(sen, 'id')
  s += printNode(node, 'ID\\n{}'.format(sen.id.value))
  s += linkNodes(backNode, node)

  if sen.expressions:
    node = nodeName(sen, 'par')
    s += printNode(node, 'Parametros')
    s += linkNodes(backNode, node)

    for ex in sen.expressions:
      s += printExpression(ex, node)

  return s

def printIf(sen:If, backNode):
  s = ''

  node = nodeName(sen, 'ex')
  s += printNode(node, 'Condición')
  s += linkNodes(backNode, node)
  s += printExpression(sen.ex, node)

  node = nodeName(sen, 'ins')
  s += printNode(node, 'Instrucciones true')
  s += linkNodes(backNode, node)
  s += printInstructions(sen.ins, node)

  if sen.elseif:
    node = nodeName(sen, 'else')

    if type(sen.elseif) is Else:
      s += printNode(node, 'Instrucciones false')
      s += linkNodes(backNode, node)
      s += printInstructions(sen.elseif.ins, node)
    else:
      s += printNode(node, 'If')
      s += linkNodes(backNode, node)
      s += printIf(sen.elseif, node)

  return s

def printWhile(sen:While, backNode):
  s = ''

  node = nodeName(sen, 'ex')
  s += printNode(node, 'Condición')
  s += linkNodes(backNode, node)
  s += printExpression(sen.ex, node)

  node = nodeName(sen, 'ins')
  s += printNode(node, 'Instrucciones')
  s += linkNodes(backNode, node)
  s += printInstructions(sen.ins, node)

  return s

def printFor(sen:For, backNode):
  s = ''
  node = nodeName(sen, 'id')
  s += printNode(node, 'ID\\n{}'.format(sen.id.value))
  s += linkNodes(backNode, node)

  node = nodeName(sen, 'ite')
  s += printNode(node, 'Iterable')
  s += linkNodes(backNode, node)
  s += printExpression(sen.ex, node)

  node = nodeName(sen, 'ins')
  s += printNode(node, 'Instrucciones')
  s += linkNodes(backNode, node)
  s += printInstructions(sen.ins, node)

  return s

def printReturn(sen:Return, backNode):
  s = ''

  node = nodeName(sen, 'ex')
  s += printNode(node, 'Expresión')
  s += linkNodes(backNode, node)
  s += printExpression(sen.ex, node)

  return s

def execute(sen, backNode):
  T = type(sen)
  if T is Assignment: return printAssignment(sen, backNode)
  if T is Function: return printFunction(sen, backNode)
  if T is Struct: return printStruct(sen, backNode)
  if T is Call: return printCall(sen, backNode)
  if T is If: return printIf(sen, backNode)
  if T is While: return printWhile(sen, backNode)
  if T is For: return printFor(sen, backNode)
  if T is Return: return printReturn(sen, backNode)

def senType(ins):
  T = type(ins)
  if T is Assignment: return 'Asignación'
  if T is Function: return 'Función'
  if T is Struct: return 'Struct'
  if T is Call: return 'Llamada'
  if T is If: return 'If'
  if T is While: return 'While'
  if T is For: return 'For'
  if T is Return: return 'Return'
  if T is Break: return 'Break'
  if T is Continue: return 'Continue'
