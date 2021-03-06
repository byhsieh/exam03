import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
# MQTT broker hosted on local machine
mqttc = paho.Client()


# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev,9600,timeout=5)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x196\r\n".encode())
char = s.read(3)
print("Set MY 0x196.")
print(char.decode())

s.write("ATDL 0x296\r\n".encode())
char = s.read(3)
print("Set DL 0x296.")
print(char.decode())

s.write("ATID 0x4\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x4.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(4)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")

t=np.arange(0,20,1)
num=np.arange(0,20,1)
xbeenum=[]
count=0
x=[]
y=[]
z=[]
vxy=[]
sampletime=[]


while True:
    s.write("/Vel_Val/run\r".encode())
    line=s.read(6)
    print("read velocity:")
    print(line.decode())
    vxy.append(line)
    count=count+1
    time.sleep(0.1)
    if count==50 :
        break

'''  

s.write("/Vel_Val/run\r".encode())
numcount=s.read(3).decode()
print(numcount)


for i in range(0,int(numcount)):
    line=s.read(6)
    #print(line.decode())
    x.append(float(line.decode()))
for i in range(0,int(numcount)):
    line=s.read(6)
    #print(line.decode())
    y.append(float(line.decode()))
for i in range(0,int(numcount)):
    line=s.read(6)
    #print(line.decode())
    z.append(float(line.decode()))

for i in range(0,int(numcount)):
    line=s.read(6)
    print(line.decode())
    vxy.append(float(line.decode()))

for i in range(0,int(numcount)):
    line=s.read(6)
    print(line.decode())
    sampletime.append(float(line.decode()))

for i in range(0,19):
    num[i]=xbeenum[i+1]
    #print(num[i])

num[19]=2

plt.figure()
plt.plot(t,num)
plt.xlim((0,20))
plt.xlabel('timestamp')
plt.ylabel('number')
plt.title('# of collected data plot')
plt.show()
'''

# Settings for connection
host = "localhost"
topic= "velocity"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

#mesg = "S"+numcount
#mqttc.publish(topic, mesg)

'''
for i in range(0,int(numcount)):
    mesg = "X"+str(x[i])
    mqttc.publish(topic, mesg)
    print(mesg)
    time.sleep(0.1)
for i in range(0,int(numcount)):
    mesg = "Y"+str(y[i])
    mqttc.publish(topic, mesg)
    print(mesg)
    time.sleep(0.1)
for i in range(0,int(numcount)):
    mesg = "Z"+str(z[i])
    mqttc.publish(topic, mesg)
    print(mesg)
    time.sleep(0.1)
'''
for i in range(0,50):
    mesg = "V"+str(vxy[i])
    mqttc.publish(topic, mesg)
    print(mesg)
    time.sleep(0.1)
'''
for i in range(0,int(numcount)):
    mesg = "T"+str(sampletime[i])
    mqttc.publish(topic, mesg)
    print(mesg)
    time.sleep(0.1)
'''
mesg = "E27.14"
mqttc.publish(topic, mesg)
s.close()