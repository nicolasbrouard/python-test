#!/usr/bin/python3.2
from datetime import datetime

start = datetime.now()
print start

print("Hello World!")

the_world_is_flat = True
if the_world_is_flat:
    print("Be careful not to fall off!")

for i in range(10, 20, 2):
    print(i)

class myClass:
    def __init__(self):
        print("constructor")
    pass

    def test(self):
        print("test")
        return "result"

obj = myClass()
print(obj.test())

l = list(range(0, 2, 1))
reverse = l.reverse()

stop = datetime.now()
print stop
print "Elapsed time: ", 1000.0 / (stop - start).microseconds, " ms"

print True
print not True