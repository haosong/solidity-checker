# class Warning:
#   def __init__(self, start, end, message):
#     self.start = start
#     self.end = end
#     self.message = message

# def printWarning(warning):


def printWarning(filename, start, end, message):
  filename = 'simpledao.sol'
  f = open(filename, 'r')
  lineRanges = []
  lines = f.readlines()
  idx = 0
  for lineNum, line in enumerate(lines):
    lineEnd = idx + len(line)
    lineRanges.append((idx, lineEnd))
    idx = lineEnd
  startLine = endLine = 0

  for lineNum, lineRange in enumerate(lineRanges):
    if lineRange[0] <= start and start <= lineRange[1]:
      startLine = lineNum
    if lineRange[0] < end and end <= lineRange[1]:
      endLine = lineNum
  print '================================ warning ================================\n'
  if startLine == endLine: # inline error
    offset = start - lineRanges[startLine][0]
    print lines[startLine].strip('\n')
    print ' ' * offset + '^--', message, '\n'
  else:
    for line in lines[startLine:endLine + 1]:
      print line.strip('\n')
    print '-->', message, '\n'
