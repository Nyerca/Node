//Write an HTTP server that receives only POST requests and converts incoming
//POST body characters to upper-case and returns it to che client.
//The server listen on the port procided as first argument.
//Use through2-map which allows you to create a transform stream using only a single
//function that takes a chunk of data and returns a chunk of data.

var http = require('http');
var map = require('through2-map');
    

var server = http.createServer(function (request, response) { //Callback function called once for each connection
	if (request.method !== 'POST') {
		return res.end('send me a POST\n')
    }
	//The incominc data "request" is converted to a String (if it isn't already), then the method
	//toUpperCase is called and the result is passed to "response"
	request.pipe(map(function (chunk) {
       return chunk.toString().toUpperCase();
    })).pipe(response)
})
server.listen(process.argv[2]);