
function assembleWordStructureForCurrentSentence() {

    var struct = "";
    $('#sentence .word').each(function(i, word) {
        $(word).find(".sub-word").each(function(j, subword) {
            struct += $(subword).find(".literal").text();
            var $furigana = $(subword).find(".furigana");
            if ($furigana.length != 0)
                struct += "[" + $furigana.html() + "]";
        });
        struct += " ";
    });
    return struct.trim();
}


var PronunciationOption = function(kanji, text, pronunciationSetVM) {

    var that = this;

    this.pronunciation = text,
    this.selected = ko.observable(false)
    
    this.toggleSelected = function() {

        var isSelected = that.selected();
        pronunciationSetVM.clearSelection();
        that.selected(!isSelected);
    };
}

var KanjiPronunciationSet = function(onyomis, kunyomis) {

    // onyomis
    this.ON = [];
    for (i in onyomis)
        this.ON.push(new PronunciationOption(kanji, onyomis[i], this));
    // kunyomis
    this.KN = [];
    for (i in kunyomis)
        this.KN.push(new PronunciationOption(kanji, kunyomis[i], this));
}

KanjiPronunciationSet.prototype.getSelectedOption = function() {

    for (i in this.ON) {
        if ( this.ON[i].selected() )
            return this.ON[i];
    }
    for (i in this.KN) {
        if ( this.KN[i].selected() )
            return this.KN[i];
    }
    return undefined;
}

KanjiPronunciationSet.prototype.clearSelection = function() {

    for (i in this.ON) this.ON[i].selected(false);
    for (i in this.KN) this.KN[i].selected(false);
}

// TODO: move to a subclass
SentenceViewModel.prototype.clearSelections = function() {

    for (kanji in this.pronunciations) {
        this.pronunciations[kanji].clearSelection();
    }
}

var searchViewModel = {

    searchQuery : ko.observable(""),
    
    init : function(parent) {

        this.parentViewModel = parent;
    },

    doSearch : function() {

        var kanji = this.searchQuery().trim();
        if (kanji == null || kanji == '') {
            bootbox.alert("You must enter a Kanji to search sentences.");
        } else {
            location.hash = "kanji/" + kanji;
        }
    }

}


var trainViewModel = {

    kanji : ko.observable(""),

    sentence : ko.observable(),

    nextSentenceDisabled : ko.observable(false),

    doSearch : function(kanji) {

        this.page = 0;
        this.kanji(kanji);
        this.onNextSentence();
    },

    onNextSentence : function() {
    
        var that = this;
        issueAjaxJSONCall('train/api/get_sentences', { 'kanji': this.kanji(), 'page': this.page++ },
            function(data) { that.handleGetNextSentenceCompleted(data); },
            function() { that.handleGetNextSentenceFailed(); });
    },

    onLearnSentence : function() {

        var sentence = this.sentence().text;
        var struct = this.sentence().structure;
        var pronunciations = {};

        for (kanji in this.sentence().pronunciations) {
            var set = this.sentence().pronunciations[kanji];
            var selected = set.getSelectedOption();
            // TMP: temporarily commented out until we have a NONE marker
            //if ( !selected ) {
            //    bootbox.dialog('No pronunciation selected for: ' + kanji, { "label" : "OK", "class" : "btn-danger" });
            //    return;
            //}
            if (selected) {
                pronunciations[kanji] = selected.pronunciation;
            }
        }

        bootbox.confirm(
            'Are you sure you want to save the sentence?',
            "Not really...", "Yes!",
            function(result) {

                if (result) {
                    // issue the call
                    $.ajax({
                        url: 'train/api/learn_sentence',
                        type: 'POST',
                        dataType: 'json',
                        contentType: 'application/json',
                        data: { text: sentence, structure: struct, pronunciations: JSON.stringify(pronunciations) },
                        complete: function(jqXHR, textStatus) {
                           
                            if (textStatus == 'success') {
                                bootbox.dialog("The sentence as been saved successfully.", {
                                    "label" : "Cool!",
                                    "class" : "btn-success"
                                });
                            } else {
                                bootbox.dialog("There was a problem saving the sentence (" + textStatus + ").", {
                                    "label" : "Too bad",
                                    "class" : "btn-danger"
                                });
                            }
                        }});
                }
            });
    },
    
    onReset : function() {

        this.sentence().clearSelections();
    },

    onListen : function() {

        var audioTagSupport = !!(document.createElement('audio').canPlayType);
        if (!audioTagSupport) return;

        var audio = document.createElement('audio');
        audio.setAttribute('src', 'train/api/get_audio?text=' + this.sentence().text );
        audio.load();
        audio.play();
    },

    handleGetNextSentenceCompleted : function(data) {

        data = data[0]; // not paginated for now
        var vm = new SentenceViewModel(data.sentence, data.structure, data.translations[0], true);

        // TODO: extend the SentenceViewModel class adding a
        // method that creates the PronunciationOption view models.
        vm.pronunciations = {};
        for (kanji in data.pronunciations) {
            var on = data.pronunciations[kanji].ON;
            var kn = data.pronunciations[kanji].KN;
            vm.pronunciations[kanji] = new KanjiPronunciationSet(on, kn);
        }

        this.sentence(vm); 
    },

    handleGetNextSentenceFailed : function() {

        this.nextSentenceDisabled(true);
    },

    onEdit: function() {
       
        var that = this;
        bootbox.prompt(
            'Edit the structure',
            "Cancel", "Apply",
            function(result) {
                
                if (result) {
                    that.sentence().structure(result); 
                }
            },
            that.sentence().structure());
    }
}


var parentViewModel = {

    searchViewModel : ko.observable(null),

    trainViewModel : ko.observable(null),

    init : function() {

        var that = this;
        Sammy(function() {

            this.get('#kanji/:literal', function() {
                that.searchViewModel(null);
                that.trainViewModel(trainViewModel);
                that.trainViewModel().doSearch(this.params.literal);
            });

            this.get('#search', function() {
                that.trainViewModel(null);
                that.searchViewModel(searchViewModel);
                that.searchViewModel().init(this);
            });

            this.get('train', function() { this.app.runRoute('get', '#search'); });

        }).run();

        // apply Knockout bindings
        ko.applyBindings(this);
    },
}

ko.bindingHandlers.bootstrapPopover = {

    update: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
        var options = valueAccessor();
        var show = options.if != undefined ? options.if : true;
        if (show) {
            var template = $("script[type*=html][id=" + options.template + "]").clone().html();
            $(element).popover({ content: template, html: true, title: options.title, trigger: 'manual', placement: options.placement || 'bottom' });
            element.showing = false; // initialize a tracking value
            $(element).click(function(e) {

                var that = this;
                // close all other popovers first
                $("a[data-bind*=bootstrapPopover]").each(function() {
                    if (this != that) {
                        $(this).popover('hide');
                        this.showing = false;
                    }
                });

                // toggle this one
                $(this).popover('toggle');
                element.showing = !element.showing; 

                if (element.showing) {
                    // bind it to the ViewModel
                    var thePopover = $('.popover').last()[0]; // take the most recent one
                    var popoverContent = $(thePopover).find('.popover-content')[0];
                    var childBindingContext = bindingContext.createChildContext(viewModel);
                    ko.applyBindings(childBindingContext, popoverContent);

                    $(thePopover).click(function(e) {

                        // don't let it reach the body
                        // click or it will close
                        e.stopPropagation();
                    });
                }

                // don't let it reach the body click
                e.stopPropagation();
            });
        }
    }
};


$(document).ready(function() {
        
    parentViewModel.init();

    // popover hiding when clicking anywhere else
    $("html").click(function() {

        $(".kanji").children("a").each(function() {

            $(this).popover('hide');
            this.showing = false;
        });
    });
});



