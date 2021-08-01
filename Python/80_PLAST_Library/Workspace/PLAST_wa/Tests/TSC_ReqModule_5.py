'''
    Author: Laurentiu Nitu
    Purpose: Test of SWT ReqModule Requirement: TSC_ReqModule_5
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

def TEST_3(testcase):
    testcase.time_begin = time.ctime(time.time())
    
    testcase.description = """REQ_05: After reset the foo_init shall be called."""
    testcase.traceability = 'REQ_05'
    testcase.safety_requirement = 'No'
    
    try:
        testplan = TestPlan()
        
#         cMgr = ic.ConnectionMgr() # Get the connection
#         cMgr.connectMRU('')       # initialize the target
#         dbg = ic.CDebugFacade(cMgr)
         
        precondition = testplan.addPrecondition()
        precondition.addChildPrecondition("- stop target")
        precondition.addChildPrecondition("- delete all breakpoints")
        precondition.addChildPrecondition("- reset target")
        
        
        dbg.stop() # error - leaved as example 
#         dbg.deleteAll() # delete all breakpoints
#         dbg.reset()
        
        step_1 = testplan.addStep()
        step_1.addChildStep("1. Set breakpoint to foo_init function")
        step_1.addChildStep("- run target")
        step_1.addChildStep("- wait until stopped")
        step_1.addExpectedResult('1. Breakpoint is reached at foo_init function.')
        
#         dbg.setBP("foo_init")
#         dbg.run()
         
        # the result will be PASSED if the breakpoint is reached in max 2 seconds
        testcase.result = FAILED
#         if dbg.waitUntilStopped(2000):
#             testcase.result = PASSED
    
        testcase.time_end = time.ctime(time.time())
        return testplan.export()
    
    except:
        print "Unexpected error:", sys.exc_info()[1]
        testcase.result = ERROR
        testcase.time_end = time.ctime(time.time())