SPOOLDIRROOT = "/home/udooer/spool/"
INTERVALFILE = "/home/udooer/script/interval.conf"

PORT = 60002
SERVERADDRS = ["show.me.the.error","canarin.net","23.23.174.61"]
#SERVERADDRS = ["canarin.net","23.23.174.61"]
#SERVERADDR = "127.0.0.1"
#SERVERADDR = "23.23.174.61"
#SERVERADDR = "canarin.net"
#SERVERADDR ="192.168.1.153"

SENSOR_ID = 42
PROJECT_ID = 2

TIMEOUT = 5 # seconds

### Field/Value datatype (fieldId:datatype)
ID2TYPE = {}
ID2TYPE[0] = "B" # interval(conf) T=0 u_int8
ID2TYPE[1] = "f" # latitude       T=1 float(4)
ID2TYPE[2] = "f" # longtitude     T=2 float(4)
ID2TYPE[3] = "h" # altitude       T=3 int16
ID2TYPE[4] = "h" # temperature    T=4 int16
ID2TYPE[5] = "H" # humidity       T=5 u_int16
ID2TYPE[6] = "H" # air pressure   T=6 u_int16
ID2TYPE[7] = "H" # pm2.5          T=7 u_int16
ID2TYPE[8] = "H" # pm10           T=8 u_int16
ID2TYPE[9] = "H" # pm1.0          T=9 u_int16
ID2TYPE[10] = "H" # batt volt.    T=10 u_int16
ID2TYPE[11] = "f" # formaldehyde  T=11 float(4)
ID2TYPE[12] = "255s" # status  
ID2TYPE[15] = "H" # no2           T=15 u_int16

### File endings (endfix) to type id
ENDFIX2ID = {}
ENDFIX2ID["glat"] = 1
ENDFIX2ID["glng"] = 2
ENDFIX2ID["galt"] = 3
ENDFIX2ID["temp"] = 4
ENDFIX2ID["humi"] = 5
ENDFIX2ID["pres"] = 6
ENDFIX2ID["pm25"] = 7
ENDFIX2ID["pm10"] = 8
ENDFIX2ID["pm1"] = 9
ENDFIX2ID["form"] = 11
ENDFIX2ID["status"] = 12
ENDFIX2ID["no2"] = 15

import traceback
import socket
import time
import struct
import os
import re
import sys
from common import *
import sys
from random import randint


server = None
oldTime = 42701 #beginning of epoch, 1970/01/01
#fileToDel =[]

split0 = ""
split1 = ""
split2 = ""
split3 = ""

Linux2ServerExceptionFile="/home/udooer/script/Linux2ServerException.txt"

def readDataFile(filepath):
    value = {}
    # reverse split "123456790.endfix" ==> "endfix"
    endfix = filepath.rsplit(".",1)[-1]
    if endfix in ENDFIX2ID:
        # open file
        with open(filepath, "r") as f:
            val = f.read() #read full file
            # ## old
            # val = val.strip() #remove junk characters (\r, \n, tab or space)
            # val = float(val) #convert to number, doesnt care if it is 'int'
            # value[endfix] = val

            # ## new
            splitted = val.split("*")
            split0 = splitted[0]
            split1 = splitted[1]
            split2 = splitted[2]
            split3 = splitted[3]
            print ("SENDING" + " " + split0 + " " + split1 + " " + split2 + " " + split3)
            value["glat"] = float(splitted[0])
            value["glng"] = float(splitted[1])
            value["galt"] = float(splitted[2])
            if re.search('[a-zA-Z]', splitted[3]) is not None:
                #print "STRING: " + splitted[3]
                value[endfix] = splitted[3]
            else:
                #print "ELSE: " + str(float(splitted[3]))
                value[endfix] = float(splitted[3])
    return value

def createDataPkt(filepath, value):
    print ("Creating New Data Packet")
    head = encodeVarSize(long(str(SENSOR_ID)+str(PROJECT_ID))) # begin encoding with SENSOR_ID
    fullPathNoExt = filepath.rsplit(".",1)[0]
    fileNameNoExt = fullPathNoExt.rsplit("/",1)[-1]
    head += struct.pack("<Q",int(fileNameNoExt)) # Timestamp

    data = ""
    for endfix in value:
        # use dictionary
        tlvId   = ENDFIX2ID[endfix]
        tlvType = ID2TYPE[tlvId]
        tlvValue = value[endfix]
        #if tlvType == 's':
        #    tlvType = '' + str(len(tlvValue)) + 's'
        #    print "TLV CAMBIATO in " + str(tlvType)
        #print "INVIO" + " " + str(tlvId) + " " + str(tlvType) + " " + str(tlvValue)

        data += createTLV(tlvId, tlvValue, tlvType)
    # dummy data.                   # see "ID2TYPE" at very first line
    #data += createTLV(1, 48.834567, ID2TYPE[1]) # lat   T=1 float(4)
    #data += createTLV(2, 2.356789, ID2TYPE[2])  # lng   T=2 float(4)
    #data += createTLV(3, 12, ID2TYPE[3])        # alt   T=3 int16
    #data += createTLV(4, 252, ID2TYPE[4])       # temp  T=4 int16
    #data += createTLV(5, 303, ID2TYPE[5])       # humid T=5 u_int16
    #data += createTLV(6, 10001, ID2TYPE[6])     # pressure T=6 int16
    #data += createTLV(7, value["pm25"], ID2TYPE[7])
    #data += createTLV(8, 4, ID2TYPE[8])
    #data += createTLV(9, 3, ID2TYPE[9])
    #data += createTLV(10, 4123, ID2TYPE[10])
    #data += createTLV(20, 9999, "H") ## test undefined data

    head += struct.pack("<H",len(head)+2+len(data)+1) # Packet length

    pkt = head + data
    pkt += getCRC(pkt)

    # print(pkt)
    return pkt

def createHelloPkt():
    print ("Creating Hello Packet with ID " + str(SENSOR_ID)+str(PROJECT_ID))
    head = encodeVarSize(long(str(SENSOR_ID)+str(PROJECT_ID))) # begin encoding with SENSOR_ID
    head += struct.pack("<Q",0) # Special Timestamp in order to add a new SensorID
    data = struct.pack("<B", ord('|'))
    head += struct.pack("<H",len(head)+2+len(data)+1) # Packet length
    pkt = head + data
    pkt += getCRC(pkt)
    return pkt

def processConfPkt(pkt):
    global interval, nextSampling
    print ("Processing Configuration Packet")
    if ord(pkt[0]) != 0:
        print ("Error: Packet is not from server.", ord(pkt[0]))
        return False
    sid, sidlen = decodeVarSize(pkt[1:])
    if sid != long(str(SENSOR_ID)+str(PROJECT_ID)):
        print ("Error: Packet is not for me.", sid)
        return False
    print ("#"*40)
    start = 1+sidlen
    end = start+8
    ts = struct.unpack("<Q",pkt[start:end])[0]
    print ("Server timestamp:",ts)
    start = end
    end = start+2
    length = struct.unpack("<H",pkt[start:end])[0]
    print ("Packet length:",length)
    if length!=len(pkt):
        print ("Error: Invalid packet length")
        return False

    # Find config
    start = end
    while (start<len(pkt)-1):
        typeId,valLen,tlvLen = checkTLV(pkt[start:])
        if typeId==0:
            # found interval (T=0)
            typeId,value = parseTLV(pkt[start:], ID2TYPE[0])
            print ("Interval(min):",value)
            # write interval configuration: to BE READ BY arduLinuxScript and written to serial
            while is_locked(INTERVALFILE):
                time.sleep(1)
            with open(INTERVALFILE, "w") as f:
                f.write(str(value))
                f.flush()
                os.fsync(f.fileno())
            # FYI: file is closed when exiting the "with" block
        else:
            print ("Warn: Undefined type found:", typeId)
        start += tlvLen
    print ("#"*40)
    return True

#def fireAckReceived():
#    # delete all the files after the ack for that file is received
#    global fileToDel
#    for filename in fileToDel:
#
#
#    fileToDel = [] #clean the array

def sendData_recvConf(filepath):
    # Comparing string in python is fast (it uses hashing)
    todo = "send"
    spkt = None
    while todo != "done":
        if todo == "send":
            if spkt is None:#if already timeout, means already computed
                value = readDataFile(filepath)
                spkt = createDataPkt(filepath,value)
                ############################################### if(randint(0,4) == 3):
                ###############################################    spkt = createHelloPkt();

            print (int(time.time()), "Sending")
            sock.sendto(spkt, server) #blocking but fast, only UDP
            #sendto used in UDP, no need to connect to remote server, just send packet
            todo = "recv"

        elif todo == "recv":
            rpkt = None
            try:
                print (int(time.time()), "Receiving for", TIMEOUT, "sec.")
                rpkt, saddr = sock.recvfrom(1500) #saddr is address of sender, needed, but not used in practice
                # 1500 is buffer size, maximum transmission unit (MTU)
            except socket.timeout:
                # If timeout
                print (int(time.time()), "Timeout")
                todo = "send"
                sys.exit()
                # only resend packet on timeout
                # so it wont overload the server

            print (int(time.time()), "Received a packet")
            if not checkCRC(rpkt):
                print (time.time(), "Wrong CRC")
                todo = "recv"
                continue

            if not processConfPkt(rpkt):
                print (time.time(), "Invalid packet")
                todo = "recv"
                continue

            print (int(time.time()), "Processing done")
            # delete the file
            os.remove(filepath)
            spkt = None
            todo = "done"

def is_locked(filepath):
    """Checks if a file is locked by opening it in append mode.
    If no exception thrown, then the file is not locked.
    """

    locked = None
    file_object = None
    if os.path.exists(filepath):
        try:
            # print "Trying to open %s." % filepath
            buffer_size = 1
            # Opening file in append mode and read the first character.
            file_object = open(filepath, 'a', buffer_size)
            if file_object:
                # print "%s is not locked." % filepath
                locked = False
        except IOError:
                print ("File is locked (unable to open in append mode). %s." % message)
                locked = True
        finally:
            if file_object:
                file_object.close()
                # print "%s closed." % filepath
    else:
        print ("%s not found." % filepath)
    return locked

def processFile(filepath):
    """
    Function that works on every file on the current list
    """
    if not is_locked(filepath):
        sendData_recvConf(filepath)

def main():
    global sock, server

    pid_file = 'Linux2Server.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        # another instance is running
        sys.exit(0)

    sensF = open('/home/udooer/script/myID.txt', 'r')
    global SENSOR_ID
    SENSOR_ID = int(sensF.read())
    sensF.closed

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # AF_INET --> specify a (host,port) pair
    # SOCK_DGRAM --> datagram, UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # other options?? Preechai why u not comment
    # SO_REUSEADDR --> reuse address
    # Calm down
    # These lines are just a common way to create UDP socket. Its the same as the other programing languages

    # Set socket timeout: How long we can wait when sending/receiving
    sock.settimeout(TIMEOUT)

    if not os.path.exists(SPOOLDIRROOT):
        os.makedirs(SPOOLDIRROOT)

    # reason about putting a delay here of some minutes in order not to have a false positive the first time
    time.sleep(5)

### Check the address by order in the SERVERADDRS list
    testsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for address in SERVERADDRS:
        server = (address,PORT)
        #print "Trying address", address,"...",
        try:
            testsock.connect(server)
            testsock.close()
            #print "OK!"
            break
        except (socket.gaierror, socket.error) as sock_err:
            if(sock_err.errno == socket.errno.ENETUNREACH):
                sys.exit(0)
            #print "Error:", address,"is not available."
            if address == SERVERADDRS[-1]:
                #print "ERROR: cannot use any address, exiting."
                sys.exit(0)
            continue

### HELLO PACKET
    hlpkt = createHelloPkt();
    sock.sendto(hlpkt, server) #blocking but fast, only UDP

    #while True:
    try:
        for directory in sorted(os.listdir(SPOOLDIRROOT), reverse=True):   # for every directory in the SPOOLDIRROOT, one for each day
            if os.path.isdir(SPOOLDIRROOT+directory):            # if it is really a directory
                for fileName in sorted(os.listdir(SPOOLDIRROOT+directory), reverse=True)[:300]: # for every file in this directory
                    #create a list of the current file names in the directory
                    print ("PROCESSING: "+SPOOLDIRROOT+directory+"/"+fileName)
                    processFile(SPOOLDIRROOT+directory+"/"+fileName)
    except Exception:
        # catch all error so the program won't break when error
        # print time.time(), "Got an error in Linux2Server script:"
        # traceback.print_exc()

        # change to this
        print ("EXCEPTION" + " " + split0 + " " + split1 + " " + split2 + " " + split3)
        tb = traceback.format_exc()
        tbFile = open(Linux2ServerExceptionFile, 'a+')
        tbFile.write(tb)
        tbFile.flush()
        os.fsync(tbFile.fileno())
        tbFile.close()

if __name__=="__main__":
    main()
