var fs = require('fs');
var path = require('path');
var elems = [];
module.exports = function (dirName, extension, callback) {
    fs.readdir(dirName, function doneFiltering(err, list) {
	 if(err) {
		 return callback(err);
	 }
    for(var i = 0; i<list.length; i++) {
		if(path.extname(list[i]) == "."+extension) {
			elems.push(list[i]);
		}
	}
	callback(null, elems);
})

};