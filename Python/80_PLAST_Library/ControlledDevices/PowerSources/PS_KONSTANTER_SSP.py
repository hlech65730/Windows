'''
    Author: C. Bruma
    Purpose:  Konstanter SSP 240 Power Suply - Control via the Serial Communication Port    
    Date: 23-01-2015        
    Arguments: -   
    Outputs: -    
    Dependencies: -

    History:
    ------------------------------------------------------------------------------
    Revision | Date:      | Modification:                             | Author
    .......................................................................
    v0.1     | 23-01-2015 | Creation                                  | C. Bruma
    ------------------------------------------------------------------------------
'''

import time, os
import sys
import serial
import ConfigParser

'''
The following parameters can be programmed and monitored via the serial communication port:

ps = KonstanterSSPPowerSource()           # Connect with the power source. The rest of the port settings are the default ones.
ps.OpenPort()                             # Open serial port.
ps.ClosePort()                            # Close serial port.
ps.PrintConfiguration()                   # Print serial port configuration.
ps.SendCommand('*IDN?')                   # Send user command to power source. (ex: identifies the device)
ps.SetVoltage(18.000)                     # Sets the output voltage value in Volts.
ps.SetCurrent(3.000)                      # Sets the Output Current value in Amperes.
ps.SetOutputON()                          # Turns the output to ON.
ps.SetOutputOFF()                         # Turns the output to OFF
ps.Reset()                                # Resets the device

Other posible parameters for initializing the serial port are:

portTx = 'COMx'   #indicates that the transmision port is COMx
portRx = 'COMx'   #indicates that the recieving port is COMx
baudrate = xxxx   #indicates that the baudrate is xxxx
stopbits = x      #indicates that the stopbits number is x (1 / 1.5 / 2)
parity = 'X'      #indicates that the parity is 'X' ('N' / 'O' / 'E' / 'M' / 'S')
databits = x      #indicates that the databits number is x (7 / 8)
xonxoff = x       #indicates that the xonxoff handshake is x (1 = TRUE / 0 = FALSE)
rtscts = x        #indicates that the rtscts handshake is x (1 = TRUE / 0 = FALSE)
timeout = x       #indicates that the read timeout value is x


USAGE EXAMPLE:

ps=KonstanterSSPPowerSource()
ps.OpenPort()
ps.PrintPortConfiguration()
ps.SetVoltage(10.5,1)
ps.SetCurrent(1.45,1)
ps.SetVoltage(6.5,2)
ps.SetCurrent(2,2)
ps.SetVoltage(15,3)
ps.SetCurrent(10,3)
ps.SetOutputON(1)
time.sleep(1)
ps.SetOutputOFF(1)
ps.SetOutputON(2)
time.sleep(1)
ps.SetOutputOFF(2)
ps.SetOutputON(3)
time.sleep(1)
ps.SetOutputOFF(3)
print ps.GetVoltage(1)
print ps.GetVoltageSetted(1)
ps.Reset()
ps.Reset()
ps.ClosePort()
'''
cfg = ConfigParser.RawConfigParser()
cfg.read(os.environ['PLAST_WA_PATH'] + "CONFIGURATION.cfg")

class KonstanterSSPPowerSource:
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
            Sets the output maximum limit voltage value in Volts.
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
            Sets the output maximum current limit value in Amperes.
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
 
