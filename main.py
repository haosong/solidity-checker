from subprocess import call
import sys
import json
import pprint
from utils.warningLog import Warning, WarningLogger
from checkers.reentry import check_reentry
from checkers.funcLevel import check_functionLevel
from checkers.overflow import check_num_overflow

if __name__ == '__main__':
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        logger = WarningLogger(fileName)
        call(["./bin/json.sh", fileName])
        with open('./data/ast.json') as f:
            json_data = json.load(f)
            warning = check_reentry(json_data)
            warning += check_functionLevel(json_data)
            warning += check_num_overflow(json_data)
            for w in warning:
                logger.log(w)
