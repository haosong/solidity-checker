from utils.warningLog import Warning

add_check = []
assertions = []

warning = []


def check_num_overflow(node):
    add_check = []
    ass = []
    mul_check = []
    check_overflow(node, add_check, ass, mul_check)
    if len(add_check) > 0:
        for a in add_check:
            warning.append(Warning(a[3], a[4], "The addition operation might overflow\n"
                                   "https://ethereumdev.io/safemath-protect-overflows/"))
            # print("The add operation might overflow! start: ", a[3])
    if len(mul_check) > 0:
        for a in mul_check:
            warning.append(Warning(a[3], a[4], "The multiplication operation might overflow\n"
                                               "https://ethereumdev.io/safemath-protect-overflows/"))
            # print("The multiplication operation might overflow! start: ", a[3])
    return warning


def check_overflow(node, add_check, ass, mul_check):
    if isinstance(node, list):
        for n in node:
            check_overflow(n, add_check, ass, mul_check)
        return
    elif isinstance(node, dict):
        if node["type"] == "AssignmentExpression":
            expression = node["right"]
            if expression["type"] == "BinaryExpression":
                if expression["operator"] == "+":
                    add_check.append((node["left"]["name"], expression["left"]["name"],
                                      expression["right"]["name"], expression["start"], expression["end"]))  # (c,a,b)

                elif expression["operator"] == "*":
                    mul_check.append((node["left"]["name"], expression["left"]["name"],
                                      expression["right"]["name"], expression["start"], expression["end"]))  # (c,a,b)`

                elif expression["operator"] == "-":
                    arg = (expression["right"]["name"], expression["left"]["name"])  # (b, a)
                    # check if assert function has been used for the subtraction op
                    if arg not in ass:
                        warning.append(Warning(expression["start"], expression["end"],
                                               "The subtraction operation might overflow\n"
                                               "https://ethereumdev.io/safemath-protect-overflows/"))
                        # print("Find possible subtraction operation overflow at [", expression["start"],
                        #       expression["end"], "]")
        elif "callee" in node:
            expression = node["callee"]
            if expression["type"] == "Identifier" and "name" in expression and expression["name"] == "assert":
                conditions = node["arguments"]
                for c in conditions:  # check add
                    if c["type"] == "BinaryExpression":
                        pair = None
                        if c["operator"] == "||":
                            check_mul_helper((c["left"], c["right"]), mul_check)
                            break
                        elif c["operator"] == ">=" or c["operator"] == ">":
                            pair = (c["right"]["name"], c["left"]["name"])
                        elif c["operator"] == "<=" or c["operator"] == "<":
                            pair = (c["left"]["name"], c["right"]["name"])
                        else:
                            break

                        # check if it is used to verify the add op
                        f = True
                        for t in add_check:
                            if (pair[0] == t[1] or pair[0] == t[2]) and pair[1] == t[0]:
                                add_check.remove(t)
                                f = False
                                break
                        if f:
                            ass.append(pair)

        else:
            for n in node:
                check_overflow(node[n], add_check, ass, mul_check)
    pass


def check_mul_helper(exp, mul_check):
    zero = None
    div = None

    for e in exp:
        if e["type"] == "BinaryExpression" and e["operator"] == "==":
            if e["right"]["type"] == "Literal" and e["right"]["value"] == 0 and e["left"]["type"] == "Identifier":
                zero = e["left"]["name"]
            elif e["left"]["type"] == "Literal" and e["left"]["value"] == 0 and e["right"]["type"] == "Identifier":
                zero = e["right"]["name"]
            elif e["left"]["type"] == "Identifier" and e["right"]["type"] == "BinaryExpression" and e["right"][
                "operator"] == "/":
                if e["right"]["left"]["type"] == "Identifier" and e["right"]["right"]["type"] == "Identifier":
                    div = (e["right"]["left"]["name"], e["right"]["right"]["name"], e["left"]["name"])
            elif e["right"]["type"] == "Identifier" and e["left"]["type"] == "BinaryExpression" and e["left"][
                "operator"] == "/":
                if e["left"]["left"]["type"] == "Identifier" and e["left"]["right"]["type"] == "Identifier":
                    div = (e["left"]["left"]["name"], e["left"]["right"]["name"], e["right"]["name"])

    if zero and div:
        if zero != div[1]:
            return
        for t in mul_check:
            if (zero == t[1] and div[0] == t[0] and div[2] == t[2]) or (
                    zero == t[2] and div[0] == t[0] and div[2] == t[1]):
                mul_check.remove(t)
                break
