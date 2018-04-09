//Write a program that performs an HTTP GET request to a URL provided as first arg.
//Collect all the data from the server not just the "data" event and then prints
//the number of chars and the string
var http = require('http');
var b1 = require('bl'); //Module required


http.get(process.argv[2], function(res) {
	res.pipe(b1(function(err,data) { //pipe collects an entire stream of data
		if(err) {
			return console.error(err);
		}
		console.log(data.toString().length);
		console.log(data.toString());
	}));
}).on('error', console.error);