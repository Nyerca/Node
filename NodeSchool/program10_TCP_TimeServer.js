//Write a TCP Time Server which should listen to TCP connections on the port provided as first
//argument. For each connection write the current date.
//After sending the string, close the connection.

var net = require('net');

function zeroFill (i) {
	return (i < 10 ? '0' : '') + i;
}

function now () {
	var d = new Date();
	return d.getFullYear() + '-' +
	zeroFill(d.getMonth() + 1) + '-' +
	zeroFill(d.getDate()) + ' ' +
	zeroFill(d.getHours()) + ':' +
	zeroFill(d.getMinutes());
}

var server = net.createServer(function (socket) {
	socket.end(now() + '\n');
})
server.listen(process.argv[2]);