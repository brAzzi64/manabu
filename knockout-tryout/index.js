
function init() {

    var BlueTryoutViewModel = function() {
        this.theParagraph = ko.observable('the blue text');
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

