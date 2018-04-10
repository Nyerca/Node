//To set up a custom namespace, we can call the ‘of’ function on the server side

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res) {
   res.sendFile('index6.html', { root: __dirname });
});

var namespace = io.of('/my-namespace');
namespace.on('connection', function(socket) {
   console.log('someone connected');
   namespace.emit('hi', 'Hello everyone!');
});

http.listen(3000, function() {
   console.log('listening on localhost:3000');
});