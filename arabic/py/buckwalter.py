import re
import sys
import getopt
import unicodedata

cmdname=sys.argv[0]
convertNumbers = False
force = False

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

def reverseTest(inputString, outputString, mapTable):
    testTable = None
    if mapTable == a2bMap:
        testTable = b2aMap
    elif mapTable == b2aMap:
        testTable = a2bMap
    else:
        raise ValueError('unknown activeMap (neither a2bMap nor b2aMap)!')

    norm, reverseString, msg, ok = convert(outputString,testTable,False)
    if reverseString != inputString:
        err = "Reversed: {}".format(reverseString)
        return err, False
    else:
        return "", True

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

def normalise_bw(buckwalter):
    norm = buckwalter
    norm = norm.replace("a~","~a")
    norm = norm.replace("i~","~i")
    norm = norm.replace("u~","~u")
    return norm

def normalise_ar(arabic):
    norm = arabic
    norm = norm.replace("\u064E\u0651","\u0651\u064E")
    norm = norm.replace("\u0650\u0651","\u0651\u0650")
    norm = norm.replace("\u064f\u0651","\u0651\u064f")    
    return norm

def normalise(orth): # TODO: UGLY!!
    return normalise_bw(normalise_ar(orth))

def convert(string, mapTable, doReverseTest=True):
    norm = normalise(string)
    res = ""
    msg = ""
    ok = True
    for ch in string:
        if ch in arabicIndicDigits and not(convertNumbers):
            res = res + ch
        else:
            ch2 = mapTable.get(ch,"")
            if ch2 == "":
                res = res + ch                        
                if not is_common_char(ch):
                    ok = False
                    msg = "Unknown char: %s" % ch
            else:
                res = res + ch2

    if ok and doReverseTest:
        msg, ok = reverseTest(norm, res, mapTable)
    return norm, res, msg, ok

def a2b(string):
    return convert(string,a2bMap)

def b2a(string):
    return convert(string,b2aMap)


def help():
    print("* Convert Arabic<=>Buckwalter:", file=sys.stderr)
    print("  " + cmdname + " [option] <input files>", file=sys.stderr)
    print("   -r for reverse conversion (optional, default: false)", file=sys.stderr)
    print("   -n convert arabic-indic numbers to arabic (optional, default: false)", file=sys.stderr)
    print("   -f force, to fail on error (optional, default: false)", file=sys.stderr)
    print("", file=sys.stderr)
    print("* Print map table:", file=sys.stderr)
    print("  " + cmdname + " -p", file=sys.stderr)
    return


def main():        
    
    activeMap = a2bMap

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'rpnf')
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
        elif opt in ("-n"):
            convertNumbers = True
        elif opt in ("-f"):
            force = True
        
    if len(args) == 0:
        help()
        sys.exit(1)
            
    for fn in args:
        with open(fn, encoding="utf-8") as f:
            for l in f.readlines():
                l = l.rstrip()
                norm, conv, msg, ok = convert(l, activeMap)
                if ok:
                    print(l + "\t" + conv)
                elif force:
                    print(l + "\t" + conv)
                else:
                    print("CONVERSION FAILED\t" + msg + "\t" + l + "\t" + conv, file=sys.stderr)
    return

          
if __name__ == "__main__":
    main()
