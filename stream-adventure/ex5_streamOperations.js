//convert even-numbered lines to upper-case and odd-numbered
//lines to lower-case. Consider the first line to be odd-numbered.
//you can use the `split` module to split input by newlines.

var through = require('through2');
var split = require('split');

var lineCount = 0;
var tr = through(function (buf, _, next) {
    var line = buf.toString();
    this.push(lineCount % 2 === 0 //Push the line in the stream
        ? line.toLowerCase() + '\n'
        : line.toUpperCase() + '\n'
    );
    lineCount ++;
    next();
});
process.stdin
    .pipe(split()) //Execute split on rows
    .pipe(tr) //Execute tr stream operation
    .pipe(process.stdout) //Send the stream to output
;