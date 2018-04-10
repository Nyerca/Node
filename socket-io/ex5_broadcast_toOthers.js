//If we want to send an event to everyone, but the client that caused it
//we can use the socket.broadcast.emit.
//Let us send the new user a welcome message and update the other clients about him/her joining.

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res) {
   res.sendFile('index5.html', { root: __dirname });
});

var clients = 0;
io.on('connection', function(socket) {
   clients++;
   socket.emit('newclientconnect',{ description: 'Hey, welcome!'});
   socket.broadcast.emit('newclientconnect',{ description: clients + ' clients connected!'})
   socket.on('disconnect', function () {
      clients--;
      socket.broadcast.emit('newclientconnect',{ description: clients + ' clients connected!'})
   });
});

http.listen(3000, function() {
   console.log('listening on localhost:3000');
});
