'''
    Author: C. Bruma
    Purpose:  P500, P800, P1500, P3000 and P4500 Power Suply - Control via the Serial Communication Port or USB port
    Date: 22-01-2015        
    Arguments: -   
    Outputs: -    
    Dependencies: -

    History:
    ------------------------------------------------------------------------------
    Revision | Date:      | Modification:                             | Author
    .......................................................................
    v0.1     | 22-01-2015 | Creation                                  | C. Bruma
    ------------------------------------------------------------------------------
'''

import time, os
import sys
import serial
import ConfigParser

'''
The following parameters can be programmed and monitored via the serial communication port:

ps = Syskon()                             # Connect with the power source. The rest of the port settings are the default ones.
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

port = 'COMx'          #indicates that the port is COMx
baudrate = xxxx   #indicates that the baudrate is xxxx
stopbits = x      #indicates that the stopbits number is x (1 / 1.5 / 2)
parity = 'X'      #indicates that the parity is 'X' ('N' / 'O' / 'E' / 'M' / 'S')
databits = x      #indicates that the databits number is x (7 / 8)
xonxoff = x       #indicates that the xonxoff handshake is x (1 = TRUE / 0 = FALSE)
rtscts = x        #indicates that the rtscts handshake is x (1 = TRUE / 0 = FALSE)
timeout = x       #indicates that the read timeout value is x


USAGE EXAMPLE:
s=Syskon.Syskon(baudrate=115200)
s.OpenPort()

s.SetCurrent(25)
s.SetVoltage(60)
s.SetOutputON()

curr=s.ReadSetCurrentValue()
print curr
volt=s.ReadSetVoltageValue()
print volt

s.ClosePort()

USING THE USB ON SYSKON IS THE SAME AS USING THE SERIAL PORT SO...
'''

cfg = ConfigParser.RawConfigParser()
cfg.read(os.environ['PLAST_WA_PATH'] + "CONFIGURATION.cfg")

class SyskonPowerSource:
    def __init__(self):
        self.ser             = serial.Serial()
        self.ser.port        = cfg.get("SERIAL","port")
        self.ser.baudrate    = cfg.getint("SERIAL","baudrate")
        self.ser.bytesize    = cfg.getint("SERIAL","bytesize")
        self.ser.parity      = cfg.get("SERIAL","parity")
        self.ser.stopbits    = cfg.getint("SERIAL","stopbits")
        self.ser.xonxoff     = cfg.getboolean("SERIAL","xonxoff")
        self.ser.rtscts      = cfg.getboolean("SERIAL","rtscts")
        self.ser.dsrdtr      = cfg.getboolean("SERIAL","dsrdtr")
        
        if ((cfg.get("SERIAL","timeout") == "0") or(cfg.get("SERIAL","timeout") == "None"    )): 
            self.ser.timeout     = None 
        else:
            self.ser.timeout = cfg.getint("SERIAL","timeout")
            
    def OpenPort(self):
        '''
            Open serial port.
        '''
        self.ser.open()
    
    def ClosePort(self):
        '''
            Close serial port.
        '''
        self.ser.close()
    
    def PrintPortConfiguration(self):
        '''
            Print serial connection settings.
        '''
        print self.ser
        
    def SendCommand(self, data):
        '''
            Send user command to power source.
            More information about compatible commands is found in the power source manual.
        '''
        if self.ser.isOpen():
            self.ser.write(data + ';\n')
            time.sleep(0.11) # time for the power source to process the query
        else:
            print 'COM Port is not open.'
        
    def SetVoltage(self, volts):
        '''
            Sets the output voltage value in Volts.
        '''
        if self.ser.isOpen():
            if(float(volts) < float(self.GetVoltageLimit())):
                self.ser.write("USET " + str(volts) + "\n")
                time.sleep(0.11) # time for the power source to process the query
            else:
                print "Voltage higher than limit."
        else:
            print 'COM Port is not open.'
            
    def SetCurrent(self, amperes):
        ''' 
            Sets the Output Current value in Amperes.
        '''
        if self.ser.isOpen():
            if(float(amperes) < float(self.GetCurrentLimit())):
                self.ser.write("ISET " + str(amperes) + ";\n")
                time.sleep(0.11) # time for the power source to process the query
            else:
                print "Current higher than limit."
        else:
            print 'COM Port is not open.'
        
    def SetOutputON(self):
        ''' 
            Turns the output to ON.
        '''
        if self.ser.isOpen():
            self.ser.write('OUTPUT ON;\n')
            time.sleep(0.11) # time for the power source to process the query
        else:
            print 'COM Port is not open.'
        
         
    def SetOutputOFF(self):
        ''' 
            Turns the output to OFF. 
        '''
        if self.ser.isOpen():
            self.ser.write('OUTPUT OFF;\n')
            time.sleep(0.11) # time for the power source to process the query
        else:
            print 'COM Port is not open.'

    def GetCurrent(self):
        '''Returns the measured current value'''       
        if self.ser.isOpen():
            self.ser.write('IOUT?;\n')
            time.sleep(0.11)
            value=self.ser.read(14)
            return float(value[6:])    
        else:
            print 'COM Port is not open.'
            
    def GetVoltage(self):
        '''Returns the measured current value'''
        if self.ser.isOpen():
            self.ser.write('UOUT?;\n')
            time.sleep(0.11)
            value=self.ser.read(14)
            return float(value[6:])
        else:
            print 'COM Port is not open.'
                   
    def GetVoltageSetted(self):
        '''Returns the setted voltage value'''
        if self.ser.isOpen():
            self.ser.write("USET?;\n")
            value=self.ser.read(14)
            return float(value[6:])
        else:
            print 'COM Port is not open.'
            
    def GetCurrentSetted(self):
        '''Returns the setted current value'''
        if self.ser.isOpen():
            self.ser.write("ISET?;\n")
            value=self.ser.read(14)
            return float(value[6:])
        else:
            print 'COM Port is not open.'
     
    def SetVoltageLimit(self, volts):
        '''
            Sets the maximum output limit voltage value in Volts.
        '''
        if self.ser.isOpen():
            self.ser.write("ULIM " + str(volts) + ";\n")
            time.sleep(0.11) # time for the power source to process the query
        else:
            print 'COM Port is not open.'
            
    def GetVoltageLimit(self):
        '''Returns the maximum voltage limit value'''
        if self.ser.isOpen():
            self.ser.write("ULIM?;\n")
            value=self.ser.read(14)
            #print 'gvl',value
            return float(value[6:])
           
        else:
            print 'COM Port is not open.'
            return -1
            
    def SetCurrentLimit(self, amperes):
        ''' 
            Sets the maximum output current limit value in Amperes.
        '''
        if self.ser.isOpen():
            self.ser.write("ILIM " + str(amperes) + ";\n")
            time.sleep(0.11) # time for the power source to process the query
        else:
            print 'COM Port is not open.'

    def GetCurrentLimit(self):
        
        '''Returns the maximum current limit value'''
        if self.ser.isOpen():
            time.sleep(0.1)
            self.ser.write("ILIM?\n")
            value=self.ser.read(14)
            return float(value[6:])
        else:
            print 'COM Port is not open.'
            return -1
     
    def Reset(self):
        '''Resets the device'''
        if self.ser.isOpen()==True:
            self.ser.write("*RST\n")
        else:
            print 'Unopened serial port'


# src = SyskonPowerSource()
# src.OpenPort()
# src.SetVoltageLimit(15.5)
# src.SetVoltage(8.458)
# 
# src.SetCurrentLimit(6.345)
# src.SetCurrent(1)
# 
# src.SetOutputON()
# 
# print 'getCurrent', src.GetCurrent()
# print 'getVoltage',src.GetVoltage()
# print 'GetVoltageSetted',src.GetVoltageSetted()
# print 'GetCurrentSetted',src.GetCurrentSetted()
# 
# print 'GetVoltageLimit',src.GetVoltageLimit()
# print 'GetCurrentLimit',src.GetCurrentLimit()
# 
# src.SetOutputON()
# src.Reset()
# src.ClosePort()
