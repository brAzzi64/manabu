
var historyViewModel = {

    dates : ko.observableArray(),

    init : function() {

        // apply Knockout bindings
        ko.applyBindings(this);

        this.getSentences();
    },
    getSentences : function() {

        var that = this;
        issueAjaxJSONCall(
            'history/api/get_sentences', { 'page': 1 },
            function(data) { that.onGetSentences(data); });
    },
    onGetSentences : function(data) {
        
        var dates = [];
        for (date in data) {
            var dateVM = { date: date, sentences: [] }
            var sentences = data[date];
            for (i in sentences) {
                dateVM.sentences.push(new SentenceViewModel(undefined, sentences[i].structure, sentences[i].translation));
            }
            dates.push(dateVM);
        }
        this.dates(dates);
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
        
    historyViewModel.init();
});

