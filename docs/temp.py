'''
INIT
        : INS EOF
	| error EOF

INS
        : INS I puntoycoma
        | I puntoycoma

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
        | error puntoycoma

BLOQUE
        : INS end
        | end

TIPO
        : tipo_int64
        | tipo_float64
        | tipo_bool
        | tipo_char
        | tipo_string

ASIGNACION
        : id igual ASIGNACION_VALOR
        | ACCESO_STRUCT igual ASIGNACION_VALOR
        | global id igual ASIGNACION_VALOR
        | global id
        | local id igual ASIGNACION_VALOR
        | local id igual

ASIGNACION_VALOR
        : E
        | E tipo TIPO

FUNCION
        : function id parentesis_A PAR parentesis_B BLOQUE
        | function id parentesis_A parentesis_B BLOQUE

PAR
        : PAR coma P
        | P

P
        : id

STRUCT
        : struct id ATR end
        | mutable struct id ATR end

ATR
        : ATR coma A
        | A

A
        : id tipo TIPO puntoycoma
        | id puntoycoma

EXP
        : EXP coma E
        | E

E
        : E mas E
        | E menos E
        | E asterisco E
        | E barra E
        | E caret E
        | E modulo E
        | menos E
        | E mayor E
        | E menor E
        | E mayor_igual E
        | E menor_igual E
        | E igualacion E
        | E diferenciacion E
        | E or E
        | E and E
        | not E
        | parentesis_A E
        | LLAMADA
        | ACCESO_ARREGLO
        | ACCESO_STRUCT
        | ARREGLO
        | id
        | int64
        | float64
        | bool
        | char
        | string
        | nothing

ARREGLO
        : corchete_A EXP corchete_B
        | corchete_A corchete_B

LLAMADA
        : id parentesis_A EXP parentesis_B
        | id parentesis_A parentesis_B

ACCESO_ARREGLO
        : id corchete_A E corchete_B

ACCESO_STRUCT
        : ACCESO_STRUCT punto id
        | id

IF
        : if E BLOQUE
        | if E BLOQUE ELSEIF
        | if E BLOQUE ELSE

ELSEIF
        : elseif E BLOQUE ELSEIF
        | elseif E BLOQUE ELSE

ELSE
        : else BLOQUE

WHILE
        : while E BLOQUE

FOR
        : for ITERATIVO BLOQUE

ITERATIVO
        : id in RANGO
        | id in E

RANGO
        : E dospuntos E

BREAK
        : break

CONTINUE
        : continue

RETURN
        : return E
        | return
'''
