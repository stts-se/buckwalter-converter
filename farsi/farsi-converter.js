var far2latMap = {

    // CONSONANTS
    "\u0627": "’", // TODO: not in the beginning of words"
    "\u0628": "b",
    "\u067E": "p",
    "\u062A": "t",
    "\u062B": "ṯ",
    "\u062C": "j",
    "\u0686": "č",
    "\u062D": "ḥ",
    "\u062E": "ḵ",
    "\u062F": "d",
    "\u0630": "ḏ",
    "\u0631": "r",
    "\u0632": "z",
    "\u0698": "ž",
    "\u0633": "s",
    "\u0634": "š",
    "\u0635": "ṣ",
    "\u0636": "ż",
    "\u0637": "ṭ",
    "\u0638": "ẓ",
    "\u0639": "‘",
    "\u063A": "ḡ",
    "\u0641": "f",
    "\u0642": "ḳ",
    "\u06A9": "k",
    "\u06AF": "g",
    "\u0644": "l",
    "\u0645": "m",
    "\u0646": "n",
    "\u0648": "v",
    "\u0647": "h",
    "\u0629": "h",
    "\u06CC": "y",
    "\u0621": "’",
    "\u0624": "’",
    "\u0626": "’",

    // VOWELS

    "\u064E": "a",
    "\u064F": "u",
    "\u0648\u064F": "u",
    "\u0650": "e",
    "\u064E\u0627": "ā",
    "\u0622": "ā",
    "\u064E\u06CC": "ā",
    "\u06CC\u0670": "ā",
    "\u064F\u0648": "u",
    "\u0650\u06CC": "i",
    "\u064E\u0648": "ow",
    "\u064E\u06CC": "ey",
    "\u064E\u06CC": "–e",
    "\u06C0": "–ye",

    };

var commonChars = {
    " ": "",
    ".": "",
    ",": "",
    "(": "",
    ")": "",
}

function makeLat2FarMap() {
    var map = {};
    _.each(far2latMap, function(lat, far) {
	map[lat] = far;
    });
    return map;
}
var lat2farMap = makeLat2FarMap();

function ViewModel() {
    latinEdit = ko.observable("");
    farsiView = ko.computed(function() {
        return lat2far(latinEdit());
    }, this);

    farsiEdit = ko.observable("");
    latinView = ko.computed(function() {
        return far2lat(farsiEdit());
    }, this);

    // EDITING STATES
    latEditing = ko.observable(true);
    setLatEditing = function() { 
	latinEdit(latinView());
	latEditing(true); 
    }
    setFarEditing = function() { 
	farsiEdit(farsiView());
	latEditing(false); 
    }

    // SHOW MAPTABLE
    showMapTable = ko.observable(false);
    far2latObservableMap = ko.computed(function() {
	var thingy = [];
	for (var k in far2latMap) {
	    thingy.push( [k,far2latMap[k] ]);
	}
	return thingy;
    });
}

VM = new ViewModel();
mapTable = VM.mapTable;
far2latObservable = VM.far2latObservable;
ko.applyBindings(VM);

function far2lat(lat) {
    var fars = _.map(lat.trim().split(""), function(sym) {
	var far = far2latMap[sym];
	if (sym.length> 0 && far === undefined || far === null) {
	    if (commonChars[sym] !== null && commonChars[sym] !== undefined) {
		console.log("/" + sym + "/ is a common char");
		return sym;		
	    } else {
		console.log("No mapping for lat symbol /" + sym + "/");
		return "?";
	    }
	}
	else {
	    return far;
	}
    });
    var res = fars.join("")
    return res;
}

function lat2far(far) {
    var lats = _.map(far.trim().split(""), function(sym) {
	var lat = lat2farMap[sym];
	if (sym.length> 0 && lat === undefined || lat === null) {
	    if (commonChars[sym] !== null && commonChars[sym] !== undefined) {
		console.log("/" + sym + "/ is a common char");
		return sym;
	    } else {
		console.log("No mapping for far symbol /" + sym + "/");
		return "?";
	    }
	}
	else {
	    return lat;
	}
    });
    var res = lats.join("")
    return res;
}
