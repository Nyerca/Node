//Create a Node.js file that will convert the output "Hello World!" into upper-case letters

var http = require('http');
var uc = require('upper-case');
http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(uc("Hello World!"));
    res.end();
}).listen(8080);