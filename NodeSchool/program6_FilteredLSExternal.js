//Write a program that prints a list of file in a given directory filtered by the extension of the file.
//Args: DirectoryName FileExtension (to filter by)

//Use an external module

var myModule = require('./program6_Module.js');

var elems = myModule(process.argv[2],process.argv[3],doneFiltering);

function doneFiltering(error, list) {
	if(error) {
		 return console.log(error);
	 }
	for(var i = 0; i<list.length; i++) {
		console.log(list[i]);
	}
	
}
