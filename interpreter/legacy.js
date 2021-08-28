import s from './symbols.js'
import { copyArray } from '@/helper/util'

// ===================> CORE <========================

const reserved_functions = {
  print: (values) => {
    let temp = ''
    values.forEach((value) => {
      if (['int', 'string', 'char', 'boolean'].includes(value.Tipo))
        temp += value.Valor + ' '
      else if (value.Tipo === 'double')
        temp += value.Valor % 1 !== 0 ? value.Valor + ' ' : value.Valor.toFixed(2) + ' '
      else temp += `[${value.Valores.map((temp) => temp.Valor)}]`
    })

    to_print.push(temp)
  },
  tolower: (values) => {
    if (values.length !== 1)
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'toLower' únicamente recibe un parámetro`
      )
    if (values[0].Tipo !== 'string')
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'toLower' únicamente recibe cadenas`
      )

    let symbol = values[0]
    symbol.Valor = symbol.Valor.toLowerCase()
    return values[0]
  },
  toupper: (values) => {
    if (values.length > 1)
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'toUpper' únicamente recibe un parámetro`
      )
    if (values[0].Tipo !== 'string')
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'toUpper' únicamente recibe cadenas`
      )

    let symbol = values[0]
    symbol.Valor = symbol.Valor.toUpperCase()
    return values[0]
  },
  length: (values) => {
    if (values.length > 1)
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'Length' únicamente recibe un parámetro`
      )
    if (!['string', 'vector', 'list'].includes(values[0].Tipo))
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'Length' únicamente recibe cadenas, vectores o listas`
      )

    let symbol = values[0]
    let size = !['vector', 'list'].includes(symbol.Tipo)
      ? symbol.Valor.length
      : symbol.Valores.length
    return s.Simbolo(symbol.Linea, symbol.Columna, 'int', size)
  },
  truncate: (values) => {
    if (values.length > 1)
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'Truncate' únicamente recibe un parámetro`
      )
    if (!['int', 'double'].includes(values[0].Tipo))
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'Truncate' únicamente recibe números`
      )

    let symbol = values[0]
    symbol.Valor = Math.floor(symbol.Valor)
    return symbol
  },
  round: (values) => {
    if (values.length > 1)
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'Round' únicamente recibe un parámetro`
      )
    if (!['int', 'double'].includes(values[0].Tipo))
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'Round' únicamente recibe números`
      )

    let symbol = values[0]
    symbol.Valor = Math.round(symbol.Valor)
    return symbol
  },
  typeof: (values) => {
    if (values.length > 1)
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'TypeOf' solo recibe un parámetro`
      )

    let symbol = values[0]
    return s.Simbolo(symbol.Linea, symbol.Linea, 'string', symbol.Tipo)
  },
  tostring: (values) => {
    if (values.length > 1)
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'toString' solo recibe un parámetro`
      )

    let symbol = values[0]
    let str = !['vector', 'list'].includes(symbol.Tipo)
      ? symbol.Valor.toString()
      : `[${symbol.Valores.map((temp) => temp.Valor)}]`
    return s.Simbolo(symbol.Linea, symbol.Columna, 'string', str)
  },
  tochararray: (values) => {
    if (values.length > 1)
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'toCharArray' solo recibe un parámetro`
      )
    if (values[0].Tipo !== 'string')
      return Error(
        values[0].Linea,
        values[0].Columna,
        `La función 'toCharArray' únicamente recibe cadenas`
      )

    let symbol = values[0]
    return s.Lista(
      symbol.Linea,
      symbol.Columna,
      'char',
      '',
      'char',
      symbol.Valor.split('').map((value) => {
        return s.Simbolo(symbol.Linea, symbol.Columna, 'char', value)
      })
    )
  }
}

const default_values = {
  int: 0,
  double: 0.0,
  boolean: true,
  char: '\u0000',
  string: ''
}

const operation_results = {
  suma: {
    int: {
      int: 'int',
      double: 'double',
      boolean: 'int',
      char: 'int',
      string: 'string'
    },
    double: {
      int: 'double',
      double: 'double',
      boolean: 'double',
      char: 'double',
      string: 'string'
    },
    boolean: {
      int: 'int',
      double: 'double',
      string: 'string'
    },
    char: {
      int: 'int',
      double: 'double',
      char: 'string',
      string: 'string'
    },
    string: {
      int: 'string',
      double: 'string',
      boolean: 'string',
      char: 'string',
      string: 'string'
    }
  },
  resta: {
    int: {
      int: 'int',
      double: 'double',
      boolean: 'int',
      char: 'int'
    },
    double: {
      int: 'double',
      double: 'double',
      boolean: 'double',
      char: 'double'
    },
    boolean: {
      int: 'int',
      double: 'double'
    },
    char: {
      int: 'int',
      double: 'double'
    },
    string: {}
  },
  multiplicacion: {
    int: {
      int: 'int',
      double: 'double',
      char: 'int'
    },
    double: {
      int: 'double',
      double: 'double',
      char: 'double'
    },
    boolean: {},
    char: {
      int: 'int',
      double: 'double'
    },
    string: {}
  },
  division: {
    int: {
      int: 'double',
      double: 'double',
      char: 'double'
    },
    double: {
      int: 'double',
      double: 'double',
      char: 'double'
    },
    boolean: {},
    char: {
      int: 'double',
      double: 'double'
    },
    string: {}
  },
  potencia: {
    int: {
      int: 'int',
      double: 'double'
    },
    double: {
      int: 'double',
      double: 'double'
    },
    boolean: {},
    char: {},
    string: {}
  },
  modulo: {
    int: {
      int: 'double',
      double: 'double'
    },
    double: {
      int: 'double',
      double: 'double'
    },
    boolean: {},
    char: {},
    string: {}
  },
  igualacion: {
    int: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    double: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    boolean: {
      boolean: 'boolean'
    },
    char: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    string: {
      string: 'boolean'
    }
  },
  diferenciacion: {
    int: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    double: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    boolean: {
      boolean: 'boolean'
    },
    char: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    string: {
      string: 'boolean'
    }
  },
  menor: {
    int: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    double: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    boolean: {
      boolean: 'boolean'
    },
    char: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    string: {
      string: 'boolean'
    }
  },
  menorigual: {
    int: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    double: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    boolean: {
      boolean: 'boolean'
    },
    char: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    string: {
      string: 'boolean'
    }
  },
  mayor: {
    int: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    double: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    boolean: {
      boolean: 'boolean'
    },
    char: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    string: {
      string: 'boolean'
    }
  },
  mayorigual: {
    int: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    double: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    boolean: {
      boolean: 'boolean'
    },
    char: {
      int: 'boolean',
      double: 'boolean',
      char: 'boolean'
    },
    string: {
      string: 'boolean'
    }
  },
  or: {
    int: {
      int: 'boolean',
      double: 'boolean',
      boolean: 'boolean',
      char: 'boolean',
      string: 'boolean'
    },
    double: {
      int: 'boolean',
      double: 'boolean',
      boolean: 'boolean',
      char: 'boolean',
      string: 'boolean'
    },
    boolean: {
      int: 'boolean',
      double: 'boolean',
      boolean: 'boolean',
      char: 'boolean',
      string: 'boolean'
    },
    char: {
      int: 'boolean',
      double: 'boolean',
      boolean: 'boolean',
      char: 'boolean',
      string: 'boolean'
    },
    string: {
      int: 'boolean',
      double: 'boolean',
      boolean: 'boolean',
      char: 'boolean',
      string: 'boolean'
    }
  },
  and: {
    int: {
      int: 'boolean',
      double: 'boolean',
      boolean: 'boolean',
      char: 'boolean',
      string: 'boolean'
    },
    double: {
      int: 'boolean',
      double: 'boolean',
      boolean: 'boolean',
      char: 'boolean',
      string: 'boolean'
    },
    boolean: {
      int: 'boolean',
      double: 'boolean',
      boolean: 'boolean',
      char: 'boolean',
      string: 'boolean'
    },
    char: {
      int: 'boolean',
      double: 'boolean',
      boolean: 'boolean',
      char: 'boolean',
      string: 'boolean'
    },
    string: {
      int: 'boolean',
      double: 'boolean',
      boolean: 'boolean',
      char: 'boolean',
      string: 'boolean'
    }
  },
  casteo: {
    int: {
      int: 'int',
      double: 'int',
      char: 'int'
    },
    double: {
      int: 'double',
      double: 'double',
      char: 'double'
    },
    boolean: {},
    char: {
      int: 'char',
      double: 'char'
    },
    string: {
      int: 'string',
      double: 'string'
    }
  }
}

const unary_operation_results = {
  negacion: {
    int: 'int',
    double: 'double'
  },
  not: {
    int: 'boolean',
    double: 'boolean',
    boolean: 'boolean',
    char: 'boolean',
    string: 'boolean'
  },
  incremento: {
    int: 'int',
    double: 'double'
  },
  decremento: {
    int: 'int',
    double: 'double'
  }
}

const operations = {
  suma: (izq, der) =>
    izq.Tipo === 'string' ||
    der.Tipo === 'string' ||
    (izq.Tipo === 'char' && der.Tipo === 'char')
      ? izq.Valor + der.Valor
      : (izq.Tipo === 'char' ? izq.Valor.charCodeAt(0) : izq.Valor) +
        (der.Tipo === 'char' ? der.Valor.charCodeAt(0) : der.Valor),
  resta: (izq, der) =>
    (izq.Tipo === 'char' ? izq.Valor.charCodeAt(0) : izq.Valor) -
    (der.Tipo === 'char' ? der.Valor.charCodeAt(0) : der.Valor),
  multiplicacion: (izq, der) =>
    (izq.Tipo === 'char' ? izq.Valor.charCodeAt(0) : izq.Valor) *
    (der.Tipo === 'char' ? der.Valor.charCodeAt(0) : der.Valor),
  division: (izq, der) =>
    (izq.Tipo === 'char' ? izq.Valor.charCodeAt(0) : izq.Valor) /
    (der.Tipo === 'char' ? der.Valor.charCodeAt(0) : der.Valor),
  potencia: (izq, der) => izq.Valor ** der.Valor,
  modulo: (izq, der) => izq.Valor % der.Valor,
  negacion: (izq, _der) => -izq.Valor,
  mayor: (izq, der) =>
    (izq.Tipo === 'char' ? izq.Valor.charCodeAt(0) : izq.Valor) >
    (der.Tipo === 'char' ? der.Valor.charCodeAt(0) : der.Valor),
  menor: (izq, der) =>
    (izq.Tipo === 'char' ? izq.Valor.charCodeAt(0) : izq.Valor) <
    (der.Tipo === 'char' ? der.Valor.charCodeAt(0) : der.Valor),
  mayorigual: (izq, der) =>
    (izq.Tipo === 'char' ? izq.Valor.charCodeAt(0) : izq.Valor) >=
    (der.Tipo === 'char' ? der.Valor.charCodeAt(0) : der.Valor),
  menorigual: (izq, der) =>
    (izq.Tipo === 'char' ? izq.Valor.charCodeAt(0) : izq.Valor) <=
    (der.Tipo === 'char' ? der.Valor.charCodeAt(0) : der.Valor),
  igualacion: (izq, der) =>
    (izq.Tipo === 'char' ? izq.Valor.charCodeAt(0) : izq.Valor) ===
    (der.Tipo === 'char' ? der.Valor.charCodeAt(0) : der.Valor),
  diferenciacion: (izq, der) =>
    (izq.Tipo === 'char' ? izq.Valor.charCodeAt(0) : izq.Valor) !==
    (der.Tipo === 'char' ? der.Valor.charCodeAt(0) : der.Valor),
  not: (izq, _der) => !izq.Valor,
  and: (izq, der) => Boolean(izq.Valor) && Boolean(der.Valor),
  or: (izq, der) => Boolean(izq.Valor) || Boolean(der.Valor),
  casteo: (izq, der) => {
    if (['int', 'double'].includes(izq.Tipo))
      return der.Tipo === 'char'
        ? der.Valor.charCodeAt(0)
        : izq.Tipo === 'int'
        ? parseInt(der.Valor)
        : der.Valor
    else if (izq.Tipo === 'string') return String(der.Valor)
    else if (izq.Tipo === 'char') return String.fromCharCode(der.Valor)
  },
  incremento: (izq, _der) => izq.Valor + 1,
  decremento: (izq, _der) => izq.Valor - 1
}

// ===================> CORE <========================

const to_print = [],
  errors = [],
  symbols = []

const Error = function (Linea, Columna, Mensaje) {
  errors.push({ Linea, Columna, Tipo: 'Semántico', Mensaje })
}

const getErrors = () => {
  return [...errors]
}

const getSymbols = () => {
  if (!symbols.length)
    for (let env of environments) {
      for (let [id, value] of Object.entries(env.Simbolos)) {
        if (value.Tipo_retorno)
          symbols.push([
            value.Linea,
            value.Columna,
            env.ID,
            value.Tipo_retorno === 'void' ? 'Metodo' : 'Funcion',
            value.Tipo_retorno,
            value.ID
          ])
        else
          symbols.push([value.Linea, value.Columna, env.ID, 'Variable', value.Tipo, id])
      }
    }

  return [...symbols]
}

const getPrinted = () => {
  return [...to_print]
}

const cycles = [],
  functions = [],
  environments = []

const Environment = (ID = 'global', Anterior = null) => {
  return {
    ID,
    Anterior,
    Simbolos: {}
  }
}

const Declare = (env, id, value) => (env.Simbolos[id.toLowerCase()] = { ...value })

const getDeclared = (env, id) => env.Simbolos[id.toLowerCase()]

const getDeclaredGlobal = (env, id) => {
  let temp_env = env
  while (temp_env) {
    if (temp_env.Simbolos[id.toLowerCase()]) return temp_env.Simbolos[id.toLowerCase()]
    temp_env = temp_env.Anterior
  }
}

let global_env = Environment()

const interpret = (INS) => {
  to_print.length = 0
  errors.length = 0
  symbols.length = 0
  cycles.length = 0
  functions.length = 0
  environments.length = 0
  global_env = Environment()
  environments.push(global_env)

  let toExecute

  for (let Instruction of INS)
    if (Instruction.Tipo === 'Exec') {
      if (toExecute)
        return Error(
          Instruction.Linea,
          Instruction.Columna,
          "Se encontró más de una instrucción 'Exec'"
        )
      toExecute = Instruction
    }

  if (!toExecute) return Error(0, 0, "No se encontró una instrucción 'Exec'")

  INS = INS.filter((Instruction) => Instruction.Tipo !== 'Exec')

  for (let Instruction of INS)
    if (['Funcion', 'Metodo'].includes(Instruction.Tipo))
      $Funcion(Instruction, global_env)

  INS = INS.filter((Instruction) => !['Funcion', 'Metodo'].includes(Instruction.Tipo))

  $Instructions(INS, global_env)
  $Llamada(toExecute.Llamada, global_env)

  return { printed: getPrinted(), interpreted_errors: getErrors(), symbols: getSymbols() }
}

const $Evaluar = (Operacion, env) => {
  if (
    ['int', 'double', 'char', 'string', 'boolean', 'vector', 'list'].includes(
      Operacion.Tipo
    )
  )
    return Operacion

  switch (Operacion.Tipo) {
    case 'id':
      let id = getDeclaredGlobal(env, Operacion.Valor)
      if (!id)
        return Error(
          Operacion.Linea,
          Operacion.Columna,
          `No se ha declarado '${Operacion.Valor}'`
        )
      return id
    case 'Llamada':
      return $Llamada(Operacion, env)
    case 'Acceso_vector':
      return $AccesoVector(Operacion, env)
    case 'Acceso_lista':
      return $AccesoLista(Operacion, env)
    default:
  }

  let left_expression = Operacion.Izquierda ? $Evaluar(Operacion.Izquierda, env) : null
  let rigth_expression = Operacion.Derecha ? $Evaluar(Operacion.Derecha, env) : null

  if (!left_expression)
    return Error(
      Operacion.Linea,
      Operacion.Columna,
      `No se pudo realizar la operacion '${Operacion.Tipo}'`
    )

  if (Operacion.Tipo === 'ternaria') {
    if (!rigth_expression)
      return Error(
        Operacion.Linea,
        Operacion.Columna,
        `No se pudo realizar la operacion 'condicional'`
      )

    let condition = $Evaluar(Operacion.Condicion, env)
    if (!condition || condition.Tipo !== 'boolean')
      return Error(
        Operacion.Linea,
        Operacion.Columna,
        'No se pudo realizar la operación ternaria'
      )
    return condition.Valor ? left_expression : rigth_expression
  }

  let return_type
  if (operation_results[Operacion.Tipo]) {
    if (!rigth_expression)
      return Error(
        Operacion.Linea,
        Operacion.Columna,
        `No se pudo realizar la operacion '${Operacion.Tipo}'`
      )

    return_type =
      operation_results[Operacion.Tipo][left_expression.Tipo][rigth_expression.Tipo]
  } else return_type = unary_operation_results[Operacion.Tipo][left_expression.Tipo]

  if (!return_type)
    return Error(
      Operacion.Linea,
      Operacion.Columna,
      `No se puede aplicar '${Operacion.Tipo}' a '${left_expression.Tipo}${
        rigth_expression ? ` y ${rigth_expression.Tipo}` : ''
      }'`
    )

  if (Operacion.Tipo === 'division')
    if ((left_expression.Valor / rigth_expression.Valor) % 1 === 0) return_type = 'int'

  return s.Simbolo(
    Operacion.Linea,
    Operacion.Columna,
    return_type,
    operations[Operacion.Tipo](left_expression, rigth_expression)
  )
}

const $Declaracion = ({ Linea, Columna, Tipo_variable, ID, Expresion }, env) => {
  if (getDeclared(env, ID))
    return Error(Linea, Columna, `La variable '${ID}' ya ha sido declarada`)

  let value
  if (Expresion) {
    value = $Evaluar(Expresion, env)
    if (!value) return Error(Linea, Linea, `No se pudo realizar la declaracion`)
    if (value.Tipo !== Tipo_variable)
      if (Tipo_variable === 'double' && value.Tipo === 'int') value.Tipo = 'double'
      else if (
        Tipo_variable === 'int' &&
        value.Tipo === 'double' &&
        value.Valor % 1 === 0
      )
        value.Tipo = 'int'
      else
        return Error(
          Linea,
          Columna,
          `El tipo de la variable '${ID}' (${Tipo_variable}) no coincide con el valor asignado (${value.Tipo})`
        )
  } else value = s.Simbolo(Linea, Columna, Tipo_variable, default_values[Tipo_variable])

  Declare(env, ID, value)
}

const $Asignacion = ({ Linea, Columna, ID, Expresion }, env) => {
  let id = getDeclaredGlobal(env, ID)
  if (!id) return Error(Linea, Columna, `No se ha declarado la variable '${ID}'`)

  let value = $Evaluar(Expresion, env)
  if (!value) return Error(Linea, Columna, `No se pudo realizar la asignacion`)
  if (id.Tipo !== value.Tipo)
    if (id.Tipo === 'double' && value.Tipo === 'int') value.Tipo = 'double'
    else if (id.Tipo === 'int' && value.Tipo === 'double' && value.Valor % 1 === 0)
      value.Tipo = 'int'
    else
      return Error(
        Linea,
        Columna,
        `No se puede asignar un valor ${value.Tipo} a '${ID}' (${id.Tipo})`
      )

  id.Valor = value.Valor
}

const $Funcion = (
  { Linea, Columna, Tipo_retorno, ID, Parametros, Instrucciones },
  env
) => {
  if (reserved_functions[ID.toLowerCase()])
    return Error(Linea, Columna, `La función '${ID}' es una función de Typesty`)
  if (getDeclaredGlobal(env, ID))
    return Error(Linea, Columna, `La función '${ID}' ya ha sido declarada`)

  Declare(env, ID, { Linea, Columna, Tipo_retorno, ID, Parametros, Instrucciones })
}

const $Llamada = ({ Linea, Columna, ID, Parametros }, env) => {
  const values = []
  for (let Parametro of Parametros) {
    let value = $Evaluar(Parametro, env)
    if (!value)
      return Error(
        Linea,
        Columna,
        `No se pudo ejecutar la llamada de '${ID}' con los parámtros dados`
      )
    values.push(value)
  }

  if (reserved_functions[ID.toLowerCase()]) {
    if (!values.length)
      return Error(Linea, Columna, `La funcion ${ID} debe recibir un parámetro`)
    return reserved_functions[ID.toLowerCase()](values)
  }

  let funcion = getDeclaredGlobal(env, ID)
  if (!funcion) return Error(Linea, Columna, `No se encontró la función o método '${ID}'`)

  if (values.length !== funcion.Parametros.length)
    return Error(
      Linea,
      Columna,
      `Se esperaban ${funcion.Parametros.length} parámetros para '${ID}'`
    )

  for (let i = 0; i < values.length; i++) {
    if (funcion.Parametros[0].Tipo_variable !== values[0].Tipo)
      return Error(
        Linea,
        Columna,
        `Se esperaba un parámetro ${funcion.Parametros[0].Tipo_variable} para '${funcion.Parametros[0].ID}' (${ID})`
      )
  }

  functions.push(ID)
  let new_env = Environment(env.ID + '$' + ID, env)
  environments.push(new_env)

  funcion.Parametros.forEach((Parametro, i) => {
    Parametro.Expresion = values[i]
    $Declaracion(Parametro, new_env)
  })

  let result = $Instructions(funcion.Instrucciones, new_env)
  let return_value

  if (funcion.Tipo_retorno === 'void') {
    if (result && result.Expression)
      Error(
        result.Linea,
        result.Columna,
        `No se esperaba un retorno en el método '${ID}'`
      )
  } else if (result) {
    if (funcion.Tipo_retorno !== result.Expresion.Tipo)
      if (funcion.Tipo_retorno === 'double' && result.Expresion.Tipo === 'int')
        result.Expresion.Tipo = 'double'
      else
        Error(
          result.Linea,
          result.Columna,
          `La función '${ID}' debe retornar un ${funcion.Tipo_retorno}`
        )
    return_value = result.Expresion
  } else
    Error(
      Linea,
      Columna,
      `La funcion '${ID}' no retorna un valor '${funcion.Tipo_retorno}'`
    )

  functions.pop()
  return return_value
}

const $Incremento = ({ Linea, Columna, ID }, env) => {
  let id = getDeclaredGlobal(env, ID)
  if (!id) return Error(Linea, Columna, `No se encontró la variable '${ID}'`)
  if (!['int', 'double'].includes(id.Tipo))
    return Error(
      Linea,
      Columna,
      `No se puede incrementar la variable no numérica '${ID}'`
    )

  id.Valor += 1
}

const $Decremento = ({ Linea, Columna, ID }, env) => {
  let id = getDeclaredGlobal(env, ID)
  if (!id) return Error(Linea, Columna, `No se encontró la variable '${ID}'`)
  if (!['int', 'double'].includes(id.Tipo))
    return Error(
      Linea,
      Columna,
      `No se puede decrementar la variable no numérica '${ID}'`
    )

  id.Valor -= 1
}

const $DeclararVector = (
  { Linea, Columna, Tipo_valores, ID, Tipo_i, Tamaño, Valores },
  env
) => {
  if (getDeclaredGlobal(env, ID))
    return Error(Linea, Columna, `La variable '${ID}' ya ha sido declarada`)

  let size,
    values = []
  if (Tipo_i) {
    if (Tipo_valores !== Tipo_i)
      return Error(Linea, Columna, `Los tipos del vector '${ID}' no coinciden`)
    size = $Evaluar(Tamaño, env)
    if (!size) return Error(Linea, Columna, `No se pudo declarar el vector '${ID}'`)
    if (size.Tipo !== 'int')
      return Error(
        Linea,
        Columna,
        `El tamaño del vector '${ID}' debe ser un número entero`
      )
    if (size.Valor < 1)
      return Error(
        Linea,
        Columna,
        `El tamaño del vector '${ID}' debe ser un entero mayor a 0`
      )

    values = Array(size.Valor).fill(
      s.Simbolo(Linea, Columna, Tipo_valores, default_values[Tipo_valores])
    )
  } else {
    for (let value of Valores) {
      let temp_value = $Evaluar(value, env)
      if (!temp_value)
        return Error(Linea, Columna, `No se pudo declarar el vector '${ID}'`)
      if (temp_value.Tipo !== Tipo_valores)
        return Error(
          Linea,
          Columna,
          `El tipo del vector '${ID}' (${Tipo_valores}) no coincide con un valor asignado (${temp_value.Tipo})`
        )

      values.push(temp_value)
    }
  }

  Declare(env, ID, s.Vector(Linea, Columna, Tipo_valores, ID, Tipo_valores, size, values))
}

const $DeclararLista = ({ Linea, Columna, Tipo_valores, ID, Tipo_i, Valores }, env) => {
  if (getDeclaredGlobal(env, ID))
    return Error(Linea, Columna, `La variable '${ID}' ya ha sido declarada`)

  let values = []
  if (Tipo_i) {
    if (Tipo_valores !== Tipo_i)
      return Error(Linea, Columna, `Los tipos de la lista '${ID}' no coinciden`)
  } else {
    let temp_list = $Evaluar(Valores, env)

    if (!temp_list) return Error(Linea, Columna, `No se pudo declarar la lista '${ID}'`)
    if (temp_list.Tipo !== 'list')
      return Error(Linea, Columna, `Se debe asignar una lista a '${ID}'`)
    if (temp_list.Tipo_valores !== Tipo_valores)
      return Error(
        Linea,
        Columna,
        `Se debe asignar una lista del mismo tipo al declarado (${Tipo_valores})`
      )

    values = temp_list.Valores
  }

  Declare(env, ID, s.Lista(Linea, Columna, Tipo_valores, ID, Tipo_valores, values))
}

const $AccesoVector = ({ Linea, Columna, ID, Index }, env) => {
  let vector = getDeclaredGlobal(env, ID)
  if (!vector) return Error(Linea, Columna, `No se ha declarado el vector '${ID}'`)

  let index = $Evaluar(Index, env)
  if (!index) return Error(Linea, Columna, `No se pudo acceder al vector '${ID}'`)
  if (index.Tipo !== 'int')
    return Error(Linea, Columna, `Se esperaba un valor entero como índice en '${ID}'`)
  if (index.Valor >= vector.Valores.length)
    return Error(
      Linea,
      Columna,
      `El índice proporcionado para '${ID}' sobrepasó el tamaño del vector (${vector.Valores.length})`
    )
  if (index.Valor < 0)
    return Error(
      Linea,
      Columna,
      `El índice proporcionado para '${ID}' debe ser mayor o igual a 0`
    )

  return vector.Valores[index.Valor]
}

const $AccesoLista = ({ Linea, Columna, ID, Index }, env) => {
  let list = getDeclaredGlobal(env, ID)
  if (!list) return Error(Linea, Columna, `No se ha declarado la lista '${ID}'`)

  let index = $Evaluar(Index, env)
  if (!index) return Error(Linea, Columna, `No se pudo acceder a la lista '${ID}'`)
  if (index.Tipo !== 'int')
    return Error(Linea, Columna, `Se esperaba un valor entero como índice en '${ID}'`)
  if (index.Valor >= list.Valores.length)
    return Error(
      Linea,
      Columna,
      `El índice proporcionado para '${ID}' sobrepasó el tamaño de la lista (${list.Valores.length})`
    )
  if (index.Valor < 0)
    return Error(
      Linea,
      Columna,
      `El índice proporcionado para '${ID}' debe ser mayor o igual a 0`
    )

  return list.Valores[index.Valor]
}

const $ModificacionVector = ({ Linea, Columna, ID, Index, Expresion }, env) => {
  let vector = getDeclaredGlobal(env, ID)
  if (!vector) return Error(Linea, Columna, `No se ha declarado el vector '${ID}'`)

  let index = $Evaluar(Index, env)
  if (!index) return Error(Linea, Columna, `No se pudo modificar el vector '${ID}'`)
  if (index.Tipo !== 'int')
    return Error(Linea, Columna, `Se esperaba un valor entero como índice en  '${ID}'`)
  if (index.Valor >= vector.Valores.length)
    return Error(
      Linea,
      Columna,
      `El índice proporcionado para '${ID}' sobrepasó el tamaño del vector (${vector.Valores.length})`
    )
  if (index.Valor < 0)
    return Error(
      Linea,
      Columna,
      `El índice proporcionado para '${ID}' debe ser mayor o igual a 0`
    )

  let value = $Evaluar(Expresion, env)
  if (!value) return Error(Linea, Columna, `No se pudo modificar el vector '${ID}'`)
  if (value.Tipo !== vector.Tipo_valores)
    return Error(
      Linea,
      Columna,
      `No se puede asignar un valor ${value.Tipo} al vector '${ID}' (${vector.Tipo_valores})`
    )

  vector.Valores[index.Valor] = value
}

const $ModificacionLista = ({ Linea, Columna, ID, Index, Expresion }, env) => {
  let list = getDeclaredGlobal(env, ID)
  if (!list) return Error(Linea, Columna, `No se ha declarado la lista '${ID}'`)

  let index = $Evaluar(Index, env)
  if (!index) return Error(Linea, Columna, `No se pudo modificar la lista '${ID}'`)
  if (index.Tipo !== 'int')
    return Error(
      index.Linea,
      index.Columna,
      `Se esperaba un valor entero como índice en '${ID}'`
    )
  if (index.Valor >= list.Valores.length)
    return Error(
      Linea,
      Columna,
      `El índice proporcionado para '${ID}' sobrepasó el tamaño de la lista (${list.Valores.length})`
    )
  if (index.Valor < 0)
    return Error(
      Linea,
      Columna,
      `El índice proporcionado para '${ID}' debe ser mayor o igual a 0`
    )

  let value = $Evaluar(Expresion, env)
  if (!value) return Error(Linea, Columna, `No se pudo modificar la lista '${ID}'`)
  if (value.Tipo !== list.Tipo_valores)
    return Error(
      Linea,
      Columna,
      `No se puede asignar un valor ${value.Tipo} a la lista '${ID}' (${list.Tipo_valores})`
    )

  list.Valores[index.Valor] = value
}

const $AddLista = ({ Linea, Columna, ID, Expresion }, env) => {
  let list = getDeclaredGlobal(env, ID)
  if (!list) return Error(Linea, Columna, `No se ha declarado la lista '${ID}'`)

  let value = $Evaluar(Expresion, env)
  if (!value) return Error(Linea, Columna, `No se pudo añadir a la lista '${ID}'`)
  if (value.Tipo !== list.Tipo_valores)
    return Error(
      Linea,
      Columna,
      `No se puede añadir un valor ${value.Tipo} a la lista '${ID}' (${list.Tipo_valores})`
    )

  list.Valores.push(value)
}

const $If = (
  { Linea, Columna, Condicion, Instrucciones_true, Instrucciones_false },
  env
) => {
  let condition = $Evaluar(Condicion, env)
  if (!condition) return Error(Linea, Columna, `No se pudo ejecutar la sentencia if`)
  if (condition.Tipo !== 'boolean')
    return Error(Linea, Columna, 'Se esperaba una condicion dentro del if')

  let new_env = Environment(env.ID + `#if(${Linea},${Columna})`, env)
  if (condition.Valor) return $Instructions(Instrucciones_true, new_env)
  else if (Instrucciones_false) return $Instructions(Instrucciones_false, new_env)
}

const $Switch = ({ Linea, Columna, Expresion, Cases, Default }, env) => {
  let executed = false
  let new_env = Environment(env.ID + `#switch(${Linea},${Columna})`, env)

  cycles.push('switch')
  for (let Case of Cases) {
    let condition = $Evaluar(
      s.Operacion(Linea, Columna, 'igualacion', Expresion, Case.Expresion),
      env
    )
    if (!condition) {
      cycles.pop()
      return Error(Linea, Columna, `No se pudo ejecutar la sentencia switch`)
    }

    if (condition.Valor || executed) {
      executed = true
      let result = $Instructions(Case.Instrucciones, new_env)
      if (result) {
        cycles.pop()

        if (result.Tipo === 'Continue')
          return Error(
            result.Linea,
            result.Columna,
            `No se puede ejecutar una sentencia 'continue' dentro de un switch`
          )
        return result.Tipo === 'Return' ? result : undefined
      }
    }
  }

  if (Default && !executed) {
    let result = $Instructions(Default.Instrucciones, new_env)
    if (result) {
      cycles.pop()

      if (result.Tipo === 'Continue')
        return Error(
          result.Linea,
          result.Columna,
          `No se puede ejecutar una sentencia 'continue' dentro de un switch`
        )
      return result.Tipo === 'Return' ? result : undefined
    }
  }

  cycles.pop()
}

const $While = ({ Linea, Columna, Condicion, Instrucciones }, env) => {
  cycles.push('while')
  let new_env = Environment(env.ID + `#while(${Linea},${Columna})`, env)

  const INS = copyArray(Instrucciones)

  for (let Instruccion of INS)
    if (['Declaracion'].includes(Instruccion.Tipo)) {
      $Declaracion(Instruccion, new_env)
      Instruccion.Tipo = 'Asignacion'
      if (!Instruccion.Expresion)
        Instruccion.Expresion = s.Simbolo(
          Instruccion.Linea,
          Instruccion.Columna,
          Instruccion.Tipo_variable,
          default_values[Instruccion.Tipo_variable]
        )
    }

  while (true) {
    let condition = $Evaluar(Condicion, env)
    if (!condition) {
      cycles.pop()
      return Error(Linea, Columna, `No se pudo ejecutar la sentencia while`)
    }

    if (condition.Tipo !== 'boolean') {
      cycles.pop()
      return Error(Linea, Columna, 'Se esperaba una condicion dentro del while')
    }

    if (!condition.Valor) {
      cycles.pop()
      return
    }

    let result = $Instructions(INS, new_env)
    if (!result) continue

    if (result.Tipo === 'Return') {
      cycles.pop()
      return result
    } else if (result.Tipo === 'Break') {
      cycles.pop()
      return
    } else if (result.Tipo === 'Continue') continue
  }
}

const $For = (
  { Linea, Columna, Inicializacion, Condicion, Actualizacion, Instrucciones },
  env
) => {
  let new_env = Environment(env.ID + `$for(${Linea},${Columna})`, env)

  let init_value = $Evaluar(Inicializacion.Expresion, env)
  if (!init_value && !['int', 'double'].includes(init_value.Tipo))
    return Error(
      Inicializacion.Linea,
      Inicializacion.Columna,
      `No se asignó un valor numérico a la variable de inicializacion '${Inicializacion.ID}' del for`
    )

  let init_id = getDeclaredGlobal(env, Inicializacion.ID)

  if (Inicializacion.Tipo === 'Declaracion') {
    if (init_id)
      return Error(
        Inicializacion.Linea,
        Inicializacion.Columna,
        `La variable de inicialización '${Inicializacion.ID}' del for ya ha sido declarada`
      )
    if (!['int', 'double'].includes(Inicializacion.Tipo_variable))
      return Error(
        Inicializacion.Linea,
        Inicializacion.Columna,
        `Se esperaba la inicalización de un número en el for`
      )

    $Declaracion(Inicializacion, new_env)
  } else {
    if (!init_id)
      return Error(
        Inicializacion.Linea,
        Inicializacion.Columna,
        `La variable de inicialización del for (${Inicializacion.ID}) no fue declarada`
      )
    if (!['int', 'double'].includes(init_id.Tipo))
      return Error(
        Inicializacion.Linea,
        Inicializacion.Columna,
        `La variable de inicialización del for (${Inicializacion.ID}) no es un número`
      )

    $Asignacion(Inicializacion, new_env)
  }

  let update_id = getDeclaredGlobal(new_env, Actualizacion.ID)
  if (!update_id)
    return Error(
      Actualizacion.Linea,
      Actualizacion.Columna,
      `La variable de actualizacion del for (${Actualizacion.ID}) no fue declarada`
    )
  if (!['int', 'double'].includes(update_id.Tipo))
    return Error(
      update_id.Linea,
      update_id.Columna,
      `La variable de actualizacion del for (${Actualizacion.ID}) no es numérica`
    )

  const step = () => {
    if (Actualizacion.Tipo === 'Incremento') $Incremento(Actualizacion, new_env)
    else if (Actualizacion.Tipo === 'Decremento') $Decremento(Actualizacion, new_env)
    else if (Actualizacion.Tipo === 'Asignacion') $Asignacion(Actualizacion, new_env)
  }

  cycles.push('for')

  const INS = copyArray(Instrucciones)

  for (let Instruccion of INS)
    if (['Declaracion'].includes(Instruccion.Tipo)) {
      $Declaracion(Instruccion, new_env)
      Instruccion.Tipo = 'Asignacion'
      if (!Instruccion.Expresion)
        Instruccion.Expresion = s.Simbolo(
          Instruccion.Linea,
          Instruccion.Columna,
          Instruccion.Tipo_variable,
          default_values[Instruccion.Tipo_variable]
        )
    }

  while (true) {
    let condition = $Evaluar(Condicion, new_env)
    if (!condition) {
      cycles.pop()
      return Error(Linea, Columna, `No se pudo ejecutar la sentencia for`)
    }
    if (condition.Tipo !== 'boolean') {
      cycles.pop()
      return Error('Se esperaba una condición dentro del for')
    }
    if (!condition.Valor) {
      cycles.pop()
      return
    }

    let result = $Instructions(INS, new_env)
    step()
    if (!result) continue

    if (result.Tipo === 'Return') {
      cycles.pop()
      return result
    } else if (result.Tipo === 'Break') {
      cycles.pop()
      return
    } else if (result.Tipo === 'Continue') continue
  }
}

const $DoWhile = ({ Linea, Columna, Condicion, Instrucciones }, env) => {
  cycles.push('do-while')
  let new_env = Environment(env.ID + `#do-while(${Linea},${Columna})`, env)

  const INS = copyArray(Instrucciones)

  for (let Instruccion of INS)
    if (['Declaracion'].includes(Instruccion.Tipo)) {
      $Declaracion(Instruccion, new_env)
      Instruccion.Tipo = 'Asignacion'
      if (!Instruccion.Expresion)
        Instruccion.Expresion = s.Simbolo(
          Instruccion.Linea,
          Instruccion.Columna,
          Instruccion.Tipo_variable,
          default_values[Instruccion.Tipo_variable]
        )
    }

  let first_iteration = s.Simbolo(Linea, Columna, 'boolean', true)

  while (true) {
    let condition = first_iteration || $Evaluar(Condicion, env)
    if (!condition) {
      cycles.pop()
      return Error(Linea, Columna, `No se pudo ejecutar la sentencia do-while`)
    }
    if (condition.Tipo !== 'boolean') {
      cycles.pop()
      return Error(Linea, Columna, 'Se esperaba una condicion dentro del do-while')
    }
    if (!condition.Valor) {
      cycles.pop()
      return
    }

    let result = $Instructions(INS, new_env)
    if (result) {
      if (result.Tipo === 'Return') {
        cycles.pop()
        return result
      } else if (result.Tipo === 'Break') {
        cycles.pop()
        return
      } else if (result.Tipo === 'Continue') continue
    }

    first_iteration = null
  }
}

export default interpret
