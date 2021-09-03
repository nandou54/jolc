from .symbols import Assignment, Expression, Function, Struct, Call, If, While, For, Return, Break, Continue

def graphAST(parsed):
  s = '''digraph G {
		nodesep=0.4;
		ranksep=0.5;

    node__ [fontsize=13 fontname = "helvetica" label="ins.ins"];'''

  s+=printInstructions(parsed, 'node__')
  s+='}'

  return s

def printInstructions(INS, backNode = ''):
  s = ''

  for sen in INS:
    name = nodeName(sen)
    s+=printNode(name, senType(sen))
    s+=linkNodes(backNode, name)
    s+=executables(sen, backNode)

  return s

def printNode(name, label):
  return '''{} [fontsize=13 fontname = "helvetica" label="{}"];\n'''.format(name, label)

def nodeName(sen):
  return '{}_{}_{}'.format(senType(sen), sen.ln, sen.col)

def linkNodes(backNode, nextNode):
  return '{} -> {};\n'.format(backNode, nextNode)

def printExpression(sen:Expression, backNode, dif=''):
  s = ''

  if sen.Tipo not in ['int', 'double', 'char', 'string', 'boolean', 'id', 'vector', 'list']:
    name = nodeName(sen)
    s += printNode(name, '''Primitivo <{Operacion.Tipo}>\\n{Operacion.Valor}''')
    s += linkNodes(backNode, name)
    return s

  if sen.type== 'Llamada':
    name = nodeName(sen)
    s += printNode(name, '''Llamada\\n{Operacion.ID}''')
    s += printCall(name, sen)
    s += linkNodes(backNode, name)
  if sen.type== 'Acceso_vector':
    name = nodeName(sen)
    s += printNode(name, '''Acceso a vector\\n{Operacion.ID}''')
    # temp_str += printAccesoVector(name, Operacion)
    s += linkNodes(backNode, name)
  else:
    name = nodeName(sen)
    s += printNode(name, '''Operacion {Operacion.Tipo}''')
    s += linkNodes(backNode, name)
    s += printExpression(sen.Izquierda, name, 'i')
    if sen.r: s += printExpression(sen.Derecha, name, 'd')

  return s

def printAssignment(sen:Assignment, backNode):
  s = ''

  name = nodeName(sen)
  s += printNode(name, 'ID\\n{ID}'.format(sen.id.value))
  s += linkNodes(backNode, name)

  name = nodeName(sen)
  s += printNode(name, 'Expresion')
  s += printExpression(sen.ex, name)
  s += linkNodes(backNode, name)

  return s

def printStructAssignment(sen:StructAssignment, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, 'Tipo: {ID}')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Índice''')
  # temp_str += printExpression(sen.index, name)
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Expresion''')
  # temp_str += printExpression(sen.ex, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printArrayAssignment(sen:ArrayAssignment, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''Tipo: {ID}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Índice''')
  temp_str += printExpression(sen.index, name)
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Expresion''')
  temp_str += printExpression(sen.ex, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printFunction(sen:Function, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''ID\\n{ID}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Tipo\\n{Tipo_retorno}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''ins.ins''')
  temp_str += printInstructions(sen.ins, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printStruct(sen:Struct, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''ID\\n{ID}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Tipo\\n{Tipo_retorno}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''ins.ins''')
  temp_str += printInstructions(sen.ins, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printCall(sen:Call, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''ID\\n{ID}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Parametros''')
  temp_str += linkNodes(backNode, name)

  for Parametro in sen.parametros:
    temp_str += printExpression(Parametro, name)

  return temp_str

def printAccess(sen:Access, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''Tipo: {ID}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Índice''')
  temp_str += printExpression(sen.index, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printIf(sen:If, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''Condicion''')
  temp_str += printExpression(sen.ex, name)
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''ins.ins true''')
  temp_str += printInstructions(sen.ins, name)
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''ins.ins false''')
  # temp_str += printInstructions(Instrucciones_false, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printWhile(sen:While, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''Condicion''')
  temp_str += printExpression(sen.ex, name)
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''ins.ins''')
  temp_str += printInstructions(sen.ins, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printFor(sen:For, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''Tipo: Inicializacion''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Tipo: Condicion''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Tipo: Actualizacion''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''ins.ins''')
  temp_str += linkNodes(backNode, name)
  temp_str += printInstructions(sen.ins, name)

  return temp_str

def printBreak(sen:Break, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''Sentencia Break''')
  temp_str += linkNodes(backNode, name)

  return temp_str

def printContinue(sen:Continue, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''Sentencia Continue''')
  temp_str += linkNodes(backNode, name)

  return temp_str

def printReturn(sen:Return, backNode):
  temp_str = ''

  name = nodeName(sen)
  temp_str += printNode(name, '''Sentencia Return''')
  temp_str += linkNodes(backNode, name)

  name = nodeName(sen)
  temp_str += printNode(name, '''Expresion''')
  temp_str += printExpression(sen.ex, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def executables(sen, backNode):
  T = type(sen)
  if T is Assignment: return printAssignment(sen, backNode)
  if T is StructAssignment: return printStructAssignment(sen, backNode)
  if T is ArrayAssignment: return printArrayAssignment(sen, backNode)
  if T is Function: return printFunction(sen, backNode)
  if T is Struct: return printStruct(sen, backNode)
  if T is Call: return printCall(sen, backNode)
  if T is Access: return printAccess(sen, backNode)
  if T is If: return printIf(sen, backNode)
  if T is While: return printWhile(sen, backNode)
  if T is For: return printFor(sen, backNode)
  if T is Return: return printFor(sen, backNode)
  if T is Break: return printBreak(sen, backNode)
  if T is Continue: return printContinue(sen, backNode)

def senType(ins):
  T = type(ins)
  if T is Assignment: return 'Asignacion'
  if T is StructAssignment: return 'Asignacion_struct'
  if T is ArrayAssignment: return 'Asignacion_array'
  if T is Function: return 'Funcion'
  if T is Struct: return 'Struct'
  if T is Call: return 'Llamada'
  if T is Access: return 'Access'
  if T is If: return 'If'
  if T is While: return 'While'
  if T is For: return 'For'
  if T is Return: return 'Return'
  if T is Break: return 'Break'
  if T is Continue: return 'Continue'
