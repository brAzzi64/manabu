var sentence;

function init(kanji) {

    $(document).ready(function() {
        
        setupCSRFTokenHook();

        // initial page
        var page = 0;

        $("#btn-next").click(function(event) { page++; issueGetNextSentence(kanji, page); });
        $("#btn-join").click(function(event) { joinSelectedWords(); });
        $("#btn-reset").click(function(event) { resetSentence(); });
        $("#btn-learn").click(function(event) { issueLearnSentence(); });

        issueGetNextSentence(kanji, page);

        // the Kanji to look sentences for has already been
        // set by the backend when returning the template.
    });
}

function issueGetNextSentence(kanji, page) {
    
    issueAjaxJSONCall('train/api/get_sentences', { 'kanji': kanji, 'page': page },
        function(data) { onGetSentenceArrived(data); });
}

function issueLearnSentence() {

    var st = assembleWordStructureForCurrentSentence();
    var ps = {};

    for (kanji in sentence['pronunciations']) {
        var prs = sentence['pronunciations'][kanji];
        if (!prs.USED) {
            bootbox.dialog('No pronunciation selected for: ' + kanji, { "label" : "OK", "class" : "btn-danger" });
            return;
        }
        ps[kanji] = prs.USED;
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
                    data: { text: sentence['sentence'], structure: st, pronunciations: JSON.stringify(ps) },
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
}

function disassembleWordStructure(wordStructure) {

    var struct = [];
    while (wordStructure != '') {
                                       // hira-kata* all-but-hira-kata+ [ pronunciation* ] rest*
        var match = wordStructure.match(/([\u3040-\u309F\u30A0-\u30FF]*)([^\u3040-\u309F\u30A0-\u30FF]+)\[(.*?)\](.*)/);
        if (match == null) {
            struct.push([wordStructure]);
            break;
        } else {
            if ( match[1] != '' )
                struct.push([match[1]]);       // pre-word
            struct.push([match[2], match[3]]); // kanji + pronunciation
            wordStructure = match[4];          // rest of the string
        }
    }
    return struct;
}

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

function onGetSentenceArrived(data) {
    
    // obtaining first element while items_per_page is hardcoded to 1 in backend
    sentence = data[0];

    loadSentence(sentence);
}

function is_kanji(k) {

    var charCode = k.charCodeAt(0);
    return charCode >= 0x4E00 && charCode < 0x9FFF;
}

function loadSentence(data) {

    // add the received elements
    if ( data['sentence'] ) {
        $('#sentence').empty();
        var chars = data['structure'].split(" ");
        for (i in chars) {
            var structure = disassembleWordStructure(chars[i]);
            var bun = $('#sentence').append("<div class='word'></div>");
            for (j in structure) {
                var part = structure[j];
                var word = bun.find(".word:last").append("<div class='sub-word'></div>");
                var subword = word.find(".sub-word:last");
                if ( part.length > 1 )
                    subword.append("<div class='furigana'>" + part[1] + "</div>");
                for ( k in part[0] ) {
                    if ( is_kanji( part[0][k] ) ) {
                        var $wrapper = $("<div class='literal kanji'>");
                        var $anchor = $("<a rel='popover' data-title='MI' href='#'>")
                                        .data("onyomis", data['pronunciations'][ part[0][k] ].ON)
                                        .data("kunyomis", data['pronunciations'][ part[0][k] ].KN);
                        subword.append( $wrapper.append( $anchor.append( part[0][k] ) ) );
                    } else { // iteration mark falls here
                        subword.append("<div class='literal'>" + part[0][k] + "</div>");
                    }
                }
            }
        }

        // Initialize furigana editors
        var onFuriganaDblClick = function() {

            var $el = $(this);

            // current pronunciation
            var text = $el.html();
            var $parent = $(this).parent();
            var width = $parent[0].scrollWidth;

            $el.wrap("<input class='furigana-edit' type='text'></input>").remove();
            var $input = $parent.find('input.furigana-edit').val(text);
            $parent.css('width', width); // hack to prevent parent from widening

            $input.keypress( function(e) {
                if (e.which == 13) {
                    $parent.css('width', '');
                    var text = $input.val();
                    $input.wrap("<div class='furigana'>" + text + "</div>").remove();
                    $parent.find('.furigana').dblclick(onFuriganaDblClick);
                }
            });
        };

        $('.furigana').dblclick(onFuriganaDblClick);

        // Initialize kanji pronunciation selections
        $.each(sentence['pronunciations'], function(index, value) {
             sentence['pronunciations'][index].USED = false;
        });

        // Initialize popovers
        var hovering = false;
        var kanji;

        $("[rel=popover]").hover(
            function() { // hover IN
                hovering = true;
                var currentKanji = $(this).html();
                if (currentKanji == kanji) // if popup still didn't close...
                    return;

                kanji = currentKanji; 

                // generate the HTML content
                var $el = $(this);
                var $content = $("<div style='margin-top: 0px; margin-bottom: 0px;'>").wrap('<div>')
                    .append("<div class='pronunciation-title'>on'yomi</div>").append("<div class='onyomi'>")
                    .append("<div class='pronunciation-title'>kun'yomi</div>").append("<div class='kunyomi'>");
                var $onyomi = $content.find(".onyomi");
                var $kunyomi = $content.find(".kunyomi");
                var $item = null;
                $.each($el.data('onyomis'), function(index, value) {
                    $item = $("<a href='#' class='pro-option'>" + value + "</a>");
                    $onyomi.append($item);
                    $item = null;
                });
                $.each($el.data('kunyomis'), function(index, value) {
                    $item = $("<a href='#' class='pro-option'>" + value + "</a>");
                    $kunyomi.append($item);
                    $item = null;
                });
              
                // close all other popovers:
                $('body .popover').remove();

                // show new
                $el.popover({ content: $content.parent().html(), trigger: 'manual', placement: 'bottom', html: true }).popover('show');

                // remove the header, we'll manage the whole area ourselves
                $('body .popover-inner > .popover-title').remove();
                
                // reflect the state of the selections in the popover 
                $('.pro-option').each(function(index, obj) {
                    $(obj).toggleClass('selected', sentence['pronunciations'][kanji].USED == $(obj).text());
                });
                
                // on click, select the pronunciation for the Kanji 
                $('.pro-option').click(function(e) {

                    if ( $(this).hasClass('selected') ) {
                        $(this).removeClass('selected');
                        sentence['pronunciations'][kanji].USED = null;
                    } else {
                        $('.pro-option').not(this).removeClass('selected');
                        $(this).addClass('selected');
                        sentence['pronunciations'][kanji].USED = $(this).text();
                    }
                });
            },
            function() { // hover OUT
                var $el = $(this);
                var $popover = $('body .popover');
                var hideFn = function () {
                    if (!hovering) {
                        kanji = null;
                        $popover.fadeOut(100);
                        setTimeout( function() { $el.popover('hide'); }, 100 );
                    }
                };
                $popover.hover(
                    function() { hovering = true; },
                    function() {
                        hovering = false;
                        setTimeout(hideFn, 400);
                    } );
                setTimeout(hideFn, 400);

                hovering = false;
            });

        // Fill the translations
        $('#translation').empty();
        for (i in data['translations']) {
            var line = data['translations'][i];
            $('#translation').append("<p>" + line + "</p>");
        }
        
        if ( data['isLast'] )
            $('#btn-next').attr("disabled", true);
    }
    else { console.log("should not happen"); }
}

function resetSentence() {

    $('#sentence').empty();
    $('#translation').empty();

    loadSentence(sentence);
}

function joinSelectedWords() {

    var sel = window.getSelection();
    if (sel.rangeCount == 0)
        return; // no selection

    var range = sel.getRangeAt(0);
    var startWord = $(range.startContainer).parents(".word")[0]; 
    var endWord = $(range.endContainer).parents(".word")[0];

    // check if selection is under the handled area and is valid
    if (startWord && endWord && startWord != endWord) {

        var iter = $(startWord).next()[0];
        while (true) {
            var childs = $(iter).children();
            $(startWord).append(childs);
            
            if (iter == endWord) {
                $(iter).remove();
                break;
            } else {
                var toDelete = iter;
                iter = $(iter).next()[0];
                $(toDelete).remove();
            }
        }
    }

    clearSelection();
}

function clearSelection() {

    if (window.getSelection) {
        if (window.getSelection().empty) {  // webkit
            window.getSelection().empty();
        } else if (window.getSelection().removeAllRanges) {  // mozilla
            window.getSelection().removeAllRanges();
        }
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
            this.parentViewModel.doSearch(kanji);        
        }
    }

}


var trainViewModel = {

    kanji : ko.observable(""),

    sentence : ko.observable(),

    doSearch : function(kanji) {

        this.page = 0;
        this.kanji(kanji);
        this.getNextSentence();
    },

    getNextSentence : function() {
    
        var that = this;
        issueAjaxJSONCall('train/api/get_sentences', { 'kanji': this.kanji(), 'page': this.page++ },
            function(data) { that.handleGetNextSentenceCompleted(data); });
    },

    handleGetNextSentenceCompleted : function(data) {

        var vm = new SentenceViewModel(data[0].sentence, data[0].structure, data[0].translations[0]);
        vm.readingAidEnabled(true);
        this.sentence(vm); 
    },
}


var parentViewModel = {

    searchViewModel : searchViewModel,

    trainViewModel : trainViewModel,

    current : ko.observable(searchViewModel),

    init : function() {

        this.searchViewModel.init(this);

        // apply Knockout bindings
        ko.applyBindings(this);
    },

    doSearch : function(kanji) {

        this.current(trainViewModel);
        this.trainViewModel.doSearch(kanji);
    },
    
    changeToSearchView : function() {

        this.current('search');
    },
    
    changeToTrainView : function() {

        this.currentView('train');
    }

}

parentViewModel.searchViewVisible = ko.computed(function() {
        return this.current() == this.searchViewModel;
}, parentViewModel),

parentViewModel.trainViewVisible = ko.computed(function() {
        return this.current() == this.trainViewModel;
}, parentViewModel),


$(document).ready(function() {
        
    parentViewModel.init();
});

