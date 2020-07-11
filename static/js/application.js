
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

        // Konfigurasi pemutaran video.
        if(msg.number == 1){
            $('.video').html('<video controls autoplay> <source src="static/video/video.mp4"  type="video/mp4"> </video>');
        }else if (msg.number == 0){
            $('.video').html('Tidak ada video.');
        }
    });
});