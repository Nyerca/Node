use admin
db.createUser(
  {
    user: "myUserAdmin",
    pwd: "abc123",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)

mongo
use admin
db.auth("myUserAdmin", "abc123" )



mongo --port 27017 -u "myUserAdmin" -p "abc123" --authenticationDatabase "admin"





-------
use test
db.createUser(
  {
    user: "myTester",
    pwd: "xyz123",
    roles: [ { role: "readWrite", db: "test" },
             { role: "read", db: "reporting" } ]
  }
)
mongo --port 27017 -u "myTester" -p "xyz123" --authenticationDatabase "test"

use test
db.auth("myTester", "xyz123" )


Connect and authenticate as myTester.
To authenticate during connection
Start a mongo shell with the -u <username>, -p <password>, and the --authenticationDatabase <database> command line options:

mongo --port 27017 -u "myTester" -p "xyz123" --authenticationDatabase "test"
To authenticate after connecting
Connect the mongo shell to the mongod:

mongo --port 27017
Switch to the authentication database (in this case, test), and use db.auth(<username>, <pwd>) method to authenticate:

use test
db.auth("myTester", "xyz123" )
Insert into a collection as myTester.
As myTester, you have privileges to perform read and write operations in the test database (as well as perform read operations in the reporting database). 
For example, you can peform the following insert operation in the test database:
db.foo.insert( { x: 1, y: 1 } )



------------------
show users