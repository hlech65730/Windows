'''
Created on Apr 15, 2015

@author: uidv9994
'''
'''
USAGE EXEMPLE

ps=PowerSourceInstance()
 
ps.OpenPort()
ps.PrintPortConfiguration()
ps.SetVoltage(12,3)
ps.SetCurrent(2.5,3)
  
ps.SetVoltage(6.5,2)
ps.SetCurrent(2,2)
  
ps.SetVoltage(15,3)
ps.SetCurrent(10,3)
  
ps.SetOutputON(3)
time.sleep(1)
ps.SetOutputOFF(1)
 
ps.SetOutputON(2)
time.sleep(1)
ps.SetOutputOFF(2)
  
ps.SetOutputON(3)
time.sleep(1)
ps.SetOutputOFF(3)
 
print ps.GetVoltage(3)
time.sleep(0.11)
print ps.GetVoltageSetted(3)
time.sleep(0.11)
print ps.GetCurrent(3)
time.sleep(0.11)
print ps.GetCurrentSetted(3)
 
ps.Reset()
time.sleep(1)
ps.SetOutputOFF(1) 
ps.ClosePort()
print "Done"

'''

import time, os
import serial
import ConfigParser
import sys,os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add the Workspace directory to PATH
sys.path.append('\\'.join(os.path.dirname(__file__).split('\\')[:-1])) # line required because path is a symlink - it only adds the root SWT directory to path
# POWER SUPPLIES
from ControlledDevices.PowerSources.PS_HAMEG_HMP                       import *
from ControlledDevices.PowerSources.PS_KONSTANTER_SSP                  import *
from ControlledDevices.PowerSources.PS_LAB_SM                          import *
from ControlledDevices.PowerSources.PS_SYSKON                          import *
from ControlledDevices.PowerSources.PS_TDK_LAMBDA                      import *

# SIGNAL GENERATORS
from ControlledDevices.SignalGenerators.SG_HAMEG_HMF                   import *

# SMS
from ControlledDevices.SimpleMechanicsSimulator.SMS                    import *

#USB RelayBox
from ControlledDevices.RelayBox.USB_DriverInterface                    import *

cfg = ConfigParser.RawConfigParser()
cfg.read(os.environ['PLAST_WA_PATH'] + "CONFIGURATION.cfg")

class PowerSourceInstance:
    def __init__(self):
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            self.ps = HamegHMPPowerSource()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            self.ps = TDKLambdaPowerSource()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            self.ps = KonstanterSSPPowerSource()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            self.ps = SyskonPowerSource()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            self.ps = LABSMPowerSource()
            
    def OpenPort(self):
        '''
            Open serial port.
        '''
        self.ps.OpenPort()
        
    def ClosePort(self):
        '''
            Close serial port.
        '''
        self.ps.ClosePort()
        
    def PrintPortConfiguration(self):
        '''
            Print serial connection settings.
        '''
        self.ps.PrintPortConfiguration()
        
    def SetVoltage(self, volts, channel = 1):
        '''
            Sets the output voltage value in Volts.
        '''
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            self.ps.SetVoltage(volts, channel)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            self.ps.SetVoltage(volts)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            self.ps.SetVoltage(volts)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            self.ps.SetVoltage(volts)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            self.ps.SetVoltage(volts)

    def SetCurrent(self, amperes, channel = 1):
        ''' 
            Sets the Output Current value in Amperes.
        '''
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            self.ps.SetCurrent(amperes, channel)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            self.ps.SetCurrent(amperes)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            self.ps.SetCurrent(amperes)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            self.ps.SetCurrent(amperes)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            self.ps.SetCurrent(amperes)
        
    def SetOutputON(self, channel = 1):
        ''' 
            Turns the output to ON.
        '''
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            self.ps.SetOutputON(channel)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            self.ps.SetOutputON()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            self.ps.SetOutputON()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            self.ps.SetOutputON()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            self.ps.SetOutputON()
         
    def SetOutputOFF(self, channel = 1):
        ''' 
            Turns the output to OFF. 
        '''
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            self.ps.SetOutputOFF(channel)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            self.ps.SetOutputOFF()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            self.ps.SetOutputOFF()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            self.ps.SetOutputOFF()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            self.ps.SetOutputOFF()
            
    def Reset(self):
        '''Resets the device parameters'''         
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            self.ps.Reset()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            self.ps.Reset()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            self.ps.Reset()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            self.ps.Reset()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            self.ps.Reset()  
                      
    def GetVoltage(self,channel = 1):        
        '''Reads the measured voltage'''    
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            return self.ps.GetVoltage(channel)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            return self.ps.GetVoltage()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            return self.ps.GetVoltage()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            return self.ps.GetVoltage()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            return self.ps.GetVoltage()           
              
    def GetVoltageSetted(self,channel=1):       
        '''Reads the output setted voltage value'''
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            return self.ps.GetVoltageSetted(channel)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            return self.ps.GetVoltageSetted()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            return self.ps.GetVoltageSetted()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            return self.ps.GetVoltageSetted()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            return self.ps.GetVoltageSetted()    
                     
    def SetVoltageLimit(self, volts):   
        '''Returns the maximum voltage limit value'''     
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            self.ps.SetVoltageLimit(volts)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            self.ps.SetVoltageLimit(volts)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            self.ps.SetVoltageLimit(volts)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            self.ps.SetVoltageLimit(volts)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            self.ps.SetVoltageLimit(volts)   

    def GetVoltageLimit(self):   
        '''Returns the maximum voltage limit value'''     
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            return self.ps.GetVoltageLimit()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            return self.ps.GetVoltageLimit()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            return self.ps.GetVoltageLimit()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            return self.ps.GetVoltageLimit()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            return self.ps.GetVoltageLimit()             

    def GetCurrent(self,channel=1):
        '''Reads the measured current'''
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            return self.ps.GetCurrent(channel)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            return self.ps.GetCurrent()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            return self.ps.GetCurrent()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            return self.ps.GetCurrent()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            return self.ps.GetCurrent()  
                        
    def GetCurrentSetted(self,channel=1):
        '''Reads the setted current'''
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            return self.ps.GetCurrentSetted(channel)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            return self.ps.GetCurrentSetted()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            return self.ps.GetCurrentSetted()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            return self.ps.GetCurrentSetted()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            return self.ps.GetCurrentSetted()   
                  
    def SetCurrentLimit(self, amperes):        
        '''Sets the current limit'''
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            self.ps.SetCurrentLimit(amperes)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            self.ps.SetCurrentLimit(amperes)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            self.ps.SetCurrentLimit(amperes)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            self.ps.SetCurrentLimit(amperes)
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            self.ps.SetCurrentLimit(amperes)             

    def GetCurrentLimit(self):
        '''Returns the maximum current limit value'''
        if   cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_HAMEG_HMP':
            return self.ps.SetCurrentLimit()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_TDK_LAMBDA':
            return self.ps.SetCurrentLimit()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_KONSTANTER_SSP':
            return self.ps.SetCurrentLimit()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_SYSKON':
            return self.ps.SetCurrentLimit()
        elif cfg.get("POWER_SOURCE","ConnectedDevice") == 'PS_LAB_SM':
            return self.ps.SetCurrentLimit()   

        
""" Power Source 
#ps = PowerSourceInstance()
#ps.ClosePort()
#ps.OpenPort()
#ps.SetOutputON(3)
#ps.SetVoltage(10,3 )
#time.sleep(1)
#ps.SetOutputON(3)
"""

            
class SMSInstance():
    def __init__(self):
        self.sms = SMS()
        '''Get the SMS DEVICE NUMBER from CONFIGURATION.cfg'''
        self.smsDevice_1 = cfg.get("SMS","smsId_1")
        self.smsDevice_2 = cfg.get("SMS","smsId_2")
        self.smsDevice_3 = cfg.get("SMS","smsId_3")
        self.smsDevice_4 = cfg.get("SMS","smsId_4")
     
    def SetPos(self,serNum,newPos):
        '''Sets the position of the device number serNum to newPos'''
        self.sms.SetPos(serNum,newPos)

    def GetPos(self,serNum):
        '''Returns the position of the device number serNum'''
        return self.sms.GetPos(serNum) 
         
    def Reset(self,serNum):
        '''Resets the device number serNum to default values'''
        self.sms.Reset(serNum)
         
    def Inc(self,serNum):
        '''Increase position '''
        self.sms.Inc(serNum)
     
    def Dec(self,serNum):
        '''Decrease position '''
        self.sms.Dec(serNum)
        
    def GetHallState(self,serNum):
        '''Returns the status of hall sensors of the device number serNum'''
        return self.sms.GetHallState(serNum)
    
    def SetHallErr(self,serNum,string):
        '''Sets the status of hall sensors of the device number serNum'''
        self.sms.SetHallErr(serNum,string)
        
    def SetPinch(self,serNum,pinchPos,pinchType):    
        '''Pinching will be triggered if the specified position is reached'''
        self.sms.SetPinch(serNum,pinchPos,pinchType)
       
    def SetBlock(self,serNum,blockPos,blockType):
        '''Blocking occours if the specified position is reached'''
        self.sms.SetBlock(serNum,blockPos,blockType)

'''
sms = SMSInstance()
GLASS_PANEL = sms.smsDevice_1
BLIND       = sms.smsDevice_2
sms.Reset(GLASS_PANEL)
sms.SetBlock(GLASS_PANEL,100,"HALF")
'''
  


class RelayBoxInstance():
    
    def __init__(self):
        pass
    def USB_SendCommand(self,CommandReq):
        """ Send command to RelayBox """
        USB_SendCommand(CommandReq)
        
    def USB_SendMultipleCommands(self,CommandReqList): 
        """ Send multiple command to RelayBox """
        USB_SendMultipleCommands(CommandReqList)
    
    def USB_ReadUSBData(self):
        return USB_ReadUSBData() 
    
    def GetPortStringStatus(self,PortStatusValue):
        return GetPortStringStatus(PortStatusValue)   
    
    def GetDevicesIdentification(self):
        GetDevicesIdentification()

""" USB Relay Box 
 
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
  PORT_PLANT_MODE_ON         =   0x11
  PORT_PLANT_MODE_OFF        =   0x12

#Relay Box       
rb = RelayBoxInstance()

rb.USB_SendCommand(PORT_ON_LOCAL_CLOSE)
time.sleep(1)
rb.USB_SendCommand(PORT_ALL_OFF)


CommandReqList = [(PORT_ON_LOCAL_OPEN,0.5) , (PORT_ALL_OFF,1) , (PORT_ON_LOCAL_CLOSE,1) , (PORT_ALL_OFF,1) ]
rb.USB_SendMultipleCommands(CommandReqList)  

rb.USB_ReadUSBData() 
print rb.GetPortStringStatus(PORT_ALL_OFF)  

#Read Serial Number to put in CONFIGURATION.cfg  
rb = RelayBoxInstance() 
rb.GetDevicesIdentification()

"""
