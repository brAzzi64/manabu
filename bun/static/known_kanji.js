init();

function init() {

    $(document).ready(function() {
        
        setupCSRFTokenHook();

        $(".kanji").click(function(event) { 

            event.preventDefault();
            $(this).toggleClass("known").addClass("updated");                    
        });

        $("#btn-update").click(function(event) {

            var updated_kanjis = {};
            $("#kanji-list a.updated").each(function(i, e) {

                updated_kanjis[ $(this).text() ] = $(this).hasClass("known");
            });

            // issue the call
            $.ajax({
                url: 'api/update_known_kanji',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: { updates: JSON.stringify(updated_kanjis) },
                complete: function(jqXHR, textStatus) {
                   
                    if (textStatus == 'success') {
                        bootbox.dialog("The known kanji have been updated successfully.", {
                            "label" : "Awesome!",
                            "class" : "btn-success"
                        });

                        // reset the updated indicator
                        $('.kanji.updated').removeClass('updated');
                    } else {
                        bootbox.dialog("There was a problem updating the known kanji (" + textStatus + ").", {
                            "label" : "Crap!",
                            "class" : "btn-danger"
                        });
                    }
                }});
        });
    });
}

