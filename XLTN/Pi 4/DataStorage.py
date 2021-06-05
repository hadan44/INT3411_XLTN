import json
import mysql.connector as mysqll
import pymysql.cursors
from datetime import datetime

# SQLite DB Name
db_hostname = "localhost"
db_username = "root"
db_password = "123456"
db_database = "IOT"

class DatabaseManager():
    def __init__(self):
        self.conn = mysqll.connect(host = "localhost", user = "root", passwd = "123456", database = "IOT", port = 3306)
        self.conn.commit()
        self.cur = self.conn.cursor()
        
    def modifyDbRecord(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()
        
    def selectFromDb(self, sql_query):
        self.cur.execute(sql_query)
        return cur.fetchall()

def infraRegister(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	Infra_id = json_Dict['infra_id']
	Type = json_Dict['type']
	inTopic = json_Dict['in_topic']
	outTopic = json_Dict['out_topic']

	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.modifyDbRecord("insert into Infra (infra_id, type, in_topic, out_topic) values (%s, %s, %s, %s)",
	[Infra_id, Type, inTopic, outTopic])
	del dbObj

# Save sensor data
def insertSensorData(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	Infra_id = json_Dict['infra_id']
	Created_Date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	Value = json_Dict['value']
	
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.modifyDbRecord("insert into Sensor_data (infra_id, created_date, Value) values (%s, %s, %s)",
	[Infra_id, Created_Date, Value])
	del dbObj
	print("Inserted sensor Data into Database.")
	print("")

# Save switch data
def insertSwitchData(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	Infra_id = json_Dict['id']
	status = json.dumps(json_Dict['data'])
	createdDate = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.modifyDbRecord("insert into Switch_data (infra_id, created_date, status) values (%s, %s, %s)",
	[Infra_id, createdDate, status])
	del dbObj
	print("Inserted switch Data into Database.")
	print("")

# Data Handler
def dataHandler(topic, jsonData):
	if topic == "Iot/Sensor":
		insertSensorData(jsonData)
	elif topic == "Iot/Infra/Register":
		infraRegister(jsonData)
	elif topic == "CyberLink/input/json":
		insertSwitchData(jsonData)
		
		
conn = mysqll.connect(host = "localhost", user = "root", passwd = "123456", database = "IOT", port = 3306)
cur = conn.cursor()
cur.execute("select * from Sensor_data where infra_id = 'h_sensor_01'")
data = cur.fetchall()
print(data)