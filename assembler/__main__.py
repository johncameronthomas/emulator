import sys
import json

from assemble import assemble

f = open(sys.argv[1])
code = f.read()
f.close()

program = assemble(code)

f = open('bin.json', 'w')
json.dump(program, f)
f.close()
