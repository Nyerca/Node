var http = require('http');
http.createServer(function (req, res) { 
	res.writeHead(200, {'Content-Type': 'text/plain'}); 
	res.end('Hello World!'); 
	console.log("Response sent"); 
}).listen(8080); 
console.log("A node web server is running!");