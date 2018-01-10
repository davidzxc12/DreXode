$(document).ready(function () {
    var key = '3a3302ad37558f0abfe30187e99af15a';
    $.endlessPaginate({
        paginateOnScroll: true,
        onCompleted: function (context, fragment) {
            $('.likeBtn').off('click').on('click', function (e) {
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
            $('.dislikeBtn').off('click').on('click', function (e) {
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
            });
        }
    });

    function getWeather(position = null) {
        var lat = 24;
        var lon = 121;
        if (position != null) {
            lat = position.coords.latitude;
            lon = position.coords.longitude;
        }
        $.ajax({
            type: 'GET',
            url: 'http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&APPID=' + key,
            dataType: "json",
            success: function (resp) {
                console.log(resp);
                var temp = resp.main.temp - 273.15;
                resp = resp.weather[0];
                var prefix = 'wi wi-';
                var code = resp.id;
                var icon = weatherIcons[code].icon;

                if (!(code > 699 && code < 800) && !(code > 899 && code < 1000)) {
                    icon = 'day-' + icon;
                }
                icon = prefix + icon;
                $('.weather-icon i').attr('class', icon);
                $('.weather-icon').attr('weather', resp.main);
                $('.weather-icon').attr('temperature', temp);
            }
        })
    }
    getWeather();


    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('img.preview').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("input#pic").change(function () {
        readURL(this);

        $('img.preview').css('top', '0');
        $('img.preview').css('max-height', '150px');
        $('img.preview').css('max-width', '150px');
    });

    $('.getWeatherByLoc').on('click', function () {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(getWeather);
        } else {
            alert('Can not get your location!');
        }
    })

    $('.submit-post').on('click', function () {
        var form = $('.postForm');
        form.find('input[name!="csrfmiddlewaretoken"]').remove();
        form.append($('.upper-section input').clone());
        form.append('<input name="temp" value="' + $('.weather-icon').attr('temperature') + '">');
        form.append('<input name="weather" value="' + $('.weather-icon').attr('weather') + '">');
        form.append('<input name="weather-icon" value="' + $('.weather-icon i').attr('class') + '">');
        if (form.find('input#pic').val() == '') {
            alert('Must select one photo!');
            form.find('input[name!="csrfmiddlewaretoken"]').remove();
        } else
            form.submit();
        return;
    })

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

    $('.filter li').on('click',function(){
        window.location.href='/feed/'+$(this).attr('id')
    })
    



})