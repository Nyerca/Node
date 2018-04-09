//Write a program that accepts one or more number as command-line arguments and print
//the sum of those numbers to the console.

var i;
var sum = 0;
for (i = 2; i < process.argv.length; i++) { 
    sum = sum + Number(process.argv[i]);
}

console.log(sum);