
function initOld() {

    var BlueTryoutViewModel = function() {
        this.theParagraph = ko.observable(sentence);
    };

    var RedTryoutViewModel = function() {
        this.theText = ko.observable('the red text');
    };

    var mainViewModel = {
        blueTryout: new BlueTryoutViewModel(),
        redTryout: new RedTryoutViewModel()
    };

    ko.applyBindings(mainViewModel);
}

function init() {

    var SentenceViewModel = function(structure) {

        this.sentence = this.parseStructure(structure);
    };
    
    SentenceViewModel.prototype.parseStructure = function(struct) {

        
    };

    var struct = '竹[たけ] は 風[かぜ] で たわむ 。';
    ko.applyBindings(new SentenceViewModel(struct);
}

