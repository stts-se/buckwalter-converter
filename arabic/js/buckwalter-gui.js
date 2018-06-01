//var BWC = new BWC();

var BWG = {}

BWG.toUnicode = function(str) { 
  var hex = str.charCodeAt(0).toString(16).split('');
  while(hex.length < 4) hex.splice(0, 0, 0);
  return '\\u' + hex.join(''); 
}

BWG.ViewModel = function() {
    buckwalterEdit = ko.observable("");
    messages = ko.observableArray([])

    arabicView = ko.computed(function() {
	let bw = buckwalterEdit();
	if (bw.length > 0) {
	    let res = BWC.b2a(bw);
	    // messages.clear();
	    // self.messages = res.errors;
            return res.output;
	}
    }, this);

    
    arabicEdit = ko.observable("");
    buckwalterView = ko.computed(function() {
	let ar = arabicEdit();
	if (ar.length > 0) {
	    let res = BWC.a2b(ar);
	    // messages.clear();
	    // self.messages = res.errors;
            return res;
	}
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
    b2aObservableMap = ko.computed(function() {
	var thingy = [];
	for (let i = 0; i < BWC.chartable.length; i++) {
	    ch = BWC.chartable[i];
	    thingy.push( [ch.bw, ch.ar, BWG.toUnicode(ch.ar) ]);
	}
	return thingy;
    });
}

VM = new BWG.ViewModel();
mapTable = VM.mapTable;
b2aObservable = VM.b2aObservable;
ko.applyBindings(VM);

