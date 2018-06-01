import re
import sys
import getopt
import unicodedata

cmdname = "buckwalter"
do_debug = False
force = False
quiet = False
 
class Result:
    input = ""       # Input string
    result = ""      # Converted string
    msgs = []        # Error messages, if any
    ok = True        # Conversion success True/False

    def __str__(self):
        return self.result

    # def json(self):
    #     return {
    #         'input': self.input,
    #         'result': self.result,
    #         'msgs': self.msgs,
    #         'ok': self.ok
    #     }


class char:
    ar = ""
    bw = ""

    def __init__(self, ar, bw):
        self.ar = ar
        self.bw = bw
    
    def desc(self):
        ucode = 'U+%04x' % ord(a)
        uname = unicodedata.name(a)
        return "%s %s" % (ucode, uname)

class maptable:
    fr = ""
    to = ""
    table = {}

    def __init__(self, fr, to, table):
        self.fr = fr
        self.to = to
        self.table = table

    def name(self):
        return "%s2%s" % (self.fr, self.to)
    
# http://www.qamus.org/transliteration.htm
#  To make it XML-friendly I would:
#  * replace < with I (for hamza-under-alif)
#  * replace > with O (for hamza-over-alif—the A is already used for bare alif)
#  * replace & with W (for hamza-on-waw)

# https://en.wikipedia.org/wiki/Buckwalter_transliteration

chartable = [
    char("\u0627", "A"), # bare alif
    char("\u0628", "b"),
    char("\u062A", "t"),
    char("\u062B", "v"),
    char("\u062C", "j"),
    char("\u062D", "H"),
    char("\u062E", "x"),
    char("\u062F", "d"),
    char("\u0630", "*"),
    char("\u0631", "r"),
    char("\u0632", "z"),
    char("\u0633", "s"),
    char("\u0634", "$"),
    char("\u0635", "S"),
    char("\u0636", "D"),
    char("\u0637", "T"),
    char("\u0638", "Z"),
    char("\u0639", "E"),
    char("\u063A", "g"),
    char("\u0641", "f"),
    char("\u0642", "q"),
    char("\u0643", "k"),
    char("\u0644", "l"),
    char("\u0645", "m"),
    char("\u0646", "n"),
    char("\u0647", "h"),
    char("\u0648", "w"),
    char("\u064A", "y"),
    char("\u0629", "p"), #teh marbuta

    char("\u064E", "a"), # fatha
    char("\u064f", "u"), # damma
    char("\u0650", "i"), # kasra
    char("\u064B", "F"), # fathatayn
    char("\u064C", "N"), # dammatayn
    char("\u064D", "K"), # kasratayn
    char("\u0651", "~"), # shadda
    char("\u0652", "o"), # sukun

    char("\u0621", "'"), # lone hamza
    char("\u0623", ">"), # hamza on alif
    char("\u0625", "<"), # hamza below alif
    char("\u0624", "&"), # hamza on wa
    char("\u0626", "}"), # hamza on ya
    
    char("\u0622", "|"), # madda on alif
    char("\u0671", "{"), # alif al-wasla
    char("\u0670", "`"), # dagger alif
    char("\u0649", "Y"), # alif maqsura

    # # http://www.qamus.org/transliteration.htm
    # char("\u067e", "P"), # peh
    # char("\u0686", "J"), # tcheh
    # char("\u06a4", "V"), # veh
    # char("\u06af", "G"), # gaf
    # char("\u0640", "_"), # tatweel

    # # Arabic-indic digits
    char("\u0660", "0"),
    char("\u0661", "1"), 
    char("\u0662", "2"),
    char("\u0663", "3"),
    char("\u0664", "4"),
    char("\u0665", "5"),
    char("\u0666", "6"),
    char("\u0667", "7"),
    char("\u0668", "8"),
    char("\u0669", "9"),

    # # punctuation
    char("\u060C", ","),
    char("\u061B", ";"),
    char("\u061F", "?"),
]

a2bMap = maptable("a", "b", {ch.ar: ch.bw for ch in chartable})
b2aMap = maptable("b", "a", {ch.bw: ch.ar for ch in chartable})

def printMapTable():
    print("%s\t%s\t%s" % ("BW", "ARABIC", "DESCRIPTION"))
    for a, b in a2bMap.table.items():
        ucode = 'U+%04x' % ord(a)
        uname = unicodedata.name(a)
        print("%s\t%s\t%s %s" % (b, a, ucode, uname))
    return

def reverseTest(mapTo, testRes):
    remaptable = {}
    if mapTo == a2bMap.to:
        remaptable = a2bMap
    elif mapTo == b2aMap.to:
        remaptable = b2aMap
        
    rev = convert(remaptable, testRes.result, False)
    if rev.result != testRes.input:
        err = "Reverse test failed!\tReverse %s != Input %s" % (rev.result, testRes.input)
        return err, False
    else:
        return "", True

def convert(maptable, string, doReverseTest=True):
    result = Result()
    result.input = string
    acc = ""
    ok = True
    for ch in result.input:
        ch2 = maptable.table.get(ch,"")
        if ch2 == "":
            acc = acc + ch                        
            if not is_common_char(ch):
                ok = False
                ucode = 'U+%04x' % ord(ch)
                msg = "Unknown input symbol: %s (%s)" % (ch, ucode)
                if not msg in result.msgs:
                    result.msgs.append(msg)
        else:
            acc = acc + ch2

    result.result = normalise(maptable.to, acc)
    if ok and doReverseTest:
        msg, ok = reverseTest(maptable.fr, result)
        if not msg in result.msgs:
            result.msgs.append(msg)
    result.ok = ok
    return result


commonChars = {
    ' ': True,
    '.': True,
    ',': True,
    '(': True,
    ')': True,
}

def is_common_char(char):
    return char in commonChars
    # unum = ord(char)
    # if unum < 128: # ASCII
    #     return True
    # elif char == "\u060c": # ARABIC COMMA
    #     return True
    # else:
    #     return False

def normalise_bw(string):
    return re.sub(r'([aiuoFKN])(~)', "\\2\\1", string)

def normalise_ar(string):
    return unicodedata.normalize('NFC', string)

def normalise(outputName, orth):
    if outputName == "b":
        return normalise_bw(orth)
    else:
        return normalise_ar(orth)        

def a2b(string):
    return convert(a2bMap, string)
    
def b2a(string):
    return convert(b2aMap, string)


def debug(string):
    if do_debug:
        if string == "":
            print("", file=sys.stderr)
        else:
            print("[%s] %s" % (cmdname, string), file=sys.stderr)


def help():
    print("* Convert Arabic<=>Buckwalter:", file=sys.stderr)
    print("  " + cmdname + " [option] <input files>", file=sys.stderr)
    print("   -c convert specified column (optional, default: convert each full line)", file=sys.stderr)
    print("   -i input mode a/b (default: a)", file=sys.stderr)
    print("   -f force, do not halt on error (optional, default: false)", file=sys.stderr)
    print("   -q quiet, no error messages (optional, default: false)", file=sys.stderr)
    print("", file=sys.stderr)
    print("* Print map table:", file=sys.stderr)
    print("  " + cmdname + " -p", file=sys.stderr)
    return


def main():        

    global force
    global quiet
    
    column = -1
    maptable = a2bMap
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'rpfqhc:')
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
        elif opt in ("-i"):
            if arg == a:
                maptable = a2bMap
            elif arg == b:
                maptable == b2aMap
            else:
                print("invalid input mode %s" % arg, file=sys.stderr)
                help()
                sys.exit(1)
        elif opt in ("-f"):
            force = True
        elif opt in ("-q"):
            quiet = True
        elif opt in ("-c"):
            column = int(arg)
        
    if len(args) == 0:
        help()
        sys.exit(1)

    for fn in args:
        with open(fn, encoding="utf-8") as f:
            for l in f.readlines():
                l = l.rstrip()
                if l.strip() == "":
                    print("")
                    continue
                if l.strip().startswith("#"):
                    print("SKIPPING:\t" + l, file=sys.stderr)
                    continue
                input_s = ""
                if column  < 0: # column not set - use whole line
                    input_s = l
                else:
                    fs = l.split("\t")
                    if len(fs) > column:
                        input_s = fs[column]

                if input_s == "":
                    print(l)
                    continue
                        
                res = convert(maptable, input_s)
                if res.ok:
                    print(l + "\t" + res.result)
                else:
                    if not quiet:
                        print("CONVERSION FAILED\tMessage: " + "; ".join(res.msgs) + "\tInput: " + l + "\tResult: " + res.result, file=sys.stderr)
                    if not force:
                        sys.exit(1)
                        # print(l + "\t" + res.result)
    return

          
if __name__ == "__main__":
    main()
