import buckwalter
import sys

## TODO: Add tests to check for expected fails (non-ascii characters that couldn't be converted)!

with open("test_a2b.txt") as f:        
    for l in f.readlines():
        l = l.rstrip()
        fs = list(filter(None, l.split("\t")))
        a = fs[0]
        b = fs[1]
        a2, ok1 = buckwalter.b2a(b, True)
        b2, ok2 = buckwalter.a2b(a, True)
        a2x, ok3 = buckwalter.b2a(b, False)
        b2x, ok4 = buckwalter.a2b(a, False)
        if a2 != a:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, a2), file=sys.stderr)
        if b2 != b:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, b2), file=sys.stderr)
        if a2x != a:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, a2), file=sys.stderr)
        if b2x != b:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, b2), file=sys.stderr)

        if not(ok1):
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, a2), file=sys.stderr)
        if not(ok2):
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, b2), file=sys.stderr)
        if not(ok3):
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, a2x), file=sys.stderr)
        if not(ok4):
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, b2x), file=sys.stderr)

            
with open("test_b2a.txt") as f:        
    convertNumbers = True
    for l in f.readlines():
        l = l.rstrip()
        fs = list(filter(None, l.split("\t")))
        b = fs[0]
        a = fs[1]
        a2, ok1 = buckwalter.b2a(b, True)
        b2, ok2 = buckwalter.a2b(a, True)
        a2x, ok3 = buckwalter.b2a(b, False)
        b2x, ok4 = buckwalter.a2b(a, False)
        if a2 != a:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, a2), file=sys.stderr)
        if b2 != b:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, b2), file=sys.stderr)
        if a2x != a:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, a2), file=sys.stderr)
        if b2x != b:
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, b2), file=sys.stderr)

        if not(ok1):
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, a2), file=sys.stderr)
        if not(ok2):
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, b2), file=sys.stderr)
        if not(ok3):
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, a2x), file=sys.stderr)
        if not(ok4):
            print("FAIL\tFrom '{}', expected '{}', found '{}'".format(a, b, b2x), file=sys.stderr)
