
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10){
            numbers_received.shift()
        }

        // numbers_received.push(msg.number);
        
        // var alamat_gambar =numbers_received[i]
        // $('#log').html(msg.number);

        // numbers_string = '';
        // for (var i = 0; i < numbers_received.length; i++){
        //     numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        // }

        var nomor = msg.number
        var alamat_absolut = ''
        if(nomor == 0){
        }else if(nomor == 1){
            // Tidak bisa dipakai karena video akan diunggah terus menerus sesuai dengan thread yang sedang berjalan.
            // $('.video').html('<video controls autoplay> <source src="static/video/luaran.mp4" type="video/mp4"> </video>');
            $('.music').html('<audio controls autoplay> <source src="static/audio/halo.mp3"  type="audio/mpeg"> </audio>');
        }else{
            $('#log').html('Berkas telah selesai diputar.');
            $('.music').html('<audio controls> <source src=""  type="audio/mpeg"> </audio>');
            $("#video_saya").attr("src","");
        }

        // $('#log').html(numbers_string);
    });

});