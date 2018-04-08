var fs = require('fs');

fs.appendFile('trial.txt', 'Hello content!', function (err) {
  if (err) throw err;
  console.log('Saved!');
})