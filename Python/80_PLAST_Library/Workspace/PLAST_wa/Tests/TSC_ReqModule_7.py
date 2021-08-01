'''
    Author: Laurentiu Nitu
    Purpose: Test of SWT ReqModule Requirement: TSC_ReqModule_7
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

def TEST_5(testcase):
    testcase.time_begin = time.ctime(time.time())
    
    testcase.description = """REQ_07: Send a CAN message with id = 1 and a ciclicity = 10ms for a period of 20 seconds."""
    testcase.traceability = 'REQ_07'
    testcase.safety_requirement = 'No'
   
    try:
        testplan = TestPlan()
        
#         # this function store in a list the readed messages from CAN for a period of time and returns it 
#         print CAN_ReadMultipleMessages_return(20)
#         
#         # ------------------------------------------------
#         
#         # this function prints to console the readed messages from CAN for a period of time
#         CAN_ReadMultipleMessages_print(20)
#         
#         # ------------------------------------------------
#         
#         # this function send one CAN message
#         WriteMessageOnce(0x01, [0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80])
#         
#         # ------------------------------------------------
#         
#         # this function sends a CAN message for a specific time
#         WriteMessageMultiple(20, 0x01, [0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80])
#         
#         # ------------------------------------------------
#         
#         # this thread is used to send a CAN message while different paralel executions are made (ex. winIDEA manipulation while a CAN message is sent)
#         thrd = WriteCAN_Thread(0x01, [0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80], 0.01)
#         thrd.start()
#         time.sleep(20) # wait 20 seconds
#         thrd.stop()
        
        # ------------------------------------------------
   
        testcase.result = PASSED
        testcase.time_end = time.ctime(time.time())
        return testplan.export()
    except:
        testcase.result = ERROR
        testcase.time_end = time.ctime(time.time())
        print "Unexpected error:", sys.exc_info()[1] 