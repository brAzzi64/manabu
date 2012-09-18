init();

function init() {

    $(document).ready(function() {

        $("#btn-search").click(function(e) {
            
             e.preventDefault(); 
             searchInputKanji();
        });

        $("#kanji-input").keypress(function(e) {

            if (e.which == 13) {
                e.preventDefault();
                searchInputKanji();
            }
        });
    });
}

function searchInputKanji() {

    var kanji = $('#kanji-input').val();
    if (kanji == null || kanji == '') {
        bootbox.alert("You must enter a Kanji to search sentences.");
        return;
    }

    window.location.href = 'train?kanji=' + kanji;
}

