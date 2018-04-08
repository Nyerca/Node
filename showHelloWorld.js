//Include a module
var http = require('http');
var dt = require('./dateModule');

//createServer creates an HTTP server object
http.createServer(function (req, res) { //req argument represents the request from the client, as an object
	res.writeHead(200, {'Content-Type': 'text/plain'}); //The result is supposed to be displayed as HTML
	res.write("The date and time are currently: " + dt.myDateTime()); //write a response to the client
	res.write(req.url);
	res.end('Hello World!'); //end the response
	console.log("Response sent"); 
}).listen(8080); //the server object listens on port 8080
console.log("A node web server is running!");