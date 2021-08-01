'''
    Author: user
    Purpose: Test of SWT MODULE Requirement: TSC_MODULE_ID
    Date: DD.MM.YYYY   
    Arguments: -  
    Outputs: -   
    Dependencies: -

    History:
    ------------------------------------------------------------------------------
    Revision | Date:      | Modification:                             | Author
    .......................................................................
    v0.1     | DD.MM.YYYY | Creation                                  | user
    ------------------------------------------------------------------------------
'''

from PlatformFiles import *
from _UserFunctions import *

FAILED, PASSED, NORUN, ERROR = 0, 1, 2, 3

def TEST_N(testcase):
    testcase.time_begin = time.ctime(time.time())
    
    testcase.description = """ Write here the requirements or what this test case cover. """
    testcase.traceability = 'REQ_N'      # REQ_1, REQ_2, ... ,REQ_n (ex. testcase.traceability = 'TSC_LCE_99, TSC_SI_43' / LCE - Exterior Lights, SI - Safety Integrity)
    testcase.safety_requirement = 'No'   # Yes / No
    
    try:
        testplan = TestPlan()
       
        # TEST CASE CODE AREA BEGIN
        
#         #################################################################################
#         #                             DEBUGGER EXAMPLE - most used                      #
#         #################################################################################
#         
#         cMgr = ic.ConnectionMgr()                                               # create the winIDEA connection
#         cMgr.connectMRU('')                                                     # initialize winIDEA
#         dbg = ic.CDebugFacade(cMgr)                                             # get winIDEA instance
#         
#         dbg.stop()                                                              # Stops the execution.
#         dbg.deleteAll()                                                         # Deletes all execution breakpoints.
#         dbg.deleteBP("foo_")                                                    # Deletes breakpoint at the function, given symbol name.
#         dbg.reset()                                                             # Resets the target.
#         dbg.run()                                                               # Runs the program.
#         dbg.download()                                                          # Downloads executable to the target.
#         dbg.evaluate(IConnectDebug.fRealTime, 'var_global').getInt()            # Evaluate value from a global variable, given symbol name. Returns integer value for bit sizes 8, 16, and 32.
#         dbg.evaluate(IConnectDebug.fMonitor, 'var_local').getInt()              # Evaluate value from a local variable, given symbol name. Returns integer value for bit sizes 8, 16, and 32.
#         dbg.evaluate(IConnectDebug.fMonitor, '@R6').getInt()                    # Evaluate value from a register. Returns integer value for bit sizes 8, 16, and 32.
#         dbg.evaluate(IConnectDebug.fMonitor, '*(uint32*)(0xB16B00B5)').getInt() # Evaluate value from an address. Returns integer value for bit sizes 8, 16, and 32.
#         dbg.modify(IConnectDebug.fRealTime, 'var_global', '255')                # Modify value from a global variable, given symbol name.
#         dbg.modify(IConnectDebug.fMonitor, 'var_local', '255')                  # Modify value from a local variable, given symbol name.
#         dbg.modify(IConnectDebug.fMonitor, '@R6', '11')                         # Modify value from a register.
#         dbg.modify(IConnectDebug.fMonitor, '*(uint32*)(0xB16B00B5)', '11')      # Modify value from an address.
#         dbg.waitUntilStopped()                                                  # This method returns when CPU is stopped.
#         dbg.waitUntilStopped(2000)                                              # This method returns when CPU is stopped or timeout expires in 2 seconds. (true if CPU is in stopped state, false if timeout expired)
#         dbg.runUntilReturn()                                                    # Runs the program until return. 
#         dbg.stepHigh()                                                          # Steps one statement in the source code.
#         dbg.stepOverHigh()                                                      # Steps one statement in the source code, does not enter functions.
#         dbg.stepInst()                                                          # Executes one machine instruction.
#         dbg.stepOverInst()                                                      # Executes one machine instruction, does not enter subroutines.
#         status = dbg.getCPUStatus(True)                                         # Returns execution status of the target.
#         status.isStopped()                                                      # Returns true, if CPU is stopped.
#         status.isRunning()                                                      # Returns true, if CPU is running.
#         status.isReset()                                                        # Returns true, if CPU is held in reset.
#         status.isHalted()                                                       # Returns true, if CPU is halted by target.
#         
#         # ---------------------------------------------------------------------------
#         
#         # search for a particular line inside the code (avoid using spaces in the searched text)
#         lineFound = 0
#         while (lineFound == 0):
#             status = dbg.getCPUStatus(True)
#             if 'break;' in dbg.getSymbolAtAddress(ic.IConnectDebug.sFunctions, status.getExecutionArea(), status.getExecutionPoint(), ic.IConnectDebug.sSourceCode).strip():
#                 lineFound = 1
#                 var1 = dbg.evaluate(IConnectDebug.fRealTime, 'var1').getInt()
#                 dbg.modify(IConnectDebug.fRealTime, 'var2', str(var1))
#                 break
#             else:
#                 dbg.stepOverHigh()
#         
#         # ---------------------------------------------------------------------------
#         
#         # measure the cyclicity of a function or between two execution stops
#         timerMs = '*(uint32*)(0xFFF3C004)' # STM System Timer Module address, MPC5646C microcontroller (if your project use a different microcontroller then you should look for a different timer/counter or variable name which is incremented every ms or less)
#         functionName = 'foo_'
#         
#         dbg.deleteAll() # delete all breakpoints
#         dbg.stop()
#         dbg.reset()
#     
#         dbg.setBP(functionName)
#         dbg.run()
#         dbg.waitUntilStopped()
#         firstTime = dbg.evaluate(IConnectDebug.fRealTime, timerMs).getLong() # STM System Timer Module - in microseconds
#      
#         dbg.run()
#         dbg.waitUntilStopped()
#         secondTime = dbg.evaluate(IConnectDebug.fRealTime, timerMs).getLong() # STM System Timer Module - in microseconds
#      
#         dbg.deleteAll()
#      
#         print 'First time:', firstTime, 'microseconds'
#         print 'Second time:', secondTime, 'microseconds'
#         print 'Cycle time:', (secondTime - firstTime)/float(1000), 'milliseconds'
#         print 'Rounded cycle time:', round((secondTime - firstTime)/float(1000), 2) # - in milliseconds
#      
# 
#         #################################################################################
#         #                                DOORS EXAMPLE                                  #
#         #################################################################################
#         
#         precondition = testplan.addPrecondition()
#         precondition.addChildPrecondition("stop target")
#         precondition.addChildPrecondition("delete all breakpoints")
#         precondition.addChildPrecondition("reset target")
#         precondition.addChildPrecondition("run target")
#         precondition.addChildPrecondition("full communication")
#         precondition.addChildPrecondition("battery voltage at 12V")
#         precondition.addChildPrecondition("KL.15")
#          
#         step_1 = testplan.addStep()
#         step_1.addChildStep("1. Set breakpoint to foo_ function.")
#         step_1.addChildStep("- run target")
#         step_1.addChildStep("- wait until stopped")
#          
#         step_2 = testplan.addStep()
#         step_2.addChildStep("2. Read value from variable var_1")
#         step_2.addChildStep("- run target")
#         step_2.addChildStep("- wait until stopped")
#         step_2.addComment("2. Breakpoint reached at foo_ function.")
#          
#         step_3 = testplan.addStep()
#         step_3.addChildStep("3. Read value from variable var_2")
#         step_3.addExpectedResult("3. var_1 = var_2 = E_OK")
#         step_3.addComment("3. E_OK = 1")
#         step_3.addTesterComment("3. Tested on v1.x, v2.x and v3.x variants.")
# 
# 
#         #################################################################################
#         #                           VECTOR EXAMPLE                                      #
#         #################################################################################
#         
#         # This function store in a list the messages from CAN for a period of time and returns it.
#         # params: seconds
#         print CAN_ReadMultipleMessages_return(20)
#         
#         # This function prints to console the messages from CAN for a period of time.
#         # params: seconds
#         CAN_ReadMultipleMessages_print(20)
#         
#         # this function send one CAN message to channel 1
#         # params: id, data, channel
#         WriteMessageOnce(0x01, [0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80], 1)
#         
#         # this function sends a CAN message for a specific time to channel 2
#         # params: seconds, id, data, cycle time, channel
#         WriteMessageMultiple(20, 0x01, [0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80], 0.01, 2) 
#         
#         # this thread is used to send a CAN message  through channel 3, while different parallel executions are made (ex. winIDEA manipulation while a CAN message is sent)
#         # params: id, data, cycle time, channel
#         thrd = WriteCAN_Thread(0x01, [0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80], 0.01, 3) 
#         thrd.start()
#         time.sleep(20) # wait 20 seconds
#         thrd.stop()
#         
#         #################################################################################
#         #                           DBC PARSER EXAMPLE                                  #
#         #################################################################################
#         
#         dbcParser = DBC_Parser('FA_CAN.dbc')                        # Load database which contain the CAN message.
#         
#         msg = CANMessage(dbcParser, "V_VEH")                        # Initialize an CAN message.
#         msg.data = msg.SetSignalValue("CRC_V_VEH", "0xFF")          # Set signal value from the CAN message.
#         msg.data = msg.SetSignalValue("ALIV_V_VEH", "0x0A")         # Set signal value from the CAN message.
#         msg.data = msg.SetSignalValue("ST_V_VEH_NSS", "0x03")       # Set signal value from the CAN message.
#         msg.data = msg.SetSignalValue("V_VEH_COG", "0x2A3B")        # Set signal value from the CAN message.
#         msg.data = msg.SetSignalValue("QU_V_VEH_COG", "0x08")       # Set signal value from the CAN message.
#         msg.data = msg.SetSignalValue("DVCO_VEH", "0x03")           # Set signal value from the CAN message.
#         
#         print msg.data                                              # Print the message data.
#         
#         msg.StartSending()                                          # Start sending the CAN message.
#         time.sleep(5)                                               # Wait 5 seconds.
#         msg.StopSending()                                           # Stop sending the CAN message.
#         
#         
#         #################################################################################
#         #                   LDF PARSER EXAMPLE - Master/Slave                           #
#         #################################################################################
#         
#         ldfParser = LIN_Parser("K_LIN_08.LDF")              # Load database which contain the LIN node.
# 
#         frame = LINFrame(ldfParser, "ST_FAS_LIN")           # Initialize a LIN frame.
#         frame.SetSignalValue("ST_LED_IBRK_DRS_LIN", 0x01)   # Set signal value from the LIN frame.
#         
#         print frame.GetSignalValue("ST_LED_IBRK_DRS_LIN")   # Print the value of the signal.
#         
#         master = LINNode(ldfParser, "RUN_MAIN")             # Creates a LINNode object.
#         master.AddFrame(frame)                              # Add a frame to the LINNode object.
# 
#         framesList = master.GetFrames()                     # Get the list of frames from the LINNode object
#         for frameObj in framesList:
#             print "name:", frameObj.name                    # Print the name of the first frame of the LINNode object
#             print "id:", frameObj.frameID                   # Print the frameID of the first frame of the LINNode object
#             for sgn in frameObj.signals:
#                 print "signal - name:", sgn.name
# 
#         master.StartSending()                               # Start LIN frame.
#         time.sleep(5)                                       # Wait 5 seconds.
#         master.StopSending()                                # Stop LIN frame.
# 
#         
#         #################################################################################
#         #                           POWER SUPPLY EXAMPLE                                #
#         #################################################################################
#         
#         ps = PowerSourceInstance()  # get Power Source instance based on CONFIGURATION.cfg
#         ps.OpenPort()               # Open serial port.
#         ps.PrintPortConfiguration() # Print serial connection settings.
#         ps.SetCurrent(5, 1)         # Sets the Output Current value in Amperes.
#         ps.SetVoltage(9, 1)         # Sets the output voltage value in Volts.
#         ps.SetOutputON(1)           # Turns the output to ON.
#         time.sleep(1)               # wait 1 second or use winIDEA / Vector instructions | time.sleep is used as NOP in this case
#         ps.SetVoltage(10, 1)        # Sets the output voltage value in Volts.
#         time.sleep(1)               # wait 1 second or use winIDEA / Vector instructions | time.sleep is used as NOP in this case
#         ps.SetVoltage(11, 1)        # Sets the output voltage value in Volts.
#         time.sleep(1)               # wait 1 second or use winIDEA / Vector instructions | time.sleep is used as NOP in this case
#         ps.SetVoltage(12, 1)        # Sets the output voltage value in Volts.
#         time.sleep(1)               # wait 1 second or use winIDEA / Vector instructions | time.sleep is used as NOP in this case
#         ps.SetVoltage(16, 1)        # Sets the output voltage value in Volts.
#         time.sleep(1)               # wait 1 second or use winIDEA / Vector instructions | time.sleep is used as NOP in this case
#         ps.SetVoltage(12, 1)        # Sets the output voltage value in Volts.
#         time.sleep(1)               # wait 1 second or use winIDEA / Vector instructions | time.sleep is used as NOP in this case
#         ps.SetOutputOFF(1)          # Turns the output to OFF.
#         ps.ClosePort()              # Close serial port.
        
        # TEST CASE CODE AREA END
   
        testcase.result = FAILED
        testcase.time_end = time.ctime(time.time())
        return testplan.export()
    except:
        testcase.result = ERROR
        testcase.time_end = time.ctime(time.time())
        print "Unexpected error:", sys.exc_info()[1] 