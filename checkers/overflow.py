from utils.warningLog import Warning

add_check = []
assertions = []

warning = []


def check_num_overflow(node):
    check_overflow(node, add_check, assertions)
    return warning


def check_overflow(node, add_check, assertions):
    if isinstance(node, list):
        for n in node:
            check_overflow(n, add_check, assertions)
        return
    elif isinstance(node, dict):
        # print(node["start"])
        if node["type"] == "AssignmentExpression":
            expression = node["right"];
            if expression["type"] == "BinaryExpression":
                if expression["operator"] == "+":
                    # print("add")
                    add_check.append((node["left"]["name"], expression["left"]["name"],
                                      expression["right"]["name"], expression["start"]));  # (c,a,b)
                    # print("add_check:", add_check)

                elif expression["operator"] == "-":
                    # print("sub")
                    arg = (expression["right"]["name"], expression["left"]["name"])  # (b, a)
                    # check if assert function has been used for the subtraction op
                    # print("assertions: ", assertions)
                    if arg not in assertions:
                        warning.append(
                            Warning(expression["start"], expression["end"], "The subtraction operation might overflow\n"
                                                                            "https://ethereumdev.io/safemath-protect-overflows/"))
                        # print("Find possible subtraction operation overflow at [", expression["start"],
                        #       expression["end"], "]")

        elif "callee" in node:
            expression = node["callee"]
            if expression["type"] == "Identifier" and "name" in expression and expression["name"] == "assert":
                conditions = node["arguments"]
                for c in conditions:
                    if c["type"] == "BinaryExpression":

                        pair = None
                        if c["operator"] == ">=" or c["operator"] == ">":
                            pair = (c["right"]["name"], c["left"]["name"])
                        elif c["operator"] == "<=" or c["operator"] == "<":
                            pair = (c["left"]["name"], c["right"]["name"])

                        # check if it is used to verify the add op
                        f = True
                        # print("pair:", pair)
                        for t in add_check:
                            if (pair[0] == t[1] or pair[0] == t[2]) and pair[1] == t[0]:
                                add_check.remove(t)
                                f = False
                                break
                        if f:
                            assertions.append(pair)
        else:
            for n in node:
                check_overflow(node[n], add_check, assertions)
    pass
