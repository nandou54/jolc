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

