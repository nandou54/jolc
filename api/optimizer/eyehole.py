from api.optimizer.analyzer import parse
from api.optimizer.symbols import Assignment, Goto, Id, Tag

def reset():
  global optimizations
  optimizations = 0

  reports.clear()

def Report(ln, type, rule, original, optimized):
  return [ln, type, rule, original, optimized]

def addReport(ln, type, rule, original, optimized):
  reports.append(Report(ln, type, rule, original, optimized))

optimizations = 0
reports = []

def optimize(input):
  global reports
  reset()

  res = parse(input)
  INS = []
  for function in res['ast']:
    INS += function.ins

  for optimizer in optimization_functions:
    optimizer(INS)

  print(reports)

def optimize_redundant_instructions(INS: list):
  INS_COPY = INS.copy()
  for ins in INS_COPY:
    if type(ins) is not Assignment: continue
    if type(ins.ex) is not Id: continue
    if ins.deleted: continue

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

def optimize_unreachable_code(INS: list):
  INS_COPY = INS.copy()
  for ins in INS_COPY:
    if type(ins) is not Goto: continue
    if ins.deleted: continue

    index = INS_COPY.index(ins)
    INS2 = INS_COPY[index+1:]

    for ins2 in INS2:
      if type(ins2) is Tag and ins.tag==ins2.id: break
      ins2.deleted = True
      INS.remove(ins2)
      addReport(ins2.ln, 'Mirilla', 'Eliminacion de codigo inalcanzable R1', f'{ins}\n{ins2}', str(ins))

optimization_functions = [optimize_redundant_instructions, optimize_unreachable_code]
