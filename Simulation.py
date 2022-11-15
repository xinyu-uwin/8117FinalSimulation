from flask import Flask, render_template
import datetime
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import screen_brightness_control as sbc
from livereload import Server


devices = {
				"lightBrightness": 0,  
				"curtainPer": 0,
				"temp": 20, 
				"heat": 0}	#0: cold, 1: heat

app = Flask(__name__)
@app.route("/")
def index():	
	return render_template("Simulation.html", devices = devices)

def customCallbackLight(client,userdata,message):
	data = json.loads(message.payload)
	# print("Data received from Server: ", data)
	time = datetime.datetime.now()

	username = data["username"]
	room_name = data["room_name"]
	print(">>> In room: " + room_name + " of user: " + username, end="\n")
	
	print(time, end=" ")
	light_on_percent = data["light-on"]
	if light_on_percent == 0:
		print("--- LIGHT TURNED OFF")
	else:
		print("--- LIGHT TURNED ON Percentage = ", light_on_percent)
	devices["lightBrightness"] = light_on_percent
	print("\n")


def customCallbackThermo(client,userdata,message):
	data = json.loads(message.payload)
	# print("Data received from Server: ", data)
	time = datetime.datetime.now()
	
	username = data["username"]
	room_name = data["room_name"]
	print(">>> In room: " + room_name + " of user: " + username, end="\n")

	print(time, end=" ")
	if data["heat"] == 1:
		devices["heat"] = 1
		devices["temp"] = data["temperature"]
		print("--- heater status = ON with Temperature = {}".format(data["temperature"]))
	elif data["cold"] == 1:
		devices["heat"] = 0
		devices["temp"] = data["temperature"]
		print("--- cooler status = ON with Temperature = {}".format(data["temperature"]))
	print("\n")


def customCallbackCurtain(client,userdata,message):
	data = json.loads(message.payload)
	# print("Data received from Server: ", data)
	time = datetime.datetime.now()

	username = data["username"]
	room_name = data["room_name"]
	print(">>> In room: " + room_name + " of user: " + username, end="\n")
	
	print(time, end=" ")
	curtain_open_percent = data["curtain-open"]
	if curtain_open_percent == 0:
		print("--- CURTAIN CLOSED")
	else:
		print("--- CURTAIN OPEN Percentage =", curtain_open_percent)
	devices["curtainPer"] = curtain_open_percent
	print("\n")
		


def devicesConnect():
	myMQTTClientLight = AWSIoTMQTTClient("light_bulb")
	myMQTTClientThermo = AWSIoTMQTTClient("thermostat")
	myMQTTClientCurtain = AWSIoTMQTTClient("curtain")
	myMQTTClientLight.configureEndpoint("a32yk77mbrevmu-ats.iot.us-east-2.amazonaws.com", 8883)
	myMQTTClientLight.configureCredentials("./AmazonRootCA1.pem","./private.pem.key", "./certificate.pem.crt")
	myMQTTClientThermo.configureEndpoint("a32yk77mbrevmu-ats.iot.us-east-2.amazonaws.com", 8883)
	myMQTTClientThermo.configureCredentials("./AmazonRootCA1.pem","./private.pem.key", "./certificate.pem.crt")
	myMQTTClientCurtain.configureEndpoint("a32yk77mbrevmu-ats.iot.us-east-2.amazonaws.com", 8883)
	myMQTTClientCurtain.configureCredentials("./AmazonRootCA1.pem","./private.pem.key", "./certificate.pem.crt")

	myMQTTClientLight.connect()
	print("Device light_bulb Connected to server!")
	myMQTTClientLight.subscribe("trigger/light_on",1,customCallbackLight)
	# print("Device light_bulb waiting for a trigger...\n")

	myMQTTClientThermo.connect()
	print("Device Thermostat Connected to server!")
	myMQTTClientThermo.subscribe("trigger/thermostat_update",1,customCallbackThermo)

	myMQTTClientCurtain.connect()
	print("Device Curtain Connected to server!")
	myMQTTClientCurtain.subscribe("trigger/curtain_open",1,customCallbackCurtain)	





if __name__ == "__main__":
	devicesConnect()
	app.run(debug=True)
	exit = input()





"""
devices = {
				"light":"off", 
				"lightBrightness": 0, 
				"curtain":"closed", 
				"curtainPer": 0,
				"temp": 20, 
				"thermoMode": "heat"}
				"""