import speech_recognition as sr
import webbrowser
import subprocess
import paho.mqtt.client as mqtt
from gtts import gTTS
from playsound import playsound
import os
import mysql.connector as mysqll
import json

# install speech_recognition, python-espeak, gtts
# 
# 



lightTopic = "CyberLink/commands/1037600"
tiviTopic = "tivi"
aircondTopic = "aircond"
webTopic = "iot/web"

## Switch den
lightOn = {
    "id":"1037600",
    "data":{
        "out1":0,
        "out2":100,
        "out3":0
    }
}
lightOf = {
    "id":"1037600",
    "data":{
        "out1":0,
        "out2":0,
        "out3":0
    }
}
lightSwitch={
    "bật đèn": lightOn,
    "tắt đèn": lightOf
}
## Switch TV

tiviSwitch={
    "mở cài đặt": "KEY_MENU",
    "tắt tiếng": "KEY_MUTE",
    "mỡ tiếng": "KEY_MUTE",
    "tăng âm lượng": "KEY_VOLUMEUP",
    "giảm âm lượng":"KEY_VOLUMEDOWN", 
    "tiến kênh": "KEY_10CHANNELSUP",
    "lùi kênh": "KEY_10CHANNELSDOWN",
    "bật tivi":"KEY_POWER",
    "tắt tivi":"KEY_POWER",
    "lên": "KEY_UP",
    "xuống": "KEY_DOWN",
    "trái": "KEY_LEFT",
    "phải": "KEY_RIGHT",
    "ok":"KEY_OK",
    "phát": "KEY_PLAY",
    "thoát": "KEY_EXIT",
    "dừng":"KEY_STOP",
    "kênh không":"KEY_0",
    "kênh 0": "KEY_0",
    "kênh một":"KEY_1",
    "kênh 1":"KEY_1",
    "kênh hai":"KEY_2",
    "kênh 2":"KEY_2",
    "kênh ba":"KEY_3",
    "kênh 3":"KEY_3",
    "kênh bốn":"KEY_4",
    "kênh 4":"KEY_4",
    "kênh năm":"KEY_5",
    "kênh 5":"KEY_5",
    "kênh sáu":"KEY_6",
    "kênh 6":"KEY_6",
    "kênh bảy":"KEY_7",
    "kênh 7":"KEY_7",
    "kênh tám":"KEY_8",
    "kênh 8":"KEY_9",
    "kênh chín":"KEY_9",
    "kênh 9":"KEY_9"
}

## Switch air conditioner

aircondSwitch={
    "bật":"",
    "tắt":"",
    "tăng nhiệt độ": "",
    "giảm nhiệt độ": ""
}

## Switch infra
infraSwitcher={
    "đèn": {"topic" : lightTopic, "switch":lightSwitch},
    "tivi": {"topic" : tiviTopic, "switch":tiviSwitch},
    "điều hòa": {"topic" : aircondTopic, "switch":aircondSwitch}
}

#
# Connect to mqtt broker
# And publish data
#


MQTT_Broker = "localhost"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Humidity = "Iot/Sensor"
MQTT_Topic_Temperature = "Home/BedRoom/DHT22/Temperature"
MQTT_Topic_Switch = "CyberLink/commands/1037600"
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

#
# voice processing
#
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # print(" ", end='')
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            text = text.lower()
            print(text)
            return text
        except:
            return ""

def pushSignal(infraData, infra):
    while (True):
        ## get audio
        text = get_audio()
        ## defind condition to exit
        if (text == "kết thúc điều khiển"): 
            tts("Đã kết thúc điều khiển")    
            return
        if ("chức năng hiện tại" in text):
            tts("Hiện tại đang thực hiện điều khiển " + infra)  
            continue  
        ## controll
        topic = infraData.get("topic")
        typee = infraData.get("switch")
        command = typee.get(text, "notFound")
        if (text == ""):
            continue
        if (command == "notFound" and text != ""):
            tts("Thiết bị không có chức năng được yêu cầu, vui lòng đưa ra yêu cầu khác")
            text = ""
            continue

        if (topic == "tivi" or topic == "điều hòa"):
            bashCommand(command)
            tts("Đã thực hiện yêu cầu " + text)
        if (topic == "CyberLink/commands/1037600"):
            publish_To_Topic(topic, json.dumps(command))
            tts("Đã thực hiện yêu cầu " + text)
        # print(command.get(text, "Không rõ lệnh, vui lòng thử lại"))

# To use, call "dieu khien" + device to start controll the device. eg: "dieu khien den"
#
def getCommand():
    while (True):
        ## get audio
        text = get_audio()
        if ("điều khiển" in text):
            data = text.split(" ")
            infra = data[len(data) - 1]
            infraData = infraSwitcher.get(infra, "Không tìm thấy thiết bị")
            if (infraData == "Không tìm thấy thiết bị"):
                tts(infraData)
                continue
            else:
                tts("Đang thực hiện điều khiển " + infra)
                pushSignal(infraData, infra)
        if ("chức năng hiện tại" in text):
            tts("không có chức năng")
        if ("nhiệt độ" in text):
            temp = selectQuery("select value from Sensor_data where infra_id = 'AM2301_T' ORDER BY id DESC limit 1")[0][0]
            tts("nhiệt độ tại nơi ở của bạn hiện tại là " + str(temp) + "độ C")
            text  = ""
        if ("độ ẩm" in text):
            humidity = selectQuery("select value from Sensor_data where infra_id = 'AM2301_H' ORDER BY id DESC limit 1")[0][0]
            tts("độ ẩm tại nơi ở của bạn hiện tại là " + str(humidity) + "phần trăm")
            text  = ""
#def bashCommand(key):
#    command = "irsend SEND_ONCE Samsung_BN59-01175B " + key
#    process = subprocess.Popen(command, stdout=subprocess.PIPE)
#    output, error = process.communicate()
    # return(output)
def bashCommand(key):
    command = "irsend SEND_ONCE Samsung_BN59-01175B " + key
    process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return(output)    

def tts(textIn):
    language='vi'
    myobj=gTTS(text=textIn,lang=language,slow=False)
    myobj.save("soundtrack.mp3")
    file = "soundtrack.mp3"
    os.system("mpg123 " + file)

def selectQuery(query):
    conn = mysqll.connect(host = "localhost", user = "root", passwd = "123456", database = "IOT", port = 3306)
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data

# pushSignal(infraSwitcher.get("tivi"))
getCommand()
#publish_To_Topic("CyberLink/commands/1037600", "123123")

