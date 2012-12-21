
var reviewViewModel = {

    sentence : ko.observable(),
    hintButtonText : ko.observable("Loading..."),

    init : function() {

        // apply Knockout bindings
        ko.applyBindings(this);

        this.getRandomSentence();
    },

    getRandomSentence : function() {

        var that = this;
        issueAjaxJSONCall(
            'review/api/get_random_sentence', {},
            function(data) { that.onGetRandomSentence(data); });
    },

    onGetRandomSentence : function(data) {
        
        this.hintButtonText("Show Furigana");

        var vm = new SentenceViewModel(undefined, data.structure, data.translation);
        this.sentence(vm);
    },

    showHint : function() {

        if ( !this.sentence().readingAidEnabled() ) {
            this.sentence().readingAidEnabled(true);
            this.hintButtonText("Show Translation");
        } else {
            if ( !this.sentence().showTranslation() ) {
                this.sentence().showTranslation(true);
                this.hintButtonText("Hide Hints");
            } else {
                this.sentence().readingAidEnabled(false);
                this.sentence().showTranslation(false);
                this.hintButtonText("Show Furigana");
            }
        }
    },
}


$(document).ready(function() {
        
    reviewViewModel.init();
});

