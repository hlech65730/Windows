'''
    Author: Laurentiu Nitu
    Purpose: Test of SWT ReqModule Requirement: TSC_ReqModule_6
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

def TEST_4(testcase):
    testcase.time_begin = time.ctime(time.time())
    
    testcase.description = """REQ_06: The foo shall be called every 20ms."""
    testcase.traceability = 'REQ_06'
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
        
        step_1 = testplan.addStep()
        step_1.addChildStep("1. Set breakpoint to foo function")
        
#         dbg.setBP('Rte_Write_SafeCaf_cafState_cafState')
        
        step_2 = testplan.addStep()
        step_2.addChildStep("2. Run target")
        step_2.addChildStep("- wait until stopped")
        
#         dbg.run()
#         dbg.waitUntilStopped()
        
        step_3 = testplan.addStep()
        step_3.addChildStep("3. Evaluate start time = value of STM System Timer Module (address: 0xFFF3C004)")
        
#         firstTime = dbg.evaluate(IConnectDebug.fRealTime, '*(uint32*)(0xFFF3C004)').getLong()
        
        step_4 = testplan.addStep()
        step_4.addChildStep("4 Run target")
        step_4.addChildStep("- wait until stopped")
        
#         dbg.run()
#         dbg.waitUntilStopped()
        
        step_5 = testplan.addStep()
        step_5.addChildStep("5. Evaluate stop time = value of STM System Timer Module (address: 0xFFF3C004)")
        step_5.addExpectedResult('5. (stop time - start time) <= 20ms')
        
#         secondTime = dbg.evaluate(IConnectDebug.fRealTime, '*(uint32*)(0xFFF3C004)').getLong()
        
#         cycleTime = (secondTime - firstTime)/1000
#         print 'Cycle time:', cycleTime, 'milliseconds'
#         if cycleTime <= 20:
#             testcase.result = PASSED
#         else:
#             testcase.result = FAILED
            
        dbg.deleteAll() # delete all breakpoints
        dbg.run()
        
#         testcase.result = FAILED
        testcase.time_end = time.ctime(time.time())
        return testplan.export()
    
    except:
        print "Unexpected error:", sys.exc_info()[1]
        testcase.result = ERROR
        testcase.time_end = time.ctime(time.time())
