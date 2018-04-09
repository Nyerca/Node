var fs = require('fs');

fs.unlink('trial.txt', function (err) {
  if (err) throw err;
  console.log('File deleted!');
});