'''
Created on Oct 05, 2015

@author: uidj6652
'''

import UltraDbg
import UltraDbg.Projects.PowerClosures_LIN_Platform

import time, os
import ConfigParser
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add the Workspace directory to PATH
sys.path.append('\\'.join(os.path.dirname(__file__).split('\\')[:-1])) # line required because path is a symlink - it only adds the root SWT directory to path

cfg = ConfigParser.RawConfigParser()
cfg.read(os.environ['PLAST_WA_PATH'] + "CONFIGURATION.cfg")


def LINComInstance():
    device = cfg.get("LIN_COMMUNICATION","device") 
    if (device == "VECTOR"):
        InstanceLIN = generateLINObject("VECTOR")
    elif(device == "TUF"):
        InstanceLIN = generateLINObject("TUF")
    else:
        print "Device not supported"
    if not InstanceLIN.isConnected():
        try:
            InstanceLIN.connect()
        except:
            print "No communication device to connect or duplicate connection"
    time.sleep(0.5)
    return InstanceLIN

def generateLINObject(device):
    # LDF file address
    ldffile = cfg.get("LIN_COMMUNICATION","ldf_file")
    ldfDataLin=open(ldffile).read()
    # Schedule tables
    scheduleListLin = (cfg.get("LIN_COMMUNICATION","scheduleList")).split() #convert string to list
    # Name of diagnostic LIN node
    diagNodeLin = cfg.get("LIN_COMMUNICATION","diagNode")
    # Connected diagnostic LIN node
    userNADLin = int(cfg.get("LIN_COMMUNICATION","userNAD"),16) #convert string to int
    # Schedule Mode
    scheduleModeLin = int(cfg.get("LIN_COMMUNICATION","scheduleMode"))
    # Simulated LIN slaves
    slaveListLin = (cfg.get("LIN_COMMUNICATION","slaveList")).split() #convert string to list
    
    if (device == "TUF"):
        # Instance of TUF
        TUFLin = UltraDbg.Com.TUF()
        obj = UltraDbg.Com.LIN(ldfData=ldfDataLin,TUF=TUFLin,scheduleMode=scheduleModeLin,userNAD=userNADLin,diagNode=diagNodeLin,scheduleList=scheduleListLin,slaveList=slaveListLin)
    elif(device == "VECTOR"):
        # Vector HW
        obj = UltraDbg.Com.LIN(ldfData=ldfDataLin,scheduleMode=scheduleModeLin,userNAD=userNADLin,diagNode=diagNodeLin,scheduleList=scheduleListLin,slaveList=slaveListLin)
    return obj
 
'''USAGE EXEMPLE 1

def test():
    #LIN communication instance
    LinCom = LINComInstance()

    # Set LIN signals
    LinCom.setSignal("ig1",0x01)    
    LinCom.setSignal("ig2",0x01)
    LinCom.setSignal("key_off_timer",0x01)
    time.sleep(1)
    
    # Send diagnostics message
    (status, response) = LinCom.diagMessage([0x19, 0x02, 0x7f], True)
    
    print "Response lenght:",len(response),"bytes"
    
    # Response is byte array type
    for by in response:
        print hex(by)," ",
    print ""
    
    #Print one byte from the response 
    print hex(response[0])
    
    #Disconnect LIN communication
    LinCom.disconnect();    #very important to disconnect, otherwise another LinCom instance won't work

test()

'''

'''USAGE EXEMPLE 2

def test02(testcase): 
    testcase.time_begin = time.ctime(time.time())
    testcase.description = "Test localSwitch_task call"  
    testcase.safety_requirement = "No" 

    try:
        LinCom = LINComInstance()

        ### TEST BODY

        testcase.time_end = time.ctime(time.time())
        LinCom.disconnect();   #very important to disconnect, otherwise another LinCom instance won't work
    except:
        LinCom.disconnect();   #very important to disconnect, otherwise another LinCom instance won't work
        print "Test error"
        testcase.result = ERROR
        testcase.time_end = time.ctime(time.time()) 
'''