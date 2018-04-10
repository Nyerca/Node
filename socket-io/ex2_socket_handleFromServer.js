//Message was a built-in event provided by the API, but is of not much use in a real application, 
//as we need to be able to differentiate between events.
//To allow this, Socket.IO provides us the ability to create custom events. 
//You can create and fire custom events using the socket.emit function.

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

//The require('socket.io')(http) creates a new socket.io instance attached to the http server. 
//The io.on event handler handles connection, disconnection, etc., events in it, using the socket object.


app.get('/', function(req, res) {
   res.sendFile('index2.html', { root: __dirname });
});

//Whenever someone connects this gets executed
io.on('connection', function(socket) {
   console.log('A user connected');

   //Send a message after a timeout of 4seconds
   setTimeout(function() {
      //Sending an object when emmiting an event
      socket.emit('testerEvent', { description: 'A custom event named testerEvent!'});
   }, 4000);
   
   //Whenever someone disconnects this piece of code executed
   socket.on('disconnect', function () {
      console.log('A user disconnected');
   });
});

http.listen(3000, function() {
   console.log('listening on *:3000');
});


