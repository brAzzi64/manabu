
var reviewViewModel = {

    sentences : ko.observableArray(),

    init : function() {

        // apply Knockout bindings
        ko.applyBindings(this);

        this.getSentences();
    },
    getSentences : function() {

        var that = this;
        issueAjaxJSONCall(
            'review/api/get_sentences', { 'page': 1 },
            function(data) { that.onGetSentences(data); });
    },
    onGetSentences : function(data) {
        
        for (i in data) {
            data[i].sentence = new SentenceViewModel(undefined, data[i].sentence.structure, data[i].sentence.translation);
        }
        this.sentences(data);
    },
}

// extend the SentenceViewModel prototype
SentenceViewModel.prototype.onMouseEnter = function() {

    this.readingAidEnabled(true);
}

SentenceViewModel.prototype.onMouseLeave = function() {

    this.readingAidEnabled(false);
    this.showTranslation(false);
}

SentenceViewModel.prototype.toggleShowTranslation = function() {

    this.showTranslation( !this.showTranslation() );
}


$(document).ready(function() {
        
    reviewViewModel.init();
});

