var BWC = {}

BWC.bw2araMap = {
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
    "p": "ة", //teh marbuta

    "a": '\u064E', // fatha
    "u": '\u064f', // damma
    "i": '\u0650', // kasra
    "F": '\u064B', // fathatayn
    "N": '\u064C', // dammatayn
    "K": '\u064D', // kasratayn
    "~": '\u0651', // shadda
    "o": '\u0652', // sukun

    "'": '\u0621', // lone hamza
    ">": '\u0623', // hamza on alif
    "<": '\u0625', // hamza below alif
    "&": '\u0624', // hamza on wa
    "}": '\u0626', // hamza on ya

    "|": '\u0622', // madda on alif
    "{": '\u0671', // alif al-wasla
    "`": '\u0670', // dagger alif
    "Y": '\u0649', // alif maqsura

    // punctuation
    ",": "\u060C",
    ";": "\u061B",
    "?": "\u061F",
}

BWC.commonChars = {
    " ": "",
    ".": "",
    ",": "",
    "(": "",
    ")": "",
}

BWC.makeAra2bwMap = function() {
    var map = {};
    for (var bw in BWC.bw2araMap) {
	ara = BWC.bw2araMap[bw]
	map[ara] = bw;
    };    
    return map;
}

BWC.ara2bwMap = BWC.makeAra2bwMap();

BWC.bw2ara = function(bw) {
    var aras = [];
    //console.log("bw2ara input", bw)
    syms = bw.trim().split("");
    for (var i = 0; i < syms.length; i++) {
	sym = syms[i];
	var ara = BWC.bw2araMap[sym];
	if (sym.length> 0 && ara === undefined || ara === null) {
	    if (BWC.commonChars[sym] !== null && BWC.commonChars[sym] !== undefined) {
		console.log("/" + sym + "/ is a common char");
		aras.push(sym);
	    } else {		
		console.log("No mapping for bw symbol /" + sym + "/");
		aras.push("?");
	    }
	}
	else {
	    aras.push(ara);
	}
    }
    return aras.join("");
};

BWC.ara2bw = function(ara) {
    var bws = [];
    //console.log("ara2bw input", ara)
    syms = ara.trim().split("");
    for (var i = 0; i < syms.length; i++) {
	sym = syms[i];
	var bw = BWC.ara2bwMap[sym];
	if (sym.length> 0 && bw === undefined || bw === null) {
	    if (BWC.commonChars[sym] !== null && BWC.commonChars[sym] !== undefined) {
		console.log("/" + sym + "/ is a common char");
		bws.push(sym);
	    } else {
		console.log("No mapping for ara symbol /" + sym + "/");
		bws.push("?")
	    }
	}
	else {
	    bws.push(bw);
	}
    }
    return bws.join("");
};
