//Write a program that prints a list of file in a given directory filtered by the extension of the file.
//Args: DirectoryName FileExtension (to filter by)

var fs = require('fs'); //Modul needed to perform filesystem operations
var path = require('path');


//fs.readdir takes a pathname as its first argument and a callback as its second
//list is an array of filename strings.
fs.readdir(process.argv[2], function doneReading(err, list) {
	 if(err) {
		 return console.log(err);
	 }
    for(var i = 0; i<list.length; i++) {
		if(path.extname(list[i]) == "."+process.argv[3]) {
			console.log(list[i]);
		}
	}
})
