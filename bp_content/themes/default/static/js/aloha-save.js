    Aloha.ready(function() {
    Aloha.require( ['aloha', 'aloha/jquery'], function( Aloha, jQuery) {

        // save all changes after leaving an editable
        Aloha.bind('aloha-editable-deactivated', function(){
            var content = Aloha.activeEditable.getContents();
            var contentId = Aloha.activeEditable.obj[0].id;
            var pageId = window.location.pathname;

            // textarea handling -- html id is "xy" and will be "xy-aloha" for the aloha editable
            if ( contentId.match(/-aloha$/gi) ) {
                contentId = contentId.replace( /-aloha/gi, '' );
            }

            var request = jQuery.ajax({
                url: '//' + window.location.host +"/_ah/api/contentapi/v1/aloha",
                type: "POST",
                data: JSON.stringify({
                    content : content,
                    contentId : contentId,
                    pageId : pageId
                }),
                dataType: "json"
            });

            request.done(function(msg) {
                jQuery("#log").html( msg ).show().delay(800).fadeOut();
            });

            request.error(function(jqXHR, textStatus) {
                alert( "Request failed: " + textStatus );
            });
        });

    });
    });
