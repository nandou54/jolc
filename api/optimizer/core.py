from api.optimizer.symbols import Expression, Goto, Id, If, Number, Tag

block_counter = 0

optimizations = 0
reports = []

def reset():
  global optimizations
  optimizations = 0

  reports.clear()

def Report(ln, type, rule, original, optimized):
  return [ln, type, rule, original, optimized]

def addReport(ln, type, rule, original, optimized):
  reports.append(Report(ln, type, rule, original, optimized))

class Block():
  def __init__(self, ins):
    global block_counter
    self.id = f'B{block_counter}'
    block_counter += 1
    self.ins = ins
    self.nextBlocks = []

  def addNextBlock(self, block):
    if block not in self.nextBlocks:
      self.nextBlocks.append(block)

def getBlocks(INS):
  blocks = []
  instructions = []
  add_block = False

  blocks.append(Block(instructions))

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

def getIds(ex):
  if type(ex) is Id: return [ex]
  if type(ex) is Expression:
    return [*getIds(ex.left), *getIds(ex.right)]
  return []

def expressionsAreEqual(ex1, ex2):
  if type(ex1) is Expression and type(ex2) is Expression:
    return expressionsAreEqual(ex1.left, ex2.left) and expressionsAreEqual(ex1.right, ex2.right)
  elif type(ex1) is Number and type(ex2) is Number:
    return ex1.value==ex2.value
  elif type(ex1) is Id and type(ex2) is Id:
    return ex1.value==ex2.value
  return False
