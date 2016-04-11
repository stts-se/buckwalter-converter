var bw2araMap = {
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

    " ": " ",
    ".": "."
};

function makeAra2bwMap() {
    var map = {};
    _.each(bw2araMap, function(v, k) {
	map[v] = k;
    });    
    return map;
}
var ara2bwMap = makeAra2bwMap();

function ViewModel() {
    buckwalterEdit = ko.observable("");
    arabicView = ko.computed(function() {
        return bw2ara(buckwalterEdit());
    }, this);

    arabicEdit = ko.observable("");
    buckwalterView = ko.computed(function() {
        return ara2bw(arabicEdit());
    }, this);

    // EDITING STATES
    bwEditing = ko.observable(true);
    setBwEditing = function() { 
	buckwalterEdit(buckwalterView());
	bwEditing(true); 
    }
    setAraEditing = function() { 
	arabicEdit(arabicView());
	bwEditing(false); 
    }

    // SHOW MAPTABLE
    showMapTable = ko.observable(false);
    bw2araObservableMap = ko.computed(function() {
	var thingy = [];
	for (var k in bw2araMap) {
	    thingy.push( [k,bw2araMap[k] ]);
	}
	return thingy;
    });
}

VM = new ViewModel();
mapTable = VM.mapTable;
bw2araObservable = VM.bw2araObservable;
ko.applyBindings(VM);

function bw2ara(bw) {
    var aras = _.map(bw.trim().split(""), function(sym) {
	var ara = bw2araMap[sym];
	if (sym.length> 0 && ara === undefined || ara === null) {
	    console.log("No mapping for bw symbol /" + sym + "/");
	    return "?";
	}
	else {
	    return ara;
	}
    });
    var res = aras.join("")
    return res;
}

function ara2bw(ara) {
    var bws = _.map(ara.trim().split(""), function(sym) {
	var bw = ara2bwMap[sym];
	if (sym.length> 0 && bw === undefined || bw === null) {
	    console.log("No mapping for ara symbol /" + sym + "/");
	    return "?";
	}
	else {
	    return bw;
	}
    });
    var res = bws.join("")
    return res;
}
