'''
Created on Apr 2 ,  2015

@author :  uidr0108
'''

from PlatformFiles import *
from _UserFunctions import *
import threading

'''Create a DBC parser object, parse a *.DBC file and memorize the necesary data'''
dbcParser = DBC_Parser('FA_CAN.dbc')  #create a DBC file parser

'''Create a CAN message, set the values of its signals and print the message data'''
msg = CANMessage(dbcParser, "V_VEH")                        #initialize a message from 2nd parser
msg.data = msg.SetSignalValue("CRC_V_VEH", "0xFF")          #set a value for a signal from the initialized message
msg.data = msg.SetSignalValue("ALIV_V_VEH", "0x0A")          #set a value for a signal from the initialized message
msg.data = msg.SetSignalValue("ST_V_VEH_NSS", "0x03")        #set a value for a signal from the initialized message
msg.data = msg.SetSignalValue("V_VEH_COG", "0x2A3B")        #set a value for a signal from the initialized message
msg.data = msg.SetSignalValue("QU_V_VEH_COG", "0x08")        #set a value for a signal from the initialized message
msg.data = msg.SetSignalValue("DVCO_VEH", "0x03")           #set a value for a signal from the initialized message
print msg.data  

'''Create a new thread and send the message'''               
msg.StartSending()    #send the initialized message on CAN

'''Wait for 5 seconds and then stop the trasmision'''
time.sleep(5)             # wait 5 seconds
msg.StopSending()     #stop sending the message

print 'done'