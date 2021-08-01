'''
    Author: Laurentiu Nitu
    Purpose: Test of SWT ReqModule Requirement: TSC_ReqModule_8
    Date: 05.03.2015    
    Arguments: -   
    Outputs: -    
    Dependencies: -

    History:
    ------------------------------------------------------------------------------
    Revision | Date:      | Modification:                             | Author
    .......................................................................
    v0.1     | 05.03.2015 | Creation                                  | L. Nitu 
    ------------------------------------------------------------------------------
'''

from PlatformFiles import *
from _UserFunctions import *

FAILED, PASSED, NORUN, ERROR = 0, 1, 2, 3

def TEST_6(testcase):
    testcase.time_begin = time.ctime(time.time())
    
    testcase.description = """REQ_08: SafePWMThreshold = min( ( 8,4V / (U_KL30 - 2V) )^2; 1)"""
    testcase.traceability = 'REQ_08'
    testcase.safety_requirement = 'Yes'
   
    try:
        testplan = TestPlan()
        
        precondition = testplan.addPrecondition()
        precondition.addChildPrecondition("- stop target")
        precondition.addChildPrecondition("- delete all breakpoints")
        precondition.addChildPrecondition("- reset target")
        
#         cMgr = ic.ConnectionMgr()
#         cMgr.connectMRU('') # initialize the target
#         dbg = ic.CDebugFacade(cMgr)
#         exeCtrl = ic.CExecutionController(cMgr)
# 
#         ps = PowerSourceInstance()
#         ps.OpenPort()
#         ps.PrintPortConfiguration()
#         ps.SetCurrent(5, 1)
#         
#         dbg.run()
        
        step_1 = testplan.addStep()
        step_1.addChildStep("1. Set output voltage from power source to 9 volts.")
        
#         ps.SetVoltage(9, 1)
#         ps.SetOutputON(1)
        
        step_1.addChildStep("- set breakpoint to x function")
        step_1.addChildStep("- wait until stopped")
        step_1.addChildStep("- run until return")
        
#         dbg.setBP('x')
#         dbg.waitUntilStopped()
#         dbg.runUntilReturn()
        
        step_1 = testplan.addStep()
        step_1.addChildStep('1. Read value from SafePWMThreshold variable')
        step_1.addExpectedResult('1. SafePWMThreshold == 0xC837')
        
#         print (dbg.evaluate(IConnectDebug.fRealTime, 'SafePWMThreshold').getInt() & 0xFF00) >> 8
#         dbg.run()
       
        step_2 = testplan.addStep()
        step_2.addChildStep("2. Set output voltage from power source to 10 volts.")
        
#         ps.SetVoltage(10, 1)
        
        step_2.addChildStep("- set breakpoint to x function")
        step_2.addChildStep("- wait until stopped")
        step_2.addChildStep("- run until return")
        
#         dbg.setBP('x')
#         dbg.waitUntilStopped()
#         dbg.runUntilReturn()
        
        step_2 = testplan.addStep()
        step_2.addChildStep('2. Read value from SafePWMThreshold variable')
        step_2.addExpectedResult('2. SafePWMThreshold == 0xC837')
        
#         print (dbg.evaluate(IConnectDebug.fRealTime, 'SafePWMThreshold').getInt() & 0xFF00) >> 8
#         dbg.run()
        
        step_3 = testplan.addStep()
        step_3.addChildStep("3. Set output voltage from power source to 11 volts.")
        
#         ps.SetVoltage(11, 1)
        
        step_3.addChildStep("- set breakpoint to x function")
        step_3.addChildStep("- wait until stopped")
        step_3.addChildStep("- run until return")
        
#         dbg.setBP('x')
#         dbg.waitUntilStopped()
#         dbg.runUntilReturn()
        
        step_3 = testplan.addStep()
        step_3.addChildStep('3. Read value from SafePWMThreshold variable')
        step_3.addExpectedResult('3. SafePWMThreshold == 0xC837')
        
#         print (dbg.evaluate(IConnectDebug.fRealTime, 'SafePWMThreshold').getInt() & 0xFF00) >> 8
#         dbg.run()
        
        step_4 = testplan.addStep()
        step_4.addChildStep("4. Set output voltage from power source to 12 volts.")
        
#         ps.SetVoltage(12, 1)
        
        step_4.addChildStep("- set breakpoint to x function")
        step_4.addChildStep("- wait until stopped")
        step_4.addChildStep("- run until return")
        
#         dbg.setBP('x')
#         dbg.waitUntilStopped()
#         dbg.runUntilReturn()
        
        step_4 = testplan.addStep()
        step_4.addChildStep('4. Read value from SafePWMThreshold variable')
        step_4.addExpectedResult('4. SafePWMThreshold == 0xC837')
        
#         print (dbg.evaluate(IConnectDebug.fRealTime, 'SafePWMThreshold').getInt() & 0xFF00) >> 8
#         dbg.run()
       
        step_5 = testplan.addStep()
        step_5.addChildStep("1. Set output voltage from power source to 16 volts.")
        
#         ps.SetVoltage(16, 1)
        
        step_5.addChildStep("- set breakpoint to x function")
        step_5.addChildStep("- wait until stopped")
        step_5.addChildStep("- run until return")
        
#         dbg.setBP('x')
#         dbg.waitUntilStopped()
#         dbg.runUntilReturn()
        
        step_5 = testplan.addStep()
        step_5.addChildStep('5. Read value from SafePWMThreshold variable')
        step_5.addExpectedResult('5. SafePWMThreshold == 0xC837')
        
#         print (dbg.evaluate(IConnectDebug.fRealTime, 'SafePWMThreshold').getInt() & 0xFF00) >> 8
       
       
#         ps.SetVoltage(12, 1)
#         ps.ClosePort()
#         dbg.deleteAll() # delete all breakpoints
#         dbg.run()

        testcase.result = PASSED
        testcase.time_end = time.ctime(time.time())
        return testplan.export()
    except:
        testcase.result = ERROR
        testcase.time_end = time.ctime(time.time())
        print "Unexpected error:", sys.exc_info()[1] 