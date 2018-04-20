from pymongo import MongoClient
import pprint
from random import uniform
from decimal import Decimal
from bson.decimal128 import Decimal128

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

def generate_random_sensor(db, id):
    latitude = round((uniform(0, 20)),4)
    longitude = round((uniform(0, 20)),4)
    height = round((uniform(0, 20)),4)
    sensor = {'_id' : id, 'latitude': latitude, 'longitude': longitude, 'height': height, 'type': 'temp'}
    collection = db['sensors']
    sensor_id = collection.insert(sensor)
    return sensor_id

	
def insert_into_db(db, tbl_node, id, name, interval):
    complete_value = {'_id': id, 'name': name, 'interval': interval}
    collection = db['values']
    value_id = collection.insert(complete_value)
    return value_id

	
def get_value(db):
    collection = db['values']
    projs = {}
    count = 0
    for value in collection.find():
        pprint.pprint(value)
        projs[count] = value
        count = count + 1
    return projs
	
def get_value_temp(db):
    collection = db['sensors']
    all_sensors = {}
    count = 0
    for sensor in collection.find():
        if(sensor['type'] == 'temp'):
            all_sensors[count] = sensor
            print("temperatura")
        count = count + 1
    collection = db['values']
    vals = {}
    count = 0
    for sensor in range(len(all_sensors)):
        for value in collection.find({'sensor':all_sensors[sensor]['_id']}):
            pprint.pprint(value)
            vals[count] = value
            count = count + 1

def get_sensor_1or2(db):
    collection = db['sensors']
    all_sensors = {}
    count = 0
    for sensor in collection.find({"$or":[{"_id":"temp1"},{"_id":"temp2"}]}):
        if(sensor['type'] == 'temp'):
            all_sensors[count] = sensor
            print("temp")
        count = count + 1
def get_higher_20_temp(db):
    collection = db['sensors']
    all_sensors = {}
    count = 0
    for sensor in collection.find():
        if(sensor['type'] == 'temp'):
            all_sensors[count] = sensor
        count = count + 1
    collection = db['values']
    vals = {}
    count = 0
    for sensor in range(len(all_sensors)):
		# Seleziona il valore dei sensori, il cui campo value >= 20
        for value in collection.find({'sensor':all_sensors[sensor]['_id'], 'value':{"$gte":20}},{'value':1}):
            pprint.pprint(value)
            vals[count] = value
            count = count + 1

def clean_all(db):
	collection = db['values']
	collection.remove()
	collection = db['sensors']
	collection.remove()

dict = {'host': 'localhost', 'port': 27017, 'db_name': 'test', 'username': 'myTester', 'pwd': 'xyz123'}
db = get_database_dictionary(dict);

clean_all(db)
#id_sensor = generate_random_sensor(db, 'temp2')
#insert_into_db(db, 'x', 1, 'temperatura', 10)
#get_value(db)
#get_value_temp(db)
#get_sensor_1or2(db)
get_higher_20_temp(db)