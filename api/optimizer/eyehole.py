from copy import deepcopy
from api.optimizer.analyzer import parse
from api.optimizer.core import addReport, reset, reports
from api.optimizer.symbols import Assignment, Expression, Goto, Id, If, Number, Tag, inverse_operators

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

  INS = []
  for function in functions: INS.extend(function.ins)

  eyehole_length = 20
  for _ in range(10):
    reports_length = len(reports)
    for optimizer in optimization_functions: optimizer(INS, eyehole_length)
    if len(reports) == reports_length:
      if eyehole_length > len(INS): break
      eyehole_length += 20

  output = header + str('\n\n'.join(str(function) for function in functions))
  return {'output': output, 'reports': reports}

def optimize_redundant_instructions(INS, eyehole_length):
  INS_COPY = INS[:eyehole_length]
  for ins in INS_COPY:
    if type(ins) is not Assignment: continue
    if ins.deleted: continue
    if type(ins.ex) is not Id: continue

    index = INS_COPY.index(ins)
    INS2 = INS_COPY[index+1:]

    for ins2 in INS2:
      if type(ins2) is Tag: break
      if type(ins2) is not Assignment: continue
      if type(ins2.ex) is not Id: continue
      if ins.id.value == ins2.ex.value and ins.ex.value == ins2.id.value:
        ins2.deleted = True
        INS.remove(ins2)
        addReport(ins2.ln, 'Mirilla', 'Eliminacion de instrucciones redundantes R1', f'{ins}\n{ins2}', str(ins))

def optimize_unreachable_code(INS, eyehole_length):
  INS_COPY = INS[:eyehole_length]
  for ins in INS_COPY:
    if type(ins) is not Goto: continue
    if ins.deleted: continue

    index = INS_COPY.index(ins)
    INS2 = INS_COPY[index+1:]
    instructions_to_remove = []
    tag = None

    for ins2 in INS2:
      if type(ins2) is Tag:
        if ins.tag==ins2.id: tag = ins2
        else: instructions_to_remove.clear()
        break
      instructions_to_remove.append(ins2)

    if instructions_to_remove:
      instructions_to_remove.insert(0, ins)

      for ins2 in instructions_to_remove:
        ins2.deleted = True
        INS.remove(ins2)
      instructions = '\n'.join(str(i) for i in instructions_to_remove)
      addReport(ins2.ln, 'Mirilla', 'Eliminacion de codigo inalcanzable R2', f'{instructions}\n{tag}', str(tag))

def optimize_control_flow(INS, eyehole_length):
  INS_COPY = INS[:eyehole_length]
  for ins in INS_COPY:
    if type(ins) is not If: continue
    if ins.deleted: continue

    index = INS_COPY.index(ins)
    INS2 = INS_COPY[index+1:]
    if len(INS2)<2: continue

    goto = INS2[0]
    if type(goto) is not Goto: continue

    true_tag = INS2[1]
    if type(true_tag) is not Tag: continue
    if ins.goto.tag != true_tag.id: continue

    target_tag = None

    for ins2 in INS2[2:]:
      if type(ins2) is Tag and goto.tag == ins2.id:
        target_tag = ins2
        break

    if not target_tag: continue

    original_ins = deepcopy(ins)

    ins.ex.type = inverse_operators[ins.ex.type]
    copy_goto = deepcopy(goto)
    ins.goto = copy_goto

    goto.deleted = True
    INS.remove(goto)
    true_tag.deleted = True
    INS.remove(true_tag)

    original = '\n'.join(str(i) for i in [original_ins, goto, true_tag, '...', target_tag])
    optimized = '\n'.join(str(i) for i in [ins, '...', target_tag])

    addReport(ins.ln, 'Mirilla', 'Optimizaciones de flujo de control R3', original, optimized)

  for ins in INS_COPY:
    if type(ins) is not Goto: continue
    if ins.deleted: continue

    index = INS_COPY.index(ins)
    INS2 = INS_COPY[index+1:]
    target_tag = None

    for ins2 in INS2:
      if type(ins2) is Tag and ins.tag == ins2.id:
        target_tag = ins2
        break

    if not target_tag: continue
    tag_index = INS.index(target_tag)

    if tag_index+1 >= len(INS): continue

    goto = INS[tag_index+1]
    if type(goto) is not Goto: continue

    original_ins = deepcopy(ins)

    ins.tag = goto.tag

    original = '\n'.join(str(i) for i in [original_ins, '...', target_tag, goto])
    optimized = '\n'.join(str(i) for i in [ins, '...', target_tag, goto])

    addReport(ins.ln, 'Mirilla', 'Optimizaciones de flujo de control R4', original, optimized)

  for ins in INS_COPY:
    if type(ins) is not If: continue
    if ins.deleted: continue

    index = INS_COPY.index(ins)
    INS2 = INS_COPY[index+1:]
    target_tag = None

    for ins2 in INS2:
      if type(ins2) is Tag and ins.goto.tag == ins2.id:
        target_tag = ins2
        break

    if not target_tag: continue
    tag_index = INS.index(target_tag)

    if tag_index+1 >= len(INS): continue

    goto = INS[tag_index+1]
    if type(goto) is not Goto: continue

    original_ins = deepcopy(ins)

    ins.goto.tag = goto.tag

    original = '\n'.join(str(i) for i in [original_ins, '...', target_tag, goto])
    optimized = '\n'.join(str(i) for i in [ins, '...', target_tag, goto])

    addReport(ins.ln, 'Mirilla', 'Optimizaciones de flujo de control R4', original, optimized)

def optimize_algebraic_expressions(INS, eyehole_length):
  INS_COPY = INS[:eyehole_length]
  for ins in INS_COPY:
    if type(ins) is not Assignment: continue
    if type(ins.ex) is not Expression: continue
    if ins.ex.type not in ['suma', 'resta', 'multiplicacion', 'division']: continue
    if type(ins.ex.left) is not Id and type(ins.ex.right) is not Id: continue

    if ins.ex.type in ['suma', 'multiplicacion']:
      id = ins.ex.left if type(ins.ex.left) is Id else ins.ex.right
      other = ins.ex.right if id==ins.ex.left else ins.ex.left
    else:
      id = ins.ex.left
      other = ins.ex.right

    if type(id) is not Id: continue
    if ins.id.value != id.value: continue
    if type(other) is not Number: continue

    if ins.ex.type in ['suma', 'resta'] and other.value == 0 or ins.ex.type in ['multiplicacion', 'division'] and other.value == 1:
        ins.deleted = True
        INS.remove(ins)
        addReport(ins.ln, 'Mirilla', 'Simplificacion algebraica R6', str(ins), '')

  for ins in INS_COPY:
    if type(ins) is not Assignment: continue
    if type(ins.ex) is not Expression: continue
    if ins.ex.type not in ['suma', 'resta', 'multiplicacion', 'division']: continue
    if type(ins.ex.left) is not Id and type(ins.ex.right) is not Id: continue

    if ins.ex.type in ['suma', 'multiplicacion']:
      id = ins.ex.left if type(ins.ex.left) is Id else ins.ex.right
      other = ins.ex.right if id==ins.ex.left else ins.ex.left
    else:
      id = ins.ex.left
      other = ins.ex.right

    if type(id) is not Id: continue
    if ins.id.value == id.value: continue
    if type(other) is not Number: continue

    original = deepcopy(ins)
    if ins.ex.type in ['suma', 'resta'] and other.value == 0 or ins.ex.type in ['multiplicacion', 'division'] and other.value == 1:
        ins.ex = id
        addReport(ins.ln, 'Mirilla', 'Simplificacion algebraica R7', str(original), str(ins))

  for ins in INS_COPY:
    if type(ins) is not Assignment: continue
    if type(ins.ex) is not Expression: continue
    if ins.ex.type not in ['multiplicacion', 'division']: continue
    if type(ins.ex.left) is not Id and type(ins.ex.right) is not Id: continue

    if ins.ex.type == 'multiplicacion':
      id = ins.ex.left if type(ins.ex.left) is Id else ins.ex.right
      other = ins.ex.right if id==ins.ex.left else ins.ex.left
    else:
      id = ins.ex.right
      other = ins.ex.left

    if type(id) is not Id: continue
    if type(other) is not Number: continue

    original = deepcopy(ins)
    if ins.ex.type == 'multiplicacion' and other.value in [0, 2] or ins.ex.type == 'division' and other.value == 0:
        if other.value==0:
          ins.ex = other
        else:
          ins.ex.type = 'suma'
          if id==ins.ex.left: ins.ex.right = id
          else: ins.ex.left = id
        addReport(ins.ln, 'Mirilla', 'Simplificacion algebraica R8', str(original), str(ins))

optimization_functions = [optimize_redundant_instructions, optimize_unreachable_code, optimize_control_flow, optimize_algebraic_expressions]
