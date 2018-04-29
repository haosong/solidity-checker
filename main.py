from subprocess import call
import sys
import json
import pprint
from utils.warningLog import Warning, WarningLogger
from checkers.reentry import checkReentry
from checkers.funcLevel import checkFunctionLevel



if __name__ == '__main__':
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        logger = WarningLogger(fileName)
        call(["./bin/json.sh", fileName])
        with open('./data/ast.json') as f:
            json_data = json.load(f)
            warning = checkReentry(json_data)
            warning += checkFunctionLevel(json_data)
            for w in warning:
                logger.log(w)            

