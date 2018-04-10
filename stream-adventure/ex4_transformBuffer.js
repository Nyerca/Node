//Convert data from `process.stdin` to upper-case data on `process.stdout` using the `through2` module.
var through = require('through2');
var stream = through(write, end);

//Create a through stream with a `write` and `end` function:
//The `write` function is called for every buffer of available input
//If `write` is not specified, the default implementation passes the input data to
//the output unmodified.
//Inside the write function, call `this.push()` to produce output data and call
//`next()` when you're ready to receive the next chunk

 function write (buffer, encoding, next) {
        this.push(buffer.toString().toUpperCase());
		next();
    }
	
//and the `end` function is called when there is no more data
//and call `done()` to finish the output:

function end (done) {
        done();
    }
	
process.stdin.pipe(stream).pipe(process.stdout);


