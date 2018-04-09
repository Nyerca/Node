//Write a program that uses a single Asynchronous filesystem operation to read a file
//and print the number of newlines (\n) it contains to the console, similar to running
//cat file | wc -l

//The full path to the file to read will be provided as the first command-line argument
//(process.argv[2])

//Callbacks are functions that are executed asynchronously, or at a later time.
//https://github.com/maxogden/art-of-node#callbacks

var fs = require('fs'); //Modul needed to perform filesystem operations
var dim = undefined;
function count(callback) {
  fs.readFile(process.argv[2],'utf8', function doneReading(err, fileContents) {
	 if(err) {
		 return console.log(err);
	 }
    callback(fileContents);
  })
}

function logMyDim(fileContents) {
	dim = fileContents.split('\n').length - 1;
  console.log(dim);
}

count(logMyDim);