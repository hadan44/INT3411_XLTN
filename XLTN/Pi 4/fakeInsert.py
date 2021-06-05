import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

# MQTT Settings 
MQTT_Broker = "localhost"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Humidity = "Iot/Sensor"
MQTT_Topic_Temperature = "Home/BedRoom/DHT22/Temperature"
MQTT_Topic_Switch = "CyberLink/commands/1037600" #CyberLink/input/json

MQTT_Topic_Register = "Iot/Infra/Register"

def on_connect(client, userdata, rc,  properties=None):
	if rc != 0:
		print("Unable to connect to MQTT Broker...")
	else:
		print("Connected with MQTT Broker: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
	pass
		
def on_disconnect(client, userdata, rc):
	if rc !=0:
		print("pass")
		
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))		

		
def publish_To_Topic(topic, message):
	mqttc.publish(topic,message)
	print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	print("")

# Fake insert data

def publish_Fake_Sensor_Values_to_MQTT():
	threading.Timer(3.0, publish_Fake_Sensor_Values_to_MQTT).start()
	Humidity_Fake_Value = float("{0:.2f}".format(random.uniform(50, 100)))

	Humidity_Data = {}
	Humidity_Data['infra_id'] = "h_sensor_01"
	Humidity_Data['value'] = Humidity_Fake_Value
	humidity_json_data = json.dumps(Humidity_Data)

	print("Publishing fake Humidity Value: " + str(Humidity_Fake_Value) + "...")
	publish_To_Topic (MQTT_Topic_Humidity, humidity_json_data)

def publish_data_to_switch():
	switchData = {
		"id":"1037600",
		"data":{
			"out1":0,
			"out2":100,
			"out3":0
		}
	}
	switchDataJson = json.dumps(switchData)
	publish_To_Topic (MQTT_Topic_Switch, switchDataJson)

def infraRegister():
	data = {
		"infra_id": "h_sensor_01",
		"type": "humidity",
		"in_topic": "in",
		"out_topic": "out"
	}

	dataJson = json.dumps(data)
	publish_To_Topic(MQTT_Topic_Register, dataJson)

# infraRegister()	
publish_data_to_switch()
#publish_Fake_Sensor_Values_to_MQTT()
