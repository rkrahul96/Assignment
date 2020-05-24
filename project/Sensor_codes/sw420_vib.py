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
url = "https://13x2x9xib5.execute-api.us-east-1.amazonaws.com/dev/vms/SW420"
response = urllib.urlopen(url)
data = json.loads(response.read())
total = data['Count']
curr_count = total + 1
# Publish to the same topic in a loop forever
while True:
    vn = "TN05BC1234"
    bg = ["O+ve","A+ve","B+ve","A-ve","B-ve","O-ve","AB+ve","AB-ve"]
    list1 = ["mike","9876540123",bg[2],"Appolo123276"]
    list2 = ["vijay","9765900765",bg[1],"lifeline6424"]
    list3 = ["khan","9688800765",bg[5],"healthcare123276"]
    a = random.randint(1,30)
    url_s = "https://13x2x9xib5.execute-api.us-east-1.amazonaws.com/dev/vms/ADXL345"
    response = urllib.urlopen(url_s)
    data_s = json.loads(response.read())
    total_s = data_s['Count']
    recent_s = total_s - 1
    time_s = data_s['Items'][recent_s]['payload']['M']['timestamp']['S']
    speed = data_s['Items'][recent_s]['payload']['M']['speed']['N']
    if a==8:
        content = "IMPACT ALERT !!! THE VEHICLE {} HAS CRASHED, CONTACT INFORMATION - DRIVER_NAME: {} , EMERGENCY_NUMBER: {} , BLOOD_GROUP: {} , INSURANCE_NUMBER: {} .".format(vn,*list1)
    elif a==16:
        content = "IMPACT ALERT !!! THE VEHICLE {} HAS CRASHED, CONTACT INFORMATION - DRIVER_NAME: {} , EMERGENCY_NUMBER: {} , BLOOD_GROUP: {} , INSURANCE_NUMBER: {} .".format(vn,*list2)
    elif a==21:
        content = "IMPACT ALERT !!! THE VEHICLE {} HAS CRASHED, CONTACT INFORMATION - DRIVER_NAME: {} , EMERGENCY_NUMBER: {} , BLOOD_GROUP: {} , INSURANCE_NUMBER: {} .".format(vn,*list3)
    else:
        content = "The vehicle {} is traveling towards the destination with speed of {}kph and its location can be checked through our app".format(vn,speed)
    message_4 = {}
    message_4['monitoring'] = content
    message_4['device_id'] = "SW420"
    message_4['data_count'] = curr_count
    message_4['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d Time:%H:%M:%S")
    messageJson_4 = json.dumps(message_4)
    myAWSIoTMQTTClient.publish(topic, messageJson_4, 1)
    print('Published topic %s: %s\n' % (topic, messageJson_4))
    curr_count += 1
    time.sleep(10)
myAWSIoTMQTTClient.disconnect()

