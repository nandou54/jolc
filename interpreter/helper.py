def graphAST(parsed):
  s = '''digraph G {
		nodesep=0.4;
		ranksep=0.5;

    node__ [fontsize=13 fontname = "helvetica" label="ins.ins"];'''

  s+=printInstructions(parsed, 'node__')
  s+='}'

  return s

def printInstructions(INS, backNode = ''):
  tempStr = ''

  for sen in INS:
    name = nodeName(sen.Tipo, sen.ln, sen.col)
    tempStr+=printNode(name, sen.Tipo)
    tempStr+=linkNodes(backNode, name)
    tempStr+=print[sen.Tipo](name, sen)

  return tempStr

def printNode(node, text):
  return '''${} [fontsize=13 fontname = "helvetica" label="${}"];\n'''.format(node, text)

def nodeName(Tipo, ins):
  return '${}_${}_${}'.format(Tipo, ins.ln, ins.col)

def linkNodes(backNode, nexNode):
  return '${} -> ${};\n'.format(backNode, nexNode)

def printOperacion(Operacion, backNode, dif):
  temp_str = ''

  if Operacion.Tipo not in ['int', 'double', 'char', 'string', 'boolean', 'id', 'vector', 'list']:
    name = nodeName('Primitivo', Operacion.ins.ln, Operacion.ins.col)
    temp_str += printNode(name, '''Primitivo <${Operacion.Tipo}>\\n${Operacion.Valor}''')
    temp_str += linkNodes(backNode, name)
    return temp_str

  if Operacion.type== 'Llamada':
    name = nodeName('Llamada', Operacion.ins.ln, Operacion.ins.col)
    temp_str += printNode(name, '''Llamada\\n${Operacion.ID}''')
    temp_str += printLlamada(name, Operacion)
    temp_str += linkNodes(backNode, name)
  if Operacion.type== 'Acceso_vector':
    name = nodeName('Acceso_vector', Operacion.ins.ln, Operacion.ins.col)
    temp_str += printNode(name, '''Acceso a vector\\n${Operacion.ID}''')
    # temp_str += printAccesoVector(name, Operacion)
    temp_str += linkNodes(backNode, name)
  else:
    name = nodeName(Operacion.Tipo + dif, Operacion.ins.ln, Operacion.ins.col)
    temp_str += printNode(name, '''Operacion ${Operacion.Tipo}''')
    temp_str += linkNodes(backNode, name)
    temp_str += printOperacion(Operacion.Izquierda, name, 'i')
    if Operacion.r: temp_str += printOperacion(Operacion.Derecha, name, 'd')

  return temp_str

def printAsignacion(backNode, ins):
  temp_str = ''

  name = nodeName('ID', ins.ln, ins.col)
  temp_str += printNode(name, '''ID\\n${ID}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName('Expresion', ins.ln, ins.col)
  temp_str += printNode(name, '''Expresion''')
  temp_str += printOperacion(ins.ex, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printFuncion(backNode, ins):
  temp_str = ''

  name = nodeName('ID', ins.ln, ins.col)
  temp_str += printNode(name, '''ID\\n${ID}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName('Tipo_retorno', ins.ln, ins.col)
  temp_str += printNode(name, '''Tipo\\n${Tipo_retorno}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName('ins.ins', ins.ln, ins.col)
  temp_str += printNode(name, '''ins.ins''')
  temp_str += printInstructions(ins.ins, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printLlamada(backNode, ins):
  temp_str = ''

  name = nodeName('ID', ins.ln, ins.col)
  temp_str += printNode(name, '''ID\\n${ID}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName('Parametros', ins.ln, ins.col)
  temp_str += printNode(name, '''Parametros''')
  temp_str += linkNodes(backNode, name)

  for Parametro in ins.parametros:
    temp_str += printOperacion(Parametro, name)

  return temp_str

def printAccesoLista(backNode, ins):
  temp_str = ''

  name = nodeName('ID', ins.ln, ins.col)
  temp_str += printNode(name, '''Tipo: ${ID}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName('Index', ins.ln, ins.col)
  temp_str += printNode(name, '''Índice''')
  temp_str += printOperacion(ins.index, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printModificacionLista(backNode, ins):
  temp_str = ''

  name = nodeName('ID', ins.ln, ins.col)
  temp_str += printNode(name, '''Tipo: ${ID}''')
  temp_str += linkNodes(backNode, name)

  name = nodeName('Index', ins.ln, ins.col)
  temp_str += printNode(name, '''Índice''')
  temp_str += printOperacion(ins.index, name)
  temp_str += linkNodes(backNode, name)

  name = nodeName('Expresion', ins.ln, ins.col)
  temp_str += printNode(name, '''Expresion''')
  temp_str += printOperacion(ins.ex, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printIf(backNode, ins):
  temp_str = ''

  name = nodeName('Condicion', ins.ln, ins.col)
  temp_str += printNode(name, '''Condicion''')
  temp_str += printOperacion(ins.ex, name)
  temp_str += linkNodes(backNode, name)

  name = nodeName('Instrucciones_true', ins.ln, ins.col)
  temp_str += printNode(name, '''ins.ins true''')
  temp_str += printInstructions(ins.ins, name)
  temp_str += linkNodes(backNode, name)

  name = nodeName('Instrucciones_false', ins.ln, ins.col)
  temp_str += printNode(name, '''ins.ins false''')
  # temp_str += printInstructions(Instrucciones_false, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printWhile(backNode, ins):
  temp_str = ''

  name = nodeName('Condicion', ins.ln, ins.col)
  temp_str += printNode(name, '''Condicion''')
  temp_str += printOperacion(ins.ex, name)
  temp_str += linkNodes(backNode, name)

  name = nodeName('ins.ins', ins.ln, ins.col)
  temp_str += printNode(name, '''ins.ins''')
  temp_str += printInstructions(ins.ins, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

def printFor(backNode, ins):
  temp_str = ''

  name = nodeName('Inicializacion', ins.ln, ins.col)
  temp_str += printNode(name, '''Tipo: Inicializacion''')
  temp_str += linkNodes(backNode, name)

  name = nodeName('Condicion', ins.ln, ins.col)
  temp_str += printNode(name, '''Tipo: Condicion''')
  temp_str += linkNodes(backNode, name)

  name = nodeName('Actualizacion', ins.ln, ins.col)
  temp_str += printNode(name, '''Tipo: Actualizacion''')
  temp_str += linkNodes(backNode, name)

  name = nodeName('ins.ins', ins.ln, ins.col)
  temp_str += printNode(name, '''ins.ins''')
  temp_str += linkNodes(backNode, name)
  temp_str += printInstructions(ins.ins, name)

  return temp_str

def printBreak(backNode, ins):
  temp_str = ''

  name = nodeName('Break', ins.ln, ins.col)
  temp_str += printNode(name, '''Sentencia Break''')
  temp_str += linkNodes(backNode, name)

  return temp_str

def printContinue(backNode, ins):
  temp_str = ''

  name = nodeName('Continue', ins.ln, ins.col)
  temp_str += printNode(name, '''Sentencia Continue''')
  temp_str += linkNodes(backNode, name)

  return temp_str

def printReturn(backNode, ins):
  temp_str = ''

  name = nodeName('Return', ins.ln, ins.col)
  temp_str += printNode(name, '''Sentencia Return''')
  temp_str += linkNodes(backNode, name)

  name = nodeName('Expresion', ins.ln, ins.col)
  temp_str += printNode(name, '''Expresion''')
  temp_str += printOperacion(ins.ex, name)
  temp_str += linkNodes(backNode, name)

  return temp_str

print = {
  "Asignacion": printAsignacion,
  "Funcion": printFuncion,
  "Llamada": printLlamada,
  "Modificacion_lista": printModificacionLista,
  "If": printIf,
  "While": printWhile,
  "For": printFor,
  "Break": printBreak,
  "Continue": printContinue,
  "Return": printReturn
}
