import flask
import json
import urllib
from flask import render_template 
import time
import thread

app=flask.Flask(__name__)
app.config["DEBUG"]=True
url_dht = "https://13x2x9xib5.execute-api.us-east-1.amazonaws.com/dev/vms/DHT11"
url_accel = "https://13x2x9xib5.execute-api.us-east-1.amazonaws.com/dev/vms/ADXL345"
url_imp = "https://13x2x9xib5.execute-api.us-east-1.amazonaws.com/dev/vms/SW420"
url_sonic = "https://13x2x9xib5.execute-api.us-east-1.amazonaws.com/dev/vms/HCSR04"
dht = {}
accel = {}
imp = {}
sonic = {}
@app.route('/', methods=['GET'])
def home():
    print("home function run ")
    return "<h1>VMS-IoT Application</h1><p>This site is a prototype API for Vehicle Monitoring System IoT Product </p>"
@app.route('/VMS-IOT', methods=['GET'])
def func():
    print("fuct run")
    while True:
        #DHT data sorting
        response = urllib.urlopen(url_dht)
        data_dht = json.loads(response.read())
        #print data  
	#print (data.keys())
	#print (data.values())
        total_dht = data_dht['Count']
        #print("Total number of DHT11 datas: {}".format(total_dht))
        recent_dht = total_dht - 1
        time_dht = data_dht['Items'][recent_dht]['payload']['M']['timestamp']['S']   
        tempc = data_dht['Items'][recent_dht]['payload']['M']['temperatureC']['N']
        tempf = data_dht['Items'][recent_dht]['payload']['M']['temperatureF']['N']
        hum = data_dht['Items'][recent_dht]['payload']['M']['humidity']['N']
        #DHT data to HTML
        dht['TEMPERATURE in Celsius:'] = tempc
        dht['TEMPERATURE in Farenheit:'] = tempf
        dht['Humidity in % :'] = hum
        dht['Recorded Time :'] = time_dht
        #accelerometer data sorting
        response = urllib.urlopen(url_accel)
        data_accel = json.loads(response.read())
        total_accel = data_accel['Count']
        #print("Total number of ADXL345 datas: {}".format(total_accel))
        recent_accel = total_accel - 1
        time_accel = data_accel['Items'][recent_accel]['payload']['M']['timestamp']['S']   
        speed = data_accel['Items'][recent_accel]['payload']['M']['speed']['N']
        #ADXL345 Data to HTML
        accel['SPEED in KPH'] = speed
        accel['Recorded Time :'] = time_accel
        #SW420 impact sensor  data sorting
        response = urllib.urlopen(url_imp)
        data_imp = json.loads(response.read())
        total_imp = data_imp['Count']
        #print("Total number of SW420 datas: {}".format(total_imp))
        recent_imp = total_imp - 1
        time_imp = data_imp['Items'][recent_imp]['payload']['M']['timestamp']['S']   
        impact = data_imp['Items'][recent_imp]['payload']['M']['monitoring']['S']
        #SW420 Data to HTML
        imp['Watching :'] = impact
        imp['Recorded Time :'] = time_imp
        #HCSR04 ultra sonic sensor  data sorting
        response = urllib.urlopen(url_sonic)
        data_sonic = json.loads(response.read())
        total_sonic = data_sonic['Count']
        #print("Total number of HCSR04 datas: {}".format(total_sonic))
        recent_sonic = total_sonic - 1
        time_sonic = data_sonic['Items'][recent_sonic]['payload']['M']['timestamp']['S']   
        distance = data_sonic['Items'][recent_sonic]['payload']['M']['distance_btwn']['N']
        #HCSR04 Data to HTML
        sonic['Feet to CRASH '] = distance
        sonic['Recorded Time :'] = time_sonic
        return render_template('index.html', result1 = dht , result2 = accel , result3 = imp , result4 = sonic)
if __name__ == '__main__':
    print("if function")
    app.run(host = '0.0.0.0')
	
print("Application Stopped...!! ")
	
