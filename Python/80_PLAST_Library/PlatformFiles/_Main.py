'''
Created on 05.03.2015
  
@author: Laurentiu Nitu
'''

PLAST_Version = '2.0'
MAIN_PASSED = 0x00
MAIN_FAILED = 0x01
MAIN_ERROR  = 0x10

import sys, os
# Begin: Development Mode
# os.environ['PLAST_WA_PATH'] = r'D:\Sandboxes\SW_AUT_ITS\Software\Library\Workspace\PLAST_wa\\'
# End: Development Mode
try:
    os.environ['PLAST_WA_PATH']
except:
    sys.exit('PLAST_wa path is missing from environment variables. Use registerPLASTwa.bat, Log off and try again.')

# print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add the SWT_PLAST_PLATFORM directory to PATH
sys.path.append(os.environ['PLAST_WA_PATH']) # add the PLAST_wa directory to PATH
sys.dont_write_bytecode = True # do not generate *.pyc files

from PlatformFiles import *
cfg = ConfigParser.RawConfigParser()
cfg.read(os.environ['PLAST_WA_PATH'] + "CONFIGURATION.cfg")

class testcase_type(ctypes.Structure):
    _fields_ = [("description", ctypes.c_char_p),
                ("traceability", ctypes.c_char_p),
                ("safety_requirement", ctypes.c_char_p),
                ("result", ctypes.c_int),
                ("time_begin", ctypes.c_char_p),
                ("time_end", ctypes.c_char_p)]
      
class testcase_results:
    def __init__(self, testcasefilename, coveredreq, descr, res, time_b, time_e, prec, ste, expRes, comm, testcomm, safetyreq):
        self.testCaseFilename = testcasefilename
        self.coveredRequirement = coveredreq
        self.description = descr
        self.result = res
        self.time_begin = time_b
        self.time_end = time_e
        self.preconditions = prec
        self.steps = ste
        self.expected_results = expRes
        self.comments = comm
        self.tester_comments = testcomm
        self.safety_requirement = safetyreq
        self.test_duration = ''
         
    def getTestCaseName(self):
        return self.testCaseFilename
     
    def getCoveredRequirement(self):
        return self.coveredRequirement
      
    def getDescription(self):
        return self.description
      
    def getResult(self):
        return self.result
      
    def getTestDuration(self):
        testcase_h = time.strptime(self.time_end, '%a %b %y %H:%M:%S %Y').tm_hour - time.strptime(self.time_begin, '%a %b %y %H:%M:%S %Y').tm_hour
        testcase_m = time.strptime(self.time_end, '%a %b %y %H:%M:%S %Y').tm_min - time.strptime(self.time_begin, '%a %b %y %H:%M:%S %Y').tm_min
        testcase_s = time.strptime(self.time_end, '%a %b %y %H:%M:%S %Y').tm_sec - time.strptime(self.time_begin, '%a %b %y %H:%M:%S %Y').tm_sec
        self.test_duration = "%02d:%02d:%02d" % (testcase_h, testcase_m, testcase_s)
        return self.test_duration
      
    def getPreconditions(self):
        return self.preconditions
      
    def getSteps(self):
        return self.steps
      
    def getExpectedResults(self):
        return self.expected_results
      
    def getComments(self):
        return self.comments
      
    def getTesterComments(self):
        return self.tester_comments
    
    def isSafetyRequirement(self):
        return self.safety_requirement
     
# getKey - function used to sort the results for the report
def getKey(customobj):
    return customobj.getTestCaseName()
 
# def getWinIDEAConfiguration():
#     connectionMgr = ic.ConnectionMgr()
#     connectionConfig = ic.CConnectionConfig()
#     winIDEAInstances = ic.VectorWinIDEAInstanceInfo()
#     hostAddress = ''
#     connectionMgr.enumerateWinIDEAInstances(hostAddress, connectionConfig, winIDEAInstances)
#     singleReadFlag = 0
#     winideaWorkspace = ''
#     for instance in winIDEAInstances:
#         if singleReadFlag == 0:
#             winideaWorkspace = instance.getWorkspace()
#             singleReadFlag = 1
#     return winideaWorkspace
  
def timelimit(timeout, func, args=(), kwargs={}):
    """ Run func with the given timeout. If func didn't finish running
        within the timeout, raise error
        http://eli.thegreenplace.net/2011/08/22/how-not-to-set-a-timeout-on-a-computation-in-python
    """
    import threading
    
    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            CoInitializeEx(COINIT_APARTMENTTHREADED)
            self.result = func(*args, **kwargs)

        def _stop(self):
            if self.isAlive():
                Thread._Thread__stop(self)
                CoUninitialize()

    it = FuncThread()
    it.start()
    it.join(timeout)
    if it.isAlive():
        it._stop()
        args[0].result = ERROR
        args[0].time_end = time.ctime(time.time())
        print func.__name__ + ' stopped due to timeout.'
        return None
#         raise TimeLimitExpired()
    else:
        return it.result
    
nrOfQMRequirementsCovered = 0
nrOfASILRequirementsCovered = 0
nrOfExecutedTests = 0
nrOfPassedTests = 0
nrOfFailedTests = 0
nrOfErrorTests = 0
nrOfManualTests = 0

def printToConsole(string1, string2):
    print '{0:20} : {1:1}'.format(string1, string2)

def main(testToRun=None):
    global nrOfQMRequirementsCovered
    global nrOfASILRequirementsCovered
    global nrOfExecutedTests
    global nrOfPassedTests
    global nrOfFailedTests
    global nrOfErrorTests
    global nrOfManualTests
    
    nrOfQMRequirementsCovered = 0
    nrOfASILRequirementsCovered
    nrOfExecutedTests = 0
    nrOfPassedTests = 0
    nrOfFailedTests = 0
    nrOfErrorTests = 0
    nrOfManualTests = 0
    
#     print testToRun.__name__
    if '_' in testToRun.__name__:
        variant = testToRun.__name__.split("_TestsToRun_")[1]
    else:
        variant = testToRun.__name__
#     print variant
       
#     if testToRun is None:
#         print 'no arguments'
#     else:
#         print testToRun
    
         
#     ###########################################################################
#     # Remove old reports if specified in CONFIGURATION.cfg.                   # this applies only for this project variant
#     ###########################################################################
#      
#     if cfg.getboolean("REPORT", "CleanReports"):
#         filelist = [ f for f in os.listdir(os.environ['PLAST_WA_PATH'] + "Reports") if f.endswith(('.xlsx', '.html', '.csv')) ]
#         for f in filelist:
#             if variant in f:
#                 print os.environ['PLAST_WA_PATH'] + 'Reports\\' + f + ' removed.'
#                 os.remove(os.environ['PLAST_WA_PATH'] + "Reports\\" + f)
         
    if len(testToRun.listOfAllTests):
             
        if cfg.getboolean("REPORT", "csv"):
            if cfg.getboolean("WORKSPACE", "IsJenkinsUsed"):
                csvfile = open(time.strftime(os.environ['PLAST_WA_PATH'] + "Reports\\PLAST_TestLog_" + variant + ".csv", time.localtime()), 'wb')
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            else:
                csvfile = open(time.strftime(os.environ['PLAST_WA_PATH'] + "Reports\\%Y-%m-%d-%H%M%S_TestLog_" + variant + ".csv", time.localtime()), 'wb')
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
           
        overalltestbegin = time.time()
          
        listOfExecutedTests = []
      
        offset__step = 0  # steps            are located at position 0
        offset__expectedResults = 1  # expected results are located at position 1
        offset__comments = 2  # comments         are located at position 2
        offset__testerComments = 3  # tester comments  are located at position 3
        buffer__preconditions = []  # buffer used by spamwriter to write in excel
        buffer__step = []  # buffer used by spamwriter to write in excel
        buffer__expectedResults = []  # buffer used by spamwriter to write in excel
        buffer__comments = []  # buffer used by spamwriter to write in excel
        buffer__testerComments = []  # buffer used by spamwriter to write in excel
          
        results_data_html = []
        results_data_xlsx = []
        
        all_requirements_in_traceability_list = []
        req_cnt = 0
        
        for test in testToRun.listOfAllTests:
            time.sleep(1)
            
            testcase_data = testcase_type()
            traceability_list = []
            
              
            print '------------------------------------------------'
            printToConsole('Test filename', test.__module__)
            printToConsole('Test function', test.__name__)
#             print 'Test filename:', test.__module__
#             print 'Test function:', test.__name__ 
              
            # clear buffers previously used by spamwriter
            buffer__preconditions = []
            buffer__step = []
            buffer__expectedResults = []
            buffer__comments = []
            buffer__testerComments = []
            overallPreconditions_ = []
            overallStepDetails_ = []
            retVal = None
            safety_req = 'No'
              
            if cfg.getfloat("WORKSPACE", "Testcase_Timeout") == 0:
                retVal = test(testcase_data) # execute test
            else:
                retVal = timelimit(cfg.getfloat("WORKSPACE", "Testcase_Timeout"), test, args=(testcase_data,))


            if retVal:
                overallPreconditions_, overallStepDetails_ = retVal
              
            # populate the buffers used by spamwriter to write in excel
            for idx in range(0, len(overallPreconditions_)):
                if len(overallPreconditions_[idx]) > 0:
                    buffer__preconditions.append(overallPreconditions_[idx])
               
            for idx in range(0, len(overallStepDetails_), 4):
    #             print 'Step: '
                if len(overallStepDetails_[idx + offset__step]) > 0:
                    for step in overallStepDetails_[idx + offset__step]:
                        buffer__step.append(step)
    #                     print step
                       
    #             print 'Expected Results: '
                if len(overallStepDetails_[idx + offset__expectedResults]) > 0:
                    for expectedResult in overallStepDetails_[idx + offset__expectedResults]:
                        buffer__expectedResults.append(expectedResult)
    #                     print expectedResult
                   
    #             print 'Comments: '
                if len(overallStepDetails_[idx + offset__comments]) > 0:
                    for comment in overallStepDetails_[idx + offset__comments]:
                        buffer__comments.append(comment)
    #                     print comment
                       
    #             print 'Tester Comments: '
                if len(overallStepDetails_[idx + offset__testerComments]) > 0:
                    for testerComment in overallStepDetails_[idx + offset__testerComments]:
                        buffer__testerComments.append(testerComment)
    #                     print testerComment
              
    #             Uncomment next lines for steps preview in console (wysiwyg - What you see is what you get)
                          
    #         print 'Preconditions:'  
    #         print '\n'.join(buffer__preconditions)
    #         print 'Steps:'
    #         print '\n'.join(buffer__step)
    #         print 'Expected Results:'
    #         print '\n'.join(buffer__expectedResults)
    #         print 'Comments:'
    #         print '\n'.join(buffer__comments)
    #         print 'Tester Comments:'
    #         print '\n'.join(buffer__testerComments)
              
    #         namespl = test.__name__.split('_')
             
            if testcase_data.traceability:
                if ',' in testcase_data.traceability:
                    traceability_list = testcase_data.traceability.split(',')
                else:
                    traceability_list.append(testcase_data.traceability)
            else:
                traceability_list.append(test.__name__)
            
                
            # testcase has the safety_requirement variable set?
            if testcase_data.safety_requirement:
                safety_req = testcase_data.safety_requirement.lower()
                
            for traceability in range(0, len(traceability_list)):
                req_cnt = req_cnt + 1
                if traceability_list[traceability].strip() in all_requirements_in_traceability_list:
                    pass
                else:
                    if (safety_req.lower() == 'yes'):
                        nrOfASILRequirementsCovered = nrOfASILRequirementsCovered + 1
                    else:
                        nrOfQMRequirementsCovered = nrOfQMRequirementsCovered + 1
                    all_requirements_in_traceability_list.append(traceability_list[traceability].strip())
                listOfExecutedTests.append(testcase_results(traceability_list[traceability].strip(), test.__name__, testcase_data.description, testcase_data.result, testcase_data.time_begin, testcase_data.time_end, ' ' + '<br>'.join(buffer__preconditions), ' ' + '<br>'.join(buffer__step), ' ' + '<br>'.join(buffer__expectedResults), ' ' + '<br>'.join(buffer__comments), ' ' + '<br>'.join(buffer__testerComments), safety_req.lower()))

            if safety_req == 'yes':
                printToConsole('Test trace (ASIL)', ','.join(traceability_list))
            elif safety_req == 'no':
                printToConsole('Test trace (QM)', ','.join(traceability_list))
            else:
                printToConsole('Test trace', ','.join(traceability_list))

            if testcase_data.result == 1:
                nrOfPassedTests = nrOfPassedTests + 1
                printToConsole('Test result', 'Passed!')
            else:
                if testcase_data.result == 0:
                    nrOfFailedTests = nrOfFailedTests + 1
                    printToConsole('Test result', 'Failed!')
                else:
                    if testcase_data.result == 2:
                        nrOfManualTests = nrOfManualTests + 1
                        printToConsole('Test result', 'No Run!')
                    else:
                        if testcase_data.result == 3:
                            nrOfErrorTests = nrOfErrorTests + 1
                            printToConsole('Test result', 'Error!')
    
            
                
                 
        nrOfExecutedTests = nrOfPassedTests + nrOfFailedTests + nrOfManualTests + nrOfErrorTests
        overalltestend = time.time() - overalltestbegin
         
        print '\n====================== TEST SUMMARY ======================\n'
        summary_data = [
                ['Project Name', cfg.get("WORKSPACE", "Project_Name")],
                ['Test Date', time.strftime('%d-%m-%Y', time.localtime())],
                ['Tested Baseline', variant],
                ['Test Performed By', os.environ.get("USERNAME")],
                ['Windows Computer Name', os.environ.get("COMPUTERNAME")],
                ['Final Test Time (H:M:S)', time.strftime('%H:%M:%S', time.gmtime(overalltestend))],
                ['Number of QM requirements planned', cfg.getint("WORKSPACE", "QM_RequirementsPlanned")],
                ['Number of QM requirements covered', nrOfQMRequirementsCovered],
                ['Number of ASIL requirements planned', cfg.getint("WORKSPACE", "ASIL_RequirementsPlanned")],
                ['Number of ASIL requirements covered', nrOfASILRequirementsCovered],
                ['Existing number of tests', nrOfExecutedTests],
                ['Number of passed tests', nrOfPassedTests],
                ['Number of failed tests', nrOfFailedTests],
                ['Number of manual tests', nrOfManualTests],
                ['Number of tests with error', nrOfErrorTests]
                ]
          
        for info in summary_data:
            print '{0:40} : {1:1}'.format(str(info[0]), str(info[1]))
#             print info[0], info[1]
            if cfg.getboolean("REPORT", "csv"):
                spamwriter.writerow(info)
        if cfg.getboolean("REPORT", "csv"):
            spamwriter.writerow([''])
            spamwriter.writerow(['General Test Information'])
          
#         print '\n--\n'
          
        if cfg.getboolean("REPORT", "csv"):
            if cfg.getboolean("REPORT", "TemplateCompatible"):
                spamwriter.writerow(['TC - identifier', 'V', 'R', 'N', 'Description', 'Precondition', 'Test Procedures', 'Expected Results', 'Ok/ Nok Comments /description'])
            else:
                spamwriter.writerow(['Covered Requirement', 'Test case name', 'Test duration (H:M:S)', 'Test description', 'Test result', 'TC Precondition', 'TC Test Steps', 'TC Expected Results', 'TC Comment', 'Tester Comment', 'Safety Requirement'])
     
    #     print listOfExecutedTests
        print '\n====================== TEST RESULTS ======================\n'
        for testExecuted in sorted(listOfExecutedTests, key=getKey):
            if testExecuted.getResult() == 0:
    #             print testExecuted.getTestCaseName(), testExecuted.getTimeBegin(), testExecuted.getTimeEnd(), testExecuted.getDescription(), 'FAIL'
#                 print testExecuted.getTestCaseName(), 'FAIL'
                printToConsole(testExecuted.getTestCaseName(), 'FAIL')
                if cfg.getboolean("REPORT", "xlsx") or cfg.getboolean("REPORT", "xml"):
                    results_data_xlsx.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'Failed', '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getComments().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>')), testExecuted.isSafetyRequirement()])
                if cfg.getboolean("REPORT", "html"):
                    results_data_html.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'Failed'])
                if cfg.getboolean("REPORT", "csv"):
                    if cfg.getboolean("REPORT", "TemplateCompatible"):
                        spamwriter.writerow([testExecuted.getTestCaseName(), "", "", "", testExecuted.getDescription(), '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>'))])
                    else:
                        spamwriter.writerow([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'Failed', '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getComments().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>')), testExecuted.isSafetyRequirement()])
            else:
                if testExecuted.getResult() == 1:
    #                 print testExecuted.getTestCaseName(), testExecuted.getTimeBegin(), testExecuted.getTimeEnd(), testExecuted.getDescription(), 'PASS'
                    printToConsole(testExecuted.getTestCaseName(), 'PASS')
#                     print testExecuted.getTestCaseName(), 'PASS'
                    if cfg.getboolean("REPORT", "xlsx") or cfg.getboolean("REPORT", "xml"):
                        results_data_xlsx.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'Passed', '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getComments().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>')), testExecuted.isSafetyRequirement()])
                    if cfg.getboolean("REPORT", "html"):
                        results_data_html.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'Passed'])
                    if cfg.getboolean("REPORT", "csv"):
                        if cfg.getboolean("REPORT", "TemplateCompatible"):
                            spamwriter.writerow([testExecuted.getTestCaseName(), "", "", "", testExecuted.getDescription(), '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>'))])
                        else:
                            spamwriter.writerow([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'Passed', '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getComments().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>')), testExecuted.isSafetyRequirement()])
                      
                else:
                    if testExecuted.getResult() == 2:
    #                     print testExecuted.getTestCaseName(), testExecuted.getTimeBegin(), testExecuted.getTimeEnd(), testExecuted.getDescription(), 'MANUAL'
                        printToConsole(testExecuted.getTestCaseName(), 'MANUAL')
#                         print testExecuted.getTestCaseName(), 'MANUAL'
                        if cfg.getboolean("REPORT", "xlsx") or cfg.getboolean("REPORT", "xml"):
                            results_data_xlsx.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'No Run', '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getComments().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>')), testExecuted.isSafetyRequirement()])
                        if cfg.getboolean("REPORT", "html"):
                            results_data_html.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'No Run']) 
                        if cfg.getboolean("REPORT", "csv"):
                            if cfg.getboolean("REPORT", "TemplateCompatible"):
                                spamwriter.writerow([testExecuted.getTestCaseName(), "", "", "", testExecuted.getDescription(), '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>'))])
                            else:
                                spamwriter.writerow([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'No Run', '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getComments().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>')), testExecuted.isSafetyRequirement()])
                          
                    else:
                        if testExecuted.getResult() == 3:
    #                         print testExecuted.getTestCaseName(), testExecuted.getTimeBegin(), testExecuted.getTimeEnd(), testExecuted.getDescription(), 'ERROR'
                            printToConsole(testExecuted.getTestCaseName(), 'ERROR')
#                             print testExecuted.getTestCaseName(), 'ERROR'
                            if cfg.getboolean("REPORT", "xlsx") or cfg.getboolean("REPORT", "xml"):
                                results_data_xlsx.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'Error', '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getComments().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>')), testExecuted.isSafetyRequirement()])
                            if cfg.getboolean("REPORT", "html"):
                                results_data_html.append([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'Error']) 
                            if cfg.getboolean("REPORT", "csv"):
                                if cfg.getboolean("REPORT", "TemplateCompatible"):
                                    spamwriter.writerow([testExecuted.getTestCaseName(), "", "", "", testExecuted.getDescription(), '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>'))])
                                else:
                                    spamwriter.writerow([testExecuted.getTestCaseName(), testExecuted.getCoveredRequirement(), testExecuted.getTestDuration(), testExecuted.getDescription(), 'Error', '\n'.join(testExecuted.getPreconditions().split('<br>')), '\n'.join(testExecuted.getSteps().split('<br>')), '\n'.join(testExecuted.getExpectedResults().split('<br>')), '\n'.join(testExecuted.getComments().split('<br>')), '\n'.join(testExecuted.getTesterComments().split('<br>')), testExecuted.isSafetyRequirement()])
        
        print '\n'
                          
        if cfg.getboolean("REPORT", "xlsx"):
            report_generator(variant, overalltestbegin, overalltestend, req_cnt, nrOfPassedTests, nrOfFailedTests, nrOfManualTests, nrOfErrorTests, listOfExecutedTests, cfg.getboolean("WORKSPACE", "IsJenkinsUsed")).GetXlsxReport(summary_data, results_data_xlsx)
        if cfg.getboolean("REPORT", "html"):
            report_generator(variant, overalltestbegin, overalltestend, req_cnt, nrOfPassedTests, nrOfFailedTests, nrOfManualTests, nrOfErrorTests, listOfExecutedTests, cfg.getboolean("WORKSPACE", "IsJenkinsUsed")).GetHtmlReport(summary_data, results_data_html)
        if cfg.getboolean("REPORT", "xml"):
            report_generator(variant, overalltestbegin, overalltestend, req_cnt, nrOfPassedTests, nrOfFailedTests, nrOfManualTests, nrOfErrorTests, listOfExecutedTests, cfg.getboolean("WORKSPACE", "IsJenkinsUsed")).GetXmlReport(summary_data, results_data_xlsx, PLAST_Version)
            
        MAIN_RESULT = MAIN_PASSED
        
        if (nrOfFailedTests > 0) or (nrOfManualTests > 0):
            MAIN_RESULT = MAIN_RESULT | MAIN_FAILED
        if (nrOfErrorTests > 0):
            MAIN_RESULT = MAIN_RESULT | MAIN_ERROR
        
        return MAIN_RESULT # Jenkins error
    else:
        print testToRun.__name__, 'contain no test.'


if cfg.getboolean("REPORT", "StoreConsoleToLog"):
    te = open(os.environ['PLAST_WA_PATH'] + 'Reports\ConsoleOutput.log','w')  # File where you need to keep the logs

class Unbuffered:
   def __init__(self, stream):
       self.stream = stream

   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
       te.write(data)    # Write the data of stdout here to a text file as well

def plast_main():
    if cfg.getboolean("REPORT", "StoreConsoleToLog"):
        sys.stdout=Unbuffered(sys.stdout)
    listOfTests = []
    errorCounter = 0
    
    ###########################################################################
    # Remove old reports if specified in CONFIGURATION.cfg.                   # this applies for all project variants
    ###########################################################################
     
    if cfg.getboolean("REPORT", "CleanReports") or cfg.getboolean("WORKSPACE", "IsJenkinsUsed"):
        filelist = [ f for f in os.listdir(os.environ['PLAST_WA_PATH'] + "Reports") if f.endswith(('.xlsx', '.html', '.csv', '.xml')) ]
        for f in filelist:
#             if variant in f:
            print os.environ['PLAST_WA_PATH'] + 'Reports\\' + f + ' removed.'
            os.remove(os.environ['PLAST_WA_PATH'] + "Reports\\" + f)
    
    if len(sys.argv) <= 1:
        _TestsToRunFromConfig = cfg.get("WORKSPACE", "TestsToRun_Variants").split(',')
        if (len(_TestsToRunFromConfig) <= 1) and ((_TestsToRunFromConfig[0] == '') or (_TestsToRunFromConfig[0] == ';')):
            print 'No list of tests was specified in arguments nor configuration file.'
        else:
            listOfTests = _TestsToRunFromConfig
    else:
        listOfTests = sys.argv[1:]
        
    for testToBeRunned in listOfTests:
        try:
            errorCounter = main(__import__(testToBeRunned.strip(), globals=globals())) 
        except:
            print "Unexpected error:", sys.exc_info()[1]
            print 'Finished: ERROR'
            return 1
            
    if (errorCounter == MAIN_PASSED):
        print 'Finished: PASSED'
        return 0
    else:
        if (errorCounter == MAIN_FAILED):
            print 'Finished: FAILED'
            return 0
        else:
            if (errorCounter == MAIN_ERROR) or (errorCounter == (MAIN_ERROR | MAIN_FAILED)):
                print 'Finished: ERROR'
                return 1
        
if __name__ == "__main__":
    res = plast_main()
    sys.exit(res)