'''
    Author: Laurentiu Nitu
    Purpose: Test of SWT ReqModule Requirement: TSC_ReqModule_4
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

def TEST_2(testcase):
    testcase.time_begin = time.ctime(time.time())
    
    testcase.description = """REQ_04: On each reported test passed event, foo shall decrement the corresponding counter by a configured value down to min. limit = 0."""
    testcase.traceability = 'REQ_04'
    testcase.safety_requirement = 'Yes'
    
    
    try:
        testplan = TestPlan()
        
        resultList = []
        
        precondition = testplan.addPrecondition()
        precondition.addChildPrecondition("- stop target")
        precondition.addChildPrecondition("- delete all breakpoints")
        precondition.addChildPrecondition("- reset target")
        
#         cMgr = ic.ConnectionMgr()
#         cMgr.connectMRU('') # initialize the target
#         dbg = ic.CDebugFacade(cMgr)
#         dbg.stop()
#         dbg.deleteAll() # delete all breakpoints
#         dbg.reset()
        
        step_1 = testplan.addStep()
        step_1.addChildStep("1. Set breakpoint to foo function")
        step_1.addChildStep('- run target')
        step_1.addChildStep('- wait until stopped')
        
#         dbg.setBP('foo')
#         dbg.run()
#         dbg.waitUntilStopped()
        
        step_2 = testplan.addStep()
        step_2.addChildStep("2. modify counter value with 2")
        
#         dbg.modify(IConnectDebug.fMonitor, 'counter', '2')
        
        step_3 = testplan.addStep()
        step_3.addChildStep("3. run target")
        step_3.addChildStep("- wait until stopped")
        
#         dbg.run()
#         dbg.waitUntilStopped()
        
        step_4 = testplan.addStep()
        step_4.addChildStep("4. Read counter value")
        step_4.addExpectedResult('4. counter = 1')
        
#         resultList.append(hex(dbg.evaluate(IConnectDebug.fRealTime, 'counter').getInt()))
        
        step_5 = testplan.addStep()
        step_5.addChildStep("5. run target")
        step_5.addChildStep("- wait until stopped")
        
#         dbg.run()
#         dbg.waitUntilStopped()
        
        step_6 = testplan.addStep()
        step_6.addChildStep("6. Read counter value")
        step_6.addExpectedResult('6. counter = 0')
        
#         resultList.append(hex(dbg.evaluate(IConnectDebug.fRealTime, 'counter').getInt()))
        
        step_7 = testplan.addStep()
        step_7.addChildStep("7. run target")
        step_7.addChildStep("- wait until stopped")
        
#         dbg.run()
#         dbg.waitUntilStopped()
        
        step_8 = testplan.addStep()
        step_8.addChildStep("8. Read counter value")
        step_8.addExpectedResult('8. counter = 0')
        
#         resultList.append(hex(dbg.evaluate(IConnectDebug.fRealTime, 'counter').getInt()))
#         if (resultList[0] == '1') and (resultList[1] == '0') and (resultList[2] == '0'):
#             testcase.result = PASSED
#         else:
#             testcase.result = FAILED
#
#         dbg.deleteAll() # delete all breakpoints
#         dbg.run()
        testcase.result = NORUN
        testcase.time_end = time.ctime(time.time())
        return testplan.export()
    
    except:
        testcase.result = ERROR
        testcase.time_end = time.ctime(time.time())
        print "Unexpected error:", sys.exc_info()[1]
