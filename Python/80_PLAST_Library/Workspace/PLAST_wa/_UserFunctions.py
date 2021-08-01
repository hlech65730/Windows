'''
    Author: user
    Purpose: User created functions
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

def MeasureCycleTime(functionName):
    cMgr = ic.ConnectionMgr() # Get the connection
    cMgr.connectMRU('')       # initialize the target
    dbg = ic.CDebugFacade(cMgr)
    
    dbg.deleteAll() # delete all breakpoints
    dbg.stop()
    dbg.reset()

    dbg.setBP(functionName)
    dbg.run()
    dbg.waitUntilStopped()
    firstTime = dbg.evaluate(IConnectDebug.fRealTime, '*(uint32*)(0xFFF3C004)').getLong() # STM System Timer Module - in microseconds
 
    dbg.run()
    dbg.waitUntilStopped()
    secondTime = dbg.evaluate(IConnectDebug.fRealTime, '*(uint32*)(0xFFF3C004)').getLong() # STM System Timer Module - in microseconds
 
#     print 'First time:', firstTime, 'microseconds'
#     print 'Second time:', secondTime, 'microseconds'
#     print 'Cycle time:', (secondTime - firstTime)/float(1000), 'milliseconds'
#     print 'Rounded cycle time:', round((secondTime - firstTime)/float(1000), 2) # - in milliseconds
 
    dbg.deleteAll()
    cycleTime = (secondTime - firstTime)/1000
    return cycleTime 

def printVariables(partitionIdx, dataCtrl):
    vars = ic.VariableVector()
    dataCtrl.getVariables(partitionIdx, vars)
    for var in vars:
        print '  Var name: ', var.getName()
        print '  Var type: ', var.getType()
        print '  ------------------'


def printLabels(partitionIdx, dataCtrl):
    labels = ic.VariableVector()
    dataCtrl.getLabels(partitionIdx, labels)
    for label in labels:
        print '  Label name: ', label.getName()
        print '  Label type: ', label.getType()
        print '  ------------------'

    
def printModules(partitionIdx, dataCtrl):
    modules = ic.ModuleVector()
    dataCtrl.getModules(partitionIdx, modules)
    for module in modules:
        print '  Module name: ', module.getName()
        print '  Module path: ', module.getPath()
        print '  ------------------'

    
def printFunctions(partitionIdx, dataCtrl):
    functions = ic.FunctionVector()
    dataCtrl.getFunctions(partitionIdx, functions)

    for function in functions:
        print '  Function: ', function.getName()
        print '    Scope: ', function.getScope()
        print '    Type: ', function.getReturnType()
        print '    Module idx: ', function.getModuleIndex()
        print '    Parameters:'
        params = function.getParameters()
        for param in params:
            print '      Name: ', param.getName()
            print '      Type: ', param.getType()
            print '      ----'
            
        print '  ------------------'


def printTypes(partitionIdx, dataCtrl):
    types = ic.TypeVector()
    dataCtrl.getTypes(partitionIdx, types)
    for ctype in types:
        print '  Type name: ', ctype.getName()
        stype = ctype.getType()
        # see winIDEA/WCommon/globdefs.h, struct SType2
        # for type enum definitions. From Python
        # the type enums are accessible as object members: dir(type).
        print '  type: ', stype.m_byType
        print '  type2: ', stype.m_byType2
        print '  bitSize: ', stype.m_byBitSize
        print '  ------------------'

        
def printTypedefs(partitionIdx, dataCtrl):
    typedefs = ic.TypedefVector()
    dataCtrl.getTypedefs(partitionIdx, typedefs)
    for typedef in typedefs:
        print '  Typedef name: ', typedef.getTypedefName()
        print '  Type name: ', typedef.getTypeName()
        print '  ------------------'

def addFilesToDownloadList():
    
    connectionMgr = ic.ConnectionMgr()
    connectionMgr.connectMRU('')  
    loader = ic.CLoaderController(connectionMgr)
    
    loader.clearDownloadList(ic.CLoaderController.DLIST_PRIMARY)
    
    downloadConfig = ic.CDownloadConfiguration()
    downloadConfig.setSymbolsOffset(0).setUsedInFullDownload(1).setDownloadFileFormat(ic.CDownloadConfiguration.ftELF);
    loader.addToDownloadList(downloadConfig, ic.CLoaderController.DLIST_PRIMARY, 'D:/AUD_MLB_BCM2/FilesForDownload/RH850/AUDI_MLBe_16_BCU_BCM2_MaC_RH850_F1L.abs', '')
    
    downloadConfig = ic.CDownloadConfiguration()
    downloadConfig.setCodeOffset(0).setUsedInFullDownload(1).setDownloadFileFormat(ic.CDownloadConfiguration.ftMotorolaS);
    loader.addToDownloadList(downloadConfig, ic.CLoaderController.DLIST_PRIMARY, 'D:/AUD_MLB_BCM2/FilesForDownload/RH850/UTIP_AUD_MLBe_16_BCU_BCM2_MaC_with_FBL.s19', '')
    
    downloadList = loader.getDownloadList(ic.CLoaderController.DLIST_PRIMARY, True)
    for dlFile in downloadList:
        print('file: ', dlFile.fileName)
        print('options: ', dlFile.options)

#     loader.download()
    
    dataCtrl = ic.CDataController(connectionMgr)


    paths = ic.StrVector()
    dlFileNames = ic.StrVector()
    dataCtrl.getPartitions(paths, dlFileNames)

    partitionIdx = 0
    for dlFile in dlFileNames:
        print 'Download file: ', dlFile
#         printVariables(partitionIdx, dataCtrl)
#         printLabels(partitionIdx, dataCtrl)
        printModules(partitionIdx, dataCtrl)
#         printFunctions(partitionIdx, dataCtrl)
#         printTypes(partitionIdx, dataCtrl)
#         printTypedefs(partitionIdx, dataCtrl)
    
        partitionIdx += 1
        
        
def AUDTargetReset():
    # Get the connection and controller objects
    cMgr = ic.ConnectionMgr()
    cMgr.connectMRU('') # initialize the target
    dbg = ic.CDebugFacade(cMgr)
    exeCtrl = ic.CExecutionController(cMgr)
    dbg.stop() # stop target
    dbg.deleteAll() # Deletes all execution breakpoints.
    dbg.deleteAllHWBP() # Deletes all hardware breakpoints.
    dbg.reset()     # reset target
    dbg.setBP('SchM_Tasks_FG1_1s_List')
    dbg.run()
    dbg.waitUntilStopped()
    dbg.modify(IConnectDebug.fMonitor, 'HW_VARIANTS.HWConfigCurr.b1.p_Reserved5', '1')
    dbg.deleteAll()
    dbg.run()

def BDCTargetReset():
    # Get the connection and controller objects
    cMgr = ic.ConnectionMgr()
    cMgr.connectMRU('') # initialize the target
    dbg = ic.CDebugFacade(cMgr)
    exeCtrl = ic.CExecutionController(cMgr)
    
    dbg.stop() # stop target
    dbg.deleteAll() # Deletes all execution breakpoints.
    dbg.deleteAllHWBP() # Deletes all hardware breakpoints.
    dbg.reset()     # reset target
    
    loop = 1
    
    print 'Reseting target.'
#     print dbg.evaluate(IConnectDebug.fRealTime, 'SysInt_Counters[0]').getInt()
#     print hex(dbg.evaluate(IConnectDebug.fRealTime, 'SysInt_Counters[0]').getInt())
    while loop:
        status = exeCtrl.getCPUStatus(True)
        if status.isStopped():
            dbg.run()
            time.sleep(1)
        if status.isRunning() and ('0xff00' == hex(dbg.evaluate(IConnectDebug.fRealTime, 'SysInt_Counters[0]').getInt())):
            loop = 0
            
#     print 'DONE!'
            
#     print hex(dbg.evaluate(IConnectDebug.fRealTime, 'SysInt_Counters[0]').getInt())
            


def forceModify(mode, name, value):
    # Get the connection and controller objects
    cMgr = ic.ConnectionMgr()
    cMgr.connectMRU('') # initialize the target
    dbg = ic.CDebugFacade(cMgr)
    
    verificationLoop = 1
    while verificationLoop:
        modifyReturnValue = dbg.modify(mode, name, value)
        if '\\' in modifyReturnValue:
#             print modifyReturnValue.split(' ')[0]
            if (int(value) == int('0' + (modifyReturnValue.split(' ')[0])[1:], 16)):
                verificationLoop = 0
        else:
#         print modifyReturnValue
            if (int(value) == int(modifyReturnValue, 16)):
                verificationLoop = 0
#     print int(modifyReturnValue, 16)
#     print int(value)
    
# def TSC_AUD_Startup(testcase):
#     testcase.description = '''
#                                 TSC_AUD_Startup:
#                                 Startup example for AUD MLB BCM2 Project.
#                           '''
#     testcase.time_begin = time.ctime(time.time())
#     
#     testplan = TestPlan()
#     
# #     Get the connection and controller objects
#     cMgr = ic.ConnectionMgr()
#     cMgr.connectMRU('') # initialize the target
# #     dbg = ic.CDebugFacade(cMgr)
# #     addFilesToDownloadList()
# #     loader = ic.CLoaderController(cMgr)
#     
#     ide = ic.CIDEController(cMgr)
#     print ide.getDynamicOptionSize("/IDE/");
#     
#     # The first parameter selects download list: DLIST_PRIMARY or DLIST_TARGET
#     # If the second parameter is true, absolute paths are returned.
#     
#     
#     
#     
#     
#     
# #     precondition = testplan.addPrecondition()
# #     precondition.addChildPrecondition("- stop target")
# #     precondition.addChildPrecondition("- delete all breakpoints")
# #     precondition.addChildPrecondition("- reset target")
# #     precondition.addChildPrecondition("- run target")
#     
# #     AUDTargetReset()
# #     
#     testcase.result = 2
# #     dbg.deleteAll() # delete all breakpoints
# #     dbg.run()
#     testcase.time_end = time.ctime(time.time())
#     return testplan.export()