//Include a module
var http = require('http');
var dt = require('./dateModule');
var url = require('url');

//createServer creates an HTTP server object
http.createServer(function (req, res) { //req argument represents the request from the client, as an object
	res.writeHead(200, {'Content-Type': 'text/plain'}); //The result is supposed to be displayed as HTML
	res.write("The date and time are currently: " + dt.myDateTime()); //write a response to the client
	res.write(req.url); //url holds the part of the url that comes after the domain name
	//end the response
	var q = url.parse(req.url, true).query;
	var txt = q.year + " " + q.month;
	res.end("\n" + txt);
	console.log("Response sent"); 
}).listen(8080); //the server object listens on port 8080
console.log("A node web server is running!");


//example URL: http://localhost:8080/?year=2017&month=July