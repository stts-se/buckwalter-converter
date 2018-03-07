import buckwalter
import sys
import re

## TODO: Add tests to check for expected fails (non-ascii characters that couldn't be converted)!

with open("test_data/test_a2b.txt", encoding="utf-8") as f:  
    for l in re.split("\n\n+", f.read()):
        l = l.rstrip()
        if l.strip() == "":
            continue
        if l.strip().startswith("#"):
            print("SKIPPING:\n" + l, file=sys.stderr)
            continue
        fs = list(filter(None, l.split("\n")))
        a = fs[0]
        b = fs[1]
        
        buckwalter.convertNumbers = True
        bn, a2, msg1, ok1 = buckwalter.b2a(b)
        an, b2, msg2, ok2 = buckwalter.a2b(a)
        buckwalter.convertNumbers = False
        bn, a2x, msg3, ok3 = buckwalter.b2a(b)
        an, b2x, msg4, ok4 = buckwalter.a2b(a)

        if a2 != an:
            print("FAIL a2b (1)\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(bn, a, a2), file=sys.stderr)
        elif b2 != bn:
            print("FAIL a2b (2)\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(an, b, b2), file=sys.stderr)
        elif a2x != an:
            print("FAIL a2b (3)\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(bn, a, a2x), file=sys.stderr)
        elif b2x != bn:
            print("FAIL a2b (4)\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(an, b, b2x), file=sys.stderr)
        elif not ok1:
            print("FAIL a2b (5) {}\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(msg1, bn, a, a2), file=sys.stderr)
        elif not ok2:
            print("FAIL a2b (6) {}\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(msg2, an, b, b2), file=sys.stderr)
        elif not ok3:
            print("FAIL a2b (7) {}\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(msg3, bn, a, a2x), file=sys.stderr)
        elif not ok4:
            print("FAIL a2b (8) {}\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(msg4, an, b, b2x), file=sys.stderr)


            
with open("test_data/test_b2a.txt", encoding="utf-8") as f:
    convertNumbers = True
    for l in re.split("\n\n+", f.read()):
        l = l.rstrip()
        if l.strip() == "":
            continue
        if l.strip().startswith("#"):
            print("SKIPPING\t" + l, file=sys.stderr)
            continue
        fs = list(filter(None, l.split("\n")))
        b = fs[0]
        a = fs[1]

        buckwalter.convertNumbers = True
        bn, a2, msg1, ok1 = buckwalter.b2a(b)
        an, b2, msg2, ok2 = buckwalter.a2b(a)
        buckwalter.convertNumbers = False
        bn, a2x, msg3, ok3 = buckwalter.b2a(b)
        an, b2x, msg4, ok4 = buckwalter.a2b(a)

        if a2 != an:
            print("FAIL b2a (1)\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(bn, a, a2), file=sys.stderr)
        elif b2 != bn:
            print("FAIL b2a (2)\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(an, b, b2), file=sys.stderr)
        elif a2x != an:
            print("FAIL b2a (3)\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(bn, a, a2x), file=sys.stderr)
        elif b2x != bn:
            print("FAIL b2a (4)\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(an, b, b2x), file=sys.stderr)
        elif not ok1:
            print("FAIL b2a (5) {}\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(msg1, bn, a, a2), file=sys.stderr)
        elif not ok2:
            print("FAIL b2a (6) {}\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(msg2, an, b, b2), file=sys.stderr)
        elif not ok3:
            print("FAIL b2a (7) {}\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(msg3, bn, a, a2x), file=sys.stderr)
        elif not ok4:
            print("FAIL b2a (8) {}\nfrom\t{}\nexpected\t{}\nfound\t{}\n".format(msg4, an, b, b2x), file=sys.stderr)
