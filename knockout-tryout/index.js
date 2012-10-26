

function isKanji(k) {

    var charCode = k.charCodeAt(0);
    return charCode >= 0x4E00 && charCode < 0x9FFF;
}

var SentenceViewModel = function(sentence, structure, translation) {

    this.sentence = sentence;
    this.structure = structure;
    this.translation = translation;
    this.sentenceStruct = this.parseStructure(structure);

    this.showFurigana = ko.observable(true);
    this.spaceWords = ko.observable(true);
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


function init() {

    var sentence = '竹はま私風までたわむ 。';
    var struct = '竹[たけ] は ま私[わし]風[かぜ]ま で たわむ 。';
    var translation = 'This is the meaning of the text in English.';

    var mainViewModel = {
        sentenceVM: new SentenceViewModel(sentence, struct, translation),
        toggleReadingAid: function () {

            var showing = this.sentenceVM.showFurigana();
            this.sentenceVM.showFurigana(!showing);
            this.sentenceVM.spaceWords(!showing);
        },
    };

    ko.applyBindings(mainViewModel);
    console.log(mainViewModel.sentenceVM.sentence);
}

