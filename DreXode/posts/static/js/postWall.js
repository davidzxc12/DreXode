$(document).ready(function() {
    var key = '3a3302ad37558f0abfe30187e99af15a';

    // $.ajax({
    //     type:'GET',
    //     url:'http://api.openweathermap.org/data/2.5/weather?lat=24.1469&lon=120.683899&APPID='+key,
    //     dataType: "json",
    //     success:function(resp){
    //         resp = resp.weather[0];
    //         $('.weather-icon').attr('src','http://openweathermap.org/img/w/'+resp.icon+'.png')
    //     }
    // })


    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('img.preview').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("input#pic").change(function() {
        readURL(this);
      });

})