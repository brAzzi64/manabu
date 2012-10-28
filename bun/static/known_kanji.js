
/*
    KnownKanji - ViewModel prototype for each kanji
*/
var KnownKanji = function(literal, known) {

    this.literal = ko.observable(literal);
    this.known = ko.observable(known);
    this.hasChanged = ko.observable(false);
};

KnownKanji.prototype.toggleKnown = function() {

    this.known( !this.known() );
    if (!this.hasChanged())
        this.hasChanged(true);
};


/*
    Page - ViewModel prototype for a page button element
*/
var Page = function(number, knownKanjiVM) {

    this.number = number;
    
    var that = this;
    this.active = ko.computed(function() {
            return knownKanjiVM.currentPage() == that.number;
    }, this);
    this.clicked = function(e) {
        // navigate to new page
        knownKanjiVM.getKanjiPage(that.number);
    };
};


/*
    kanjiNavigator - ViewModel object for the page navigator component
*/
var kanjiNavigator = {

    pages : [],

    knownKanjiVM : undefined,

    init : function(knownKanjiVM) {

        this.knownKanjiVM = knownKanjiVM;
        for (i = 1; i <= 12; i++) {
            this.pages.push(new Page(i, knownKanjiVM));
        }
    },

    previousClicked : function() {

        var page = this.knownKanjiVM.currentPage();
        if (page > 1) {
            // navigate to previous page
            this.knownKanjiVM.getKanjiPage(page - 1);
        }
    },

    nextClicked : function() {

        var page = this.knownKanjiVM.currentPage();
        if (page < 12) {
            // navigate to next page
            this.knownKanjiVM.getKanjiPage(page + 1);
        }
    },
};


/*
    knownKanjiViewModel - ViewModel object for the whole page
*/
var knownKanjiViewModel = {
    
    kanjis : ko.observableArray(),

    currentPage : ko.observable(1),

    navigator : kanjiNavigator,

    init : function() {

        this.navigator.init(this);

        // apply Knockout bindings
        ko.applyBindings(this);

        this.getKanjiPage(1);
    },

    getKanjiPage : function(page) {

        var that = this;
        issueAjaxJSONCall(
            'known_kanji/api/get_kanji', { 'page': page - 1 },
            function(data) {
                that.handleGetKanjiCompleted(data);
                that.currentPage(page);
            });
    },

    handleGetKanjiCompleted : function(data) {

        var kanjis = [];
        for (i in data) {
            kanjis.push( new KnownKanji(data[i].literal, data[i].known) );
        }

        this.kanjis(kanjis);
    },

    updateClicked : function() {
        
        var toUpdate = [];
        for (i in this.kanjis()) {
            var kanji = this.kanjis()[i];
            if (kanji.hasChanged())
                toUpdate.push({ literal: kanji.literal(), known: kanji.known() }); 
        }

        var that = this;

        // issue the call
        $.ajax({
            url: 'known_kanji/api/update_known_kanji',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: { updates: JSON.stringify(toUpdate) },
            complete: function(jqXHR, textStatus) {

                that.handleUpdateKnownKanjiCompleted(textStatus == 'success' ? true : false);
            }});

    },
    
    handleUpdateKnownKanjiCompleted : function(succeeded) {
                       
        if (succeeded) {
            bootbox.dialog("The known kanji have been updated successfully.", {
                "label" : "Awesome!",
                "class" : "btn-success"
            });

            // reset the updated indicator
            for (i in this.kanjis()) {
                var kanji = this.kanjis()[i];
                kanji.hasChanged(false);
            }
        } else {
            bootbox.dialog("There was a problem updating the known kanji (" + textStatus + ").", {
                "label" : "Crap!",
                "class" : "btn-danger"
            });
        }
    },
};


$(document).ready(function() {
        
    //setupCSRFTokenHook();

    knownKanjiViewModel.init();
});


