
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
            data[i].sentence = new SentenceViewModel(undefined, data[i].sentence.structure, undefined);
        }
        this.sentences(data);
    },
}

// extend the SentenceViewModel prototype
SentenceViewModel.prototype.toggleReadingAid = function() {

    this.readingAidEnabled( !this.readingAidEnabled() );
}


function init() {
   
    reviewViewModel.init();
}

