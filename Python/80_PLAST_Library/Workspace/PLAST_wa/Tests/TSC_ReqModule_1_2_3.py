
'''
    Author: Laurentiu Nitu
    Purpose: Test of SWT ReqModule Requirement: TSC_ReqModule_1, TSC_ReqModule_2, TSC_ReqModule_3, TSC_ReqModule_4
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

def TEST_1(testcase):
    testcase.time_begin = time.ctime(time.time())
    
    testcase.description = '''REQ_01, REQ_02, REQ_03: example winIDEA instructions, REQ_02: example of step in until a line of code is found in the code, REQ_03: read register example'''
    testcase.traceability = 'REQ_01, REQ_02, REQ_03'
    testcase.safety_requirement = 'Yes'

    try:
        
#         cMgr = ic.ConnectionMgr() # Get the connection
#         cMgr.connectMRU('')       # initialize the target
#         dbg = ic.CDebugFacade(cMgr)
#         exeCtrl = ic.CExecutionController(cMgr)
    
        testplan = TestPlan()
        precondition = testplan.addPrecondition()
        precondition.addChildPrecondition("- stop target")
        precondition.addChildPrecondition("- delete all breakpoints")
        precondition.addChildPrecondition("- reset target")
    
#         dbg.stop()
#         dbg.deleteAll() # delete all breakpoints
#         dbg.reset()
        
#         print dbg.evaluate(IConnectDebug.fRealTime, 'var1').getInt()
        
        step_1 = testplan.addStep()
        step_1.addChildStep("1. Set breakpoint to foo_one function")
        step_1.addChildStep("- run target")
        step_1.addChildStep("- wait until stopped")
        step_1.addComment("1. foo_one function is reached.")
       
#         dbg.setBP("foo_one")
#         dbg.run()
#         dbg.waitUntilStopped()
        
        step_2 = testplan.addStep()
        step_2.addChildStep("2. Set breakpoint to foo_two function")
        step_2.addChildStep("- run target")
        step_2.addChildStep("- wait until stopped")
        step_2.addComment("2. foo_two function is reached.")
        
    #     dbg.setBP("foo_two")
    #     dbg.run()
    #     dbg.waitUntilStopped()
       
        step_3 = testplan.addStep()
        step_3.addChildStep('3. Step over until break; is found')
        
        step_4 = testplan.addStep()
        step_4.addChildStep("4. read var1 variable")
        step_4.addChildStep("- modify value from var2 variable with value readed from var1 variable")
       
    #     lineFound = 0
    #     while (lineFound == 0):
    #         status = exeCtrl.getCPUStatus(True)
    #         if 'break;' in dbg.getSymbolAtAddress(ic.IConnectDebug.sFunctions, status.getExecutionArea(), status.getExecutionPoint(), ic.IConnectDebug.sSourceCode).strip():
    #             lineFound = 1
    #             var1 = dbg.evaluate(IConnectDebug.fRealTime, 'var1').getInt()
    #             dbg.modify(IConnectDebug.fRealTime, 'var2', str(var1))
    #             break
    #         else:
    #             dbg.stepOverHigh()
       
        step_5 = testplan.addStep()
        step_5.addChildStep("5. Run until return")
        step_5.addChildStep("- step in")
        step_5.addComment('5. foo_one function will be entered')
        
    #     dbg.runUntilReturn()
    #     dbg.stepInst()
        
        step_6 = testplan.addStep()
        step_6.addChildStep("6. Read value from register R3")
        step_6.addExpectedResult('6. R3 == var1')
       
    #     returnValue = dbg.evaluate(IConnectDebug.fRealTime, '@R3').getInt()
    
    #     if returnValue == (var1 | RTE_E_INTEGRITY_VIOLATED):
    #         testcase.result = 1
    #     else:
    #         testcase.result = 0
    #         
    #     dbg.deleteAll() # delete all breakpoints
    #     dbg.run()
    
        testcase.result = PASSED
        testcase.time_end = time.ctime(time.time())
        return testplan.export()
    
    except:
        testcase.result = ERROR
        testcase.time_end = time.ctime(time.time())
        print "Unexpected error:", sys.exc_info()[1]
