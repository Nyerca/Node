PORT = 60002

#### DATABASE
DBHOST="AAAAAAAAA"
DBNAME="AAAAAAAAA"
DBUSER="AAAAAAAAA"
DBPASS="AAAAAAAAA"

#### Node table fallback
NODETBL_DEFAULT = "unified-node"

import traceback
import socket
import time
import threading
import struct
import re
import socketserver
import MySQLdb
import MySQLdb.cursors
from common import *

def dbConnect():
    dbconn = MySQLdb.connect( \
            host = DBHOST, db = DBNAME, \
            user = DBUSER, passwd = DBPASS, \
            cursorclass = MySQLdb.cursors.DictCursor, \
            autocommit = True)
    return dbconn

def insertNewID(id_sensor, name_sensor, interval_sensor, proj_id):
    dbConn = dbConnect()
    try:
        allProj = getAllProjects(dbConn)
        assocProj = getAssocProjects(dbConn, id_sensor, allProj)
        if len(assocProj) > 0:
            return
        print ("@ else " + str(proj_id))
        if proj_id in allProj:
            tbl_node = allProj[proj_id]["table_node"]
        else:
            tbl_node = NODETBL_DEFAULT
        # add node to the correct table
        sql = "INSERT INTO `%s` VALUES ('%d', '%s', '%d')" \
                %(tbl_node, id_sensor, str(name_sensor), interval_sensor)
        dbCursor = dbConn.cursor()
        print ("@>", sql)
        dbCursor.execute(sql)
        dbCursor.close()
    except MySQLdb.IntegrityError:
        pass
    finally:
        dbConn.close()

def getAllProjects(dbConn):
    global getAllProjectsCache, getAllProjectsCacheTS
    if 'getAllProjectsCacheTS' in globals() \
            and time.time() < getAllProjectsCacheTS+5:
        return getAllProjectsCache

    projs = {}
    sql = "SELECT * FROM `unified-proj`"
    print (">", sql)
    dbCursor = dbConn.cursor()
    count = dbCursor.execute(sql)
    for row in dbCursor:
        projs[row["id"]] = row
    dbCursor.close()

    getAllProjectsCache, getAllProjectsCacheTS = projs, time.time()
    return projs

def getAssocProjects(dbConn, id_sensor, projs=None):
    if projs is None:
        projs = getAllProjects(dbConn)

    ret = {}
    for pid in projs:
        sql = "SELECT `id` FROM `%s` WHERE `id`=%d" \
                %(projs[pid]["table_node"], id_sensor)
        print (">", sql)
        dbCursor = dbConn.cursor()
        count = dbCursor.execute(sql)
        dbCursor.close()
        if count > 0:
            ret[pid] = projs[pid]
    print ("@ ID: " + str(id_sensor) \
            + " Projects: " + ",".join([ ret[pid]["project"] for pid in ret ]))
    return ret

def processDataPkt(pkt):
    print ("Processing Data Packet")
    print ("")
    print ("#"*40)

    # Parsing headers
    data = {}
    data["node_id"], sidLen = decodeVarSize(pkt)
    print ("Sensor ID:", data["node_id"])
    start = sidLen
    end = start+8
    data["timestamp"] = struct.unpack("<Q",pkt[start:end])[0]
    if (data["timestamp"] == 0):  #ADD NEW ID
        print ("Timestamp 0 --> ADD NEW NODE ID")
        print ("Sensor: " + str(data["node_id"]) + " Project num: " + str((data["node_id"] % 10)))
        nodeName = "node" + str(data["node_id"])
        insertNewID(data["node_id"], nodeName, 5, data["node_id"] % 10)
        return True
    print ("Sample timestamp:", data["timestamp"] \
            , time.ctime(data["timestamp"]))

    start = end
    end = start+2
    pktLen = struct.unpack("<H",pkt[start:end])[0]
    print ("Packet length:", pktLen)
    if pktLen != len(pkt):
        print ("Error: Invalid packet length")
        return False

    # Collect all TLVs
    tlv = {}
    start = end

    while (start < len(pkt)-1):
        typeId,valLen,tlvLen = checkTLV(pkt[start:])
        tlv[typeId] = pkt[start : start+tlvLen]
        start += tlvLen

    if len(tlv) > 0:
        # Connect to database
        dbConn = dbConnect()
        try:
            # Query expected typeId from database
            datatype = {}
            sql = "SELECT * FROM `unified-type` WHERE `id` IN (%s)" \
                    %(",".join(map(str,tlv.keys())))
            print (">", sql)
            dbCursor = dbConn.cursor()
            count = dbCursor.execute(sql)
            for row in dbCursor:
                datatype[row["id"]] = row
            dbCursor.close()

            # Convert TLV to data
            for t in tlv:
                if t not in datatype:
                    print ("Warn: Undefined datatype", t)
                    continue
                field = datatype[t]["notes"]
                dtype = datatype[t]["datatype"]
                mult = datatype[t]["multiplier"]
                bias = datatype[t]["bias"]
                idType = datatype[t]["id"]
                #print "field: " + str(field)
                #print "dtype: " + str(dtype)
                #print "mult: " + str(mult)
                #print "bias: " + str(bias)
                #print "idType: " + str(idType)
                #print "tvl[t]: " + str(tlv[t])
                tid, value = parseTLV(tlv[t], dtype)
                #print "Value: " + str(value)
                if type(value) is str:
                    data[idType] = value
                else:
                    data[idType] = value * mult + bias
                #print "%s:"%(idType), value

            # Put the data into the database
            fields = []
            values = []
            upds = []
            for key in data:
                f = str(key)
                #f = "`%s`"%(key)
                v = data[key]
                if key=="timestamp" :
                    nodeTime = v;
                if key=="node_id" :
                    nodeID = v;
                if key=="timestamp" or key=="node_id":
                    continue
                fields.append(f)
                values.append(v)

            ## Finding which table to insert new data
            proj = getAssocProjects(dbConn, nodeID)
            nodeTables = [ proj[pid]["table_node"] for pid in proj]
            dataTables = [ proj[pid]["table_data"] for pid in proj]
            for tbl in dataTables:
                for i in range(len(fields)):
                    sql = "INSERT INTO `%s` (`node_id`,`server_timestamp`,`timestamp`,`type_id`,`value_num`, `value_str`)" \
                            %(tbl)
                    if type(values[i]) is str:
                        sql += " VALUES (%s,'%d',%s,%s,NULL,%s)"%(nodeID, time.time(), nodeTime, fields[i], values[i])
                    else:
                        sql += " VALUES (%s,'%d',%s,%s,%s,NULL)"%(nodeID, time.time(), nodeTime, fields[i], values[i])
                    print (">", sql)
                    dbCursor = dbConn.cursor()
                    try:
                        count = dbCursor.execute(sql)
                    except MySQLdb.IntegrityError as err:
                        #print ("DUPLICATE ENTRY: SENSOR " + str(nodeID) + " - TIMESTAMP " + str(nodeTime) + " -  TYPE " + str(fields[i]))
                        print (err)
                        pass
                    dbCursor.close()
        finally:
            dbConn.close()

        if count == 0:
            print ("Warn: Duplicated packet")
            return True
    else:
        print ("No data, this is a time sync request.")

    print ("#"*40)
    print ("")
    return True

def createConfPkt(rpkt):
    print ("Creating Configuration Packet")
    print ("")
    print ("#"*40)

    sid, sidLen = decodeVarSize(rpkt)
    print ("To Sensor:", sid)

    conf = {}
    datatype = {}
    # Conncet to database
    dbConn = dbConnect()
    try:
        proj = getAssocProjects(dbConn, sid)
        nodeTable = NODETBL_DEFAULT
        try:
            nodeTable = proj[proj.keys()[0]]["table_node"]
        except (IndexError, KeyError):
            pass
        # Query sensor configuration from database
        sql = "SELECT * FROM `%s` WHERE `id`='%d'"%(nodeTable, sid)
        print (">", sql)
        dbCursor = dbConn.cursor()
        count = dbCursor.execute(sql)
        colNames = [ desc[0] for desc in dbCursor.description ]
        row = dbCursor.fetchone()
        if row is not None:
            conf = row
        dbCursor.close()

        # Query id and datatype of the configuration
        fields = []
        for key in conf:
            fields.append("'%s'"%(key))
        if len(conf)>0:
            sql = "SELECT * FROM `unified-type` WHERE `notes` IN (%s)" \
                    %(",".join(fields))
            print (">", sql)
            dbCursor = dbConn.cursor()
            count = dbCursor.execute(sql)
            for row in dbCursor:
                datatype[row["notes"]] = row
            dbCursor.close()
    finally:
        dbConn.close()

    # Building packet
    pktHead = "\0" # server is 0x00
    pktHead += encodeVarSize(sid) # To sensor ID
    pktHead += struct.pack("<Q",int(time.time())) # Timestamp

    # Convert configuration to TLV
    pktData = ""
    for field in datatype:
        value = conf[field]
        if value is None:
            continue
        typeId = datatype[field]["id"]
        dtype = datatype[field]["datatype"]
        pktData += createTLV(typeId, value, dtype)
        print ("%s:"%(field), value)

    pktHead += struct.pack("<H",len(pktHead)+2+len(pktData)+1) # Pkt length

    pkt = pktHead + pktData
    pkt += getCRC(pkt)
    print ("#"*40)
    print ("")
    return (pkt)

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        addr = self.client_address
        rpkt = self.request[0]
        sock = self.request[1]
        try:
            print (time.time(), "Received", len(rpkt), "bytes from", addr)
            printHex(rpkt)
            if not checkCRC(rpkt):
                print (time.time(), "Wrong CRC")
                return
            if not processDataPkt(rpkt):
                print (time.time(), "Invalid packet")
                return
            spkt = createConfPkt(rpkt)
            if spkt is not None:
                print (time.time(), "Sending", len(spkt), "bytes to", addr)
                printHex(spkt)
                sock.sendto(spkt, addr)
        except Exception:
            print (time.time(), "Got an error:")
            traceback.print_exc()

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

if __name__=="__main__":
    server = ThreadedUDPServer(("", PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    try:
        server_thread.start()
        print (time.time(), "Server - start")
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        exit()

    #server = SocketServer.UDPServer(("", PORT), PktHandler)
    #print time.time(), "Server - start"
    #server.serve_forever()