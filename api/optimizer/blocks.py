from copy import deepcopy
from api.optimizer.analyzer import parse
from api.optimizer.core import Block, addReport, reset, reports
from api.optimizer.symbols import Assignment, Expression, Goto, Id, If, Number, Tag, inverse_operators

def optimize(input):
  global reports
  reset()

  header = ''
  for _ in range(10):
    index = input.find('\n')
    header += input[:index+1]
    input = input[index+1:]

  header += '\n'
  res = parse(input)
  functions = res['ast']

  blocks = {function.id: getBlocks(function.ins) for function in functions}

  for function_blocks in blocks:
    for block in function_blocks:
      for optimizer in optimization_functions:
        optimizer(block.ins)

  for function in functions:
    function.ins = []
    for function_blocks in blocks[function.id]:
      for block in function_blocks:
        function.ins += block.ins

  output = header + str('\n\n'.join(str(function) for function in functions))
  return {'output': output, 'reports': reports}

def getBlocks(INS):
  blocks = []
  instructions = []
  add_block = False

  for ins in INS:
    if type(ins) is Tag or add_block:
      instructions = []
      blocks.append(Block(instructions))
      add_block = False
    elif type(ins) in [Goto, If]:
      add_block = True
    instructions.append(ins)

  previousBlock = None
  for block in blocks:
    if previousBlock: previousBlock.addNextBlock(block)
    previousBlock = block

  for block in blocks:
    ins = block.ins[-1]
    if type(ins) not in [Goto, If]: continue

    for nextBlock in blocks:
      tag = nextBlock.ins[0]
      if type(tag) is not Tag: continue
      if (type(ins) is Goto and tag.id != ins.tag or
          type(ins) is If   and tag.id != ins.goto.tag): continue
      block.addNextBlock(nextBlock)

  return blocks

def optimize_common_subexpressions(ins):
  print(ins)

def optimize_copies_propagation(ins):
  print(ins)

def optimize_dead_code(ins):
  print(ins)

def optimize_constants_propagation(ins):
  print(ins)

optimization_functions = [optimize_common_subexpressions, optimize_copies_propagation, optimize_dead_code, optimize_constants_propagation]
