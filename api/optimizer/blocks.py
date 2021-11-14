from copy import deepcopy
from api.optimizer.analyzer import parse
from api.optimizer.core import addReport, expressionsAreEqual, getBlocks, getIds, reset, reports, setGlobalOptimizations
from api.optimizer.symbols import Assignment, Expression, Library, Number, Id, Number

def optimize(input):
  global reports
  reset()

  header = ''
  while True:
    index = input.find('\n')
    header += input[:index+1]
    input = input[index+1:]
    if not input or input.startswith('func'): break

  res = parse(input)
  functions = res['ast']

  blocks = {function.id: getBlocks(function.ins) for function in functions}
  INS = []

  for function_blocks in blocks.values():
    for block in function_blocks:
      for optimizer in optimization_functions:
        optimizer(block.ins)
    INS += block.ins

  setGlobalOptimizations()
  for optimizer in optimization_functions:
    optimizer(block.ins)

  for function in functions:
    function.ins = []
    for block in blocks[function.id]: function.ins += block.ins

  output = header + str('\n\n'.join(str(function) for function in functions))
  return {'output': output, 'reports': reports}

def optimize_common_subexpressions(INS):
  INS_COPY = INS.copy()
  for ins in INS_COPY:
    if type(ins) is not Assignment: continue

    to_watch = [ins.id] + getIds(ins.ex)

    index = INS_COPY.index(ins)
    INS2 = INS_COPY[index+1:]

    for ins2 in INS2:
      if type(ins2) is not Assignment: continue

      ids = [ins2.id.value] + [id.value for id in getIds(ins2.ex)]

      contained = any(id.value in ids for id in to_watch)

      if not contained and expressionsAreEqual(ins.ex, ins2.ex):
        original = deepcopy(ins)
        ins2.ex = Id(ins2.ex.ln, ins2.ex.col, ins.id.value)
        addReport(ins2.ln, 'Bloques', 'Subexpresiones comunes R1', f'{ins}\n...\n{original}', f'{ins}\n...\n{ins2}')

def optimize_copies_propagation(INS):
  INS_COPY = INS.copy()
  for ins in INS_COPY:
    if type(ins) is not Assignment: continue
    if type(ins.ex) is not Id: continue
    if ins.ex.wrappers: continue

    index = INS_COPY.index(ins)
    INS2 = INS_COPY[index+1:]

    for ins2 in INS2:
      if type(ins2) is not Assignment: continue
      if ins2.id.value in [ins.id.value, ins.ex.value]: break

      ids = getIds(ins2.ex)
      id_values = [id.value for id in ids]

      if ins.id.value in id_values:
        original = deepcopy(ins2)
        for id in ids:
          if id.value == ins.id.value: id.value = ins.ex.value

        addReport(ins2.ln, 'Bloques', 'Propagación de copias R2', f'{ins}\n...\n{original}', f'{ins}\n...\n{ins2}')

def optimize_dead_code(INS):
  INS_COPY = INS.copy()
  for ins in INS_COPY:
    if type(ins) is not Assignment: continue
    if ins.id.value in ['h', 'p']: continue
    if ins.id.wrappers: continue

    index = INS_COPY.index(ins)
    INS2 = INS_COPY[index+1:]
    used = False

    for ins2 in INS2:
      if type(ins2) not in [Assignment, Library]: continue

      if type(ins2) is Assignment: ids = [ins2.id] + getIds(ins2.ex)
      else: ids = getIds(ins2.parameters)

      used = any(ins.id.value==id.value for id in ids)
      if used: break

    if used: continue

    ins.deleted = True
    INS.remove(ins)
    addReport(ins.ln, 'Bloques', 'Eliminación de código muerto R3', str(ins), '')

def optimize_constants_propagation(INS):
  INS_COPY = INS.copy()
  for ins in INS_COPY:
    if type(ins) is not Assignment: continue
    if type(ins.ex) is not Number: continue

    index = INS_COPY.index(ins)
    INS2 = INS_COPY[index+1:]

    for ins2 in INS2:
      if type(ins2) is not Assignment: continue
      if ins2.id.value == ins.id.value: break

      ids = getIds(ins2.ex)
      id_values = [id.value for id in ids]

      if ins.id.value in id_values:
        original = deepcopy(ins2)
        for id in ids:
          if id.value == ins.id.value:
            new_value = Number(id.ln, id.col, ins.ex.value)
            if type(ins2.ex) is Id: ins2.ex = new_value
            elif type(ins2.ex) is Expression:
              if ins2.ex.left.value==ins.id.value: ins2.ex.left = new_value
              else: ins2.ex.right = new_value

        addReport(ins2.ln, 'Bloques', 'Propagación de constantes R4', f'{ins}\n...\n{original}', f'{ins}\n...\n{ins2}')

optimization_functions = [optimize_common_subexpressions, optimize_copies_propagation, optimize_dead_code, optimize_constants_propagation]
