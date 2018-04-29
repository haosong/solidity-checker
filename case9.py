from warningLog import Warning

def case9(ast): # detectNoReturnStatement
  errorRanges = []
  functionNodes = []
  findType(ast, 'FunctionDeclaration', functionNodes)
  # print findNoReturnStatementRanges(functionNodes)
  for funcNode in functionNodes:
    if funcNode['returnParams']:
      funcWithReturnStm = []
      findType(funcNode, 'ReturnStatement', funcWithReturnStm)
      if len(funcWithReturnStm) == 0:
        errorRanges.append(Warning(funcNode['start'], funcNode['end'], 'No Return Statement'))
  return errorRanges

def case8(ast): # detectNowUsage
  errorRanges = []
  nowNodes = []
  findTypeAndName(ast, 'Identifier', 'now', nowNodes)
  for nowNode in nowNodes:
    errorRanges.append(Warning(nowNode['start'], nowNode['end'], 'Do not use now for randomness'))
  return errorRanges

def case10(ast): # detect fallback function
  noNameFuncNodes = []
  findFallbackFunctions(ast, noNameFuncNodes)
  errorRanges = []
  if len(noNameFuncNodes) == 0:
    errorRanges.append(Warning(ast['start'], ast['end'], 'Contract has no fallback function'))
  elif len(noNameFuncNodes) > 1:
    for idx, node in enumerate(noNameFuncNodes, 1):
      errorRanges.append(Warning(node['start'], node['end'], 'More than one fallback function'))
  else:
    errorRanges += inspectFallbackFunction(noNameFuncNodes[0])
  return errorRanges

def inspectFallbackFunction(node):
  errorRanges = []
  funcWithReturnStm = []
  findType(node, 'ReturnStatement', funcWithReturnStm)
  if len(funcWithReturnStm) > 0:
    errorRanges.append(Warning(node['start'], node['end'], 'Fallback function should not have a return statement.'))
  payableModifier = []
  findTypeAndName(node, 'ModifierArgument', 'payable', payableModifier)
  if len(payableModifier) == 0:
    errorRanges.append(Warning(node['start'], node['end'], 'Fallback function should have "payable" modifier.'))
  return errorRanges

def findFallbackFunctions(node, ret):
  if not isinstance(node, dict) and not isinstance(node, list):
    return
  if node['type'] == 'FunctionDeclaration' and node['name'] == None and node['params'] == None and node['returnParams'] == None:
    return ret.append(node)
  for key, val in node.items():
    if isinstance(val, list):
      for child in val:
        findFallbackFunctions(child, ret)
    else:
      findFallbackFunctions(val, ret)

def findTypeAndName(node, type, name, ret):
  if not isinstance(node, dict) and not isinstance(node, list):
    return
  if node['type'] == type and node['name'] == name:
    return ret.append(node)
  for key, val in node.items():
    if isinstance(val, list):
      for child in val:
        findTypeAndName(child, type, name, ret)
    else:
      findTypeAndName(val, type, name, ret)


def findType(node, type, ret):
  if not isinstance(node, dict) and not isinstance(node, list):
    return
  # print 'entering', node['type'], node['start'], node['end']
  if node['type'] == type:
    return ret.append(node)
  for key, val in node.items():
    if isinstance(val, list):
      for child in val:
        findType(child, type, ret)
    else:
      findType(val, type, ret)
