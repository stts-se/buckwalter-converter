import re
import sys
import getopt

a2bMap = {
    "\u0627": "A",
    "\u0628": "b",
    "\u062A": "t",
    "\u062B": "v",
    "\u062C": "j",
    "\u062D": "H",
    "\u062E": "x",
    "\u062F": "d",
    "\u0630": "*",
    "\u0631": "r",
    "\u0632": "z",
    "\u0633": "s",
    "\u0634": "$",
    "\u0635": "S",
    "\u0636": "D",
    "\u0637": "T",
    "\u0638": "Z",
    "\u0639": "E",
    "\u063A": "g",
    "\u0641": "f",
    "\u0642": "q",
    "\u0643": "k",
    "\u0644": "l",
    "\u0645": "m",
    "\u0646": "n",
    "\u0647": "h",
    "\u0648": "w",
    "\u064A": "y",
    "\u0629": "p", #teh marbuta

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

b2aMap = {b: a for a, b in a2bMap.items()}

def printMapTable():
    import unicodedata
    print("{}\t{}\t{}\t{}".format("ARABIC", "UNICODE", "UNICODE NAME", "BUCKWALTER"))
    for a, b in a2bMap.items():
        ucode = 'U+%04x' % ord(a)
        udesc = unicodedata.name(a)
        print("{}\t{}\t{}\t{}".format(a, ucode, udesc, b))
    return

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

cmdname=sys.argv[0]

def help():
    print("* Convert Arabic<=>Buckwalter:", file=sys.stderr)
    print("  " + cmdname + " [-r] <input files>", file=sys.stderr)
    print("   -r for reverse conversion (optional)", file=sys.stderr)
    print("", file=sys.stderr)
    print("* Print map table:", file=sys.stderr)
    print("  " + cmdname + " -p", file=sys.stderr)
    return

def main(): 
    activeMap = a2bMap

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'rp')
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-p"):
            printMapTable()
            sys.exit()
        elif opt in ("-r"):
            activeMap = b2aMap
        
    if len(args) == 0:
        help()
        sys.exit(1)
            
    for fn in args:
        with open(fn) as f:
            for l in f.readlines():
                l = l.rstrip()
                conv = convert(l,activeMap)
                print(l + "\t" + conv)

    return

          
if __name__ == "__main__":
    main()
