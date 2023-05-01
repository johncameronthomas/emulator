import sys
import json

from Emulator import Emulator

f = open(sys.argv[1])
program = json.load(f)
f.close()

emulator = Emulator(program)
emulator.run()
print(emulator)