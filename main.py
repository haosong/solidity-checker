from subprocess import call
import sys
import json
import pprint
from case9 import case9, case8, case10
from warningLog import Warning, WarningLogger
from reentry import check

pp = pprint.PrettyPrinter(indent=1)
warning = []
logger = None


# def checkCases(file):
#     errorRanges = []
#     errorRanges += case8(file)
#     errorRanges += case9(file)
#     errorRanges += case10(file)
#     for errorRange in errorRanges:
#         logger.log(errorRange)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        logger = WarningLogger(fileName)
        call(["./json.sh", fileName])
        with open('./data/ast.json') as json_data:
            warning = check(json.load(json_data))
        for w in warning:
            logger.log(w)            

