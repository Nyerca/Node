//Include a module
var http = require('http');
var dt = require('./dateModule');

http.createServer(function (req, res) { 
	res.writeHead(200, {'Content-Type': 'text/plain'}); 
	res.write("The date and time are currently: " + dt.myDateTime());
	res.end('Hello World!'); 
	console.log("Response sent"); 
}).listen(8080); 
console.log("A node web server is running!");