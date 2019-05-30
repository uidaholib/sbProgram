$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    //receive details from server
    socket.on('casc_done', function(msg) {

        updates = document.getElementById('progress').innerHTML;
        updates += '<p>' + msg.info + '<p>';

        $('#progress').html(updates);

    });

});
