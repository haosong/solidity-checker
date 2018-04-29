from subprocess import call
import sys
import json
import pprint
from case9 import case9, case8, case10
from warningLog import Warning, WarningLogger

pp = pprint.PrettyPrinter(indent=1)
warning = []
logger = None


def checkCases(file):
    errorRanges = []
    errorRanges += case8(file)
    errorRanges += case9(file)
    errorRanges += case10(file)
    for errorRange in errorRanges:
        logger.log(errorRange)

# node: file node
def check(node):
    # pp.pprint(file)
    for contract in node["body"]:
        find(node)
        check_low_level_func_return(contract)
        state_var = find_state_var(contract)
        print(state_var)
        for statement in contract["body"]:
            if statement["type"] == "FunctionDeclaration":
                check_func_reentry(statement, state_var)
    #     print(len(warning))
    checkCases(node)
    pass


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
                    if_var.append(node["test"][side]["name"])
                elif node["test"][side]["type"] == "MemberExpression":
                    if_var.append(node["test"][side]["object"]["name"])
        elif node["test"]["type"] == "UnaryExpression":
            pass
        for statement in node["consequent"]["body"]:
            find_if_var(statement, if_var)
    else:
        pass


def find_call(node, state_var, if_var, flag):
    try:
        if "start" in node:
            if "type" in node and node["type"] == "CallExpression":
                flag = [True]
        if flag[0]:
            if "type" in node and node["type"] == "AssignmentExpression":
                pass
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
    if_var = []
    for obj in node["body"]["body"]:
        # find all if-statement: return set of vars
        find_if_var(obj, if_var)
        if len(if_var) == 0:
            return
        print("if_var: ", if_var)
        # find first call statement
        flag = [False]
        find_call(obj, state_var, if_var, flag)
        # check statement after that, change set of vars or not
        pass
    pass


def check_low_level_func_return(file):
    if isinstance(file, list):
        for f in file:
            check_low_level_func_return(f)
        return
    elif isinstance(file, dict):
        if file["type"] == "IfStatement":
            return
        if file["type"] == "Identifier" and "name" in file and file["name"] == "call":
            print("start", ":", file["start"], " no check!")
        else:
            for f in file:
                check_low_level_func_return(file[f])


# Check static error
def find(node):
    try:
        if "start" in node:
            start = node["start"]
            end = node["end"]
            if "name" in node:
                name = node["name"]
                if name == "sha3":
                    warning.append(Warning(start, end, name))
                    print("Find sha3() at [", start, end, "], please change to keccak256()")
                elif name == "send":
                    warning.append(Warning(start, end, name))
                    print("Find send() at [", start, end, "], please change to transfer()")
                elif name == "suicide":
                    warning.append(Warning(start, end, name))
                    print("Find suicide() at [", start, end, "], please change to selfdestruct()")
            if "type" in node and node["type"] == "ThrowStatement":
                warning.append(Warning(start, end, "throw"))
                print("Find throw at [", start, end, "], please change to revert()")
        # Iterate through current node's children
        for _, value in node.items():
            if isinstance(value, list):
                for obj in value:
                    find(obj)
            else:
                find(value)
    except:
        pass


if __name__ == '__main__':
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        logger = WarningLogger(fileName)
        call(["./json.sh", fileName])
        with open('./data/ast.json') as json_data:
            check(json.load(json_data))

