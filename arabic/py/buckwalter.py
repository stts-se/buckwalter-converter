import re
import sys
import getopt
import unicodedata

cmdname=sys.argv[0]

# http://www.qamus.org/transliteration.htm
#  To make it XML-friendly I would:
#  * replace < with I (for hamza-under-alif)
#  * replace > with O (for hamza-over-alif—the A is already used for bare alif)
#  * replace & with W (for hamza-on-waw)

# https://en.wikipedia.org/wiki/Buckwalter_transliteration

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

    # http://www.qamus.org/transliteration.htm
    "\u067e": "P", # peh
    "\u0686": "J", # tcheh
    "\u06a4": "V", # veh
    "\u06af": "G", # gaf
    "\u0640": "_", # tatweel

    # Arabic-indic digits
    "\u0660": "0",
    "\u0661": "1", 
    "\u0662": "2",
    "\u0663": "3",
    "\u0664": "4",
    "\u0665": "5",
    "\u0666": "6",
    "\u0667": "7",
    "\u0668": "8",
    "\u0669": "9",
}

arabicIndicDigits = [
    "\u0660",
    "\u0661",
    "\u0662",
    "\u0663",
    "\u0664",
    "\u0665",
    "\u0666",
    "\u0667",
    "\u0668",
    "\u0669",
]

b2aMap = {b: a for a, b in a2bMap.items()}

def printMapTable():
    print("{}\t{}\t{}\t{}".format("ARABIC", "UNICODE", "UNICODE NAME", "BUCKWALTER"))
    for a, b in a2bMap.items():
        ucode = 'U+%04x' % ord(a)
        uname = unicodedata.name(a)
        print("{}\t{}\t{}\t{}".format(a, ucode, uname, b))
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
        return False
    else:
        return True   
    return False

def is_common_char(char):
    unum = ord(char)
    if unum < 128: # ASCII
        return True
    elif char == "\u060c": # ARABIC COMMA
        return True
    else:
        ucode = 'U+%04x' % ord(char)
        udesc = unicodedata.name(char)
        print("[{}] WARNING - CANNOT CONVERT\t{}\t{}\t{}".format(cmdname, char, udesc, ucode), file=sys.stderr)
        return False
    return

# convert returns (1) the converted string, and (2) a boolean status (True if the conversion is ok, False if there was an error)
def convert(string, mapTable, convertNumbers):
    res = ""
    ok = True
    for ch in string:
        if ch in arabicIndicDigits and not(convertNumbers):
            res = res + ch
        else:
            ch2 = mapTable.get(ch,"")
            if ch2 == "":
                if is_common_char(ch):
                    res = res + ch
                else:
                    res = res + "<UNKNOWN_CHAR:%s>" % ch
                    ok = False
            else:
                res = res + ch2
    return res, ok

def a2b(string, convertNumbers):
    return convert(string,a2bMap,convertNumbers)

def b2a(string, convertNumbers):
    return convert(string,b2aMap,convertNumbers)


def help():
    print("* Convert Arabic<=>Buckwalter:", file=sys.stderr)
    print("  " + cmdname + " [-r] <input files>", file=sys.stderr)
    print("   -r for reverse conversion (optional, default: false)", file=sys.stderr)
    print("   -n convert arabic-indic numbers to arabic (optional, default: false)", file=sys.stderr)
    print("", file=sys.stderr)
    print("* Print map table:", file=sys.stderr)
    print("  " + cmdname + " -p", file=sys.stderr)
    return

def main(): 
    activeMap = a2bMap
    convertNumbers = False
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'rpn')
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
        elif opt in ("-nx"):
            convertNumbers = True
        
    if len(args) == 0:
        help()
        sys.exit(1)
            
    for fn in args:
        with open(fn) as f:
            for l in f.readlines():
                l = l.rstrip()
                conv, ok = convert(l,activeMap,convertNumbers)
                if ok:
                    print("OK\t" + l + "\t" + conv)
                else:
                    print("FAIL\t" + l + "\t" + conv)
    return

          
if __name__ == "__main__":
    main()
