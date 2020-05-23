from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import random
import datetime
import urllib

host = "alx12a5wtaacx-ats.iot.us-east-1.amazonaws.com"
certPath = "/home/rahul/IOT/trial/new-keys/"
clientId = "RaspberryPi"
topic = "raspberrypi/data"

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials("{}root-CA.pem".format(certPath), "{}private-key.pem.key".format(certPath), "{}iot-cert.pem.crt".format(certPath))

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

#code to sync the data count with the db
url = "https://13x2x9xib5.execute-api.us-east-1.amazonaws.com/dev/vms/DHT11"
response = urllib.urlopen(url)
data = json.loads(response.read())
total = data['Count']
curr_count = total + 1
# Publish to the same topic in a loop forever
while True:
    temp_data = random.randint(30,40)
    temp_faren = temp_data * 9/5 + 32
    hum_data = random.randint(30,60)
    message_1 = {}
    message_1['temperatureC'] = temp_data
    message_1['temperatureF'] = temp_faren
    message_1['humidity'] = hum_data
    message_1['device_id'] = "DHT11"
    message_1['data_count'] = curr_count
    message_1['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d Time: %H:%M:%S")
    messageJson_1 = json.dumps(message_1)
    myAWSIoTMQTTClient.publish(topic, messageJson_1, 1)
    print('Published topic %s: %s\n' % (topic, messageJson_1))
    curr_count += 1
    time.sleep(60)
myAWSIoTMQTTClient.disconnect()

