'''
    Author: C. Bruma
    Purpose:  LAB/SM Power Suply - Control via the Serial Communication Port    
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
import serial
import ConfigParser

'''
The following parameters can be programmed and monitored via the serial communication port:

ps = LABSM()                              # Connect with the power source. The rest of the port settings are the default ones.
ps.OpenPort()                             # Open serial port.
ps.ClosePort()                            # Close serial port.
ps.PrintConfiguration()                   # Print serial port configuration.
ps.SendCommand('IDN?')                   # Send user command to power source. (ex: identifies the device)
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
stopbits = x      #indicates that the stopbits number is x (1 / 2)
parity = 'X'      #indicates that the parity is 'X' ('N' / 'O' / 'E' )
databits = x      #indicates that the databits number is x (7 / 8)
xonxoff = x       #indicates that the xonxoff handshake is x (1 = TRUE / 0 = FALSE)
rtscts = x        #indicates that the rtscts handshake is x (1 = TRUE / 0 = FALSE)
timeout = x       #indicates that the read timeout value is x


USAGE EXAMPLE:
s=LABSM.LABSM(baudrate=19200)
s.OpenPort()

s.SetCurrent(25)
s.SetVoltage(25)
s.SetOutputON()

curr=s.ReadSetCurrentValue()
print curr
volt=s.ReadSetVoltageValue()
print volt

s.ClosePort()

'''

cfg = ConfigParser.RawConfigParser()
cfg.read(os.environ['PLAST_WA_PATH'] + "CONFIGURATION.cfg")

class LABSMPowerSource:
    def __init__(self):
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
            time.sleep(0.5) # time for the power source to process the query
        else:
            print 'COM Port is not open.'
            
    def SetVoltage(self, volts):
        '''
            Sets the output voltage value in Volts.
        '''
        if self.ser.isOpen():
            self.ser.write('UA, ' + str(volts) + 'V\r')
            time.sleep(0.5) # time for the power source to process the query
        else:
            print 'COM Port is not open.'
        
    def SetCurrent(self, amperes):
        ''' 
            Sets the Output Current value in Amperes.
        '''
        if self.ser.isOpen():
            self.ser.write("IA," + str(amperes) + "A\n")
            time.sleep(0.5) # time for the power source to process the query
        else:
            print 'COM Port is not open.'
            
    def SetOutputON(self):
        ''' 
            Turns the output to ON.
        '''
        if self.ser.isOpen():
            self.ser.write('SB,R\n')
            time.sleep(0.5) # time for the power source to process the query
        else:
            print 'COM Port is not open.'
        
         
    def SetOutputOFF(self):
        ''' 
            Turns the output to OFF. 
        '''
        if self.ser.isOpen():
            self.ser.write('SB,L\n')
            time.sleep(0.5) # time for the power source to process the query
        else:
            print 'COM Port is not open.'

    def Reset(self):
        if self.ser.isOpen():
            self.ser.write("*TST?\n")
        
    def GetCurrent(self):
        print "This power source model doesn't support this function."    
        return -1
            
    def GetVoltage(self):
        print "This power source model doesn't support this function."    
        return -1
                   
    def GetVoltageSetted(self):
        print "This power source model doesn't support this function."    
        return -1
            
    def GetCurrentSetted(self):
        print "This power source model doesn't support this function."    
        return -1
     
    def SetVoltageLimit(self, volts):
        print "This power source model doesn't support this function."    
        return -1
            
    def GetVoltageLimit(self):
        print "This power source model doesn't support this function."    
        return -1
            
    def SetCurrentLimit(self, amperes):
        print "This power source model doesn't support this function."    
        return -1

    def GetCurrentLimit(self):
        print "This power source model doesn't support this function."    
        return -1       
        
        
        
#     def SetVoltage2(self, val):
#         self.ser.write("OVP,"+str(val)+"V\n")
#         

#         
#     def ReadVersionRequest(self):
#         self.ser.write("*OPT?\r")
#         time.sleep(0.2)
#         value=self.ser.read(5)
#         return value
#     
#     def ReadMeasuredVoltage(self):
#         self.ser.write("MUA\n")
#         time.sleep(0.2)
#         value=self.ser.read(5)
#         return value
#     
#     def ReadMeasuredCurrent(self):
#         self.ser.write("MIA\n")
#         time.sleep(0.5)
#         value=self.ser.read(5)
#         return value
#     
#     def ReadSetCurrentValue(self):
#         self.ser.write("STATUS,IA\n")
#         time.sleep(0.5)
#         value=self.ser.read(5)
#         return value
#     
#     def ReadSetVoltageValue(self):
#         self.ser.write("STATUS,UA\n")
#         time.sleep(0.5)
#         value=self.ser.read(5)
#         return value
#     
#     def SetOutputON(self):
#         ''' 
#             Turns the output to ON. 
#         '''
#         self.ser.write('SB,R\n')
#         time.sleep(0.5) # time for the power source to process the query