'''
    Author: C. Bruma
    Purpose: Parsing a *.ldf file for communicating between devices via LIN
    Date: 08-06-2015        
    Arguments: -   
    Outputs: -    
    Dependencies: -

    History:
    ------------------------------------------------------------------------------
    Revision | Date:      | Modification:                             | Author
    .......................................................................
    v0.1     | 08-06-2015 | Creation                                  | C. Brunma
    ------------------------------------------------------------------------------
'''

import copy
import re

class Nodes:
    '''Class defining a LIN node'''    
    type = ""
    name = ""
    linProtocol = 0
    configuredNAD = 0
    initialNAD = 0
    productID = []
    responseError = "";
    P2min = "0.0 ms"
    STmin = "0.0 ms"
    configFrames = []
    jitter = "-1 ms"
    timebase = "-1 ms"
    
class ScheduleTable:
    '''Class defining a LIN schedule table'''
    frames = []
    delay = []
    name = ""
    
    def __len__(self):
        return len(self.frames)

class LINSignal: 
    '''Class defining a LIN signal'''   
    name = ""
    length = 0
    initVal = []
    publisher = ""
    subscribers = []
    startbit = -1
    
class LINDiagnosticSignal:   #just reading from LDF 
    '''Class defining a LIN diagnostic signal'''
    name = ""
    lengh = 0
    initVal = 0
    publisher = []
    subscribers = []
    
class Frame:    
    '''Class defining a LIN frame (message)'''
    name = ""
    size = 0
    publisher = ""
    subscribers = []
    frameID = 0
    signals = []
    data = "0x00"

class LIN_Parser:
    '''Class defining a *.ldf parser'''
    arrstrLines = []        #list of lines in file
    strCategory = ""        #string that shows the current reading category from file (nodes, signals, etc)
    strLine = ""            #a line in arrstrLines   
    arrNodes = []           #nodes list
    iIndex = 0              #int value used for getting the index of the message while reading the nodes attributes
    arrSignals = []         #signals list
    arrDiagSignals = []     #diagnostic signals list
    arrFrames = []          #unconditional frames list
    arrScheduleTables = []  #schedule tables list
    strFrameName = ""       #string fot getting the frame name in schedule tables
    
    
    def __init__(self, filename):
        '''
            Initializes the variables used and reads the file
            
            filename = the name of the file to be read
        '''
        self.arrstrLines = []        #list of lines in file
        self.strCategory = ""        #string that shows the current reading category from file (nodes, signals, etc)
        self.strLine = ""            #a line in arrstrLines       
        self.arrNodes = []           #nodes list
        self.iIndex = 0              #int value used for getting the index of the message while reading the nodes attributes
        self.arrSignals = []         #signals list
        self.arrDiagSignals = []     #diagnostic signals list
        self.arrFrames = []          #unconditional frames list
        self.arrScheduleTables = []  #schedule tables list
        self.strFrameName = ""       #string fot getting the frame name in scheule tables
        
        fo = open(filename ,  "r")
        self.arrstrLines = fo.readlines()     
        fo.close()
        
        self.GetNodes()
        self.GetScheduleTables()
    
    def GetNodes(self):
        '''
            Reads all the information about all the nodes from the *.ldf file
        '''
        self.arrNodes = []
        #get the frames
        self.GetFrames()
        
        #create a master node
        master = Nodes()
        master.configFrames = []
        master.productID = []
        master.type = "M" #Master
                    
        #foreach line in file
        for self.strLine in self.arrstrLines:
            #split the line in values
            if("//" in self.strLine):
                self.strLine = self.strLine[ : self.strLine.index("//")]
            self.strLine = re.split(' |;|:|,|\n|=|"', self.strLine)
            self.strLine = filter(None, self.strLine)
            
            #preapere for reading node names
            if("Nodes" in self.strLine):
                self.strCategory = "nodes"
            '''Read node name and node attributes'''
            
            #exit the slave nodes 
            if('}' in self.strLine and self.strCategory == "Snode"):
                self.strCategory = "nodes"
            
            if("Mnode" in self.strCategory):
                if(len(self.strLine) >= 5):
                    #get the master node name and set its type
                    master.name = self.strLine[1]
                    #get the timebase value
                    master.timebase = self.strLine[2]
                    #get the jitter value
                    master.jitter = self.strLine[4] 
                    
                    self.strCategory = "nodes"                   
                    self.arrNodes.append(master)
                else:
                    if(len(self.strLine) == 1 or len(self.strLine) == 3):
                        if(master.name == ""):
                            master.name = self.strLine[0]
                    if(len(self.strLine) == 2):
                        if(master.timebase == "-1 ms"):
                            master.timebase = self.strLine[0]
                        elif(master.jitter == "-1 ms"):
                            master.jitter = self.strLine[0]
                            self.strCategory = "nodes"                   
                            self.arrNodes.append(master)
                    if(len(self.strLine) == 3):
                        if(master.timebase == "-1 ms"):
                            master.timebase = self.strLine[1]
                        elif(master.jitter == "-1 ms"):
                            master.jitter = self.strLine[1]
                            self.strCategory = "nodes"                   
                            self.arrNodes.append(master)
                    if(len(self.strLine) == 4):
                        if(master.timebase == "-1 ms"):
                            master.timebase = self.strLine[0]
                        elif(master.jitter == "-1 ms"):
                            master.jitter = self.strLine[2]
                            self.strCategory = "nodes"                   
                            self.arrNodes.append(master)
                
            #read the slave node name    
            if("Snode" in self.strCategory):
                for i in range(0, len(self.strLine)):
                    if(self.strLine[i] != "Slaves"):
                        #create new node
                        node = Nodes()
                        node.productID = []
                        node.configFrames = []
                        #get the slave node name and set its type
                        node.name = self.strLine[i]
                        node.type = "S" #Slave
                        
                        self.arrNodes.append(node)
                        
            if("nodes" in self.strCategory):
                #read the master node name    
                if("Master" in self.strLine):
                    self.strCategory = "Mnode"
                if("Slaves" in self.strLine):
                    self.strCategory = "Snode"
                    
            #prepare for reading the node attributes
            if("Node_attributes" in self.strLine):
                self.strCategory = "nodeAttrib"
             
            if(self.strCategory == "nodeAttrib"):
                for i in range(len(self.arrNodes)):
                    if(self.arrNodes[i].name in self.strLine):
                        self.iIndex = i
                        self.strCategory = "specificNodeAtrib"
                        
            if(self.strCategory == "specificNodeAtrib"):         
                #get the lin_protocol value
                if("LIN_protocol" in self.strLine):
                    self.arrNodes[self.iIndex].linProtocol = self.strLine[1]
                #get the configured_NAD value
                if("configured_NAD" in self.strLine):
                    self.arrNodes[self.iIndex].configuredNAD = self.strLine[1]
                #get the initial_NAD value
                if("initial_NAD" in self.strLine):
                    self.arrNodes[self.iIndex].initialNAD = self.strLine[1]
                #get the response_error value
                if("response_error" in self.strLine):
                    self.arrNodes[self.iIndex].responseError = self.strLine[1]
                #get the P2_min value. +2 = the begining tab
                if("P2_min" in self.strLine):
                    self.arrNodes[self.iIndex].P2min = self.strLine[1]
                #get the ST_min value. +2 = the begining tab
                if("ST_min" in self.strLine):
                    self.arrNodes[self.iIndex].STmin = self.strLine[1]
                #get the product_id array
                if("product_id" in self.strLine):
                    for i in range(1, len(self.strLine)):
                        self.arrNodes[self.iIndex].productID.append(self.strLine[i])
                    
                if("configurable_frames" in self.strLine and '{' in self.strLine):
                    self.strCategory = 'nodeAtribFrames'
                                 
            #get the frames configurable for each node
            if(self.strCategory == 'nodeAtribFrames'):
                #skip the fisrt and last line
                if(not 'configurable_frames' in self.strLine and not "}" in self.strLine):
                    for frm in self.arrFrames:
                        if(frm.name == self.strLine[0]):                            
                            #add the frame to the corresponding node
                            self.arrNodes[self.iIndex].configFrames.append(frm)
                            #if the frame has a message ID specified or not
                            if(len(self.strLine) == 2):
                                self.arrNodes[self.iIndex].configFrames[len(self.arrNodes[self.iIndex].configFrames) - 1].messageID = self.strLine[1]
                            else:
                               self.arrNodes[self.iIndex].configFrames[len(self.arrNodes[self.iIndex].configFrames) - 1].messageID = "Frame Ind %d"%(len(self.arrNodes[self.iIndex].configFrames) - 1)

            #exit the function                                     
            if('}' in self.strLine and self.strCategory == "nodeAttrib"):
                return
            #exit the specified node attributes section to the generic node attributes
            if('}' in self.strLine and self.strCategory == "specificNodeAtrib"):
                self.strCategory = "nodeAttrib"
            #exit the configurable frames section to the specific node attriutes
            if('}' in self.strLine and self.strCategory == "nodeAtribFrames"):
                self.strCategory = "specificNodeAtrib"

    def GetSignals(self):
        '''
            Gets all the information about signals from file
        '''
        self.arrSignals = []
        #foreach line in file
        for self.strLine in self.arrstrLines:
            #remove comments and split the line in values
            if("//" in self.strLine):
                self.strLine = self.strLine[ : self.strLine.index("//")]
            self.strLine = re.split(' |;|:|,|\n|=|"', self.strLine)
            self.strLine = filter(None, self.strLine)  
               
            #prepare for reading the signals
            if("Signals" in self.strLine):
                self.strCategory = "signals"
             
            #end reading the signals
            if("}" in self.strLine and self.strCategory == "signals"):
                self.strCategory = ""  
                return
                 
            if(self.strCategory == "signals"):                
                #skip the first line
                if(not "Signals" in self.strLine and not '}' in self.strLine and not '{' in self.strLine):
                    if(len(self.strLine) > 3):
                        #create a new signal
                        signal = LINSignal()
                        signal.subscribers = []
                        #get the signal name
                        signal.name = self.strLine[0]
                        #get the signal length
                        signal.length = int(self.strLine[1])
                        #get the signal init value
                        try:
                            signal.initVal.append(int(self.strLine[2]))
                        except ValueError:
                            if(self.strLine[2] == "{"):
                                pass
                            elif(self.strLine[2].startswith("{")):
                                signal.initVal.append(self.strLine[2][1 : ])
                            try:
                                for i in range(3, self.strLine.index("}")):
                                    signal.initVal.append(int(self.strLine[i]))
                            except ValueError:
                                for i in range(3, len(self.strLine)):
                                    if(self.strLine[i].endswith("}")):
                                        signal.initVal.append(self.strLine[i][ : -1])
                                        break
                                    else:
                                        signal.initVal.append(self.strLine[i])
                            
                                        
                        #get the signal publisher value
                        signal.publisher = self.strLine[3]
                        
                        for i in range(4, len(self.strLine)):
                            #get subscriber value
                            signal.subscribers.append(self.strLine[i])
                        #add the signal to the ligals list
                        
                        self.arrSignals.append(signal)  
    
    def GetDiagnosticSignals(self): 
        '''
            Gets the information about the diagnostic signals from the LDF file
        '''
        self.arrDiagSignals = []
        #foreach line in file
        for self.strLine in self.arrstrLines:
            #remove comments and split the line in values
            if("//" in self.strLine):
                self.strLine = self.strLine[ : self.strLine.index("//")]
            self.strLine = re.split(' |;|:|,|\n|=|"', self.strLine)
            self.strLine = filter(None, self.strLine)
            #prepare for reading the disgnostic signals        
            if("Diagnostic_signals" in self.strLine):
                self.strCategory = "diagSignals"
            
            #end reading the diagnostic signals
            if("}" in self.strLine and self.strCategory == "diagSignals"):
                self.strCategory = "" 
                return
                
            if(self.strCategory == "diagSignals"):                
                #skip the first line
                if(not "Diagnostic_signals" in self.strLine and not "}" in self.strLine): 
                    #create a new signal
                    signal = LINDiagnosticSignal()
                    signal.subscribers = []
                    signal.publisher = []
                    #get the signal name
                    signal.name = self.strLine[0]
                    #get the signal length
                    signal.length = int(self.strLine[1])
                    #get the signal init value
                    try:
                        signal.initVal.append(int(self.strLine[2]))
                    except ValueError:
                        if(self.strLine[2] == "{"):
                            pass
                        elif(self.strLine[2].startswith("{")):
                            signal.initVal.append(self.strLine[2][1 : ])
                        try:
                            for i in range(3, self.strLine.index("}")):
                                signal.initVal.append(int(self.strLine[i]))
                        except ValueError:
                            for i in range(3, len(self.strLine)):
                                if(self.strLine[i].endswith("}")):
                                    signal.initVal.append(self.strLine[i][ : -1])
                                    break
                                else:
                                    signal.initVal.append(self.strLine[i])
                    
                    if("Master" in signal.name):
                        for node in self.arrNodes:
                            if(node.type == "M"):
                                signal.publisher.append(node.name)
                            if(node.type == "S"):
                                signal.subscribers.append(node.name)
                    if("Slave" in signal.name):
                        for node in self.arrNodes:
                            if(node.type == "S"):
                                signal.publisher.append(node.name)
                            if(node.type == "M"):
                                signal.subscribers.append(node.name)
                                
                    #add the signal to the DiagSignals list
                    self.arrDiagSignals.append(signal)
        
    def GetFrames(self):  
        '''
            Get all the info about the frames from the LDF file
        '''
        self.arrFrames = [] 
        #get signals from file
        self.GetSignals()
        
        #foreach line in file
        for self.strLine in self.arrstrLines:      
            #remove comments and split the line in values
            if("//" in self.strLine):
                self.strLine = self.strLine[ : self.strLine.index("//")]
            self.strLine = re.split(' |\t|:|;|,|\n|=|"', self.strLine)
            self.strLine = filter(None, self.strLine)
            
            #prepare for reading the unconditional frames        
            if("Frames" in self.strLine):
                self.strCategory = "uFrames"
            
            if(self.strCategory == "uFrames" and not "Frames" in self.strLine):    
                if(len(self.strLine) > 3):
                    self.strCategory = "specificUFrame"
                    #Create a new frame object
                    uFrame = Frame()
                    uFrame.subscribesrs = []
                    uFrame.signals = []
                    #get the frame name, frameID, publisher, size
                    uFrame.name = self.strLine[0]
                    uFrame.frameID = int(self.strLine[1])
                    uFrame.publisher = self.strLine[2]
                    uFrame.size = int(self.strLine[3])
                    
                    self.arrFrames.append(uFrame)
                    
            if(self.strCategory == "specificUFrame" and not '{' in self.strLine and not '}' in self.strLine):        #if we are in a frame, on a line with signals
                for i in range(len(self.arrSignals)):
                    if(self.strLine[0] == self.arrSignals[i].name):
                        self.arrFrames[len(self.arrFrames) - 1].subscribers = []
                        #create a copy of the signal and eliminate the value from the line
                        sgn=copy.copy(self.arrSignals[i])
                        #get the startbit value
                        sgn.startbit = int(self.strLine[1]) 
                        #add the signal to the frame
                        self.arrFrames[len(self.arrFrames) - 1].signals.append(sgn)

                        for subscriber in sgn.subscribers:
                            ok = False
                            for frameSubscriber in self.arrFrames[len(self.arrFrames) - 1].subscribers:
                                if(subscriber == frameSubscriber):
                                    if(self.arrFrames[len(self.arrFrames) - 1].name=="ST_FAS_LIN"):
                                        ok = True
                            if(ok == False):
                                self.arrFrames[len(self.arrFrames) - 1].subscribers.append(subscriber)
             
            #exit function
            if('}' in self.strLine and self.strCategory == "uFrames"):
                self.strCategory = ""
                return
            #exit a specific frame section to the generic frames section
            if('}' in self.strLine and self.strCategory == "specificUFrame"):
                self.strCategory = "uFrames"
        
    def GetScheduleTables(self):  
        '''
            Gets the information about the schedule tables from the file
        '''  
        self.arrScheduleTables = []
        #get frames
        self.GetFrames()
        #foreach line in file
        for self.strLine in self.arrstrLines:
            #remove comments and split the line in values
            if("//" in self.strLine):
                self.strLine = self.strLine[ : self.strLine.index("//")]
            self.strLine = re.split(' |;|:|,|\n|=|"', self.strLine)
            self.strLine = filter(None, self.strLine)
            
            if("Schedule_tables" in self.strLine):
                self.strCategory = "schTables"
                
            if(self.strCategory == "schTables" and len(self.strLine) > 0 and self.strLine[0] != "{" and self.strLine[0] != "}"):
                if(not "Schedule_tables" in self.strLine):
                    #for skipping the Diagnostic Frames
                    if(not any("diag" in str.lower() for str in self.strLine) and len(self.strLine) >= 1):
                        #initialize a new table
                        schTable = ScheduleTable()
                        schTable.frames = []
                        schTable.delay = []
                        #extract the table name from file
                        schTable.name = self.strLine[0]
                        #add the table to the tables list
                        self.arrScheduleTables.append(schTable)
                        self.strCategory = "specificSchTable"
                    else:
                        self.strCategory = "specificInvalidSchTable"
                        
            #if the current line is in a valid table and has useful data (frame/delay)
            if(self.strCategory == "specificSchTable" and not '{' in self.strLine and not '}' in self.strLine): 
                #search for a frame with the name from file. if the frame is found, add it to the table frames
                for frame in self.arrFrames:
                    if(frame.name == self.strLine[0]):                        
                        self.arrScheduleTables[len(self.arrScheduleTables) - 1].frames.append(frame)
                        self.strFrameName = frame.name
                        self.arrScheduleTables[len(self.arrScheduleTables) - 1].delay.append(self.strLine[2])
                    
            #if the schedule tables section is ending, in file
            if('}' in self.strLine and self.strCategory == "schTables"):
                self.strCategory = ""
                return
                
            #if the current table section is ending in file
            if('}' in self.strLine and (self.strCategory == "specificSchTable" or self.strCategory == "specificInvalidSchTable")):
                self.strCategory = "schTables"
                
    def GetParams(self):
        '''
            Returns the information about the LIN parameters from the file
        '''  
        params = []
        speed = 0
        protocol = 0.0
        for self.strLine in self.arrstrLines:
            #remove comments and split the line in values
            if("//" in self.strLine):
                self.strLine = self.strLine[ : self.strLine.index("//")]
            self.strLine = re.split(' |;|:|,|\n|=|"', self.strLine)
            self.strLine = filter(None, self.strLine)
            
            if("LIN_speed" in self.strLine):
                try:
                    speed = float(self.strLine[1])
                    if(self.strLine[2].lower() == "kbps"):
                        speed = speed * 1000;
                    elif (self.strLine[2].lower() == "mbps"):
                        speed = speed * 1000000;
                except:
                    pass
            if("LIN_protocol_version" in self.strLine):
                protocol = self.strLine[1]
                
        params.append(int(speed))
        params.append(protocol)
        
        return params[0]  #params[0] = the LIN speed; params[1] = the protocol version
            