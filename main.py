from subprocess import call
import sys
import json
import pprint

pp = pprint.PrettyPrinter(indent=1)

def check(file):
    pp.pprint(file)
    pass


if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            fileName = sys.argv[1]
            call(["./json.sh", fileName])
            with open('./tmp/result.json') as json_data:
                check(json.load(json_data))
    except:
        sys.exit(1)
