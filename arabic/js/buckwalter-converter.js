let BWC = {}

class BWChar {
    constructor(ar, bw) { this.ar = ar; this.bw = bw; }
}

class BWMaptable {

    constructor(from, to, table) {
	this.from = from;
	this.to = to;
	this.table = table;
  }
    
    name() { return this.from + "2" + this.to; }
}


BWC.chartable = [
    new BWChar("ا", "A"), // bare alif
    new BWChar("ب", "b"),
    new BWChar("ت", "t"),
    new BWChar("ث", "v"),
    new BWChar("ج", "j"),
    new BWChar("ح", "H"),
    new BWChar("خ", "x"),
    new BWChar("د", "d"),
    new BWChar("ذ", "*"),
    new BWChar("ر", "r"),
    new BWChar("ز", "z"),
    new BWChar("س", "s"),
    new BWChar("ش", "$"),
    new BWChar("ص", "S"),
    new BWChar("ض", "D"),
    new BWChar("ط", "T"),
    new BWChar("ظ", "Z"),
    new BWChar("ع", "E"),
    new BWChar("غ", "g"),
    new BWChar("ف", "f"),
    new BWChar("ق", "q"),
    new BWChar("ك", "k"),
    new BWChar("ل", "l"),
    new BWChar("م", "m"),
    new BWChar("ن", "n"),
    new BWChar("ه", "h"),
    new BWChar("و", "w"),
    new BWChar("ي", "y"),
    new BWChar("ة", "p"), //teh marbuta

    new BWChar("\u064E", "a"), // fatha
    new BWChar("\u064f", "u"), // damma
    new BWChar("\u0650", "i"), // kasra
    new BWChar("\u064B", "F"), // fathatayn
    new BWChar("\u064C", "N"), // dammatayn
    new BWChar("\u064D", "K"), // kasratayn
    new BWChar("\u0651", "~"), // shadda
    new BWChar("\u0652", "o"), // sukun

    new BWChar("\u0621", "'"), // lone hamza
    new BWChar("\u0623", ">"), // hamza on alif
    new BWChar("\u0625", "<"), // hamza below alif
    new BWChar("\u0624", "&"), // hamza on wa
    new BWChar("\u0626", "}"), // hamza on ya

    new BWChar("\u0622", "|"), // madda on alif
    new BWChar("\u0671", "{"), // alif al-wasla
    new BWChar("\u0670", "`"), // dagger alif
    new BWChar("\u0649", "Y"), // alif maqsura

    // punctuation
    new BWChar("\u060C", ","),
    new BWChar("\u061B", ";"),
    new BWChar("\u061F", "?"),

];

BWC.normalise_bw = function(s) {
    return s.replace(/([aiuoFKN])(~)/g, "$2¡1", s);
}

BWC.normalise_ar = function(s) {
    return s.normalize('NFC');
}

BWC.normalise = function(outputName, orth) {
    if (outputName === "bw")
        return BWC.normalise_bw(orth);
    else
        return BWC.normalise_ar(orth);        

}

BWC.commonChars = {
    " ": "",
    ".": "",
    ",": "",
    "(": "",
    ")": "",
}

BWC.alwaysAcceptASCII = true;

BWC.isCommonChar = function(sym) {
    // ALL ASCII CHARS? CHAR NUM <128; WITH THIS, REVERSE TEST WON'T WORK
    if (BWC.commonChars[sym] !== null && BWC.commonChars[sym] !== undefined)
	return true;
    num = sym.charCodeAt(0);
    if (num < 128) {
	return true;
    }
    return false;
}

BWC.makeA2BMap = function() {
    let map = {};
    for (let i = 0; i < BWC.chartable.length; i++) {
	ch = BWC.chartable[i];
	map[ch.ar] = ch.bw;
    };    
    return new BWMaptable("ar", "bw", map);
}

BWC.makeB2AMap = function() {
    let map = {};
    for (let i = 0; i < BWC.chartable.length; i++) {
	let ch = BWC.chartable[i];
	map[ch.bw] = ch.ar;
    };    
    return new BWMaptable("bw", "ar", map);
}

BWC.a2bMap = BWC.makeA2BMap();
BWC.b2aMap = BWC.makeB2AMap();

class BWResult {
    constructor(output, errors, ok) { this.output = output; this.errors = errors; this.ok = ok; }    
}

BWC.reverseTest = function(mapTo, input, result) {
    let remaptable = {};
    if (mapTo === BWC.a2bMap.to)
        remaptable = BWC.a2bMap;
    else if (mapTo === BWC.b2aMap.to)
        remaptable = BWC.b2aMap;
    else
	return "Couldn't find maptable for " + mapTo;

    let rev = BWC.convert(remaptable, result, false);
    if (rev.output !== input) {
        let err = "Reverse test failed: input " + input + " != reverse " + rev.output;
	return err;
    }
    else
	return null;
}

BWC.convert = function(maptable, input, doReverseTest) {
    //console.log("convert called with '" + input + "'");
    let res = [];
    let errs = [];    
    for (let i = 0; i < input.length; i++) {
	let sym = input[i];
	let ar = maptable.table[sym];
	if (sym.length> 0 && ar === undefined || ar === null) {
	    if (BWC.isCommonChar(sym)) {
		//console.log("/" + sym + "/ is a common char");
		res.push(sym);
	    } else {
		res.push("?");
		let msg = "No mapping for " + maptable.from + " symbol '" + sym + "'";
		errs.push(msg);
	    }
	}
	else {
	    res.push(ar);
	}
    }

    let ok = (errs.length > 0); 
    let mapped = res.join("");
    mapped = BWC.normalise(maptable.to, mapped)
    
    if (errs.length == 0 && doReverseTest) {
	let err = BWC.reverseTest(maptable.from, input, mapped)
	if (err !== null) {
	    errs.push(err)
	}
    }
    let r = new BWResult(mapped, errs, ok);
    return r;
}

BWC.b2a = function(s) {
    return BWC.convert(BWC.b2aMap, s, true);
};

BWC.a2b = function(s) {
    return BWC.convert(BWC.a2bMap, s, true);
};
