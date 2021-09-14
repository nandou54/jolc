INPUT = '''
struct Actor
    nombre:: String;
    edad:: Int64;
end;

struct Pelicula 
    nombre::String;
    posicion::Int64;
end;

struct Contrato
    actor;
    pelicula;
end;

actores = ["Elizabeth Olsen", "Adam Sandler", "Christian Bale", "Jennifer Aniston"];
peliculas = ["Avengers: Age of Ultron", "Mr. Deeds", "Batman: The Dark Knight", "Marley & Me"];

function contratar(actor, pelicula)
    return Contrato(actor,pelicula);
end;

function crearActor(nombre, edad)
    return Actor(nombre,edad);
end;

function crearPelicula(nombre, posicion) 
    return Pelicula(nombre,posicion);
end;

function imprimir(contrato)
    println("Actor: ", contrato.actor.nombre, "   Edad: ", contrato.actor.edad);
    println("Pelicula: ", contrato.pelicula.nombre, "   Genero: ", contrato.pelicula.posicion);
end;

function contratos()
    for i in 1:(1*1+2)
        contrato = Contrato(Actor("",0),Pelicula("",0));
        if(i < 4)
            actor = crearActor(actores[i], i+38);
            pelicula = crearPelicula(peliculas[i], i);
            contrato = contratar(actor, pelicula);
        end;
        imprimir(contrato);
    end;
end;

contratos();
'''

lexer = False
parser = False
interpreter = True

def run(INPUT, lexer=False, parser=False, interpreter=False):
  # LEXER
  if lexer:
    from interpreter.analyzer import lexer as lex
    print('=== LEXER ===')
    lex.input(INPUT)
    for tok in lex:
        print(tok)

  import json
  # PARSER
  if parser:
    from interpreter.analyzer import parse
    print('=== PARSER ===')
    res = parse(INPUT)
    try:
      print(json.dumps(res, indent=2))
    except:
      print(res)

  # INTERPRETER
  if interpreter:
    from interpreter.main import interpret
    print('=== INTERPRETER ===')
    res = interpret(INPUT)
    try:
      print('\n'.join(res['output']))
      print(json.dumps(res['errors'], indent=2))
    except:
      print(res['output'])
      print(res['errors'])

run(INPUT, lexer, parser, interpreter)
