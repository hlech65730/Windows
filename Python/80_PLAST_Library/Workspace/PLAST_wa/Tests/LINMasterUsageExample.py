'''
Created on Jul 21, 2015

@author: uidr0108
'''

from PlatformFiles import *

ldfParser = LIN_Parser("K_LIN_08.LDF")      # Create a LDF_Parser object and parse the 'filename.ldf' file

frame = LINFrame(ldfParser, "ST_FAS_LIN")           # Create a LINFrame object with the name 'frameName'. The frame data will be 
                                                    # Read from the ldfParser
frame.SetSignalValue("ST_LED_IBRK_DRS_LIN", 0x01)   # Sets the value of signal 'signalName' to '0x01'
print frame.GetSignalValue("ST_LED_IBRK_DRS_LIN")   # Prints the value of the signal 'signalName'

master = LINNode(ldfParser, "RUN_MAIN")          # Creates a LINNode object
master.AddFrame(frame)                           # Add a frame to the LINNode object

framesList = master.GetFrames()     # Get the list of frames from the LINNode object
for frameObj in framesList:
    print "name:", frameObj.name                # Print the name of the first frame of the LINNode object
    print "id:", frameObj.frameID               # Print the frameID of the first frame of the LINNode object
    for sgn in frameObj.signals:
        print "signal - name:", sgn.name
    
master.StartSending()     # Opens the thread thrd and and starts sending the message

time.sleep(5)
master.StopSending()      # Stops sending the message and closes the thread on which the message is being sent

print "done"