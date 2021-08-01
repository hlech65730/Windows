'''
Created on Jun 15, 2015

@author: uidr0108
'''

from PlatformFiles import *

ldfParser = LIN_Parser("K_LIN_08.LDF")      # Create a LDF_Parser object and parse the 'filename.ldf' file

frame = LINFrame(ldfParser, "CTR_LP_SW_LIN")           # Create a LINFrame object with the name 'CTR_LP_SW_LIN'. The frame data will be 
                                                       # read from the ldfParser
frame.SetSignalValue("CTR_LOWB_FN_LED_LIN", 0x01)      # Sets the value of signal 'CTR_LOWB_FN_LED_LIN' to '0x01'
print frame.GetSignalValue("CTR_LOWB_FN_LED_LIN")      # Prints the value of the signal 'CTR_LOWB_FN_LED_LIN'

slave = LINNode(ldfParser)   # Creates a LINNode object
slave.AddFrame(frame)        # Add a frame to the LINNode object

framesList = slave.GetFrames()                  # Get the list of frames from the LINNode object
for frameObj in framesList:
    print "name:", frameObj.name                # Print the name of the first frame of the LINNode object
    print "id:", frameObj.frameID               # Print the frameID of the first frame of the LINNode object
    for sgn in frameObj.signals:
        print "signal - name:", sgn.name

slave.StartSending()     # Opens the thread thrd and and starts sending the message

time.sleep(5)
slave.StopSending()      # Stops sending the message and closes the thread on which the message is being sent

print 'done'