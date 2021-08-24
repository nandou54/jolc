output:list = []
errors:list = []
symbols:list = []

class Environment():
  def __init__(self, id = 'global') -> None:
    self.id = id
    self.back = None
    self.symbols = {}

  def declareSymbol(self, id, value):
    self.symbols[id] = value
  
  def getLocalSymbol(self, id):
    if id not in self.symbols.keys(): return False
    return self.symbols[id]
    
  def getGlobalSymbol(self, id):
    tempEnv = self
    while tempEnv != None:
      if tempEnv.getLocalSymbol(id):
        return tempEnv.getLocalSymbol(id)
      tempEnv = tempEnv.back
    return False


globalEnv = Environment()


RESERVED_FUNCTIONS:dict = {}

OPERATION_RESULTS:dict = {}
