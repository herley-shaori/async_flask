
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    console.log('Alamat Socket: ' + socket)

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10){
            numbers_received.shift()
        }            
        numbers_received.push(msg.number);
        
        // numbers_string = '';
        // for (var i = 0; i < numbers_received.length; i++){
        //     numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        // }

        var nomor = numbers_received[0]
        var alamat_absolut = ''
        if(nomor == 0){
            alamat_absolut = 'static/images/2.JPG'
            $('#log').html(alamat_absolut);
            $("#gambar_saya").attr("src",alamat_absolut);
        }else{
            alamat_absolut = 'static/images/1.JPG'
            $('#log').html(alamat_absolut);
            $("#gambar_saya").attr("src",alamat_absolut);
            $('.music').html('<audio controls autoplay> <source src="static/audio/halo.mp3"  type="audio/mpeg"> </audio>');
        }
        // $('#log').html(numbers_string);
    });

});