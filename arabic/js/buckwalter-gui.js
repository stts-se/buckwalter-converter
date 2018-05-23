//var BWC = new BWC();

var BWG = {}

BWG.ViewModel = function() {
    buckwalterEdit = ko.observable("");
    arabicView = ko.computed(function() {
        return BWC.bw2ara(buckwalterEdit());
    }, this);

    arabicEdit = ko.observable("");
    buckwalterView = ko.computed(function() {
        return BWC.ara2bw(arabicEdit());
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
	for (var k in BWC.bw2araMap) {
	    thingy.push( [k,BWC.bw2araMap[k] ]);
	}
	return thingy;
    });
}

VM = new BWG.ViewModel();
mapTable = VM.mapTable;
bw2araObservable = VM.bw2araObservable;
ko.applyBindings(VM);

