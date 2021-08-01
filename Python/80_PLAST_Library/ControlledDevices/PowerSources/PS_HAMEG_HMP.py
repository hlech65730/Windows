'''
    Author: C. Bruma
    Purpose: HAMEG HPM 2020/4030/4040 Power Supply - Control via the Serial Communication Port or USB port
    Date: 22-01-2015        
    Arguments: -   
    Outputs: -    
    Dependencies: -

    History:
    ------------------------------------------------------------------------------
    Revision | Date:      | Modification:                             | Author
    .......................................................................
    v0.1     | 22-01-2015 | Creation                                  | C. Brunma
    ------------------------------------------------------------------------------
'''

import time, os
import serial
import ConfigParser
import sys
import usb.core
'''
The following parameters can be programmed and monitored via the serial communication port:

ps = PowerSourceInstance()                # Connect with the power source through serial port. The rest of the port settings are the default ones.
ps.OpenPort()                             # Open serial port.
ps.ClosePort()                            # Close serial port.
ps.PrintConfiguration()                   # Print serial port configuration.
ps.SendCommand('*IDN?')                   # Send user command to power source. (ex: identifies the device)
ps.SetVoltage(18.000)                     # Sets the output voltage value in Volts.
ps.SetCurrent(3.000)                      # Sets the Output Current value in Amperes.
ps.SetOutputON()                          # Turns the output to ON.
ps.SetOutputOFF()                         # Turns the output to OFF
ps.Reset()                                # Resets the device
ps.ReadSetCurrentValue()                  # Retruns the value at which the output current is set
ps.ReadSetVoltageValue()                  # Retruns the value at which the output voltage is set
ps.ReadMeasuredVoltage()                  # Returns the measured voltage value
ps.ReadMeasuredCurrent()                  # Returns the measured current value

Other posible parameters for initializing the serial port are:

port = 'COMx'     #indicates that the port is COMx
baudrate = xxxx   #indicates that the baudrate is xxxx
stopbits = x      #indicates that the stopbits number is x (1 / 2)
parity = 'X'      #indicates that the parity is 'X' ('N' / 'O' / 'E')
databits = x      #indicates that the databits number is x (7 / 8)
rtscts = x        #indicates that the rtscts handshake is x (1 = TRUE / 0 = FALSE)
timeout = x       #indicates that the read timeout value is x

USAGE EXAMPLE via serial port:
s=PowerSourceInstance()
s.OpenPort()

s.SetCurrent(25)
s.SetVoltage(60)
s.SetOutputON()

curr=s.ReadSetCurrentValue()
print curr
volt=s.ReadSetVoltageValue()
print volt

s.ClosePort()

Other parameters for initializing the USB port:

pid = 0xED72        # The product ID
vid = 0x0403        # The vendor ID
inAddr = 0x81       # The address of the USB backend input
outAddr = 0x02      # The address of the USB backend output
bus = 0             # The bus number of the device
devAddr = 1         # The device address number (it depends on the devices added in usb filter)

USAGE EXAMPLE via USB port:
s=PowerSourceInstance()
s.OpenPort() 
s.SetCurrent(25)
s.SetVoltage(60)
s.SetOutputON()

curr=s.ReadSetCurrentValue()
print curr
volt=s.ReadSetVoltageValue()
print volt

s.ClosePort()
'''

cfg = ConfigParser.RawConfigParser()
cfg.read(os.environ['PLAST_WA_PATH'] + "CONFIGURATION.cfg")

class HamegHMPPowerSource:
    def __init__(self):
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            self.ser             = serial.Serial()
            self.ser.port        = cfg.get("SERIAL","port")
            self.ser.baudrate    = cfg.getint("SERIAL","baudrate")
            self.ser.bytesize    = cfg.getint("SERIAL","bytesize")
            self.ser.parity      = cfg.get("SERIAL","parity")
            self.ser.stopbits    = cfg.getint("SERIAL","stopbits")
            self.ser.timeout     = cfg.getint("SERIAL","timeout")
            self.ser.xonxoff     = cfg.getint("SERIAL","xonxoff")
            self.ser.rtscts      = cfg.getint("SERIAL","rtscts")
            self.ser.dsrdtr      = cfg.getint("SERIAL","dsrdtr")
            
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
            self.pid = int(cfg.get("USB","pid"),16)
            self.vid = int(cfg.get("USB","vid"),16)
            self.inAddr = int(cfg.get("USB","inAddr"),16)
            self.outAddr = int(cfg.get("USB","outAddr"),16)
            self.bus = int(cfg.get("USB","bus"),16)
            self.devAddr = int(cfg.get("USB","devAddr"),16)
            
            self.devs = usb.core.find(find_all=True, idVendor=self.vid, idProduct= self.pid)
            self.dev=None
            
            for dev in self.devs:
                if dev.bus==self.bus and dev.address==self.devAddr:
                    self.dev=dev
                
            if self.dev is not None:
                self.dev.set_configuration()
            else:
                print "The device can not be found or can not be configured."
                sys.exit()
        else:
            print "Incorect connection type."
            
    def OpenPort(self):
        '''
            Open serial port.
        '''
        
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            try:
                self.ser.open()
            except(serial.serialutil.SerialException):
                print "Cannot connect to power source. Port is already open."
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
            pass
        else:
            print "Incorect connection type."

    def ClosePort(self):
        '''
            Close serial port.
        '''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            self.ser.close()
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
            usb.util.dispose_resources(self.dev)
        else:
            print "Incorect connection type."
        
    def PrintPortConfiguration(self):
        '''
            Print serial connection settings.
        '''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            print self.ser
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
            print self.dev
        else:
            print "Incorect connection type."        

    def SendCommand(self, data):
        '''
            Send user command to power source.
            More information about compatible commands is found in the power source manual.
        '''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            if self.ser.isOpen():
                self.ser.write(data + '\n')
                time.sleep(0.11) # time for the power source to process the query
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
            self.dev.write(self.outAddr,data+'\n')
            time.sleep(0.11) # time for the power source to process the query
        else:
            print "Incorect connection type." 
        
    def SetVoltage(self, volts, channel = 1):
        '''
            Sets the output voltage value in Volts.
        '''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            if self.ser.isOpen():
                self.ser.write('INST OUT' + str(channel) + '\n')
                time.sleep(0.11) # time for the power source to process the query
                self.ser.write('VOLT ' + str(volts) + '\n')
                time.sleep(0.11) # time for the power source to process the query
            else:
                print 'COM Port is not open.'
                
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
            self.dev.write(self.outAddr, 'INST OUT' + str(channel) + '\n')
            time.sleep(0.11) # time for the power source to process the query
            self.dev.write(self.outAddr, 'VOLT ' + str(volts) + '\n')
            time.sleep(0.11) # time for the power source to process the query

        else:
            print "Incorect connection type." 
            
    def SetCurrent(self, amperes, channel = 1):
        ''' 
            Sets the Output Current value in Amperes.
        '''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            if self.ser.isOpen():
                if ((channel == 1) and (amperes <= 10)) or ((channel == 2) and (amperes <= 10)) or ((channel == 3) and (amperes <= 10)):
                    self.ser.write('INST OUT' + str(channel) + '\n')
                    time.sleep(0.11) # time for the power source to process the query
                    self.ser.write('CURR ' + str(amperes) + '\n')
                    time.sleep(0.11) # time for the power source to process the query
                elif((channel >= 1) and (channel <=3)):
                    print 'Channel ' + str(channel) + ' cannot provide more than 10 amperes.'
                else:
                    print 'Incorrect channel. Channel must be 1,2 or 3.'
            else:
                print 'COM Port is not open.'
                
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
            if ((channel == 1) and (amperes <= 10)) or ((channel == 2) and (amperes <= 10)) or ((channel == 3) and (amperes <= 10)):
                self.dev.write(self.outAddr,"INST OUT"+str(channel)+"\n")
                time.sleep(0.11)
                self.dev.write(self.outAddr,"CURR "+str(amperes)+"\n")
                time.sleep(0.11)
            elif((channel >= 1) and (channel <=3)):
                print 'Channel ' + str(channel) + ' cannot provide more than 10 amperes.'
            else:
                print 'Incorrect channel. Channel must be 1,2 or 3.'
        else:
            print "Incorect connection type."             
        
    def SetOutputON(self, channel = 1):
        ''' 
            Turns the output to ON.
        '''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            if self.ser.isOpen():
                self.ser.write('INST OUT' + str(channel) + '\n')
                time.sleep(0.11) # time for the power source to process the query
                self.ser.write('OUTP ON\n')
                time.sleep(0.11) # time for the power source to process the query
            else:
                print 'COM Port is not open.'
        
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
            self.dev.write(self.outAddr,"INST OUT"+str(channel)+"\n")
            time.sleep(0.11)
            self.dev.write(self.outAddr,'OUTP ON\n')            
        else:
            print "Incorect connection type." 
         
    def SetOutputOFF(self, channel = 1):
        ''' 
            Turns the output to OFF. 
        '''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            if self.ser.isOpen():
                self.ser.write('INST OUT' + str(channel) + '\n')
                time.sleep(0.11) # time for the power source to process the query
                self.ser.write('OUTP OFF\n')
                time.sleep(0.11) # time for the power source to process the query
            else:
                print 'COM Port is not open.'
        
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
            self.dev.write(self.outAddr,"INST OUT"+str(channel)+"\n")
            time.sleep(0.11)
            self.dev.write(self.outAddr,'OUTP OFF\n')            
        else:
            print "Incorect connection type." 
        
    def Reset(self):
        '''Resets the device parameters'''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            if self.ser.isOpen()==True:
                self.ser.write("*RST\n")
            else:
                print 'Unopened serial port'
                    
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):            
            self.dev.write(self.outAddr, "*RST\n")
            time.sleep(0.11) # time for the power source to process the query        
        else:
            print "Incorect connection type."

    def GetVoltage(self,channel=1):
        '''Reads the measured voltage'''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            if self.ser.isOpen()==True:
                self.ser.write("INST OUT"+str(channel)+"\n")
                time.sleep(0.11)
                self.ser.write("MEAS:VOLT?"+"\n")
                time.sleep(0.11)
                value=self.ser.read(10)
                return float(value)
            else:
                print 'Unopened serial port'
                return -1
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
#             self.dev.write(self.outAddr,"INST OUT"+str(channel)+"\n")
#             time.sleep(0.11)
# #             self.dev.write(self.outAddr,"MEAS:VOLT?\n")
# #             time.sleep(0.11)
#             self.dev.read(self.inAddr,256)
#             time.sleep(0.11)
#             self.dev.write(self.outAddr,"MEAS:VOLT?\n")
#             time.sleep(0.11)
#             aux1=self.dev.read(self.inAddr,256)
#             value1=''.join(chr(i1) for i1 in aux1)
#             value1=value1[2:]
#             value1=value1[:-1]
#             return float(value1)
            print "Function not implemented yet on this device."
            return -1
    
        else:
            print "Incorect connection type." 
            return -1

    def GetVoltageSetted(self,channel=1):
        '''Reads the output setted voltage value'''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            if self.ser.isOpen()==True:
                self.ser.write("INST OUT"+str(channel)+"\n")
                time.sleep(0.11)
                self.ser.write("VOLT?"+"\n")
                time.sleep(0.11)
                value=self.ser.read(10)
                return float(value)
            else:
                print 'Unopened serial port'
                return -1
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
#             self.dev.write(self.outAddr,"INST OUT"+str(channel)+"\n")
#             time.sleep(0.11)
# #             self.dev.write(self.outAddr,"VOLT?\n")
# #             time.sleep(0.11)
#             self.dev.read(self.inAddr,256)
#             time.sleep(0.11)
#             self.dev.write(self.outAddr,"VOLT?\n")
#             time.sleep(0.11)
#             aux2=self.dev.read(self.inAddr,256)
#             value2=''.join(chr(i2) for i2 in aux2)
#             value2=value2[2:]
#             value2=value2[:-1]
#             return float(value2)
            print "Function not implemented yet on this device."
            return -1    
        else:
            print "Incorect connection type." 
            return -1
      
    def GetCurrent(self,channel=1):
        '''Reads the measured current'''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            if self.ser.isOpen()==True:
                self.ser.write("INST OUT"+str(channel)+"\n")
                time.sleep(0.11)
                self.ser.write("MEAS:CURR?\n")
                time.sleep(0.11)
                value=self.ser.read(10)
                return float(value)
            else:
                print 'Unopened serial port'
                return -1
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
#             self.dev.write(self.outAddr,"INST OUT"+str(channel)+"\n")
#             time.sleep(0.11)
# #             self.dev.write(self.outAddr,"MEAS:CURR?\n")
# #             time.sleep(0.11)
#             self.dev.read(self.inAddr,256)
#             time.sleep(0.11)
#             self.dev.write(self.outAddr,"MEAS:CURR?\n")
#             time.sleep(0.11)
#             aux3=self.dev.read(self.inAddr,256)
#             value3=''.join(chr(i3) for i3 in aux3)
#             value3=value3[2:]
#             value3=value3[:-1]
#             return float(value3)
            print "Function not implemented yet on this device."
            return -1    
    
        else:
            print "Incorect connection type." 
            return -1

          
    def GetCurrentSetted(self,channel=1):
        '''Reads the output current value'''
        if(cfg.get("POWER_SOURCE","ConnectionType") == "SERIAL"):
            if self.ser.isOpen()==True:
                self.ser.write("INST OUT"+str(channel)+"\n")
                time.sleep(0.11)
                self.ser.write("CURR?\n")
                time.sleep(0.11)
                value=self.ser.read(10)
                return float(value)
            else:
                print 'Unopened serial port'
                return -1
        elif(cfg.get("POWER_SOURCE","ConnectionType") == "USB"):
#             self.dev.write(self.outAddr,"INST OUT"+str(channel)+"\n")
#             time.sleep(0.11)
# #             self.dev.write(self.outAddr,"CURR?\n")
# #             time.sleep(0.11)
#             self.dev.read(self.inAddr,256)
#             time.sleep(0.11)
#             self.dev.write(self.outAddr,"CURR?\n")
#             time.sleep(0.11)
#             aux4=self.dev.read(self.inAddr,256)
#             value4=''.join(chr(i4) for i4 in aux4)
#             value4=value4[2:]
#             value4=value4[:-1]
#             return float(value4)
            print "Function not implemented yet on this device."
            return -1
        else:
            print "Incorect connection type." 
            return -1

    def SetCurrentLimit(self, amperes):
        ''' 
            This power source model doesn't support this function
        '''
        print "This power source model doesn't support this function."

    def GetCurrentLimit(self):
        ''' 
            This power source model doesn't support this function
        '''
        print "This power source model doesn't support this function."    
        return -1
    
    def SetVoltageLimit(self, volts):
        ''' 
            This power source model doesn't support this function
        '''
        print "This power source model doesn't support this function."
            
    def GetVoltageLimit(self):
        ''' 
            This power source model doesn't support this function
        '''
        print "This power source model doesn't support this function."       
        return -1    
