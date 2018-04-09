//Write a program that performs an HTTP GET request to three URL provided as first arg.
//Collect all the data from the server not just the "data" event and then prints
//the string

//queue the results and keep track of how many of the URLs have returned their entire contents.

var http = require('http');
var b1 = require('bl'); //Module required
var s1 = undefined;
var s2 = undefined;
var s3 = undefined;
var sum = 0;
first(printURL);
second(printURL);
third(printURL);

function first(callback) {
http.get(process.argv[2], function(res) {
	res.pipe(b1(function(err,data) { //pipe collects an entire stream of data
		if(err) {
			return console.error(err);
		}
		s1 = data.toString();
		sum ++;
		callback(printURL);
	}));
})
}
function second(callback) {
http.get(process.argv[3], function(res) {
	res.pipe(b1(function(err,data) { //pipe collects an entire stream of data
		if(err) {
			return console.error(err);
		}
		s2 = data.toString();
		sum++;
		callback(printURL);
	}));
}).on('error', console.error);
}

function third(callback) {
http.get(process.argv[4], function(res) {
	res.pipe(b1(function(err,data) { //pipe collects an entire stream of data
		if(err) {
			return console.error(err);
		}
		s3 = data.toString();
		sum++;
		callback(printURL);
	}));
}).on('error', console.error);
}

function printURL() {
	if(sum>2) {
		console.log(s1);
		console.log(s2);
		console.log(s3);
	}
}