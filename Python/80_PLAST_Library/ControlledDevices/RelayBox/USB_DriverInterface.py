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

#Ports command
PORT_ALL_OFF               =   0x00

PORT_ON_LOCAL_CLOSE        =   0x01
PORT_OFF_LOCAL_CLOSE       =   0x02

PORT_ON_LOCAL_OPEN         =   0x03
PORT_OFF_LOCAL_OPEN        =   0x04

PORT_ON_LOCAL_EXP_OPEN     =   0x05
PORT_OFF_LOCAL_EXP_OPEN    =   0x06

PORT_ON_LOCAL_EXP_CLOSE    =   0x07
PORT_OFF_LOCAL_EXP_CLOSE   =   0x08

PORT_ON_REMOTE_CLOSE       =   0x09
PORT_OFF_REMOTE_CLOSE      =   0x0A

PORT_ON_REMOTE_OPEN        =   0x0B
PORT_OFF_REMOTE_OPEN       =   0x0C

PORT_ON_REMOTE_EXP_OPEN    =   0x0D
PORT_OFF_REMOTE_EXP_OPEN   =   0x0E

PORT_ON_REMOTE_EXP_CLOSE   =   0x0F
PORT_OFF_REMOTE_EXP_CLOSE  =   0x10

PORT_PLANT_MODE_ON = 0x11
PORT_PLANT_MODE_OFF = 0x12


CommandStr = { \
PORT_ALL_OFF:"PORT_ALL_OFF",              
PORT_ON_LOCAL_CLOSE:"PORT_ON_LOCAL_CLOSE",
PORT_OFF_LOCAL_CLOSE:"PORT_OFF_LOCAL_CLOSE",
PORT_ON_LOCAL_OPEN:"PORT_ON_LOCAL_OPEN",
PORT_OFF_LOCAL_OPEN:"PORT_OFF_LOCAL_OPEN",
PORT_ON_LOCAL_EXP_OPEN:"PORT_ON_LOCAL_EXP_OPEN",
PORT_OFF_LOCAL_EXP_OPEN:"PORT_OFF_LOCAL_EXP_OPEN",
PORT_ON_LOCAL_EXP_CLOSE:"PORT_ON_LOCAL_EXP_CLOSE",
PORT_OFF_LOCAL_EXP_CLOSE:"PORT_OFF_LOCAL_EXP_CLOSE",
PORT_ON_REMOTE_CLOSE:"PORT_ON_REMOTE_CLOSE",
PORT_OFF_REMOTE_CLOSE:"PORT_OFF_REMOTE_CLOSE",
PORT_ON_REMOTE_OPEN:"PORT_ON_REMOTE_OPEN",
PORT_OFF_REMOTE_OPEN:"PORT_OFF_REMOTE_OPEN",
PORT_ON_REMOTE_EXP_OPEN:"PORT_ON_REMOTE_EXP_OPEN",
PORT_OFF_REMOTE_EXP_OPEN:"PORT_OFF_REMOTE_EXP_OPEN",
PORT_ON_REMOTE_EXP_CLOSE:"PORT_ON_REMOTE_EXP_CLOSE",
PORT_OFF_REMOTE_EXP_CLOSE:"PORT_OFF_REMOTE_EXP_CLOSE",
}.copy()

#object of CommandStr
ObjCommandStr = CommandStr.copy()

#port status
ALL_PORTS_OFF = 0x00
PORT_0_ON = 0x01
PORT_1_ON = 0x01 << 1
PORT_2_ON = 0x01 << 2
PORT_3_ON = 0x01 << 3
PORT_4_ON = 0x01 << 4
PORT_5_ON = 0x01 << 5
PORT_6_ON = 0x01 << 6
PORT_7_ON = 0x01 << 7

PortStatusStr = {\
# ALL_PORTS_OFF:"ALL_PORTS_OFF",                 
PORT_0_ON:"PORT_0_ON ",
PORT_1_ON:"PORT_1_ON ",
PORT_2_ON:"PORT_2_ON ",
PORT_3_ON:"PORT_3_ON ",
PORT_4_ON:"PORT_4_ON ",
PORT_5_ON:"PORT_5_ON ",
PORT_6_ON:"PORT_6_ON ",
PORT_7_ON:"PORT_7_ON ",                 
}.copy()

StatusMsgs = ['OK', 'INVALID_HANDLE', 'DEVICE_NOT_FOUND', 'DEVICE_NOT_OPENED',
        'IO_ERROR', 'INSUFFICIENT_RESOURCES', 'INVALID_PARAMETER',
        'INVALID_BAUD_RATE', 'DEVICE_NOT_OPENED_FOR_ERASE',
        'DEVICE_NOT_OPENED_FOR_WRITE', 'FAILED_TO_WRITE_DEVICE0',
        'EEPROM_READ_FAILED', 'EEPROM_WRITE_FAILED', 'EEPROM_ERASE_FAILED',
        'EEPROM_NOT_PRESENT', 'EEPROM_NOT_PROGRAMMED', 'INVALID_ARGS',
        'NOT_SUPPORTED', 'OTHER_ERROR']

def Wait(TimeVal, report = True):
    if report == True:
        print"Wait < %.3f > seconds"%TimeVal
    time.sleep(TimeVal)


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

def GetDeviceNameFromCFG(Section,Variable):
    try:
        DevName = cfg.get("SwitchBoxUSBDevName","USB_Dev_Name")
       # print "SwitchBoxUSBDevName " ,DevName, " connected."
        return DevName
    
    except Exception as ex:
        print "GetDeviceNameFromCFG error: " + str(ex)    
    
def USB_SendCommand(CommandReq):
    try:
        ftHandle = ft.FT_HANDLE()
        
        #ftStatus = ft.FT_Open(Device,ft.byref(ftHandle))
        DevSerial = str(GetDeviceNameFromCFG('SwitchBoxUSBDevName','USB_Dev_Name'))  ##"FTFWUCJ3"
        #debug
        #print"DevSerial name",DevSerial,type(DevSerial)        
        
        ftStatus = ft.FT_OpenEx(DevSerial,df.OPEN_BY_SERIAL_NUMBER,ft.byref(ftHandle))
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Open error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        
        ftStatus = ft.FT_SetDataCharacteristics(ftHandle, df.BITS_8, df.STOP_BITS_1, df.PARITY_NONE)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetDataCharacteristics error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
                
        ftStatus = ft.FT_SetFlowControl(ftHandle, df.FLOW_NONE, Xon, Xoff)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetFlowControl error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
                
        ftStatus = ft.FT_SetBaudRate(ftHandle,df.BAUD_38400)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetBaudRate error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))        
        
        ftStatus = ft.FT_Purge(ftHandle, df.PURGE_RX | df.PURGE_TX)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Purge error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))    
        
        bytesSend = ft.DWORD()
        TXBuff = (ft.c_uint8*1)(int(CommandReq))
        
        ftStatus = ft.FT_Write(ftHandle,TXBuff,ft.c_uint32(ft.sizeof(TXBuff)),ft.byref(bytesSend))            
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Write error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        print"<%s> send"%CommandStr.get(CommandReq)
        Wait(TimeWaitTransmit, False)       
        
        ftStatus = ft.FT_Close(ftHandle)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Close error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        
        pass
    except Exception as ex:
        print str(ex)
        raise
    finally:
        pass

def USB_GetUSBSwitchPortStatus():
    try:
        ftHandle = ft.FT_HANDLE()
        DevSerial = str(GetDeviceNameFromCFG('SwitchBoxUSBDevName','USB_Dev_Name'))
        ftStatus = ft.FT_OpenEx(DevSerial,df.OPEN_BY_SERIAL_NUMBER,ft.byref(ftHandle))
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Open error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        
        ftStatus = ft.FT_SetDataCharacteristics(ftHandle, df.BITS_8, df.STOP_BITS_1, df.PARITY_NONE)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetDataCharacteristics error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
                
        ftStatus = ft.FT_SetFlowControl(ftHandle, df.FLOW_NONE, Xon, Xoff)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetFlowControl error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
                
        ftStatus = ft.FT_SetBaudRate(ftHandle,df.BAUD_38400)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetBaudRate error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))  
        
        bytesSend = ft.DWORD()
        TXBuff = (ft.c_uint8*1)(int(DATA_REQUEST_COMMAND))
        
        ftStatus = ft.FT_Write(ftHandle,TXBuff,ft.c_uint32(ft.sizeof(TXBuff)),ft.byref(bytesSend))            
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Write error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        print"<%s> send"%DATA_REQUEST_COMMAND
        Wait(TimeWaitTransmit, False)       
        
        ReadTimeOut = ft.ULONG(200)
        ftStatus = ft.FT_SetTimeouts(ftHandle,ReadTimeOut,0)        
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetTimeouts error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
                
        RXBuff = (ft.c_uint8*1)()
        bytesReceived = ft.DWORD()        
        ftStatus = ft.FT_Read(ftHandle,RXBuff,ft.c_uint32(ft.sizeof(RXBuff)),ft.byref(bytesReceived))
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Read error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        print"bytesReceived = %d"%bytesReceived.value
        
        ftStatus = ft.FT_Close(ftHandle)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Close error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        
        return RXBuff
    except Exception as ex:
        print str(ex)
        raise
    finally:
        pass

def USB_ReadUSBData():
    try:
        ftHandle = ft.FT_HANDLE()
        DevSerial = str(GetDeviceNameFromCFG('SwitchBoxUSBDevName','USB_Dev_Name'))
        ftStatus = ft.FT_OpenEx(DevSerial,df.OPEN_BY_SERIAL_NUMBER,ft.byref(ftHandle))
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Open error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        
        ftStatus = ft.FT_SetDataCharacteristics(ftHandle, df.BITS_8, df.STOP_BITS_1, df.PARITY_NONE)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetDataCharacteristics error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
                
        ftStatus = ft.FT_SetFlowControl(ftHandle, df.FLOW_NONE, Xon, Xoff)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetFlowControl error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
                
        ftStatus = ft.FT_SetBaudRate(ftHandle,df.BAUD_38400)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetBaudRate error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))        
        
        ReadTimeOut = ft.ULONG(500)
        ftStatus = ft.FT_SetTimeouts(ftHandle,ReadTimeOut,0)        
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetTimeouts error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
                
        RXBuff = (ft.c_uint8*1)()
        bytesReceived = ft.DWORD()        
        ftStatus = ft.FT_Read(ftHandle,RXBuff,ft.c_uint32(ft.sizeof(RXBuff)),ft.byref(bytesReceived))
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Read error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        print"bytesReceived = %d"%bytesReceived.value
        
        ftStatus = ft.FT_Close(ftHandle)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Close error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        
        return RXBuff
    except Exception as ex:
        print str(ex)
        raise
    finally:
        pass

def GetPortStringStatus(PortStatusValue):
    StatusStr = ' '
    if PortStatusValue != ALL_PORTS_OFF:
        for items in PortStatusStr.keys():
            if PortStatusValue & items == items:
                StatusStr +=  PortStatusStr.get(items)
    else:
        StatusStr = "ALL_PORTS_OFF"
    return StatusStr
    
def USB_SendMultipleCommands(CommandReqList):
    try:
        ftHandle = ft.FT_HANDLE()
        DevSerial = str(GetDeviceNameFromCFG('SwitchBoxUSBDevName','USB_Dev_Name'))
        ftStatus = ft.FT_OpenEx(DevSerial,df.OPEN_BY_SERIAL_NUMBER,ft.byref(ftHandle))
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Open error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        
        ftStatus = ft.FT_SetDataCharacteristics(ftHandle, df.BITS_8, df.STOP_BITS_1, df.PARITY_NONE)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetDataCharacteristics error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
                
        ftStatus = ft.FT_SetFlowControl(ftHandle, df.FLOW_NONE, Xon, Xoff)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetFlowControl error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
                
        ftStatus = ft.FT_SetBaudRate(ftHandle,df.BAUD_38400)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_SetBaudRate error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))        
        
        ftStatus = ft.FT_Purge(ftHandle, df.PURGE_RX | df.PURGE_TX)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Purge error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))    
        
        bytesSend = ft.DWORD()
        TXBuff = (ft.c_uint8*1)()         
        
        for (Com,Slp) in CommandReqList:
            TXBuff[0] = int(Com)
            ftStatus = ft.FT_Write(ftHandle,TXBuff,ft.c_uint32(ft.sizeof(TXBuff)),ft.byref(bytesSend))            
            if ftStatus != ft.FT_OK:
                raise Exception("FT_Write error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
            print"<%s> send"%CommandStr.get(Com)
            Wait(Slp)       
        
        ftStatus = ft.FT_Close(ftHandle)
        if ftStatus != ft.FT_OK:
            raise Exception("FT_Close error....FT Status: %d : %s"%(ftStatus, StatusMsgs[ftStatus]))
        
        pass
    except Exception as ex:
        print str(ex)
        raise
    finally:
        pass

#if __name__ == '__main__':
# GetDevicesIdentification()
#    USB_SendCommand(PORT_ON_LOCAL_CLOSE)
#    Wait(0.5)
#    USB_SendCommand(PORT_OFF_LOCAL_CLOSE)

     
#    print hex(USB_GetUSBSwitchPortStatus()[0])
#     print GetPortStringStatus(USB_GetUSBSwitchPortStatus()[0])
#     print hex(USB_ReadUSBData()[0])
#     USB_SendCommand(0x00)
#     #USB_SendMultipleCommands([ (PORT_ON_OPEN_SWITCH, 1.3), (PORT_ON_CLOSE_SWITCH, 1.3), (PORT_OFF_CLOSE_SWITCH, 1.3), (PORT_OFF_OPEN_SWITCH, 1.3) ])
#GetDevicesIdentification()
