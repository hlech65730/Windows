'''
Created on May 27, 2015

@author: uidr0108
'''
import re
import sys

class Message():
    name = ""
    id = -1
    transmyter = ""
    dlc = 0
    signals = []
    longName = ""
    diagResponse = ""
    diagRequest = ""
    genMsgSendType = []
    genMsgDelayTime = []
    genMsgCycleTime = []
    genMsgStartDelayTime = []
    addRemark = []
    data = "0x00";
    
class CANSignal: 
    name = ""
    startbit = -1
    length = -1
    factor = -1
    offset = -1
    minimum = -1
    maximum = -1
    unit = ""
    recievers = []
    valueType = ""
    multiplexing = ""
    byteOrder = ""   

class DBC_Parser() : 
    
    arrMessages = []                   #List of all messages. Each Item is of type Message
    arrSignals = []                    #List of all signals. Each signal is of type CANSignal
    arrGenMsgSendTypeEnumAux = []      #Auxiliary list for geting enum lists
    mxGenMsgSendTypeEnum = []          #The enum list for GenMsgSendType
    strFile = ""                       #The content of the .dbc file
    strFilename = ""                   #The name of the .dbc file
    iIndex = 0                         #The self.iIndex of searched string in file
    iCursor = 0                        #Variable used for positioning the self.iCursor in file after index
    arrstrLines = []                   #The list of all lines of the file
    strLine = ""                       #A line from arrstrList
    arrDiagRequest = []                #The enum list for DiagRequest
    arrDiagResponse = []               #The enum list for DiagResponse
    arrRequestMessage = []             #The enum list for RequestMessag
    global msgDefMessage               #A message with default parameters
    arrmsgMessages = []                #Auxiliary message list for getting the message properties more efficiently 
    
    def __init__(self, filename = ""):
        '''
        Reads the file and initializes the ENUM arrays and the default message values.
        filename parameter must include the complete path to the file
        
        filename = the name (and path) of the dbc file   
        '''
#         try:
        
        '''Variable initialization'''
        self.arrMessages = []                   #List of all messages. Each Item is of type Message
        self.arrSignals = []                    #List of all signals. Each signal is of type CANSignal
        self.arrGenMsgSendTypeEnumAux = []      #Auxiliary list for geting enum lists
        self.mxGenMsgSendTypeEnum = []          #The enum list for GenMsgSendType
        self.strFile = ""                       #The content of the .dbc file
        self.strFilename = ""                   #The name of the .dbc file
        self.iIndex = 0                         #The self.iIndex of searched string in file
        self.iCursor = 0                        #Variable used for positioning the cursor in file after index
        self.arrstrLines = []                   #The list of all lines of the file
        self.strLine = ""                       #A line from arrstrList
        self.arrDiagRequest = []                #The enum list for DiagRequest
        self.arrDiagResponse = []               #The enum list for DiagResponse
        self.arrRequestMessage = []             #The enum list for RequestMessag
        self.arrmsgMessages = []    
        
        '''Open, read and close the file'''      
        fo = open(filename ,  "r")
        self.arrstrLines = fo.readlines()     
        fo.close()
        
        '''Reinitialize the message values'''
        self.msgDefMessage = Message() 
        self.msgDefMessage.name = ""
        self.msgDefMessage.id = -1
        self.msgDefMessage.transmyter = ""
        self.msgDefMessage.dlc = 0
        self.msgDefMessage.signals = []
        self.msgDefMessage.longName = ""
        self.msgDefMessage.diagResponse = ""
        self.msgDefMessage.diagRequest = ""
        self.msgDefMessage.genMsgSendType = []
        self.msgDefMessage.genMsgDelayTime = []
        self.msgDefMessage.genMsgCycleTime = []
        self.msgDefMessage.genMsgStartDelayTime = []
        self.msgDefMessage.addRemark = []
        self.msgDefMessage.data = "0x00";
        
        #for each line in file
        for self.strLine in self.arrstrLines:
            
            self.strLine = re.split(' |;|:|,|\n|=|"', self.strLine)
            self.strLine = filter(None, self.strLine)
            '''Get ENUM values for GenMsgSendType, GenMsgSendType2, GenMsgSendType3, GenMsgSendType4, GenMsgSendType5'''
            #if the line is the one with GenMsgSendType, GenMsgSendType2,GenMsgSendType3, GenMsgSendType4 or GenMsgSendType5 ENUM
            if (len(self.strLine) > 4 and self.strLine[0] == "BA_DEF_" and self.strLine[1] == "BO_" and self.strLine[3] == "ENUM" and (self.strLine[2] == "GenMsgSendType" or self.strLine[2] == "GenMsgSendType2" or self.strLine[2] == "GenMsgSendType3" or self.strLine[2] == "GenMsgSendType4" or self.strLine[2] == "GenMsgSendType5")):   
                for i in range(4, len(self.strLine)):
                    #add the value of the line
                    self.arrGenMsgSendTypeEnumAux.append(self.strLine[i]) 
                    
                self.mxGenMsgSendTypeEnum.append(self.arrGenMsgSendTypeEnumAux)
                #reinitializing tha array
                self.arrGenMsgSendTypeEnumAux = []
                
            '''Get ENUM values for DiagRequest'''
            if (len(self.strLine) == 6 and self.strLine[0] == "BA_DEF_" and self.strLine[1] == "BO_" and self.strLine[2] == "DiagRequest" and self.strLine[3] == "ENUM"):
                self.arrDiagRequest.append(self.strLine[4])
                self.arrDiagRequest.append(self.strLine[5])
                
            '''Get ENUM values for DiagResponse'''
            if (len(self.strLine) == 6 and self.strLine[0] == "BA_DEF_" and self.strLine[1] == "BO_" and self.strLine[2] == "DiagResponse" and self.strLine[3] == "ENUM"):
                self.arrDiagResponse.append(self.strLine[4])
                self.arrDiagResponse.append(self.strLine[5])
           
            '''Get the default values for a message'''            
            #get DiagRequest default value
            if (len(self.strLine) == 3 and self.strLine[0] =="BA_DEF_DEF_" and self.strLine[1] == "DiagRequest"):
                self.msgDefMessage.diagRequest = self.strLine[2]
                
            #get DiagResponse default value
            if (len(self.strLine) == 3 and self.strLine[0] == "BA_DEF_DEF_" and self.strLine[1] == "DiagResponse"):
                self.msgDefMessage.diagResponse = self.strLine[2]
              
            #get Message_Longname default value
            if (len(self.strLine) == 3 and self.strLine[0] == "BA_DEF_DEF_" and self.strLine[1] == "Message_Longname"):
                self.msgDefMessage.longName = self.strLine[ : self.iCursor]
            
            #get the default values for GenMsgSendType, GenMsgSendType2, GenMsgSendType3, GenMsgSendType4, GenMsgSendType5    
            if (len(self.strLine) == 3 and self.strLine[0] == "BA_DEF_DEF_" and (self.strLine[1] == "GenMsgSendType" or self.strLine[1] == "GenMsgSendType2" or self.strLine[1] == "GenMsgSendType3" or self.strLine[1] == "GenMsgSendType4" or self.strLine[1] == "GenMsgSendType5")):
                 #add the value of the line 
                self.msgDefMessage.genMsgSendType.append(self.strLine[2])
                
            #get the default values for AddRemark, AddRemark2, AddRemark3, AddRemark4, AddRemark5    
            if (len(self.strLine) > 1 and self.strLine[0] == "BA_DEF_DEF_" and (self.strLine[1] == "AddRemark" or self.strLine[1] == "AddRemark2" or self.strLine[1] == "AddRemark3" or self.strLine[1] == "AddRemark4" or self.strLine[1] == "AddRemark5")):
                #if the AddRemark is different from "" 
                if(len(self.strLine) == 3):
                    self.msgDefMessage.addRemark.append(self.strLine[2])
                else:
                    #if the AddRemark is ""
                    self.msgDefMessage.addRemark.append("")
            
            #get the default values for GenMsgCycleTime, GenMsgCycleTime2, GenMsgCycleTime3, GenMsgCycleTime4, GenMsgCycleTime5    
            if (len(self.strLine) == 3 and self.strLine[0] == "BA_DEF_DEF_"  and (self.strLine[1] == "GenMsgCycleTime" or self.strLine[1] == "GenMsgCycleTime2" or self.strLine[1] == "GenMsgCycleTime3" or self.strLine[1] == "GenMsgCycleTime4" or self.strLine[1] == "GenMsgCycleTime5")):
                #add the value of the line
                self.msgDefMessage.genMsgCycleTime.append(self.strLine[2])
            
            #get the default values for GenMsgDelayTime, GenMsgDelayTime2, GenMsgDelayTime3, GenMsgDelayTime4, GenMsgDelayTime5    
            if (len(self.strLine) == 3 and self.strLine[0] == "BA_DEF_DEF_" and (self.strLine[1] == "GenMsgDelayTime" or self.strLine[1] == "GenMsgDelayTime2" or self.strLine[1] == "GenMsgDelayTime3" or self.strLine[1] == "GenMsgDelayTime4" or self.strLine[1] == "GenMsgDelayTime5")):
                #add the value of the line
                self.msgDefMessage.genMsgDelayTime.append(self.strLine[2])
                
            #get the default values for GenMsgStartDelayTime, GenMsgStartDelayTime2, GenMsgStartDelayTime3, GenMsgStartDelayTime4, GenMsgStartDelayTime5    
            if (len(self.strLine) == 3 and self.strLine[0] == "BA_DEF_DEF_" and (self.strLine[1] == "GenMsgStartDelayTime" or self.strLine[1] == "GenMsgStartDelayTime2" or self.strLine[1] == "GenMsgStartDelayTime3" or self.strLine[1] == "GenMsgStartDelayTime4" or self.strLine[1] == "GenMsgStartDelayTime5")):
                #add the value of the line 
                self.msgDefMessage.genMsgStartDelayTime.append(self.strLine[2])
            try:    
                for i in range(len(self.msgDefMessage.genMsgSendType), 5):
                    self.msgDefMessage.genMsgSendType.append("")
            except TypeError:
                for i in range(0, 5):
                    self.msgDefMessage.genMsgSendType.append("")
            try:    
                for i in range(len(self.msgDefMessage.addRemark), 5):
                    self.msgDefMessage.addRemark.append("")
            except TypeError:
                for i in range(0, 5):
                    self.msgDefMessage.addRemark.append("")
            try:    
                for i in range(len(self.msgDefMessage.genMsgCycleTime), 5):
                    self.msgDefMessage.genMsgCycleTime.append("")
            except TypeError:
                for i in range(0, 5):
                    self.msgDefMessage.genMsgCycleTime.append("")
            try:    
                for i in range(len(self.msgDefMessage.genMsgDelayTime), 5):
                    self.msgDefMessage.genMsgDelayTime.append("")
            except TypeError:
                for i in range(0, 5):
                    self.msgDefMessage.genMsgStartDelayTime.append("")
            try:    
                for i in range(len(self.msgDefMessage.genMsgStartDelayTime), 5):
                    self.msgDefMessage.genMsgStartDelayTime.append("")
            except TypeError:
                for i in range(0, 5):
                    self.msgDefMessage.genMsgSendType.append("")
                
        self.getAllMessages()
#         except:
#             print "Unexpected error:", sys.exc_info()[1]
             
    def getAllMessages(self) : 
        '''
        Reads all the information about messages and puts it in the 'messages' list.
        '''    
#         try:                
        self.iIndex = 0
        #for each line in file
        for self.strLine in self.arrstrLines:
            self.iIndex = self.iIndex + 1
            
            self.strLine = re.split(' |;|:|,|\n|=|\t|"', self.strLine)
            self.strLine = filter(None, self.strLine)
            #if the line describes a message
            if (len(self.strLine) > 0 and self.strLine[0] == "BO_"):                    
                #create a new message and initialize the arrays with the default values from dbc file
                msg = Message()
                msg.name = self.msgDefMessage.name
                msg.id = self.msgDefMessage.id
                msg.transmyter = self.msgDefMessage.transmyter
                msg.dlc = self.msgDefMessage.dlc
                msg.signals = list(self.msgDefMessage.signals)
                msg.longName = self.msgDefMessage.longName
                msg.diagResponse  =self.msgDefMessage.diagResponse
                msg.diagRequest = self.msgDefMessage.diagRequest
                msg.genMsgSendType = list(self.msgDefMessage.genMsgSendType)
                msg.genMsgDelayTime = list(self.msgDefMessage.genMsgDelayTime)
                msg.genMsgCycleTime = list(self.msgDefMessage.genMsgCycleTime)
                msg.genMsgStartDelayTime = list(self.msgDefMessage.genMsgStartDelayTime)
                msg.addRemark = list(self.msgDefMessage.addRemark)
                msg.data = self.msgDefMessage.data
                
                #get the id value
                msg.id = int(self.strLine[1])
                
                #get the name value
                msg.name = self.strLine[2] 
                
                #get the DLC value                    
                msg.dlc = int(self.strLine[3])
                msg.data = "0x"
                for i in range(msg.dlc * 2):
                    msg.data = msg.data + '0'   #set the data value based on DLC
                
                #get the transmyter value
                msg.transmyter = self.strLine[4]
                i = 0
                # the delimiter between two messages is an empty line
                while self.arrstrLines[self.iIndex + i] != "\n":
                    #get the signal
                    sgn=self.getSignal(self.iIndex + i, msg.name)
                    i = i + 1
                      
                    msg.signals.append(sgn)
                    self.arrSignals.append(sgn)                    
                
                self.arrMessages.append(msg)
                self.arrmsgMessages = self.arrMessages [:]
            
            #add the DiagResponse to the message   
            if ("BA_" in self.strLine and "DiagResponse" in self.strLine and "BO_" in self.strLine):
                for iIndex in range(len(self.arrmsgMessages)):
                    #add DiagResponse to the message
                    if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):                        
                        self.arrmsgMessages[iIndex].diagResponse = self.arrDiagResponse[int(self.strLine[4])]
                        break
                                    
            #add DiagRequest to the message
            if ("BA_" in self.strLine and "DiagRequest" in self.strLine and "BO_" in self.strLine):
                for iIndex in range(len(self.arrmsgMessages)):
                    #add DiagRequest to the message
                    if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):                        
                        self.arrmsgMessages[iIndex].diagRequest = self.arrDiagRequest[int(self.strLine[4])]
                        break
                 
            #add Message_Longname to the message
            if ("BA_" in self.strLine and "Message_Longname" in self.strLine and "BO_"  in self.strLine):
                for iIndex in range(len(self.arrmsgMessages)):
                    #add Message_Longname to the message
                    if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):                        
                        self.arrmsgMessages[iIndex].longName = self.strLine[4]
                        break       
                 
            #add GenMsgCycleTime to the message
            if ("BA_" in self.strLine and "GenMsgCycleTime"  in self.strLine and "BO_"  in self.strLine):
                for iIndex in range(len(self.arrmsgMessages)):
                    #add GenMsgCycleTime to the message
                    if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):                        
                        self.arrmsgMessages[iIndex].genMsgCycleTime[4] = self.strLine[4]
                        break
                 
            #add GenMsgDelayTime to the message
            if ("BA_" in self.strLine and "GenMsgDelayTime" in self.strLine and "BO_" in self.strLine):
                self.iIndex = 0      
                for iIndex in range(len(self.arrmsgMessages)):
                    #add GenMsgDelayTime to the message   
                    if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):   
                        self.arrmsgMessages[iIndex].genMsgDelayTime[4] = self.strLine[4]
                        break  
                 
            #add GenMsgStartDelayTime to the message
            if ("BA_" in self.strLine and "GenMsgStartDelayTime" in self.strLine and "BO_" in self.strLine):
                for iIndex in range(len(self.arrmsgMessages)):
                    #add GenMsgDelayTime to the message
                    self.iIndex = self.iIndex + 1
                    if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):                       
                        self.arrmsgMessages[iIndex].genMsgStartDelayTime[4] = self.strLine[4]
                        break
                 
            #add GenMsgSendType to the message
            if ("BA_" in self.strLine and "GenMsgSendType" in self.strLine and "BO_" in self.strLine):
                for iIndex in range(len(self.arrmsgMessages)):
                    #add GenMsgDelayTime to the message
                    if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):                        
                        self.arrmsgMessages[iIndex].genMsgSendType[4] = self.strLine[4]
                        break
                 
            #add AddRemark to the message
            if ("BA_" in self.strLine and "AddRemark" in self.strLine and "BO_" in self.strLine):
                for iIndex in range(len(self.arrmsgMessages)):
                    #add AddRemark to the message
                    if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):  
                        if(len(self.strLine) > 5):                      
                            self.arrmsgMessages[iIndex].addRemark[4] = self.strLine[4]
                        else:
                            self.arrmsgMessages[iIndex].addRemark[4] = ""
                        break
                
            for i in range(2,6):
                #add GenMsgCycleTime 2-5 to the message
                if ("BA_" in self.strLine and "GenMsgCycleTime%d" %i and "BO_" in self.strLine):
                    for iIndex in range(len(self.arrmsgMessages)):
                        #add GenMsgCycleTime to the message
                        if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])): 
                            if(len(self.strLine) > 5):                     
                                self.arrmsgMessages[iIndex].genMsgCycleTime[5 -i] = self.strLine[4]
                                self.arrmsgMessages[iIndex].genMsgCycleTime[5 -i] = 0
                            break
                        
                #add GenMsgDelayTime 2-5 to the message
                if ("BA_" in self.strLine and "GenMsgDelayTime%d" %i in self.strLine and "BO_" in self.strLine):
                    for iIndex in range(len(self.arrmsgMessages)):
                        #add GenMsgDelayTime to the message
                        if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):                        
                            self.arrmsgMessages[iIndex].genMsgDelayTime[5 - i] = self.strLine[4]
                            break
                 
                #add GenMsgStartDelayTime 2-5 to the message
                if ("BA_" in self.strLine and "GenMsgStartDelayTime%d" %i in self.strLine and "BO_" in self.strLine):
                    for iIndex in range(len(self.arrmsgMessages)):
                        #add GenMsgStartDelayTime to the message
                        self.iIndex = self.iIndex + 1
                        if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):                        
                            self.arrmsgMessages[iIndex].genMsgStartDelayTime[5 - i] = self.strLine[4]
                            break
                 
                #add GenMsgSendType 2-5 to the message
                if ("BA_" in self.strLine and "GenMsgSendType%d" %i in self.strLine and "BO_" in self.strLine):
                    for index in range(len(self.arrmsgMessages)):
                        #add GenMsgSendType to the message
                        if (self.arrmsgMessages[iIndex].id == int(self.strLine[3]) ):                        
                            self.arrmsgMessages[iIndex].genMsgSendType[5 - i] = self.strLine[4]
                            break
                 
                #add AddRemark 2-5 to the message
                if ("BA_" in self.strLine and "AddRemark%d" in self.strLine and "BO_" in self.strLine):
                    for iIndex in range(len(self.arrmsgMessages)):
                        #add AddRemark to the message
                        if (self.arrmsgMessages[iIndex].id == int(self.strLine[3])):                        
                            self.arrmsgMessages[iIndex].addRemark[5 -i] = self.strLine[4]
                            break
#         except:
#             print "Unexpected error:", sys.exc_info()[1] 
            
    def getSignal(self, iLineIndex, strMsgName):
        '''
        Reads all the information about signals and returns a CANSignal object containing the neccesary information
       
        iLiniIndex = the line in DBC file where the signal info starts
        strMsgName = the name of the message the signal is bound to
        ''' 
#         try:        
        #get the line
        self.strLine = self.arrstrLines[iLineIndex]
        self.strLine = re.split(' |;|,|\n|=|@|[|]|\t|', self.strLine)
        self.strLine = filter(None, self.strLine)
        #supplimentary check to be sure that the line describes a signal
        if(len(self.strLine) > 0 and self.strLine[0] == "SG_"):
            #create a new signal
            sgn = CANSignal()
            sgn.recievers = []
            
            #get the name value
            sgn.name = self.strLine[1]
            #verfy if there is any multiplexing and set the corresponding attribute of the signal
            if (self.strLine[2] == ':'):
                #the signal is not multiplexed
                sgn.multuplexing = '-'
                self.iCursor = 3
            else:
                #the line is multiplexed
                self.iCursor = 4
                sgn.multiplexing = strMsgName + '_Multiplexor = 0x'+self.strLine[2]
            #get the startbit value                   
            sgn.startbit = int(self.strLine[self.iCursor])
            #get the length value
            sgn.length = int(self.strLine[self.iCursor + 1])
            #get the byte order value
            if ('1' in self.strLine[self.iCursor + 2]):
                sgn.byteOrder = 'Intel'
            else:
                sgn.byteOrder = 'Motorola'
            #get the value type value
            if ('+' in self.strLine[self.iCursor + 2]):
                sgn.valueType = 'Unsigned'
            else:
                sgn.valueType = 'Signed'
            #get the factor value
            sgn.factor = float(self.strLine[self.iCursor + 3][1 : ])
            #get the offset value
            sgn.offset = float(self.strLine[self.iCursor + 4][ : -1])
            #get the minimum value
            sgn.minimum = float(self.strLine[self.iCursor + 5][1 : ])
            #get the maximum value
            sgn.maximum = float(self.strLine[self.iCursor + 6][ : -1])
            #get the unit value
            sgn.unit = self.strLine[self.iCursor + 7][1 : -1]
            #get all the recievers
            for i in range(self.iCursor + 8, len(self.strLine)):
                #get the reciever value
                sgn.recievers.append(self.strLine[i])
              
            return sgn
                
#         except:
#             print "Unexpected error:", sys.exc_info()[1] 
#             return None