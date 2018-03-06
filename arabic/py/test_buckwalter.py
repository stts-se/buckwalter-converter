import buckwalter
from sys import stderr

a2bTest = {
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
    "ة": "p",
    "\u064E": "a",
    "\u064f": "u",
    "\u0650": "i",
    "\u064B": "F",
    "\u064C": "N",
    "\u064D": "K",
    "\u0651": "~",
    "\u0652": "o",
    "\u0621": "'",
    "\u0623": ">",
    "\u0625": "<",
    "\u0624": "&",
    "\u0626": "}",    
    "\u0622": "|",
    "\u0671": "{",
    "\u0670": "`",
    "\u0649": "Y",
}

b2aTest = {
    "A": "ا",
    "b": "ب",
    "t": "ت",
    "v": "ث",
    "j": "ج",
    "H": "ح",
    "x": "خ",
    "d": "د",
    "*": "ذ",
    "r": "ر",
    "z": "ز",
    "s": "س",
    "$": "ش",
    "S": "ص",
    "D": "ض",
    "T": "ط",
    "Z": "ظ",
    "E": "ع",
    "g": "غ",
    "f": "ف",
    "q": "ق",
    "k": "ك",
    "l": "ل",
    "m": "م",
    "n": "ن",
    "h": "ه",
    "w": "و",
    "y": "ي",
    "p": "ة",
    "a": "\u064E",
    "u": "\u064f",
    "i": "\u0650",
    "F": "\u064B",
    "N": "\u064C",
    "K": "\u064D",
    "~": "\u0651",
    "o": "\u0652",
    "'": "\u0621",
    ">": "\u0623",
    "<": "\u0625",
    "&": "\u0624",
    "}": "\u0626",    
    "|": "\u0622",
    "{": "\u0671",
    "`": "\u0670",
    "Y": "\u0649",
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
    
