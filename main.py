from subprocess import call
import sys
import json
import pprint
from case9 import case9, case8, case10
from printWarning import printWarning

pp = pprint.PrettyPrinter(indent=1)

def check(file):
    # pp.pprint(file['body'])
    errorRanges = []
    errorRanges += case8(file)
    errorRanges += case9(file)
    errorRanges += case10(file)
    for errorRange in errorRanges:
      printWarning('', *errorRange)


if __name__ == '__main__':
    # try:
        if len(sys.argv) == 2:
            fileName = sys.argv[1]
            call(["./json.sh", fileName])
            with open('./tmp/result.json') as json_data:
                check(json.load(json_data))
    # except:
    #     sys.exit(1)
