from utils.warningLog import Warning

warning = []


# node: file node
def check_reentry(node):
    # pp.pprint(file)
    for contract in node["body"]:
        find(node)
        check_low_level_func_return(contract)
        state_var = find_state_var(contract)
        # print(state_var)
        for statement in contract["body"]:
            if statement["type"] == "FunctionDeclaration":
                check_func_reentry(statement, state_var)
    #     print(len(warning))
    return warning


# node: contract node
def find_state_var(node):
    state_var = []
    for statement in node["body"]:
        if statement["type"] == "StateVariableDeclaration":
            state_var.append(statement["name"])
    return state_var


# DFS find all if-statement and return vars in conditions
def find_if_var(node, if_var):
    if node["type"] == "IfStatement":
        if node["test"]["type"] == "BinaryExpression":
            for side in ["left", "right"]:
                if node["test"][side]["type"] == "Identifier":
                    if node["test"][side]["name"] not in if_var:
                        if_var[node["test"][side]["name"]] = node["start"]
                elif node["test"][side]["type"] == "MemberExpression":
                    if node["test"][side]["object"]["name"] not in if_var:
                        if_var[node["test"][side]["object"]["name"]] = node["start"]
        elif node["test"]["type"] == "UnaryExpression":
            pass
        for statement in node["consequent"]["body"]:
            find_if_var(statement, if_var)
    else:
        pass


def find_call(node, state_var, if_var, flag):
    try:
        if "start" in node:
            if not flag[0] and "type" in node and node["type"] == "CallExpression":
                flag[0] = True
            if flag[0]:
                if "expression" in node and node["expression"]["type"] == "AssignmentExpression":
                    name = node["expression"]["left"]["object"]["name"]
                    if name in state_var and name in if_var:
                        warning.append(Warning(if_var[name], node["end"],
                                               "Could potentially lead to re-entrancy vulnerability\n"
                                               "http://solidity.readthedocs.io/en/develop/security-considerations.html#re-entrancy"))
                        # print("Find re-entry at [", if_var[name], node["end"], "]")
        # Iterate through current node's children
        for _, value in node.items():
            if isinstance(value, list):
                for obj in value:
                    find_call(obj, state_var, if_var, flag)
            else:
                find_call(value, state_var, if_var, flag)
        pass
    except:
        pass


# node: function node
def check_func_reentry(node, state_var):
    # array of all statements in the function
    if_var = {}
    for obj in node["body"]["body"]:
        # find all if-statement: return set of vars
        find_if_var(obj, if_var)
    # find first call statement
    if len(if_var) == 0:
        return
    # print("if_var: ", if_var)
    flag = [False]
    find_call(node, state_var, if_var, flag)
    # check statement after that, change set of vars or not


def check_low_level_func_return(node):
    if isinstance(node, list):
        for f in node:
            check_low_level_func_return(f)
        return
    elif isinstance(node, dict):
        if node["type"] == "IfStatement":
            return
        if node["type"] == "Identifier" and "name" in node and node["name"] == "call":
            warning.append(Warning(node["start"], node["end"], "Low-level call() result unchecked\n"
                                                               "https://github.com/ConsenSys/smart-contract-best-practices#external-calls"))
            # print("Find not check call() return value at [", node["start"], node["end"], "]")
        else:
            for f in node:
                check_low_level_func_return(node[f])


# Check static error
def find(node):
    try:
        if "start" in node:
            start = node["start"]
            end = node["end"]
            if "name" in node:
                name = node["name"]
                if name == "sha3":
                    warning.append(Warning(start, end, "Use keccak256() instead of sha3()\n"
                                                       "https://github.com/ethereum/EIPs/issues/59"))
                    # print("Find sha3() at [", start, end, "], please change to keccak256()")
                elif name == "send":
                    warning.append(Warning(start, end, "Use transfer() instead of send()\n"
                                                       "http://solidity.readthedocs.io/en/develop/types.html#members-of-addresses"))
                    # print("Find send() at [", start, end, "], please change to transfer()")
                elif name == "suicide":
                    warning.append(Warning(start, end, "Use selfdestruct() instead of suicide()\n"
                                                       "https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6.md"))
                    # print("Find suicide() at [", start, end, "], please change to selfdestruct()")
            if "type" in node and node["type"] == "ThrowStatement":
                warning.append(Warning(start, end, "Use revert() instead of throw\n"
                                                   "https://solidity.readthedocs.io/en/develop/control-structures.html#error-handling-assert-require-revert-and-exceptions"))
                # print("Find throw at [", start, end, "], please change to revert()")
        # Iterate through current node's children
        for _, value in node.items():
            if isinstance(value, list):
                for obj in value:
                    find(obj)
            else:
                find(value)
    except:
        pass
