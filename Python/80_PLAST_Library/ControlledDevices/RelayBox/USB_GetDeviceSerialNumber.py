'''
Created on Nov 11, 2013

@author: uidl9535
'''
import time, os
import serial
import ConfigParser
import sys
import usb.core

cfg = ConfigParser.RawConfigParser()
cfg.read(os.environ['PLAST_WA_PATH'] + "CONFIGURATION.cfg")


#ftd2xx lib original name "ftd2xx-git1-py2.6.egg" was replaced with ftd2xx
try:
    import sys,os
    if not os.getcwd()+'\_ftd2xx' in sys.path:
        sys.path.append(os.getcwd()+'\_ftd2xx')
    if  not os.getcwd()+'\defines' in sys.path:
        sys.path.append(os.getcwd()+'\defines')
    import _ftd2xx as ft
    import defines as df
except Exception as Ex:

    print str(Ex)
finally:
    pass 

#device nb
Device  = 0
Xon     = 0x11
Xoff    = 0x13
#wait this time after command was send
TimeWaitTransmit          = 0.05

#request commands for test
ENABLE_TX_COMMAND         = 77
DATA_REQUEST_COMMAND      = 33
DISABLE_TX_COMMAND        = 99

#utility to obtain device serial nb, description, etc
def GetDevicesIdentification():
    numDevs = ft.DWORD()
    devInfo = ft.POINTER(ft.FT_DEVICE_LIST_INFO_NODE)
    devTypeName = ["FT_DEVICE_BM","FT_DEVICE_AM","FT_DEVICE_100AX","FT_DEVICE_UNKNOWN","FT_DEVICE_2232C","FT_DEVICE_232R"]
    try:        
        ftStatus = ft.FT_CreateDeviceInfoList(ft.byref(numDevs))
        if ftStatus != ft.FT_OK:
            raise Exception("FT_CreateDeviceInfoList error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))

        if numDevs.value == 0:
            raise Exception("No USB device found. numDevs = %d"%numDevs.value)
        
        devInfo = ft.cast(ft.create_string_buffer( ft.sizeof(ft.FT_DEVICE_LIST_INFO_NODE) * numDevs.value),ft.POINTER(ft.FT_DEVICE_LIST_INFO_NODE) )
        if devInfo == None:
            raise Exception("Cannot alocate memory for devinfo buffer")
        
        ftStatus = ft.FT_GetDeviceInfoList(devInfo,ft.byref(numDevs))
        if ftStatus != ft.FT_OK:
            raise Exception("FT_GetDeviceInfoList error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        
        for dv_idx in range(0,numDevs.value):
            print"Dev nb            : %d  "%dv_idx
            print"Dev flags         : 0x%x"%devInfo[dv_idx].Flags
            print"Dev type          : 0x%x \t : %s"%(devInfo[dv_idx].Type,devTypeName[devInfo[dv_idx].Type])
            print"Dev ID            : 0x%x"%devInfo[dv_idx].ID
            print"Dev LocId         : 0x%x"%devInfo[dv_idx].LocId
            print"Dev SerialNumber  : %s  "%devInfo[dv_idx].SerialNumber
            print"Dev Description   : %s  "%devInfo[dv_idx].Description
            print "\n"
        pass
    except Exception as ex:
        print str(ex)
        raise
    finally:
        pass

GetDevicesIdentification()