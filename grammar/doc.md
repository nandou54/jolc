- [1. Gramática de JOLC](#1-gramática-de-jolc)
  - [1.1. Alfabeto](#11-alfabeto)
    - [1.1.1. Símbolos terminales](#111-símbolos-terminales)
      - [1.1.1.1. Expresiones regulares](#1111-expresiones-regulares)
      - [1.1.1.2. Palabras reservadas](#1112-palabras-reservadas)
    - [1.1.2. Símbolos no terminales](#112-símbolos-no-terminales)
  - [1.2. Sintáxis](#12-sintáxis)
    - [1.2.1. Precedencia](#121-precedencia)
    - [1.2.2. Producciones](#122-producciones)

# 1. Gramática de JOLC

## 1.1. Alfabeto
JOLC es case sensitive.

### 1.1.1. Símbolos terminales

#### 1.1.1.1. Expresiones regulares

| Token                   |              Patrón              |
| ----------------------- | :------------------------------: |
| t_comentario            |               #.*                |
| t_comentario_multilinea | #=([^=]\|[\r\n]\|(=+([^#])))*=+# |
| t_parentesis_A          |                (                 |
| t_parentesis_B          |                )                 |
| t_corchete_A            |                [                 |
| t_corchete_B            |                ]                 |
| t_int64                 |              [0-9]+              |
| t_float64               |          [0-9]+\.[0-9]+          |
| t_bool                  |         (true)\|(false)          |
| t_char                  |          '[a-zA-Z0-9]'           |
| t_string                |          "[a-zA-Z0-9]*"          |
| t_id                    |      [a-zA-Z_][a-zA-Z_0-9]*      |
| t_mas                   |                +                 |
| t_menos                 |                -                 |
| t_asterisco             |                *                 |
| t_barra                 |                /                 |
| t_caret                 |                ^                 |
| t_modulo                |                %                 |
| t_mayor_igual           |                >=                |
| t_mayor                 |                >                 |
| t_menor_igual           |                <=                |
| t_menor                 |                <                 |
| t_igualacion            |                ==                |
| t_diferenciacion        |                !=                |
| t_or                    |               \|\|               |
| t_and                   |                &&                |
| t_not                   |                !                 |
| t_punto                 |                .                 |
| t_coma                  |                ,                 |
| t_igual                 |                =                 |
| t_tipo                  |                ::                |
| t_dospuntos             |                :                 |
| t_puntoycoma            |                ;                 |

#### 1.1.1.2. Palabras reservadas

| Token          | Lexema   |
| -------------- | -------- |
| t_nothing      | Nothing  |
| t_tipo_int64   | Int64    |
| t_tipo_float64 | Float64  |
| t_tipo_bool    | Bool     |
| t_tipo_char    | Char     |
| t_tipo_string  | String   |
| t_struct       | struct   |
| t_local        | local    |
| t_global       | global   |
| t_function     | function |
| t_end          | end      |
| t_if           | if       |
| t_elseif       | elseif   |
| t_else         | else     |
| t_while        | while    |
| t_for          | for      |
| t_break        | break    |
| t_continue     | continue |
| t_return       | return   |
| t_mutable      | mutable  |
| t_in           | in       |

### 1.1.2. Símbolos no terminales

| Token            | Descripción                         |
| ---------------- | ----------------------------------- |
| INIT             | Estado inicial de la sintáxis       |
| EOF              | Fin del archivo                     |
| INS              | Lista de instrucciones              |
| I                | Instrucción                         |
| BLOQUE           | Bloque de instrucciones             |
| TIPO             | Tipo de una expresion               |
| ASIGNACION       | Asignacion a una variable           |
| ASIGNACION_VALOR | Valor de una asignación             |
| FUNCION          | Declaracion de una función          |
| PAR              | Lista de parámetros                 |
| P                | Parámetro de una función            |
| STRUCT           | Declaración de un struct            |
| ATR              | Lista de atributos                  |
| A                | Atributo de un struct               |
| EXP              | Lista de expresiones                |
| E                | Expresión                           |
| ARREGLO          | Expresión arreglo                   |
| LLAMADA          | Llamada a una función o struct      |
| ACCESO_ARREGLO   | Acceso a un arreglo                 |
| ID               | Acceso a un atributo de un id       |
| IF               | Sentencia condicional if            |
| ELSEIF           | Sentencia condicional elseif        |
| ELSE             | Sentencia condicional else          |
| WHILE            | Sentencia iterativa while           |
| FOR              | Sentencia iterativa for             |
| ITERATIVO        | Iterativo de una sentencia for      |
| RANGO            | Rango entre dos expresiones         |
| BREAK            | Sentencia de transferencia break    |
| CONTINUE         | Sentencia de transferencia continue |
| RETURN           | Sentencia de transferencia return   |

## 1.2. Sintáxis

### 1.2.1. Precedencia
Precedencia de operadores de más a menos:

| Precedencia | Operador                                   | Asociatividad |
| :---------: | ------------------------------------------ | ------------- |
|     11      | Agrupacion                                 | Ninguna       |
|     10      | Acceso a arreglo                           | Izquierda     |
|      9      | Llamada a función                          | Izquierda     |
|      8      | Negación unaria, not                       | Derecha       |
|      7      | Potencia                                   | Derecha       |
|      6      | Multiplicación, división, módulo           | Izquierda     |
|      5      | Suma, resta                                | Izquierda     |
|      4      | Menor, menor o igual, mayor, mayor o igual | Izquierda     |
|      3      | Igualación, diferenciación                 | Izquierda     |
|      2      | And                                        | Izquierda     |
|      1      | Or                                         | Izquierda     |


### 1.2.2. Producciones
```ru
Estado inicial = INS

INS
        : INS I t_puntoycoma
        | I t_puntoycoma

I
        : ASIGNACION
        | FUNCION
        | STRUCT
        | LLAMADA
        | IF
        | WHILE
        | FOR
        | BREAK
        | CONTINUE
        | RETURN
        | error t_puntoycoma

BLOQUE
        : INS t_end
        | t_end

TIPO
        : t_tipo_int64
        | t_tipo_float64
        | t_tipo_bool
        | t_tipo_char
        | t_tipo_string

ASIGNACION
        : ID t_igual ASIGNACION_VALOR
        | t_global t_id t_igual ASIGNACION_VALOR
        | t_global t_id
        | t_local t_id t_igual ASIGNACION_VALOR
        | t_local t_id t_igual

ASIGNACION_VALOR
        : E
        | E t_tipo TIPO

FUNCION
        : t_function t_id t_parentesis_A PAR t_parentesis_B BLOQUE
        | t_function t_id t_parentesis_A t_parentesis_B BLOQUE

PAR
        : PAR t_coma P
        | P

P
        : t_id

STRUCT
        : t_struct t_id ATR t_end
        | t_mutable t_struct t_id ATR t_end

ATR
        : ATR A
        | A

A
        : t_id t_tipo TIPO t_puntoycoma
        | t_id t_puntoycoma

EXP
        : EXP coma E
        | E

E
        : E t_mas E
        | E t_menos E
        | E t_asterisco E
        | E t_barra E
        | E t_caret E
        | E t_modulo E
        | t_menos E
        | E t_mayor E
        | E t_menor E
        | E t_mayor_igual E
        | E t_menor_igual E
        | E t_igualacion E
        | E t_diferenciacion E
        | E t_or E
        | E t_and E
        | t_not E
        | t_parentesis_A E t_parentesis_B
        | LLAMADA
        | ACCESO_ARREGLO
        | ARREGLO
        | ID
        | t_int64
        | t_float64
        | t_bool
        | t_char
        | t_string
        | t_nothing

ARREGLO
        : t_corchete_A EXP t_corchete_B
        | t_corchete_A t_corchete_B

LLAMADA
        : t_id t_parentesis_A EXP t_parentesis_B
        | t_id t_parentesis_A t_parentesis_B

ACCESO_ARREGLO
        : t_id t_corchete_A E t_corchete_B

ID
        : ID t_punto t_id
        | id

IF
        : t_if E BLOQUE
        | t_if E BLOQUE ELSEIF
        | t_if E BLOQUE ELSE

ELSEIF
        : t_elseif E BLOQUE ELSEIF
        | t_elseif E BLOQUE ELSE

ELSE
        : t_else BLOQUE

WHILE
        : t_while E BLOQUE

FOR
        : t_for ITERATIVO BLOQUE

ITERATIVO
        : t_id t_in RANGO
        | t_id t_in E

RANGO
        : E t_dospuntos E

BREAK
        : t_break

CONTINUE
        : t_continue

RETURN
        : t_return E
        | t_return
```
