import re
import sys
import getopt

a2bMap = {
    "ا": "A",
    "ب": "b",
    "ت": "t",
    "ث": "v",
    "ج": "j",
    "ح": "H",
    "خ": "x",
    "د": "d",
    "ذ": "*",
    "ر": "r",
    "ز": "z",
    "س": "s",
    "ش": "$",
    "ص": "S",
    "ض": "D",
    "ط": "T",
    "ظ": "Z",
    "ع": "E",
    "غ": "g",
    "ف": "f",
    "ق": "q",
    "ك": "k",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ه": "h",
    "و": "w",
    "ي": "y",
    "ة": "p", #teh marbuta

    "\u064E": "a", # fatha
    "\u064f": "u", # damma
    "\u0650": "i", # kasra
    "\u064B": "F", # fathatayn
    "\u064C": "N", # dammatayn
    "\u064D": "K", # kasratayn
    "\u0651": "~", # shadda
    "\u0652": "o", # sukun

    "\u0621": "'", # lone hamza
    "\u0623": ">", # hamza on alif
    "\u0625": "<", # hamza below alif
    "\u0624": "&", # hamza on wa
    "\u0626": "}", # hamza on ya
    
    "\u0622": "|", # madda on alif
    "\u0671": "{", # alif al-wasla
    "\u0670": "`", # dagger alif
    "\u0649": "Y", # alif maqsura
}

b2aMap = {v: k for k, v in a2bMap.items()}

def test(inputString, outputString, mapTable):
    testTable = None
    if mapTable == a2bMap:
        testTable = b2aMap
    elif mapTable == b2aMap:
        testTable = a2bMap
    else:
        raise ValueError('unknown activeMap (neither a2bMap nor b2aMap)!')
        sys.exit(2)

    reverseString = convert(outputString, testTable)
    if reverseString != inputString:
        print("conversion test failed! {} {}".format(inputString, outputString), file=stderr)
        return FALSE
    else:
        return TRUE    
    return FALSE

def convert(string, mapTable):
    res = ""
    for c in string:
        c2 = mapTable.get(c,c)
        res = res + c2
    return res

def a2b(string):
    return convert(string,a2bMap)

def b2a(string):
    return convert(string,b2aMap)

def help():
    print (cmdname + " [--reverse] <inputfiles>", file=sys.stderr)
    return

activeMap = a2bMap

cmdname=sys.argv[0]

try:
    opts, args = getopt.getopt(sys.argv[1:], 'r')
except getopt.GetoptError as err:
    print(err, file=sys.stderr)
    help()
    sys.exit(2)
    
for opt, arg in opts:
    if opt == '-h':
        help()
        sys.exit()
    elif opt in ("-r"):
        activeMap = b2aMap
        
if cmdname == "buckwalter.py" and len(args) == 0:
    help()
    sys.exit(1)
    
        
for fn in args:
    with open(fn) as f:
        for l in f.readlines():
            l = l.rstrip()
            conv = convert(l,activeMap)
            print(l + "\t" + conv)

          
