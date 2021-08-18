def Asignacion(scope, id, expresion, tipo):
  return {'i':'asignacion', 'scope':scope, 'id':id, 'expresion':expresion, 'tipo':tipo}

def Funcion(id, parametros):
  return {'i':'funcion', 'id':id, 'parametros':parametros}

def Struct(mutable, id, atributos):
  return {'i':'struct', 'mutable':mutable, 'id':id, 'atributos':atributos}

def Atributo(id, tipo):
  return {'id':id, 'tipo':tipo}

def Expresion(operable, unaria, izq, der, tipo):
  return {'i':'expresion', 'operable':operable, 'unaria':unaria, 'izq':izq, 'der':der, 'tipo':tipo}

def Llamada(id, expresiones):
  return {'i':'llamada', 'id':id, 'expresiones':expresiones}

def Acceso_arreglo(id, expresion):
  return {'i':'acceso', 'id':id, 'expresion':expresion}

def If(expresion, instrucciones, elseif):
  return {'i':'if', 'expresion':expresion, 'instrucciones':instrucciones, 'elseif':elseif}

def Else(instrucciones):
  return {'i':'else', 'instrucciones':instrucciones}

def While(expresion, instrucciones):
  return {'i':'while', 'expresion':expresion, 'instrucciones':instrucciones}

def For(id, expresion, instrucciones):
  return {'i':'for', 'id':id, 'expresion':expresion, 'instrucciones':instrucciones}

def Break():
  return {'i':'break'}

def Continue():
  return {'i':'continue'}

def Return(expresion):
  return {'i':'return', 'expresion':expresion}

operaciones = {
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
