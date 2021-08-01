'''
    Author: L. Nitu
    Purpose: TDK GEN 1500W Power Supply - Control via the Serial Communication Port
    Date: 21-01-2014        
    Arguments: -   
    Outputs: -    
    Dependencies: -

    History:
    ------------------------------------------------------------------------------
    Revision | Date:      | Modification:                             | Author
    .......................................................................
    v0.1     | 21-01-2014 | Creation                                  | L. Nitu
    ------------------------------------------------------------------------------
'''

import time, os
import serial
import ConfigParser

'''
The following parameters can be programmed and monitored via the serial 
communication port:

ps = TDKLambdaPowerSource(port = 'COM2')  # Connect with the power source through serial port 'COM2'. The rest of the port settings are the default ones.
ps.OpenPort()                             # Open serial port.
ps.ClosePort()                            # Close serial port.
ps.PrintConfiguration()                   # Print serial port configuration.
ps.SendCommand('SAV')                     # Send user command to power source. (ex: saves present settings)
ps.SetVoltage(18.000)                     # Sets the output voltage value in Volts.
ps.SetCurrent(3.000)                      # Sets the Output Current value in Amperes.
ps.SetOutputON()                          # Turns the output to ON.
ps.SetOutputOFF()                         # Turns the output to OFF.
ps.SetFoldbackProtectionON()              # Sets the Foldback protection to ON.
ps.SetFoldbackProtectionOFF()             # Sets the Foldback protection to OFF.

'''

cfg = ConfigParser.RawConfigParser()
cfg.read(os.environ['PLAST_WA_PATH'] + "CONFIGURATION.cfg")

class TDKLambdaPowerSource():
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
        self.ser.write('ADR 06\r') # access the power supply
        time.sleep(0.2) # time for the power source to process the query
        self.ser.read(10) # clear the buffer
        
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
            self.ser.write(data + '\r')
            time.sleep(0.2) # time for the power source to process the query
            self.ser.read(10) # clear the buffer
        else:
            print 'COM Port is not open.'
        
    def SetVoltage(self, volts):
        ''' Sets the output voltage value in Volts. The maximum number of characters is 12. 
            See the following examples for PV n format: PV 12, PV 012, PV 12.0, PV 012.00, etc. 
        '''
        if self.ser.isOpen():
            self.ser.write('PV ' + str(volts) + '\r')
            time.sleep(0.2) # time for the power source to process the query
            self.ser.read(10) # clear the buffer
        else:
            print 'COM Port is not open.'
        
    def SetCurrent(self, amperes):
        ''' Sets the Output Current value in Amperes. The maximum number of characters is 12. 
            Examples for PC n format: PC 10, PC 10.0, PC 010.00, etc. 
        '''
        if self.ser.isOpen():
            self.ser.write('PC ' + str(amperes) + '\r')
            time.sleep(0.2) # time for the power source to process the query
            self.ser.read(10) # clear the buffer
        else:
            print 'COM Port is not open.'
        
    def SetOutputON(self):
        ''' 
            Turns the output to ON. 
        '''
        if self.ser.isOpen():
            self.ser.write('OUT 1\r')
            time.sleep(0.2) # time for the power source to process the query
            self.ser.read(10) # clear the buffer
            time.sleep(0.2) # time for the power source to process the query
        else:
            print 'COM Port is not open.'
        
    def SetOutputOFF(self):
        ''' 
            Turns the output to OFF. 
        '''
        if self.ser.isOpen():
            self.ser.write('OUT 0\r')
            time.sleep(0.2) # time for the power source to process the query
            self.ser.read(10) # clear the buffer
        else:
            print 'COM Port is not open.'
        
    def GetCurrentSetted(self):
        '''Returns the programmed current value'''       
        if self.ser.isOpen():
            self.ser.write('PC?\r')
            time.sleep(0.11)
            value = self.ser.read(10)
            return float(value)
        else:
            print 'COM Port is not open.'

    def GetVoltageSetted(self):
        '''Returns the programmed voltage value'''       
        if self.ser.isOpen():
            self.ser.write('PV?\r')
            time.sleep(0.11)
            value = self.ser.read(10)
            return float(value)
        else:
            print 'COM Port is not open.'

    def GetCurrent(self):
        '''Returns the actual current value'''       
        if self.ser.isOpen():
            self.ser.write('MC?\r')
            time.sleep(0.11)
            value = self.ser.read(10)
            return float(value)
        else:
            print 'COM Port is not open.'
        
    def GetVoltage(self):
        '''Returns the actual voltage value'''       
        if self.ser.isOpen():
            self.ser.write('MV?\r')
            time.sleep(0.11)
            value = self.ser.read(10)
            return float(value)
        else:
            print 'COM Port is not open.'
     

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
        
    def Reset(self):
        '''Resets the device'''
        if self.ser.isOpen()==True:
            self.ser.write("RST\r")
            time.sleep(0.11) 
            self.ser.read(10) # clear the buffer
            time.sleep(0.11) 
        else:
            print 'Unopened serial port'   
            
            
        
#     def SetFoldbackProtectionON(self):
#         ''' 
#             Sets the Foldback protection to ON. 
#             When the Foldback protection has been activated, OUT 1 command will release the protection and re-arm it, while FLD 0 will cancel the protection. 
#         '''
#         self.ser.write('FLD 1\r')
#         time.sleep(0.2) # time for the power source to process the query
#         
#     def SetFoldbackProtectionOFF(self):
#         ''' 
#             Sets the Foldback protection to OFF. 
#             When the Foldback protection has been activated, OUT 1 command will release the protection and re-arm it, while FLD 0 will cancel the protection. 
#         '''
#         self.ser.write('FLD 0\r')
#         time.sleep(0.2) # time for the power source to process the query
        
    


# ps = TDKLambdaPowerSource()
# # ps.PrintConfiguration()
# ps.OpenPort()
#  
# ps.SetOutputOFF()
#   
# ps.SetVoltage(6.56487)
# ps.SetCurrent(10.544342)
# ps.SetOutputON()
# print ps.GetCurrentSetted()
# print ps.GetCurrent()
# print ps.GetVoltageSetted() 
# print ps.GetVoltage() 
# #ps.SetOutputOFF()
# #ps.Reset()
# 
# ps.GetCurrentLimit()
# ps.ClosePort()
# 
# 
# print "Done"
