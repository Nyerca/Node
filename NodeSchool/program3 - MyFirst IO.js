//Write a program that uses a single synchronous filesystem operation to read a file
//and print the number of newlines (\n) it contains to the console, similar to running
//cat file | wc -l

//The full path to the file to read will be provided as the first command-line argument
//(process.argv[2])

var fs = require('fs'); //Modul needed to perform filesystem operations

var buf = fs.readFileSync(process.argv[2]);
var str = buf.toString();
console.log(str.split('\n').length - 1);