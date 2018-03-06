import buckwalter
import sys

with open("test_a2b.txt") as f:        
    for l in f.readlines():
        l = l.rstrip()
        fs = list(filter(None, l.split("\t")))
        a = fs[0]
        b = fs[1]
        a2 = buckwalter.b2a(b)
        b2 = buckwalter.a2b(a)
        if b2 != b:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, b2), file=sys.stderr)
        if a2 != a:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, a2), file=sys.stderr)
        
with open("test_b2a.txt") as f:        
    for l in f.readlines():
        l = l.rstrip()
        fs = list(filter(None, l.split("\t")))
        b = fs[0]
        a = fs[1]
        b2 = buckwalter.a2b(a)
        a2 = buckwalter.b2a(b)
        if b2 != b:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, b2), file=sys.stderr)
        if a2 != a:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, a2), file=sys.stderr)
        
