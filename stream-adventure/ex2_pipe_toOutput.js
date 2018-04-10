//Use `fs.createReadStream()` to pipe the given file to `process.stdout`.

var fs = require('fs');
fs.createReadStream(process.argv[2]).pipe(process.stdout);
