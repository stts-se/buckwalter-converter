import buckwalter
from sys import stderr

a2bTest = {
}

b2aTest = {
}

for a, b in a2bTest.items():
    b2 = buckwalter.a2b(a)
    a2 = buckwalter.b2a(b)
    if b2 != b:
        print("FAIL\tFrom {}, expected {}, found {}".format(a, b, b2), file=stderr)
    if a2 != a:
        print("FAIL\tFrom {}, expected {}, found {}".format(a, b, a2), file=stderr)
    

for b, a in b2aTest.items():
    b2 = buckwalter.a2b(a)
    a2 = buckwalter.b2a(b)
    if b2 != b:
        print("FAIL\tFrom {}, expected {}, found {}".format(a, b, b2), file=stderr)
    if a2 != a:
        print("FAIL\tFrom {}, expected {}, found {}".format(a, b, a2), file=stderr)
    
