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
