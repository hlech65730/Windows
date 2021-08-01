'''
Created on May 26, 2015

@author: UIDR5732
'''
import win32com.client
import os
import time
import math
from xml.dom import minidom
from time import sleep
from win32con import NULL
from test.test_typechecks import Integer

class CANoe:

    def __init__(self):
        #Syntax    __init__() [CANoe()]    
        #Description    CANoe COM Server Class constructor. If needed, calling the constructor also launches the CANoe application. The constructor must be called before any other CANoe class method is used. It is assumed that the correct configuration is loaded (CANoe *.cfg file) or will be loaded by default when the CANoe application is launched.     
        #Parameters    -    
        #Return Values    An instance of the CANoe class.    
        #Example    can_inst = CANoe()
        self.Application = win32com.client.Dispatch('CANoe.Application')

    def CompileAllNodes(self):
        #Syntax CompileAllNodes() 
        #Description Compiles all active CAPL, XML and .NET nodes in the current configuration. Calling the CompileAllNodes() method correlates to clicking the Compile All Nodes button in the CANoe application. (see the image example of the Start method description) 
        #Parameters - 
        #Return Values - 
        #Example can_inst.CompileAllNodes() 
        self.Application.CAPL.Compile()

    def CompileErrorMessage(self):
        #Syntax CompileErrorMessage() 
        #Description Returns the compilation error message(s) resulting from the last CAPL object compilation. 
        #Parameters - 
        #Return Values String containing the error message(s). 
        #Example 
        #    if (can_inst.CompileResult() == 0):
        #        print 'Compilation successful'
        #    else:
        #        print 'Compilation error with message:\n' + can_inst.CompileErrorMessage()
        #        print 'First compilation error node:\n' + can_inst.CompileNodeName()
        #        print '\nNode location:\n' + can_inst.CompileSourceFile()
        #
        #Displays the following to the output console:
        #
        #Compilation error with message:
        #CAPL node 'BO_DIAG_NODE': Compilation of 'D:\viano\BODY-Models\diagnostic.can' failed with error(s)
        #L1209,C32: Unknown symbol 'TimeOOut'
        #
        #First compilation error node:
        #BO_DIAG_NODE
        #
        #Node location:
        #D:\viano\BODY-Models\diagnostic.can 
        return self.Application.CAPL.CompileResult.ErrorMessage

    def CompileNodeName(self):
        #Syntax CompileNodeName() 
        #Description Returns the name of the first node (CAPL object) that has a compilation error. 
        #Parameters - 
        #Return Values String containing the node name. 
        #Example 
        #    print can_inst.CompileNodeName()
        #
        #Displays the following to the output console (see the example of the CompileErrorMessage method description):
        #
        #BO_DIAG_NODE 
        return self.Application.CAPL.CompileResult.NodeName

    def CompileResult(self):
        #Syntax CompileResult() 
        #Description Returns the result of the last compilation of the CAPL object. 
        #Parameters - 
        #Return Values Integer representing the compilation result; Possible values are:
        #
        #0 - If the compilation of all the nodes completed successfully.
        #1 - If compilation errors occured. 
        #Example 
        #    print can_inst.CompileResult()
        #
        #Displays the following to the output console (see the example of the CompileErrorMessage method description):
        #
        #1 
        return self.Application.CAPL.CompileResult.Result

    def CompileSourceFile(self):
        #Syntax CompileSourceFile() 
        #Description Returns the absolute path of the program file where the first compile error occurred. 
        #Parameters - 
        #Return Values String containing the file path. 
        #Example 
        #    print can_inst.CompileSourceFile()
        #
        #Displays the following to the output console (see the example of the CompileErrorMessage method description):
        #
        #D:\viano\BODY-Models\diagnostic.can 
        return self.Application.CAPL.CompileResult.SourceFile

    def Databases(self):
        #Syntax Databases() 
        #Description Displays the number of databases used in the project, their indexes, full names, full paths and channels they are using in the currently loaded configuration (CANoe *.cfg file). 
        #Parameters - 
        #Return Values - 
        #Example 
        #    can_inst.Databases()
        #
        #Displays the following to the output console:
        #
        #2 Database(s):
        #Database No.   Channel No.   Database Name        Database Path
        #Database 1:    Channel: 1    body                 D:\viano\DBC\body.dbc
        #Database 2:    Channel: 1    body_external_env    D:\viano\DBC\body_external_env.dbc 
        dbSetup = self.Application.Configuration.GeneralSetup.DatabaseSetup
        print str(dbSetup.Databases.Count)+' Database(s):'
        print 'Database No.\tChannel No.\tDatabase Name'+' '*17+'Database Path\n'
        for i in range(1, dbSetup.Databases.Count+1):
            print'Database '+str(i)+':\t'+ 'Channel: '+str(dbSetup.Databases(i).Channel)+'\t'+str(dbSetup.Databases(i).Name)+' '*(30-len(dbSetup.Databases(i).Name))+str(dbSetup.Databases(i).FullName)

    def Running(self):
        #Syntax Running() 
        #Description Determines whether the measurement has been started. 
        #Parameters - 
        #Return Values Boolean type representing the running status; Possible return values are:
        #
        #True - If the measurement is running.
        #False - If the measurement is not running. 
        #Example print can_inst.Running()
        #
        #Displays the following to the output console:
        #
        #False 
        return self.Application.Measurement.Running

    def Animate(self):
        #Syntax Animate() 
        #Description Starts the measurement in Animation mode. Calling the Animate() method correlates to clicking the Animate button in the CANoe application. (see the image example of the Start method description) 
        #Parameters - 
        #Return Values - 
        #Example can_inst.Animate() 
        self.Application.Measurement.Animate()

    def Break(self):
        #Syntax Break() 
        #Description Interrupts the playback in Offline mode. 
        #Parameters - 
        #Return Values - 
        #Example can_inst.Break() 
        self.Application.Measurement.Break()

    def Reset(self):
        #Syntax Reset() 
        #Description Resets the measurement in Offline mode. 
        #Parameters - 
        #Return Values - 
        #Example can_inst.Reset() 
        self.Application.Measurement.Reset()

    def Start(self):
        #Syntax Start() 
        #Description Starts the measurement/replay. Calling the Start() method correlates to clicking the Start button in the CANoe application.
        #Parameters - 
        #Return Values - 
        #Example can_inst.Start() 
        self.Application.Measurement.Start()

    def Step(self):
        #Syntax Step() 
        #Description Processes a measurement event in single step. Calling the Step() method correlates to clicking the Step button in the CANoe application. (see the image example of the Start method description) 
        #Parameters - 
        #Return Values - 
        #Example can_inst.Step() 
        self.Application.Measurement.Step()

    def Stop(self):
        #Syntax Stop() 
        #Description Stops the measurement/replay. Calling the Stop() method correlates to clicking the Stop button in the CANoe application. (see the image example of the Start method description) 
        #Parameters - 
        #Return Values - 
        #Example can_inst.Stop() 
        self.Application.Measurement.Stop()

    def GetNodeStatus(self, node):
        #Syntax GetNodeStatus(node) 
        #Description Determines the status of the CAPL node (active/inactive). 
        #Parameters 1. node (string) The name of the node. 
        #Return Values Boolean type representing the node status; Possible return values are:
        #
        #True - The node node is active.
        #False - The node node is inactive. 
        #Example print can_inst.GetNodeStatus('TSSR')
        #
        #Displays the following to the output console:
        #
        #True 
        Node = self.Application.Configuration.SimulationSetup.Nodes(node)
        return Node.Active

    def ActivateNode(self, node):
        #Syntax ActivateNode(node) 
        #Description Activates the simulation for the CAPL Node node. 
        #Parameters 1. node (string) The name of the Node object that is to be activated. 
        #Return Values - 
        #Example can_inst.ActivateNode('TSSR') 
        Node = self.Application.Configuration.SimulationSetup.Nodes(node)
        Node.Active = True

    def DeactivateNode(self, node):
        #Syntax DeactivateNode(node) 
        #Description Deactivates the simulation for the CAPL Node node. This method is only available before or after a measurement, not during a measurement.
        #Parameters 1. node (string) The name of the Node object that is to be deactivated. 
        #Return Values - 
        #Example can_inst.DeactivateNode('TSSR') 
        Node = self.Application.Configuration.SimulationSetup.Nodes(node)
        Node.Active = False

    def ClearWriteWindow(self):
        #Syntax ClearWriteWindow() 
        #Description Clears the contents of all the tabs of the Write window in the CANoe application. (see the image in the WriteSystem method description) 
        #Parameters - 
        #Return Values - 
        #Example can_inst.ClearWriteWindow() 
        self.Application.UI.Write.Clear()

    def CopyWriteWindow(self):
        #Syntax CopyWriteWindow() 
        #Description Copies the contents of the Overview tab of the Write window in the CANoe application to the clipboard. 
        #Parameters - 
        #Return Values - 
        #Example can_inst.CopyWriteWindow() 
        self.Application.UI.Write.Copy()

    def DisableOutputFile(self, index = -1):
        #Syntax DisableOutputFile([index]) 
        #Description Disables logging of all outputs from a certain tab (or all the tabs) of the Write window in the CANoe application. To prevent file read/wire errors, if the EnableOutputFile method was previously called with an index, DisableOutputFile should be called with the same index. 
        #Parameters 1. [index] (integer, optional) The index of the tab for which logging of the output is to be disabled. (0 - All, 1 - System etc.) 
        #Return Values - 
        #Example 
        #can_inst.DisableOutputFile(1)
        #or:
        #can_inst.DisableOutputFile() 
        if (index == -1):
            self.Application.UI.Write.DisableOutputFile()
        else:
            self.Application.UI.Write.DisableOutputFile(index)

    def EnableOutputFile(self, path, index = -1):
        #Syntax EnableOutputFile(path, [index]) 
        #Description Enables logging of all outputs from a certain tab (or all the tabs) of the Write window in the CANoe application to the specified output file. 
        #Parameters 
        #1. path (string) The absolute path of the output file.
        #2. [index] (integer, optional) The index of the tab for which logging of the output is to be enabled. (0 - All, 1 - System etc.) 
        #Return Values - 
        #Example 
        #can_inst.EnableOutputFile('D:\\log.txt', 1)
        #or:
        #can_inst.EnableOutputFile('D:\\log.txt') 
        if (index == -1):
            self.Application.UI.Write.EnableOutputFile(path)
        else:
            self.Application.UI.Write.EnableOutputFile(path, index)

    def WriteSystem(self, text):
        #Syntax WriteSystem(text) 
        #Description Outputs a single line of text (text) to the Systems tab of the Write window in the CANoe application.
        #Parameters 1. text (string) The text to be displayed in the Systems tab of the Write window in the CANoe application. 
        #Return Values - 
        #Example can_inst.WriteSystem('Hello from Python!')
        #
        #Displays the following in the Systems tab of the Write window in the CANoe application (see the image in the method description):
        #
        #Hello from Python! 
        self.Application.UI.Write.Output(text)

    def SignalIsOnline(self, channel, message, signal):
        #Syntax SignalIsOnline(channel, message, signal) 
        #Description Checks whether the measurement is running and the signal has been received. 
        #Parameters 
        #1. channel (integer) The channel on which the signal is sent.
        #2. message (string) The name of the message to which the signal signal belongs.
        #3. signal (string) The name of the signal. 
        #Return Values Boolean type representing the signal online status; Possible return values are:
        #
        #True - If the measurement is running and the signal has been received.
        #False - Otherwise.
        #
        #Example print can_inst.SignalIsOnline(1, 'ADAS_CURRENT_ATTRIBUTES_AR', 'ADAS_CuA_Offset')
        #
        #Displays the following to the output console:
        #
        #False 
        Signal = self.Application.Bus.GetSignal(channel, message, signal)
        return Signal.IsOnline

    def SignalFullName(self, channel, message, signal):
        #Syntax SignalFullName(channel, message, signal) 
        #Description Determines the fully qualified name of a signal. 
        #Parameters 
        #1. channel (integer) The channel on which the signal is sent.
        #2. message (string) The name of the message to which the signal signal belongs.
        #3. signal (string) The name of the signal. 
        #Return Values String containing the full signal name. The usual display format is:
        #
        #[<DatabaseName>]::<MessageName>::<SignalName>  
        #Example print can_inst.SignalFullName(1, 'ADAS_CURRENT_ATTRIBUTES_AR', 'ADAS_CuA_Offset')
        #
        #Displays the following to the output console:
        #
        #ADAS_CURRENT_ATTRIBUTES_AR::ADAS_CuA_Offset 
        Signal = self.Application.Bus.GetSignal(channel, message, signal)
        return Signal.FullName

    def SignalRawValue(self, channel, message, signal):
        #Syntax SignalRawValue(channel, message, signal) 
        #Description Returns the current value of the signal exactly as it was transmitted on the bus. 
        #Parameters 
        #1. channel (integer) The channel on which the signal is sent.
        #2. message (string) The name of the message to which the signal signal belongs.
        #3. signal (string) The name of the signal. 
        #Return Values Integer representing the raw value of the signal as it was last transmitted on the bus. 
        #Example print can_inst.SignalRawValue(1, 'ADAS_CURRENT_ATTRIBUTES_AR', 'ADAS_CuA_Offset')
        #
        #Displays the following to the output console:
        #
        #8191 
        Signal = self.Application.Bus.GetSignal(channel, message, signal)
        return Signal.RawValue

    def SignalState(self, channel, message, signal):
        #Syntax SignalState(channel, message, signal) 
        #Description Returns the state of the signal; see the return values. 
        #Parameters 
        #1. channel (integer) The channel on which the signal is sent.
        #2. message (string) The name of the message to which the signal signal belongs.
        #3. signal (string) The name of the signal. 
        #Return Values Integer representing the state of the signal; Possible return values:
        #
        #0 - The default value of the signal is returned.
        #1 - The measurement is not running; the value set by the application is returned.
        #2 - The measurement is not running; the value of the last measurement is returned.
        #3 - The signal has been received in the current measurement; the current value is returned. 
        #Example print can_inst.SignalState(1, 'ADAS_CURRENT_ATTRIBUTES_AR', 'ADAS_CuA_Offset')
        #
        #Displays the following to the output console:
        #
        #1
        Signal = self.Application.Bus.GetSignal(channel, message, signal)
        return Signal.State

    def GetSignalValue(self, channel, message, signal):
        #Syntax GetSignalValue(channel, message, signal) 
        #Description Returns (the value of) a Signal object. 
        #Parameters 
        #1. channel (integer) The channel on which the signal is sent.
        #2. message (string) The name of the message to which the signal signal belongs.
        #3. signal (string) The name of the signal. 
        #Return Values Float representing the current value of the Signal object. 
        #Example print can_inst.GetSignalValue(1, 'ADAS_CURRENT_ATTRIBUTES_AR', 'ADAS_CuA_Offset')
        #
        #Displays the following to the output console:
        #
        #8191.0 
        Signal = self.Application.Bus.GetSignal(channel, message, signal)
        return Signal.Value

    def SetSignalValue(self, channel, message, signal, value):
        #Syntax SetSignalValue(channel, message, signal, value) 
        #Description Sets the value of a Signal object. 
        #Parameters 
        #1. channel (integer) The channel on which the signal is sent.
        #2. message (string) The name of the message to which the signal signal belongs.
        #3. signal (string) The name of the signal.
        #4. value (varying) The new signal value. 
        #Return Values - 
        #Example can_inst.SetSignalValue(1, 'ADAS_CURRENT_ATTRIBUTES_AR', 'ADAS_CuA_Offset', 8191) 
        Signal = self.Application.Bus.GetSignal(channel, message, signal)
        Signal.Value = value

    def GetSysVar(self, varNamespace, varName):
        #Syntax GetSysVar(varNamespace, varName) 
        #Description Returns (the value of) a SystemVariable object.
        #Parameters 
        #1. varNamespace (string) The namespace where the system variable is stored.
        #2. varName (string) The name of the system variable.
        #Return Values Varying return type representing the current value of the SystemVariable object. 
        #Example print can_inst.GetSysVar('SecurityAccess', 'TesterPresentEnable')
        #
        #Displays the following to the output console (see image in the method description):
        #
        #1 
        #or:
        #print can_inst.GetSysVar('CodingParameters::CP_F198_Param', 'ByteArray')
        #
        #Displays the following to the output console:
        #
        #(48, 49, 50, 51, 52, 53)
        return self.Application.System.Namespaces(varNamespace).Variables(varName).Value

    def GetSysVarType(self, varNamespace, varName):
        #Syntax GetSysVarType(varNamespace, varName) 
        #Description Returns the type of a SystemVariable object. 
        #Parameters 
        #1. varNamespace (string) The namespace where the system variable is stored.
        #2. varName (string) The name of the system variable. 
        #Return Values String representing the type of the SystemVariable object. 
        #Example print can_inst.GetSysVarType('SecurityAccess', 'TesterPresentEnable')
        #
        #Displays the following to the output console:
        #
        #Integer 
        varType = self.Application.System.Namespaces(varNamespace).Variables(varName).Type
        types = ['Integer', 'Float', 'String', 'Float Array', 'IntegerArray', 'LongLong', 'ByteArray', 'Generic Array', 'Struct', 'Invalid']
        returnType = ''
        if (varType <3):
            returnType = types[varType]
        elif (varType <8):
            returnType = types[varType-1]
        elif (varType <100):
            returnType = types[varType-91]
        else:
            returnType = types[9]
        return returnType

    def SetSysVar(self, varNamespace, varName, varVal):
        #Syntax SetSysVarType(varNamespace, varName, varVal) 
        #Description Sets the value of a SystemVariable object. 
        #Parameters 
        #1. varNamespace (string) The namespace where the system variable is stored.
        #2. varName (string) The name of the system variable.
        #3. varVal (varying) The value that is to be assigned to the system variable. 
        #Return Values - 
        #Example can_inst.SetSysVar('SecurityAccess', 'TesterPresentEnable', 1) 
        #or:
        #can_inst.SetSysVar('CodingParameters::CP_F198_Param', 'ByteArray', (48, 49, 50, 51, 52, 53))
        varType = self.GetSysVarType(varNamespace, varName)
        if (varType is 'Integer' or 'Float' or 'String' or 'LongLong'):
            self.Application.System.Namespaces(varNamespace).Variables(varName).Value = varVal
        elif (varType is 'Float Array' or 'Integer Array' or 'Byte Array' or 'Generic Array'):
            self.Application.System.Namespaces(varNamespace).Variables(varName).Value = varVal
        elif (varType is 'Struct'):
            self.Application.System.Namespaces(varNamespace).Variables(varName).Value = varVal
        else: #(varType is 'Invalid')
            print 'Invalid System Variable Type!'

    def GetEnvVar(self, varName):
        #Syntax GetEnvVar(varName) 
        #Description Returns (the value of) an EnvironmentVariable object. The EnvironmentVariable object must have a valid name assigned to an environment variable in the loaded database(s) from the current configuration.
        #Parameters 1. varName (string) The name of the EnvironmentVariable object. 
        #Return Values (The value of) an EnvironmentVariable object instance. The return type is the same as the environment variable type returned by calling the GetEnvVarType method with the same parameter. 
        #Example print can_inst.GetEnvVar('BO_EISCLkS_Lk_Stat3EIS_A1_')
        #
        #Displays the following to the output console (see the method description):
        #
        #7
        return self.Application.Environment.GetVariable(varName)

    def GetEnvVarType(self, varName):
        #Syntax GetEnvVar(varName) 
        #Description Returns the type of an environment variable. The EnvironmentVariable object must have a valid name assigned to an environment variable in the loaded database(s) from the current configuration. (see the GetEnvVar method description) 
        #Parameters 1. varName (string) The name of the EnvironmentVariable object.  
        #Return Values Integer representing the type of the environment variable; Possible return values are:
        #
        #0 - Integer
        #1 - Float
        #2 - String
        #3 - Data 
        #Example print can_inst.GetEnvVarType('BO_EISCLkS_Lk_Stat3EIS_A1_')
        #
        #Displays the following to the output console (see the GetEnvVar method description):
        #
        #0 
        Var = self.Application.Environment.GetVariable(varName)
        return Var.Type

    def SetEnvVar(self, varName, varVal):
        #Syntax SetEnvVar(varName, varVal) 
        #Description Returns (the value of) an EnvironmentVariable object. The EnvironmentVariable object must have a valid name assigned to an environment variable in the loaded database(s) from the current configuration. (see the GetEnvVar method description) 
        #Parameters 1. varName (string) The name of the EnvironmentVariable object.
        #2. varVal (varying, see the GetEnvVarType method) The value to be assigned to the EnvironmentVariable object varName. 
        #Return Values - 
        #Example can_inst.SetEnvVar('BO_EISCLkS_Lk_Stat3EIS_A1_', 7)
        #
        #See the GetEnvVar method description. 
        Var = self.Application.Environment.GetVariable(varName)
        Var.Value = varVal

    def CycleEnvVar(self, varName, varMinVal, varMaxVal, order, step, delay, cycles = 1):
        #Syntax CycleEnvVar(varName, varMinVal, varMaxVal, order, step, delay, [cycles]) 
        #Description Cycles through values of an Integer type EnvironmentVariable object. The EnvironmentVariable object must have a valid name assigned to an environment variable in the loaded database(s) from the current configuration. (see the GetEnvVar method description) 
        #Parameters 
        #1. varName (string) The name of the EnvironmentVariable object.
        #2. varMinVal (int) The minimum value of the EnvironmentVariable varName.
        #3. varMaxVal (int) The maximum value of the EnvironmentVariablevarName.
        #4. order (int) The order of the cycle:
        #    0 - ascending;
        #    1 - descending;
        #    2 - ascending -> descending; 
        #    3 - descending -> ascending.
        #5. step (int) The step of the cycle between varMinVal and varMaxVal.
        #6. delay (int) The delay between steps (in milliseconds).
        #7. [cycles] (int, optional) The number of cycles. 
        #Return Values - 
        #Example can_inst.CycleEnvVar('BO_HGWVehSpd_DispIC_A1_', 0, 400, 2, 100, 500)
        #
        #Displays the following to the output console:
        #
        #0
        #100
        #200
        #300
        #400
        #300
        #200
        #100
        #0
        if (varMaxVal < varMinVal):
            auxVal = varMaxVal
            varMaxVal = varMinVal
            varMinVal = auxVal
        i = 0
        if (order == 0):
            for j in range (0, cycles):
                for i in range (varMinVal, varMaxVal+1, step):
                    print i
                    self.Application.Environment.GetVariable(varName).Value = i
                    sleep(delay*0.001)
        elif (order == 1):
            for j in range (0, cycles):
                for i in range (varMaxVal, varMinVal-1, -abs(step)):
                    print i
                    self.Application.Environment.GetVariable(varName).Value = i
                    sleep(delay*0.001)
        elif (order == 2):
            for j in range (0, cycles):
                for i in range (varMinVal, varMaxVal, step):
                    print i
                    self.Application.Environment.GetVariable(varName).Value = i
                    sleep(delay*0.001)
                for i in range (varMaxVal, varMinVal, -abs(step)):
                    print i
                    self.Application.Environment.GetVariable(varName).Value = i
                    sleep(delay*0.001)
            if (i>=step):
                i-=step
            else:
                i=0
            print i
            self.Application.Environment.GetVariable(varName).Value = i
        else: #(order == 3)
            for j in range (0, cycles):
                for i in range (varMaxVal, varMinVal, -abs(step)):
                    print i
                    self.Application.Environment.GetVariable(varName).Value = i
                    sleep(delay*0.001)
                for i in range (varMinVal, varMaxVal, step):
                    print i
                    self.Application.Environment.GetVariable(varName).Value = i
                    sleep(delay*0.001)
            if (i<=varMaxVal-step):
                i+=step
            else:
                i=varMaxVal
            print i
            self.Application.Environment.GetVariable(varName).Value = i

    def AddDiagDescription(self, path, device = -1):
        #Syntax AddDiagDescription(path, [device]) 
        #Description Load the diagnostic document from the given path for the given access type. If the document is an ODX/PDX or MDX file, the identifier of one ECU defined in the ODX file set must be given. The diagNetwork property must be set to the correct path (by calling the SetDiagNetwork method) before this method can be used. 
        #Parameters 
        #1. path (string) The complete path for the CANdela (CDD), ODX/PDX or MDX file.
        #2. device (string, optional) The name of the device used in diagnostic operations. If a CDD is loaded, you do not have to specify this value. 
        #Return Values - 
        #Example 
        #can_inst.AddDiagDescription('D:\\viano\TSSR447.cdd', 'TSSR447')
        #or:
        #can_inst.AddDiagDescription('D:\\viano\TSSR447.cdd') 
        if (device == -1):
            self.Application.Configuration.GeneralSetup.DiagnosticsSetup.DiagDescriptions.Add(self.diagNetwork, path);
        else:
            self.Application.Configuration.GeneralSetup.DiagnosticsSetup.DiagDescriptions.Add(self.diagNetwork, path, device);

    diagResponseAttributes = ['', '', '', '']
        #Type List of (4) strings
        #Description The attributes of the last call of a diagnostic request method (DiagReq or DiagReqFromStream) in the following order: Response index, Response type, Response code, Response sender.
        #Access GetDiagResponseIndex, GetDiagResponseType, GetDiagResponseCode, GetDiagResponseSender 
        #Usage DiagReqFromStream 
        #Example diagResponseAttributes = ['1', 'Positive', '7', 'TSSR447'] 

    def GetDiagResponseIndex(self):
        #Syntax GetDiagResponseIndex() 
        #Description Returns the response index of the last diagnostic request (by calling the DiagReq or DiagReqFromStream methods).  
        #Parameters - 
        #Return Values String containing the last diagnostic request response index. 
        #Example print can_inst.GetDiagResponseIndex()
        #
        #Displays the following to the output console:
        #
        #1 
        return self.diagResponseAttributes[0]

    def GetDiagResponseType(self):
        #Syntax GetDiagResponseType() 
        #Description Returns the response type of the last diagnostic request (by calling the DiagReq or DiagReqFromStream methods).  
        #Parameters - 
        #Return Values String containing the last diagnostic request response type. 
        #Example print can_inst.GetDiagResponseCode()
        #
        #Displays the following to the output console:
        #
        #Positive 
        return self.diagResponseAttributes[1]

    def GetDiagResponseCode(self):
        #Syntax GetDiagResponseCode() 
        #Description Returns the response code of the last diagnostic request (by calling the DiagReq or DiagReqFromStream methods).
        #Parameters - 
        #Return Values String containing the last diagnostic request response code. 
        #Example print can_inst.GetDiagResponseCode()
        #
        #Displays the following to the output console:
        #
        #7 
        return self.diagResponseAttributes[2]

    def GetDiagResponseSender(self):
        #Syntax GetDiagResponseSender() 
        #Description Returns the response sender of the last diagnostic request (by calling the DiagReq or DiagReqFromStream methods).  
        #Parameters - 
        #Return Values String containing the last diagnostic request response sender. 
        #Example print can_inst.GetDiagResponseSender()
        #
        #Displays the following to the output console:
        #
        #TSSR447 
        return self.diagResponseAttributes[3]

    def DiagReqFromStream(self, request):
        #Syntax DiagReqFromStream(request) 
        #Description Creates a diagnostic request object with the given byte stream (as described in the diagnostic description (*.cdd) file).
        #Parameters 1. request (string of hex numbers or list of base 10 or base 16 integers) The byte stream representing the diagnostic request.  
        #Return Values List of strings representing the response byte stream. 
        #Example 
        #print can_inst.DiagReqFromStream([0x22, 0xFD, 0x07])
        #or:
        #print can_inst.DiagReqFromStream([34, 253, 7])
        #or:
        #print can_inst.DiagReqFromStream('22 FD 07')
        #or:
        #print can_inst.DiagReqFromStream('    PDU     22 fd 07   ')
        #
        #Displays the following to the output console:
        #
        #Attributes of response 1: Positive Response; With code: 7; Sender: TSSR447; Stream:
        #62 FD 07 03 03 00 1E 05 DC 0B B8 07 D0 01 2C 01 2C 01 2C 01 2C 00 00 01 F4 03 E8 00 00 00 00 89 0B 00
        #['62', 'FD', '07', '03', '03', '00', '1E', '05', 'DC', '0B', 'B8', '07', 'D0', '01', '2C', '01', '2C', '01', '2C', '01', '2C', '00', '00', '01', 'F4', '03', 'E8', '00', '00', '00', '00', '89', '0B', '00'] 
        responseStream = -1
        if (isinstance(request, basestring)):
            request = request.replace('PDU', '').replace(',', '').replace("'","").split()
            print request
            request = [int (i, 16) for i in request]
        assert isinstance(request, list)
        
        if (self.Application.Networks.Count == 0):
            print 'No active networks'
        else:
            #Wait until measurement is started before continuing.
            if (self.Running() != True):
                #self.CompileAll()
                self.Start()
            #Select the diagnostic device, create and send the request.
            diagDev = self.Application.Networks(self.diagNetwork).Devices(self.diagDevice).Diagnostic
            diagReq = diagDev.CreateRequestFromStream(request)
            diagReq.Send()
            #Wait for a response or a timeout, then output response details.
            while diagReq.Pending:
                sleep(.1) #100 ms
            if (diagReq.Responses.Count == 0):
                print 'No Response received!'
            else:
                for k in range (1, diagReq.Responses.Count + 1):
                    diagResp = diagReq.Responses(k)
                    tempstr = 'Attributes of response ' + str(k)
                    self.diagResponseAttributes[0] = str(k)
                    if (diagResp.Positive):
                        tempstr = tempstr + ': Positive'
                        self.diagResponseAttributes[1] = 'Positive'
                    else:
                        tempstr = tempstr + ': Negative'
                        self.diagResponseAttributes[1] = 'Negative'
                    tempstr = tempstr + ' Response with code: ' + str(diagResp.ResponseCode)
                    self.diagResponseAttributes[2] = str(diagResp.ResponseCode)
                    tempstr = tempstr + '; Sender: ' + str(diagResp.Sender)
                    self.diagResponseAttributes[3] = str(diagResp.Sender)
                    #tempstr = tempstr + '; AsciiStream: ' + str(diagResp.Stream)
                    responseStream = [hex(ord(i)).upper().replace("0X", "") for i in str(diagResp.Stream)]
                    for i in range(0, len(responseStream)):
                        if (len(responseStream[i])==1):
                            responseStream[i]= '0'+responseStream[i]
                    print tempstr
                    print 'Hex Bytestream:' + str([i for i in responseStream]).replace('[', '').replace(']', '').replace("'", '').replace(',','')
                    diagResp = 0
            diagDev = 0
        return responseStream

    diagNetwork = 'BODY'
        #Type String 
        #Description The (name of the) network used in diagnostic operations. 
        #Access GetDiagNetwork, SetDiagNetwork 
        #Usage AddDiagDescription, DiagReq, DiagReqFromStream 
        #Example diagNetwork = 'BODY' 

    def GetDiagNetwork(self):
        #Syntax GetDiagNetwork() 
        #Description Returns the (name of the) network used in diagnostic operations (the value of  the diagNetwork property). 
        #Parameters - 
        #Return Values String containing the name of the diagnostics network. 
        #Example print can_inst.GetDiagNetwork()
        #
        #Displays the following to the output console:
        #
        #BODY 
        return self.diagNetwork

    def SetDiagNetwork(self, network):
        #Syntax SetDiagNetwork(network) 
        #Description Sets the network used in diagnostic operations (DiagReq, DiagReqFromStream etc.) by setting the diagNetwork property. 
        #Parameters 1. network (string) The name of the network used in diagnostic operations. 
        #Return Values - 
        #Example can_inst.SetDiagNetwork('BODY') 
        self.diagNetwork = network

    diagDevice = 'TSSR447'
        #Type String 
        #Description The (name of the) device used in diagnostic operations. 
        #Access GetDiagDevice, SetDiagDevice 
        #Usage DiagReq, DiagReqFromStream 
        #Example diagDevice = 'TSSR447' 

    def GetDiagDevice(self):
        #Syntax GetDiagDevice() 
        #Description Returns the (name of the) device used in diagnostic operations (the value of  the diagDevice property). 
        #Parameters - 
        #Return Values String  containing the name of the diagnostics device. 
        #Example print can_inst.GetDiagDevice()
        #
        #Displays the following to the output console:
        #
        #TSSR447 
        return self.diagDevice

    def SetDiagDevice(self, device):
        #Syntax SetDiagDevice(device) 
        #Description Sets the device used in diagnostic operations (DiagReq, DiagReqFromStream etc.) by setting the diagDevice property. 
        #Parameters 1. device (string) The name of the deviced used in diagnostic operations. 
        #Return Values - 
        #Example can_inst.SetDiagDevice('TSSR447') 
        self.diagDevice = device

    diagPath = 'D:\DSUsers\UIDR5732\Projects\\viano\TSSR447.txt'
        #Type String 
        #Description The path of the diagnostics description (*.xml) file generated from the encrypted CANdela (*.cdd) file to be used by the DiagReq method. 
        #Access GetDiagPath, SetDiagPath 
        #Usage DiagReq 
        #Example diagPath = 'D:\\viano\TSSR447.xml' 

    def GetDiagPath(self):
        #Syntax GetDiagPath() 
        #Description Returns the path of the diagnostics description (*.xml) file generated from the encrypted CANdela (*.cdd) file to be used by the DiagReq method (the value of the diagPath property). 
        #Parameters - 
        #Return Values String containing the path of the *.xml diagnostic description file. 
        #Example print can_inst.GetDiagPath()
        #
        #Displays the following to the output console:
        #
        #D:\\viano\TSSR447.xml 
        return self.diagPath

    def SetDiagPath(self, path):
        #Syntax SetDiagPath(path) 
        #Description Sets the path of the diagnostics description (*.xml) file generated from the encrypted CANdela (*.cdd) file to be used by the DiagReq method by setting the diagPath property. 
        #Parameters 1. path (string) The absolute path of the *.xml file. 
        #Return Values - 
        #Example can_inst.SetDiagPath('D:\\viano\TSSR447.xml')
        self.diagPath = path

    diagDoc = NULL
        #Type xml.dom.minidom.Document instance 
        #Description The variable used to store the XML diagnostics description (located at diagPath) tree hierarchy to be used by the DiagReq method. 
        #Access ParseDiagDoc 
        #Usage DiagReq 
        #Example - 

    def ParseDiagDoc(self):
        #Syntax ParseDiagDoc() 
        #Description Parses the document with the path set into diagPath (with SetDiagPath) and stores it in the diagDoc variable to be used by the DiagReq operation. This method must be called before using DiagReq. 
        #Parameters - 
        #Return Values - 
        #Example can_inst.ParseDiagDoc() 
        self.diagDoc = minidom.parse(self.diagPath)

    def DiagReq(self, diagService, diagVar = -1, diagValue = -1):
        #Syntax DiagReq(diagService, [diagVar], [diagValue]) 
        #Description Creates a diagnostic request using the complex parameters (the diagnostic service diagService, the service parameter diagVar and the parameter value diagValue). 
        #Parameters 
        #1. diagService (string) The name of the diagnostics service (as described in the diagnostic description (*.cdd) file).
        #2. diagVar (string, optional) The name of the service parameter (as described in the diagnostic description (*.cdd) file).
        #3. diagValue (string, optional) The value of the service parameter (as described in the diagnostic description (*.cdd) file). 
        #Return Values List of strings representing the response byte stream. 
        #Example print can_inst.DiagReq('Configuration Lesen')
        #
        #Displays the following to the output console:
        #
        #Attributes of response 1: Positive Response; With code: 7; Sender: TSSR447; Stream:
        #62 FD 07 03 03 00 1E 05 DC 0B B8 07 D0 01 2C 01 2C 01 2C 01 2C 00 00 01 F4 03 E8 00 00 00 00 89 0B 00
        #['62', 'FD', '07', '03', '03', '00', '1E', '05', 'DC', '0B', 'B8', '07', 'D0', '01', '2C', '01', '2C', '01', '2C', '01', '2C', '00', '00', '01', 'F4', '03', 'E8', '00', '00', '00', '00', '89', '0B', '00']
        #
        #or:
        #print can_inst.DiagReq('Configuration Schreiben','Max crank restart time','1500 miliseconds')
        #
        #Displays the following to the output console:
        #
        #Attributes of response 1: Positive Response; With code: 7; Sender: TSSR447; Stream:
        #62 FD 07 03 03 00 1E 13 88 0B B8 07 D0 01 2C 01 2C 01 2C 01 2C 00 00 01 F4 03 E8 00 00 00 00 89 0B 00
        #2E FD 07 03 03 00 1E 05 DC 0B B8 07 D0 01 2C 01 2C 01 2C 01 2C 00 00 01 F4 03 E8 00 00 00 00 89 0B 00
        #Attributes of response 1: Positive Response; With code: 7; Sender: TSSR447; Stream:
        #6E FD 07
        #['6E', 'FD', '07'] 
        diagServiceAux = diagService
        if diagService.endswith('Lesen'):
            if diagService.endswith(': Lesen'):
                diagService = diagService[:-7]
            elif (diagService.endswith(' Lesen') or diagService.endswith(':Lesen')):
                diagService = diagService[:-6]
            elif diagService.endswith('Lesen'):
                diagService = diagService[:-5]
        if diagService.endswith('Schreiben'):
            if diagService.endswith(': Schreiben'):
                diagService = diagService[:-11]
            elif (diagService.endswith(' Schreiben') or diagService.endswith(':Schreiben')):
                diagService = diagService[:-10]
            elif diagService.endswith('Schreiben'):
                diagService = diagService[:-9]

        diagServiceList = self.diagDoc.getElementsByTagName('NAME')
        diagServiceIndex = -1
        for k in range (0, len(diagServiceList)):
            if (diagServiceList[k].childNodes[0].nodeValue == diagService):
                diagServiceIndex = k
                print k, '***', diagServiceList[k].childNodes[0].nodeValue
        print 'diag service index: (!=-1 OK)', diagServiceIndex
        if diagServiceAux.endswith('Schreiben'):
            diagRequestList = diagServiceList[diagServiceIndex].parentNode.getElementsByTagName('VARCODEFRAGS')[0].getElementsByTagName('VARCODEFRAG')
            diagRequestIndex = -1
            for j in range (0, len(diagRequestList)):
                if (diagRequestList[j].getElementsByTagName('FRAGNAME')[0].childNodes[0].nodeValue == diagVar):
                    diagRequestIndex = j
                    print j, '***', diagRequestList[j].getElementsByTagName('FRAGNAME')[0].childNodes[0].nodeValue
            print 'diag request index: (!=-1 OK)', diagRequestIndex
            
            diagValueList = diagRequestList[diagRequestIndex].getElementsByTagName('FRAGDESCR')
            diagValueIndex = -1
            for i in range (0, len(diagValueList)):
                if (diagValueList[i].getElementsByTagName('FRAGMEANING')[0].childNodes[0].nodeValue == diagValue):
                    diagValueIndex = i
                    print i, '***', diagValueList[i].getElementsByTagName('FRAGMEANING')[0].childNodes[0].nodeValue
            print 'diag value index: (!=-1 OK)', diagValueIndex
            print '***'
            print 'data value:', str(diagValueList[diagValueIndex].getElementsByTagName('FRAGVAL')[0].childNodes[0].nodeValue).replace("$", "").replace(" ", ", ")
            
            dataValue = str(diagValueList[diagValueIndex].getElementsByTagName('FRAGVAL')[0].childNodes[0].nodeValue).replace("$", "0x").split()
            dataValue = [str(i).upper().replace("0X", "") for i in dataValue]
            print dataValue
            
            dataType = diagRequestList[diagRequestIndex].getElementsByTagName('FRAGTYPE')[0].childNodes[0].nodeValue
            dataLength = diagRequestList[diagRequestIndex].getElementsByTagName('FRAGLENGTH')[0].childNodes[0].nodeValue
            dataPosition = diagRequestList[diagRequestIndex].getElementsByTagName('BYTEPOSITION')[0].childNodes[0].nodeValue
            
            print 'data type:', dataType
            print 'data length:', dataLength
            print 'data position:', dataPosition
            if (dataType == "BIT"):
                bitPosition = diagRequestList[diagRequestIndex].getElementsByTagName('BITPOSITION')[0].childNodes[0].nodeValue
                print 'bit position:', bitPosition
        
        for k in range (0, len(diagServiceList)):
            if (diagServiceList[k].childNodes[0].nodeValue == diagServiceAux):
                diagServiceIndex = k
                print k, '***', diagServiceList[k].childNodes[0].nodeValue
        print 'diag service index: (!=-1 OK)', diagServiceIndex
        recordDataIdentifier = str(diagServiceList[diagServiceIndex].parentNode.getElementsByTagName('PARAMETERS')[0].getElementsByTagName('PARAMETER')[0].childNodes[0].nodeValue)[1:]
        recordDataIdentifier = " ".join(recordDataIdentifier[0:])
        recordDataIdentifier = recordDataIdentifier.replace(' ', '', 1)
        recordDataIdentifier = recordDataIdentifier[:2] + ' ' + recordDataIdentifier[3:].replace(' ', '', 1)
        
        print 'recordDataIdentifier: ' + recordDataIdentifier
        print str(recordDataIdentifier).split()
        
        if diagServiceAux.endswith('Lesen'):
            return self.DiagReqFromStream('22 ' + recordDataIdentifier)
        elif diagServiceAux.endswith('Schreiben'):
            responseStream = self.DiagReqFromStream('22 ' + recordDataIdentifier)
            responseStream[0] = '2E'
            if (dataType == 'BYTE'):
                for i in range (0, int(dataLength)):
                    responseStream[i+3+int(dataPosition)] = str(dataValue).split()[i]
                requestStream = str([i for i in responseStream]).replace('[', '').replace(']', '').replace("'", '').replace(',','').replace('"','')
                print requestStream
            elif (dataType == 'BIT'):
                binSize = len(dataValue[0])*4
                binVal = bin(int(dataValue[0], 16))[2:].zfill(int(dataLength))
                binOldVal = bin(int(responseStream[3+int(dataPosition)], 16))[2:].zfill(binSize)
                binNewVal = list(binOldVal)
                for i in range (0, int(dataLength)):
                    binNewVal[7-int(bitPosition)-i] = list(binVal)[-i-1]
                responseStream[3+int(dataPosition)] = hex(int(''.join(binNewVal), 2)).upper().replace('0X', '')
                requestStream = str([i for i in responseStream]).replace('[', '').replace(']', '').replace("'", '').replace(',','').replace('"','')
            return self.DiagReqFromStream(requestStream)

    def ExtractBitsFromByte(self, byte, position, length):
        #Syntax ExtractBitsFromByte(byte, position, length) 
        #Description Extracts a sequence of bits from a byte (from the diagnostic response strem, the return value of the DiagReqFromStream method) that needs to be verified.
        #
        #Parameters
        #1. byte (string, base 10 or base 16 integer) The byte (from a diagnostic response stream) storing the bit(s) that need(s) to be verified.
        #2. position (integer) The position of the bit(s) in the byte byte in right to left order (least significant bit -> most significant bit).
        #3. length (integer) The length of the sequence of bits in the byte byte (1-7).
        #
        #Return Values Integer representing the base 10 conversion of the bit(s) that need to be verified. 
        #Example print can_inst.ExtractBitsFromByte('3D', 2, 3)
        #or:
        #print can_inst.ExtractBitsFromByte(0x3d, 2, 3)
        #or:
        #print can_inst.ExtractBitsFromByte(61, 2, 3)
        ##3D(16) = 61(10) = 00111101(2)
        #
        #Displays the following to the output console:
        #
        #7
        if isinstance(byte, basestring):        
            bitString = bin(int(byte, 16))[2:].zfill(8)
        else:
            bitString = bin(int(str(byte)))[2:].zfill(8)
        returnVal = NULL
        for i in range (0, length):
            returnVal += (2**i)*(int(bitString[-i-1-position]))
        return returnVal

    def VersionBuild(self):
        #Syntax VersionBuild() 
        #Description Returns the build number of the CANoe/CANalyzer application.
        #Parameters - 
        #Return Values String containing the CANoe application build version. 
        #Example print can_inst.VersionBuild()
        #
        #Displays the following to the output console:
        #
        #64
        return self.Application.Version.Build

    def VersionFullName(self):
        #Syntax VersionFullName() 
        #Description Returns the complete CANoe/CANalyzer version in the following format: 
        #"Vector CANoe /run 6.0.50" or "Vector CANoe.LIN /run 6.0.50"  
        #Parameters - 
        #Return Values String containing the full name of the CANoe application version. 
        #Example print can_inst.VersionFullName()
        #
        #Displays the following to the output console (see the image example of the VersionBuild method description):
        #
        #Vector CANoe.LIN /run 8.2.64 
        return self.Application.Version.FullName

    def VersionMajor(self):
        #Syntax VersionMajor() 
        #Description Returns the major version number of the CANoe/CANalyzer application. 
        #Parameters - 
        #Return Values String containing the major version number. 
        #Example print can_inst.VersionMajor()
        #
        #Displays the following to the output console (see the image example of the VersionBuild method description):
        #
        #8 
        return self.Application.Version.Major

    def VersionMinor(self):
        #Syntax VersionMinor() 
        #Description Returns the minor version number of the CANoe/CANalyzer application. 
        #Parameters - 
        #Return Values String containing the minor version number. 
        #Example print can_inst.VersionMinor()
        #
        #Displays the following to the output console (see the image example of the VersionBuild method description):
        #
        #2
        return self.Application.Version.Minor

    def VersionName(self):
        #Syntax VersionName() 
        #Description Returns The CANoe/CANalyzer version in the following format:
        #"CANoe 5.1 SP2" (with Service Pack) or "CANoe.LIN 5.1" (without Service Pack) . 
        #Parameters - 
        #Return Values String containing the version name. 
        #Example print can_inst.VersionName()
        #
        #Displays the following to the output console (see the image example of the VersionBuild method description):
        #
        #CANoe.LIN 8.2 SP2
        return self.Application.Version.Name

    def VersionPatch(self):
        #Syntax VersionPatch() 
        #Description Returns the patch number of the CANoe/CANalyzer application. 
        #Parameters - 
        #Return Values String containing the version patch. 
        #Example print can_inst.VersionPatch()
        #
        #Displays the following to the output console (see the image example of the VersionBuild method description):
        #
        #0
        return self.Application.Version.Patch

# def test():
#     can_inst = CANoe()
# 
# test()