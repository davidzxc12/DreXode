$(document).ready(function () {
    $('.newComment').on('click', function () {
        var val = $('#new-comment').val();
        if ($.trim(val) == '') {
            alert('Please enter comment.');
        } else {
            var form = $('#commentForm');
            form.find('input#ccc').val(val);
            form.submit();
        }
    })

    $.endlessPaginate({
        paginateOnScroll: true
    });



    //AJAX
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
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
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $('.likeBtn').on('click', function (e) {
        var _this = $(this);
        var userID = $.trim($('.Username').text());
        var postID = $(this).parents('.entry-container').attr('id');
        $.ajax({
            async: false,
            url: '/addlike',
            dataType: "json",
            data: {
                'user': userID,
                'post': postID,
                'action': 'like'
            },
            method: "POST",
            success: function (json) {
                resp = json;
                console.log(resp);
                _this.next('#like-count').text(json.count);
            }
        });

    })
    $('.dislikeBtn').on('click', function (e) {
        var _this = $(this);
        var userID = $.trim($('.Username').text());
        var postID = $(this).parents('.entry-container').attr('id');
        $.ajax({
            async: false,
            url: '/addlike',
            dataType: "json",
            data: {
                'user': userID,
                'post': postID,
                'action': 'dislike'
            },
            method: "POST",
            success: function (json) {
                resp = json;
                console.log(resp);
                _this.next('#dislike-count').text(json.count);
            }
        });

    })
})