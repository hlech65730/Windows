'''
    Author: C. Bruma
    Purpose: HAMEG HMF 2525 arbitrary generator - Control via the Serial Communication Port or USB port
    Date: 28-01-2015        
    Arguments: -   
    Outputs: -    
    Dependencies: -

    History:
    ------------------------------------------------------------------------------
    Revision | Date:      | Modification:                             | Author
    .......................................................................
    v0.1     | 28-01-2015 | Creation                                  | C. Brunma
    ------------------------------------------------------------------------------
'''
import time
import serial
# import usb.core

'''
The following parameters can be programmed and monitored via the serial communication port:

gs = HamegHMF(connType='SERIAL)           # Connect with the signal generator through serial port. The rest of the port settings are the default ones.
gs.OpenPort()                             # Open serial port.
gs.ClosePort()                            # Close serial port.
gs.PrintConfiguration()                   # Print serial port configuration.
gs.SendCommand('*IDN?')                   # Send user command to power source. (ex: identifies the device)
gs.SetAmplitude(18.000)                   # Sets the output voltage value in Volts.
gs.SetAmplitude()                         # Gets the Output voltage value in Volts.
gs.SetOutputON()                          # Turns the output to ON.
gs.SetOutputOFF()                         # Turns the output to OFF
gs.Reset()                                # Resets the device
gs.SetFrequency(1250)                     # Sets the output frequency
gs.SetSinWaveform()                       # Sets a sinusoidal waveform
gs.SetSquareWaveform(dutyCycle=40)        # Sets a square wafevorm with a duty cycle of 40%
gs.SetPulseWaveform(dutyCycle=30)         # Sets a pulse waveform with a duty cycle of 30%
gs.SetRampWaveform(symmetry=25)           # Sets a ramp waveform with a symmetry of 25%
gs.SetArbitraryWaveform(waveForm='SIN')   # Sets a sinusoidal arbitry waveform 

Other posible arbitrary waveforms are:

SIN  -> sinusoidal
SQU  -> square
PRAM -> positive ramp
NRAM -> negative ramp
TRI  -> triangle
WNO  -> white noise
PNO  -> pink noise
CARD -> cardinal sine
EXPR -> exponential raise
EXPF -> exponential fall
RAM  -> from RAM memory

Other posible parameters for initializing the serial port are:

port = 'COMx'     #indicates that the port is COMx
baudrate = xxxx   #indicates that the baudrate is xxxx
stopbits = x      #indicates that the stopbits number is x (1 / 2)
parity = 'X'      #indicates that the parity is 'X' ('N' / 'O' / 'E')
databits = x      #indicates that the databits number is x (7 / 8)
rtscts = x        #indicates that the rtscts handshake is x (1 = TRUE / 0 = FALSE)
timeout = x       #indicates that the read timeout value is x

USAGE EXAMPLE via serial port:
s=HamegHMF.HamegHMF(connType='SERIAL',baudrate=115200)
s.OpenPort()

s.SetAmplitude(25)
s.SetFrequency(1250)
gs.SetSquareWaveform(dutyCycle=53)
s.SetOutputON()

volt=s.GetAmplitude()
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
s=HamegHMF.HamegHMF(connType='USB')

s.SetAmplitude(25)
s.SetFrequency(1250)
gs.SetSquareWaveform(dutyCycle=53)
s.SetOutputON()

WHILE USING THE REMOTE CONTROL VIA USB THE OpenPort() AND ClosePort() FUNCTIONS MUST NOT BE USED!!!


WARNING:

The "Get" functions don't work well on USB connection, but they do on Serial connection.

'''

class HamegHMF:

    def __init__(self, **kwargs):
        if 'connType' not in kwargs or kwargs['connType'] is 'SERIAL':
            self.ser = serial.Serial()
            self.connType='SERIAL'
            if 'port' in kwargs:
                self.ser.port=kwargs['port']
            else:   
                self.ser.port='COM1'     
            if 'baudrate' in kwargs:
                self.ser.baudrate=kwargs['baudrate']
            else:   
                self.ser.baudrate=9600
            if 'bytesize' in kwargs:
                self.ser.bytesize=kwargs['bytesize']
            else:   
                self.ser.bytesize=8
            if 'parity' in kwargs:
                self.ser.parity=kwargs['parity']
            else:   
                self.ser.parity='N'
            if 'stopbits' in kwargs:
                self.ser.stopbits=kwargs['stopbits']
            else:   
                self.ser.stopbits=1
            if 'timeout' in kwargs:
                self.ser.timeout=kwargs['timeout']
            else:   
                self.ser.timeout=0
            self.ser.xonxoff=0
            if 'rtscts' in kwargs:
                self.ser.rtscts=kwargs['rtscts']
            else:   
                self.ser.rtscts=0
#         elif 'connType' in kwargs or kwargs['connType'] is 'USB':
#             self.connType='USB'
#             if 'pid' in kwargs:
#                 self.pid=kwargs['pid']
#             else:   
#                 self.pid=0xed72     
#             if 'vid' in kwargs:
#                 self.vid=kwargs['vid']
#             else:   
#                 self.vid=0x0403
#             if 'inAddr' in kwargs:
#                 self.inAddr=kwargs['inAddr']
#             else:   
#                 self.inAddr=0x81
#             if 'outAddr' in kwargs:
#                 self.outAddr=kwargs['outAddr']
#             else:   
#                 self.outAddr=0x02
#             if 'bus' in kwargs:
#                 self.bus=kwargs['bus']
#             else:   
#                 self.bus=0
#             if 'devAddr' in kwargs:
#                 self.devAddr=kwargs['devAddr']
#             else:   
#                 self.devAddr=1
#             self.devs = usb.core.find(find_all=True, idVendor=self.vid, idProduct= self.pid)
#             self.dev=None
#             
#             for dev in self.devs:
#                 if dev.bus==self.bus and dev.address==self.address:
#                     self.dev=dev
#             if self.dev is not None:
#                 self.dev.set_configuration()
#             else:
#                 print 'ERROR!!! The device can not be found or can not be configured'
#                 print "The script will now stop because it can't initialize the communication with the device"
#                 sys.exit()
#         else:
#             print "WARNING!!! Incorect connection type. Serial connection assumed"
         
    def OpenPort(self):
        '''Open serial port.''' 
        if self.ser.isOpen()==False:  
            try:
                self.ser.open()            
                time.sleep(0.5) # time for the power source to process the query
            except ValueError:
                print 'ERROR!!! A parametter has been initialized with an incorect value.'
                print "The script will now stop because it can't initialize the communication with the device"
                sys.exit()
            except SerialException:
                print 'ERROR!!! The device can not be found or can not be configured'
                print "The script will now stop because it can't initialize the communication with the device"
                sys.exit()
        else:
            print 'Serial port already opened'
            
    def ClosePort(self):
        '''Close serial port.'''
        if self.ser.isOpen()==True:
            self.ser.close()
        else:
            print 'Unopened serial port'
        
    def PrintPortConfiguration(self):
        '''Prints the port configuration'''
        if self.connType is 'SERIAL':
            print self.ser
#         if self.connType is 'USB':
#             print dev
        
    def SendCommand(self, data):
        '''Send user command to power source. More information about compatible commands is found in the power source manual.'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write(data + '\n')
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,data+'\n')
        time.sleep(0.11) # time for the power source to process the query
        
    def SetOutputON(self, channel=1):
        '''Turns the output to ON.'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write("INST OUT"+str(channel)+"\n")
                time.sleep(0.11)
                self.ser.write('OUTP ON\n')
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,"INST OUT"+str(channel)+"\n")
#             time.sleep(0.11)
#             self.dev.write(self.outAddr,'OUTP ON\n')
        time.sleep(0.11) # time for the power source to process the query
        
    def SetOutputOFF(self=1):
        '''Turns the output to OFF.'''    
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write('OUTP OFF\n')
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,'OUTP OFF\n')
        time.sleep(0.11) # time for the power source to process the query
        
    def SetAmplitude(self,val=1):
        '''Sets the output voltage'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write("VOLT "+str(val)+"\n")
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,"VOLT "+str(val)+"\n")
        time.sleep(0.11)
    
    def GetAmplitude(self):
        '''Returns the output voltage value'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write("VOLT?"+"\n")
                time.sleep(0.11)
                value=self.ser.read(7)
            else:
                print 'Unopened serial port'
                return -1
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,"VOLT?"+"\n")
#             time.sleep(0.11)
#             aux=self.dev.read(self.inAddr,256)
#             value=''.join(chr(i) for i in aux)
#             value=value[2:]
        return value
        
    def Reset(self):
        '''Resets the device parameters'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write("*RST\n")
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,"*RST\n")
        time.sleep(0.11)
    
    def SetFrequency(self,val):
        '''Sets the signal frequency'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write("FREQ "+str(val)+"\n")
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,"FREQ "+str(val)+"\n")
        time.sleep(0.11)
        
    def SetSinWaveform(self):
        '''Sets a sinusoidal waveform'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write("FUNC SIN\n")
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,"FUNC SIN\n")
        time.sleep(0.11)
        
    def SetSquareWaveform(self,dutyCycle=-1):
        '''Sets a square waveform'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                if dutyCycle>-1:
                    self.ser.write("FUNC:SQU:DCYC "+str(dutyCycle)+"\n")
                    time.sleep(0.11)
                self.ser.write("FUNC SQU\n")
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             if dutyCycle>-1:
#                 self.dev.write(self.outAddr,"FUNC:SQU:DCYC "+str(dutyCycle)+"\n")
#                 time.sleep(0.11)
#             self.dev.write(self.outAddr,"FUNC SQU\n")
        time.sleep(0.11)
        
    def SetPulseWaveform(self,dutyCycle=-1):
        '''Sets a pulse waveform'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                if dutyCycle>-1:
                    self.ser.write("FUNC:PULS:DCYC "+str(dutyCycle)+"\n")
                    time.sleep(0.11)
                self.ser.write("FUNC PULS\n")
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             if dutyCycle>-1:
#                 self.dev.write(self.outAddr,"FUNC:PULS:DCYC "+str(dutyCycle)+"\n")
#                 time.sleep(0.11)
#             self.dev.write(self.outAddr,"FUNC PULS\n")
        time.sleep(0.11)
        
    def SetRampWaveform(self,symmetry=-1):
        '''Sets a ramp waveform'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                if symmetry>-1:
                    self.ser.write("FUNC:RAMP:SYMM "+str(symmetry)+"\n")
                    time.sleep(0.11)
                self.ser.write("FUNC RAMP\n")
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             if symmetry>-1:
#                 self.dev.write(self.outAddr,"FUNC:RAMP:SYMM "+str(symmetry)+"\n")
#                 time.sleep(0.11)
#             self.dev.write(self.outAddr,"FUNC RAMP\n")
        time.sleep(0.11)
    
    def SetArbitraryWaveform(self,waveForm='SIN'):
        '''Sets a ramp waveform'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write("FUNC:ARB "+waveForm+"\n")
                time.sleep(0.11)
                self.ser.write("FUNC ARB\n")
            else:
                print 'Unopened serial port'
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,"FUNC:ARB "+waveForm+"\n")
#             time.sleep(0.11)
#             self.dev.write(self.outAddr,"FUNC ARB\n")
        time.sleep(0.11)
        
    def GetWaveformType(self):
        '''Returns the waveform type'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write("FUNC?\n")
                time.sleep(0.11)
                value=self.ser.read(4)
            else:
                print 'Unopened serial port'
                return -1
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,"FUNC ?\n")
#             time.sleep(0.11)
#             aux=self.dev.read(self.inAddr,256)
#             value=''.join(chr(i) for i in aux)
            #value=value[2:]
        return value
    
    def GetWaveformParameter(self):
        '''Returns the waveform parameter(dutycycle / symmetry / arbitrary selected)'''
        if self.connType is 'SERIAL':
            if self.ser.isOpen()==True:
                self.ser.write("FUNC?\n")
                time.sleep(0.11)
                value=self.ser.read(4)
                if 'SQU' in value:
                    self.ser.write("FUNC:SQU:DCYC?\n")
                    time.sleep(0.11)
                    value=self.ser.read(7)
                    value=float(value)*10
                if 'PULS' in value:
                    self.ser.write("FUNC:PULS:DCYC?\n")
                    time.sleep(0.11)
                    value=self.ser.read(7)
                    value=float(value)*10
                if 'RAMP' in value:
                    self.ser.write("FUNC:RAMP:SYMM?\n")
                    time.sleep(0.11)
                    value=self.ser.read(5)
                    value=float(value)*10
                if 'ARB' in value:
                    self.ser.write("FUNC:ARB?\n")
                    time.sleep(0.11)
                    value=self.ser.read(5)
            else:
                print 'Unopened serial port'
                return -1
#         if self.connType is 'USB':
#             self.dev.write(self.outAddr,"FUNC ?\n")
#             time.sleep(0.11)
#             aux=self.dev.read(self.inAddr,256)
#             value=''.join(chr(i) for i in aux)
            #value=value[2:]
        return value