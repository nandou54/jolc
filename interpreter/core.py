output:list = []
errors:list = []
symbols:list = []

envs:list = []
functions:list = []
loops:list = []


class Environment():
  def __init__(self, id = 'global', parent = None) -> None:
    self.id = id
    self.parent = parent
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
      tempEnv = tempEnv.parent
    return False

globalEnv: Environment

RESERVED_FUNCTIONS:dict = {}

OPERATION_RESULTS:dict = {}
