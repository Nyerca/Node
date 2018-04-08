//Include a module
var http = require('http');
var dt = require('./dateModule');

//createServer creates an HTTP server object
http.createServer(function (req, res) { 
	res.writeHead(200, {'Content-Type': 'text/plain'}); 
	res.write("The date and time are currently: " + dt.myDateTime()); //write a response to the client
	res.end('Hello World!'); //end the response
	console.log("Response sent"); 
}).listen(8080); //the server object listens on port 8080
console.log("A node web server is running!");