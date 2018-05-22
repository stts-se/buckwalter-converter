import re
import sys
import getopt
import unicodedata

cmdname = "buckwalter"
do_debug = False

class Config:
    convertNumbers = True  # Convert Arabic-Indian numerals
    reverse = False        # reverse = Buckwalter to Arabic conversion
    quiet = False          # quiet = no errors or warnings are printed
    column = -1
    
    def to_string(self):
        return "config: {convertNumbers=%s, reverse=%s, quiet=%s, column=%d}" % (self.convertNumbers, self.reverse, self.quiet, self.column)

    def type(self):
        if self.reverse:
            return "b2a"
        else:
            return "a2b"

    def copy_with_reverse(self, reverse):
        cp = self.copy()
        cp.reverse = reverse
        cp.column = column
        return cp
        
    def copy(self):
        cp = Config()
        cp.convertNumbers = self.convertNumbers
        cp.reverse = self.reverse
        cp.quiet = self.quiet
        cp.column = self.column
        return cp

    def __init__(self, convertNumbers = False, reverse = False, quiet = False, column = -1):
        self.convertNumbers = convertNumbers
        self.reverse = reverse
        self.quiet = quiet
        self.column = column

    
class Result:
    input = ""       # Input string
    input_norm = ""  # Normalised input string
    result = ""      # Converted string
    msgs = []        # Error messages, if any
    ok = True        # Conversion success True/False

    def __str__(self):
        return self.result

    def json(self):
        return {
            'input': self.input,
            'input_norm': self.input_norm,
            'result': self.result,
            'msgs': self.msgs,
            'ok': self.ok
        }

    
    
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

    # punctuation
    "\u060C": ",",
    "\u061B": ";",
    "\u061F": "?",
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
    print("%s\t%s\t%s\t%s" % ("ARABIC", "UNICODE", "UNICODE NAME", "BUCKWALTER"))
    for a, b in a2bMap.items():
        ucode = 'U+%04x' % ord(a)
        uname = unicodedata.name(a)
        print("%s\t%s\t%s\t%s" % (a, ucode, uname, b))
    return

def reverseTest(testRes, cfg):
    cfgRev = cfg.copy()
    if cfgRev.reverse:
        cfgRev.reverse = False
    else:
        cfgRev.reverse = True
    rev = convert(testRes.result, cfgRev, isInnerCall = True)
    if rev.result != testRes.input_norm:
        err = "Reverse test failed!\tReverse %s != Norm %s (Original input %s)" % (rev.result, testRes.input_norm, testRes.input)
        return err, False
    else:
        return "", True

def unicode_list(string):
    res = ""
    for ch in string:
        try:
            uc = ('U+%04x' % ord(ch))
        except getopt.GetoptError as err:
            print("error for char '%s' : %s" % (ch, err), file=sys.stderr)
            help()
            sys.exit(2)

        res = res + " " + uc
    return res.rstrip()


def is_common_char(char, cfg):
    unum = ord(char)
    if unum < 128: # ASCII
        return True
    elif char == "\u060c": # ARABIC COMMA
        return True
    else:
        return False
    return

def normalise_bw_input(string):
    norm = string
    norm = norm.replace("a~","~a")
    norm = norm.replace("i~","~i")
    norm = norm.replace("u~","~u")
    debug("bw norm: %s => %s" % (string, norm))
    return norm

def normalise_ar_input(string):
    # norm = unicodedata.normalize('NFC', string)
    norm = string
    norm = norm.replace("\u064E\u0651","\u0651\u064E")
    norm = norm.replace("\u0650\u0651","\u0651\u0650")
    norm = norm.replace("\u064f\u0651","\u0651\u064f")    
    debug("ar norm input:\t%s\t%s"% (string, unicode_list(string)))
    debug("ar norm output\t%s\t%s" % (norm, unicode_list(norm)))
    return norm

# TODO: reverse direction of diacritics (both ar+bw) to match unicodedata.normalize?
#       if so, test files need updating as well
#       example call: unicodedata.normalize('NFC', string)
def normalise_input(orth, cfg):
    if cfg.reverse:
        return normalise_bw_input(orth)
    else:
        return normalise_ar_input(orth)        

def mapTable(cfg):
    # debug(cfg.type())
    # debug(cfg.reverse)
    if cfg.reverse:
        return b2aMap
    else:
        return a2bMap
    
def convert(string, cfg, isInnerCall=False):
    debug(cfg.type())
    if not isInnerCall:
        debug("convert: config type = %s" % (cfg.type()))
    result = Result()
    result.input_norm = normalise_input(string, cfg)
    acc = ""
    ok = True
    for ch in result.input_norm:
        if ch in arabicIndicDigits and not(cfg.convertNumbers):
            acc = acc + ch
        else:
            debug("CFG TYPE: " + cfg.type())
            #debug("MAPTABLE %s" % (mapTable(cfg)))
            ch2 = mapTable(cfg).get(ch,"")
            if ch2 == "":
                acc = acc + ch                        
                if not is_common_char(ch, cfg):
                    result.ok = False
                    ucode = 'U+%04x' % ord(ch)
                    msg = "Unknown input symbol: %s (%s)" % (ch, ucode)
                    if not msg in result.msgs:
                        result.msgs.append(msg)
            else:
                acc = acc + ch2

    result.result = acc
    if ok and isInnerCall:
        msg, ok = reverseTest(result, cfg)
    return result

def a2b(string, cfg = Config()):
    thisCfg = cfg.copy()
    thisCfg.reverse = False
    #debug("a2b: config type = " + cfg.type())
    res = convert(string, thisCfg)
    return res
    
def b2a(string, cfg = Config()):
    thisCfg = cfg.copy()
    thisCfg.reverse = True
    #debug("b2a: config type = " + cfg.type())
    res = convert(string, thisCfg)
    return res


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
    print("   -r for reverse conversion (optional, default: false)", file=sys.stderr)
    print("   -n convert arabic-indic numbers to arabic (optional, default: false)", file=sys.stderr)
    print("   -f force, do not halt on error (optional, default: false)", file=sys.stderr)
    print("   -q quiet, no error messages (optional, default: false)", file=sys.stderr)
    print("", file=sys.stderr)
    print("* Print map table:", file=sys.stderr)
    print("  " + cmdname + " -p", file=sys.stderr)
    return


def main():        

    force = False
    config = Config()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'rpnfqhc:')
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
            config.reverse = True
        elif opt in ("-n"):
            config.convertNumbers = True
        elif opt in ("-f"):
            force = True
        elif opt in ("-q"):
            config.quiet = True
        elif opt in ("-c"):
            config.column = int(arg)
        
    if len(args) == 0:
        help()
        sys.exit(1)

    if not config.quiet:
        print("[%s] %s" % (cmdname, config.to_string()))
        
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
                if config.column  < 0: # column not set - use whole line
                    input_s = l
                else:
                    fs = l.split("\t")
                    if len(fs) > config.column:
                        input_s = fs[config.column]

                if input_s == "":
                    print(l)
                    continue
                        
                res = convert(input_s, config)
                if res.ok:
                    print(l + "\t" + res.result)
                else:
                    if not config.quiet:
                        print("CONVERSION FAILED\tMessage: " + "; ".join(res.msgs) + "\tInput: " + l + "\tResult: " + res.result, file=sys.stderr)
                    if not force:
                        sys.exit(1)
                        # print(l + "\t" + res.result)
    return

          
if __name__ == "__main__":
    main()
