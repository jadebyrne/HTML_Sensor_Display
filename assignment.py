import fcntl, socket, struct, dweepy, time, platform, random
from grovepi import *
import math

dht_sensor_port = 7
button = 2
buzzer_pin= 4

pinMode(button, "INPUT")
pinMode(buzzer_pin,"OUTPUT")
def getTemp():
    #return random.randint(1,1000)
    try:
        [temp, hum] = dht(dht_sensor_port, 0)
        print "temp = ", temp, "C\thumadity =", hum, "%"
        if math.isnan(temp):
            temp = 0
        return float(temp)
    
    except (IOError, TypeError) as e:
        print "Error"
        
def getHumidity():
    try:
        [temp, hum] = dht(dht_sensor_port, 0)
        if math.isnan(hum):
            hum = 0
        return float(hum)
    
    except (IOError, TypeError) as e:
        print "Error"
    
def getButAndBuz():
    try:
        button_status = digitalRead(button)
        if button_status:
            digitalWrite(buzzer_pin,1)
            return 1
        else:
            digitalWrite(buzzer_pin,0)
            return 0
    except KeyboardInterrupt:
        digitalWrite(buzzer_pin,0)
        
    except (IOError,TypeError) as e:
        print "Error"
        

    
def getOS():
    return platform.platform()
    
# from http://stackoverflow.com/questions/159137/getting-mac-address
def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

def post(dic):
    thing = 'Jade Byrne'
    print dweepy.dweet_for(thing, dic)
    
def getReadings():
    dict = {}
    dict["Button"] = getButAndBuz();
    dict["temperature"] = getTemp();
    #dict["Hight"] = getHight();
    #dict["mac-address"] = getHwAddr('eth0')
    dict["humidity"] = getHumidity()
    dict["operating system"] = getOS()
    return dict

while True:
    dict = getReadings();
    post(dict)
    time.sleep(5)
