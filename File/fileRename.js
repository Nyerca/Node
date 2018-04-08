var fs = require('fs');

fs.rename('trial.txt', 'trialRenamed.txt', function (err) {
  if (err) throw err;
  console.log('File Renamed!');
});