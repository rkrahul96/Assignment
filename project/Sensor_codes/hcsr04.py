#code for distance sensor!!!
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import random
import datetime
import math
import urllib

host = "alx12a5wtaacx-ats.iot.us-east-1.amazonaws.com"
certPath = "/home/rahul/project/new-keys/"
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
url = "https://13x2x9xib5.execute-api.us-east-1.amazonaws.com/dev/vms/HCSR04"
response = urllib.urlopen(url)
data = json.loads(response.read())
total = data['Count']
curr_count = total + 1 
# Publish to the same topic in a loop forever
while True:
    dist=random.randint(0,500)
    message_3 = {}
    message_3['distance_btwn'] = dist
    message_3['unit'] = 'feet'
    message_3['device_id'] = "HCSR04"
    message_3['data_count'] = curr_count
    message_3['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d Time:%H:%M:%S")
    messageJson_3 = json.dumps(message_3)
    myAWSIoTMQTTClient.publish(topic, messageJson_3, 1)
    print('Published topic %s: %s\n' % (topic, messageJson_3))
    curr_count +=1
    time.sleep(10)
myAWSIoTMQTTClient.disconnect()

