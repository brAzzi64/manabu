// common initialization         
$(document).ready(function() {
    
    setupCSRFTokenHook();
});

// CSRF Token hook for POST requests handling
function setupCSRFTokenHook() {

    $(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
}

function issueAjaxJSONCall(name, params, callback, errorCallback) {

    $.getJSON(name, params, callback).error(errorCallback || function () {
    
        console.log("Error: the call to '" + name + "' failed.");
    });
}

function isKanji(k) {

    var charCode = k.charCodeAt(0);
    return charCode >= 0x4E00 && charCode < 0x9FFF;
}

var QueryString = function () {
  // This function is anonymous, is executed immediately and 
  // the return value is assigned to QueryString!
  var query_string = {};
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    
    // Decode the parameter value
    pair[1] = decodeURIComponent( pair[1] );

    	// If first entry with this name
    if (typeof query_string[pair[0]] === "undefined") {
      query_string[pair[0]] = pair[1];
    	// If second entry with this name
    } else if (typeof query_string[pair[0]] === "string") {
      var arr = [ query_string[pair[0]], pair[1] ];
      query_string[pair[0]] = arr;
    	// If third or later entry with this name
    } else {
      query_string[pair[0]].push(pair[1]);
    }
  } 
    return query_string;
} ();

/* Sentence */

var SentenceViewModel = function(text, structure, translation, readingAidOn) {

    this.text = text; // TODO: update with structure
    this.structure = ko.observable(structure);
    this.translation = ko.observable(translation);
    this.parsedStructure = ko.computed(function() {
        return this.parseStructure(this.structure());
    }, this);
    this.readingAidEnabled = ko.observable(readingAidOn || false);
    this.showTranslation = ko.observable(false);
};

SentenceViewModel.prototype.parseStructure = function(struct) {

    var disassembleWordStructure = function (wordStructure) {

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
    };

    var sentence = [];
    var strWords = struct.split(" ");
    for (i in strWords) {
        var word = [];
        var wordStructure = disassembleWordStructure(strWords[i]);
        for (j in wordStructure) {
            var subWordStructure = wordStructure[j];
            word.push({ chars: subWordStructure[0], pron: subWordStructure[1] });
        }
        sentence.push(word);
    }

    return sentence;
};


