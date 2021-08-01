import time, os
import sys,os
import isystem.connect as ic


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # add the Workspace directory to PATH
sys.path.append('\\'.join(os.path.dirname(__file__).split('\\')[:-1])) # line required because path is a symlink - it only adds the root SWT directory to path


class debugger_helper():

    def __init__(self,dbg):
        self.dbg = dbg
    def getAccesType(self,accesFlag):
        accesType=ic.IConnectDebug.fRealTime
        if accesFlag == "fMonitor" :
            accesType=ic.IConnectDebug.fMonitor
        elif accesFlag == "fRealTime" :
            accesType=ic.IConnectDebug.fRealTime
        elif accesFlag == "fMemMask" :
            accesType=ic.IConnectDebug.fMemMask
        elif accesFlag == "fCore" :
            accesType=ic.IConnectDebug.fCore
        elif accesFlag == "fSFR" :
            accesType=ic.IConnectDebug.fSFR
        return accesType
    def getExpressionValue(self,expressionType,expression):
        retVal=None
        if expressionType=="int" or expressionType=="uint8" or expressionType=="sint8" or expressionType=="uint16" or expressionType=="sint16":
            retVal=expression.getInt()
        elif expressionType=="long" or expressionType=="uint32" or expressionType=="sint32" :
            retVal=expression.getLong()
        elif expressionType=="double":
            retVal=expression.getDouble()
        elif expressionType=="float":
            retVal=expression.getFloat()
        return retVal;
    def getCValue(self,expressionValue,expressionType):
        type = ic.SType()
        if(expressionType[0]=="u"):
            type.m_byType=ic.SType.tUnsigned
        else :
            type.m_byType=ic.SType.tSigned
        if((len(expressionType)>3) and (expressionType[1:4]=="int")):
            type.m_byBitSize = int(expressionType[4:])
        else :
            type.m_byBitSize = 32
        value = ic.CValueType(type, expressionValue)
        return value

    def modify(self,accesFlag,expression,value):
        '''helps make a debug modify call'''
        accesType=self.getAccesType(accesFlag)
        #return dbg.modify(accesType,expression,value)
        print "modified"
        return 1
    def evaluate(self,accesFlag,expression,expressionType):
        '''helps evaluate an expression'''
        accesType=self.getAccesType(accesFlag)
        evalValue=None
        evalValue=dbg.evaluate(accesType,expression)
        evalValue=self.getExpressionValue(expressionType,evalValue)
        return evalValue
    def readRegister(self,accesFlag,registerName,expressionType):
        '''helps read a register'''
        accesType=self.getAccesType(accesFlag)
        evalValue=None
        evalValue=dbg.readRegister(accesType,registerName)
        evalValue=self.getExpressionValue(expressionType,evalValue)
        return evalValue
    def writeRegister(self,accesFlag,registerName,registerValue,registerType):
        '''helps write to a register'''
        accesType=self.getAccesType(accesFlag)	
        regVal=self.getCValue(registerValue,registerType)
        return dbg.writeRegister(accesType,registerName,regVal)
        
            
    








