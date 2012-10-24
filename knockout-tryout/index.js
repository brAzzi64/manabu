
function init() {

    var BlueTryoutViewModel = function() {
        this.theParagraph = ko.observable(0);
    };

    var RedTryoutViewModel = function() {
        this.theText = ko.observable(0);
    };

    var vm = new BlueTryoutViewModel();
    ko.applyBindings(vm, $('#blue-tryout')[0]);
    vm.theParagraph('the text');

    var vm = new RedTryoutViewModel();
    ko.applyBindings(vm, $('#red-tryout')[0]);
    vm.theText('the other text');
}

