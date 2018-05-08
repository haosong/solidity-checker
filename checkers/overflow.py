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
        if node["type"] == "AssignmentExpression" and node["left"]["type"] in ("DeclarativeExpression", "Identifier"):
            expression = node["right"]
            if expression["type"] == "BinaryExpression":
                left, right = check_left_right_expression(expression)
                if left and right:
                    if expression["operator"] == "+":
                        add_check.append((node["left"]["name"], left,
                                          right, expression["start"], expression["end"]))  # (c,a,b)

                    elif expression["operator"] == "*":
                        mul_check.append((node["left"]["name"], left,
                                          right, expression["start"], expression["end"]))  # (c,a,b)`

                    elif expression["operator"] == "-":
                        arg = (right, left)  # (b, a)
                        # check if assert function has been used for the subtraction op
                        if arg not in ass:
                            warning.append(Warning(expression["start"], expression["end"],
                                                   "The subtraction operation might overflow\n"
                                                   "https://ethereumdev.io/safemath-protect-overflows/"))
                            # print("Find possible subtraction operation overflow at [", expression["start"],
                            #       expression["end"], "]")
        elif "callee" in node:
            expression = node["callee"]
            if expression["type"] == "Identifier" and expression["name"] == "assert":
                conditions = node["arguments"]
                for c in conditions:  # check add
                    if c["type"] == "BinaryExpression":
                        pair = None
                        if c["operator"] == "||":
                            check_mul_helper((c["left"], c["right"]), mul_check)
                            break
                        left, right = check_left_right_expression(c)
                        if left and right:
                            if c["operator"] == ">=" or c["operator"] == ">":
                                pair = (right, left)
                            elif c["operator"] == "<=" or c["operator"] == "<":
                                pair = (left, right)
                            else:
                                break
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


def check_left_right_expression(c):

    left = get_value_or_name(c["left"])
    right = get_value_or_name(c["right"])

    return left, right


def get_value_or_name(exp):
    if exp["type"] == "Identifier":
        return exp["name"]
    elif exp["type"] == "Literal":
        return str(exp["value"])
    else:
        return None


def check_mul_helper(exp, mul_check):
    print("check mul")
    zero = None
    div = None

    for e in exp:

        if e["right"]["type"] == "BinaryExpression" and get_value_or_name(e["left"]) and e["right"]["operator"] == "/":
            left, right = check_left_right_expression(e["right"])
            if left and right:
                div = (left, right, get_value_or_name(e["left"]))

        elif e["left"]["type"] == "BinaryExpression" and get_value_or_name(e["right"]) and e["left"]["operator"] == "/":
            left, right = check_left_right_expression(e["left"])
            if left and right:
                div = (left, right, get_value_or_name(e["right"]))

        elif e["type"] == "BinaryExpression" and e["operator"] == "==":

            z = None
            if e["right"]["type"] == "Literal" and e["right"]["value"] == 0:
                z = e["left"]
            elif e["left"]["type"] == "Literal" and e["left"]["value"] == 0:
                z = e["right"]
            if z:
                zero = get_value_or_name(z)

    if zero and div:
        if zero != div[1]:
            return
        for t in mul_check:
            if (zero == t[1] and div[0] == t[0] and div[2] == t[2]) or (
                    zero == t[2] and div[0] == t[0] and div[2] == t[1]):
                mul_check.remove(t)
                break
