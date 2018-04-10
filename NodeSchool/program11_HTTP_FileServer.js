//Write an HTTP server that serves the same file for each request it receives.
//The server should listen to a port provided by the first argument.
//The location of the file will be provided as second argument.
//Use fs.createReadStream() method to stream the file contents to the response.

var http = require('http');
var fs = require('fs');

//request is used to fetch properties
//respose is used to send data to the client
//Both of them are Node stream
var server = http.createServer(function (request, response) { //Callback function called once for each connection
	// This line opens the file as a readable stream
	var readStream = fs.createReadStream(process.argv[3]);
	readStream.on('open', function () {
    // This just pipes the read stream to the response object (which goes to the client)
    readStream.pipe(response);
  });
})
server.listen(process.argv[2]);