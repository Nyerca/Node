var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

//The require('socket.io')(http) creates a new socket.io instance attached to the http server. 
//The io.on event handler handles connection, disconnection, etc., events in it, using the socket object.


app.get('/', function(req, res) {
   res.sendFile('index.html', { root: __dirname });
});

//Whenever someone connects this gets executed
io.on('connection', function(socket) {
   console.log('A user connected');

   //Send a message after a timeout of 4seconds
   setTimeout(function() {
      socket.send('Sent a message 4seconds after connection!');
   }, 4000);
   
   //Whenever someone disconnects this piece of code executed
   socket.on('disconnect', function () {
      console.log('A user disconnected');
   });
});

http.listen(3000, function() {
   console.log('listening on *:3000');
});


