from pymongo import MongoClient
import pprint

def get_database(host, port, db_name, username, pwd):
    """Connect to a database given a credential dict.

    Args:
        cred (dict): {database, [host, port, username, password]}

    Returns:
        pymongo.database.Database: The database object.
    """
    print("hi");
    # respect potential multiprocessing fork
    conn = MongoClient(host, port)
    db = conn[db_name]
    db.authenticate(username, pwd)
    return db
	
def get_database_dictionary(dict):
    """Connect to a database given a credential dict.

    Args:
        cred (dict): {database, [host, port, username, password]}

    Returns:
        pymongo.database.Database: The database object.
    """
    print("hi");
    # respect potential multiprocessing fork
    conn = MongoClient(dict['host'], dict['port'])
    db = conn[dict['db_name']]
    db.authenticate(dict['username'], dict['pwd'])
    return db
	
def insert_into_db(db, collection, author):
    people = db[collection]
    ppl = {"author": author}
    ppl_id = people.insert_one(ppl).inserted_id
    return ppl_id
	
def get_people(db, collection):
    coll = db[collection]
    projs = {}
    count = 0
    for person in coll.find():
        #pprint.pprint(person)
        #pprint.pprint(person['author'])
        projs[count] = person
        count = count + 1
    return projs
	
def insert_operation(db, collection, person, type, measure):
    measures = db[collection]
    measu = {"person": person,
            "type": type,
            "measure": measure}
    ms_id = measures.insert_one(measu).inserted_id
    return ms_id

dict = {'host': 'localhost', 'port': 27017, 'db_name': 'test', 'username': 'myTester', 'pwd': 'xyz123'}
db = get_database_dictionary(dict);

#db = get_database('localhost',27017, "test", "myTester", "xyz123");
#insert_into_db(db, "people", "Mark")


people = get_people(db,"people")
pprint.pprint(people[0]['author']) #Stampo la prima persona

for num in range(len(people)): #Stampo tutte le persone
    pprint.pprint(people[num]['author'])
	
#insert_operation(db, "measures", "Mark","Temperature", "36")
measures = get_people(db,"measures")
str_out = measures[0]['type'] + " : " + measures[0]['measure']
pprint.pprint(str_out) #Stampo la prima persona

    

