var fs = require('fs');

function addOne(callback) {
  fs.readFile('number.txt', function doneReading(err, fileContents) {
    myNumber = parseInt(fileContents);
    myNumber++;
    callback();
  })
}

function logMyNumber() {
  console.log(myNumber);
}

addOne(logMyNumber);
console.log("printed earlier");
//When the last line of our program gets executed addOne is invoked with the logMyNumber function 
//passed as its callback argument. 
//Invoking addOne will first run the asynchronous fs.readFile function. 
//This part of the program takes a while to finish.

//With nothing to do, node idles for a bit as it waits for readFile to finish. If there was anything 
//else to do during this time, node would be available for work.

//As soon as readFile finishes it executes its callback