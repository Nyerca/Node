//We can also emit events from the client. To emit an event from your client, 
//use the emit function on the socket object.
//To handle these events, use the on function on the socket object on your server.

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res) {
   res.sendFile('index3.html', { root: __dirname });
});

io.on('connection', function(socket) {
   socket.on('clientEvent', function(data) {
      console.log(data);
   });
});

http.listen(3000, function() {
   console.log('listening on localhost:3000');
});