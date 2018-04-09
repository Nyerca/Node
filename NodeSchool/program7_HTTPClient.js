//Write a program that performs an HTTP GET request to a URL provided as first arg.
//Write the String contents of each "data" event from the response to a new line on the console.

var http = require('http');

http.get(process.argv[2], function(res) {
	res.setEncoding('utf8'); //Now "data" will emit strings
	res.on('data', function(data) {
		console.log(data);
	});
	res.on('error', console.error)
}).on('error', console.error);