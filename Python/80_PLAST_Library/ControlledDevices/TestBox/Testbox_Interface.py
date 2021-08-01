import ConfigParser
import time
import serial

serTx=serial.Serial()

TYPE_STANDARD_SWITCH = 0 
TYPE_HALL_SWITCH     = 1
TYPE_RESISTOR_CODED  = 2
TYPE_POTENTIOMETER   = 3

# Function code values. REMARK: FC+CFC is always 0xFF. ->More details can be found in BDC_Testbox_Telegramme.pdf
CMD_SET_SWITCHES     = 0x31
CMD_READ_SWITCHES    = 0x33
CMD_SET_SIMULATION   = 0x32
CMD_READ_DUT_OUTPUT  = 0x11
CMD_READ_MTB_VERSION = 0x01
CMD_MTB_RESET        = 0x02
CMD_READ_DIAGLEVEL   = 0x03
CMD_SET_DIAGLEVEL    = 0x04
CMD_READ_SETUP       = 0x08
CMD_SET_SETUP        = 0x09

DEBUG    = 1 #Debugging option(1=active, 0=inactive)
CONFIG   = 3
SEND     = None
ACTIVE   = 1               
INACTIVE = 0             

SendBufRS232=[]         
Front_SW_States=[]      
Front_Hall_States=[]    
Front_RC_States=[]  
Front_PT_States=[]

_nameList_SW  = ["ZAT1_SIG_D25","SwUnused0","DWA_HECKSCH_D12","SwUnused1","SwUnused2","BREMS_LISTR_KL54_C12","SwUnused3","AN_VORHALT2_CO8",
                   "ZAT2_SIG_D10","SwUnused4","SCH_TANKKLAP_D27","SwUnused5","SwUnused6","SwUnused7","SwUnused8","SwUnused9",
                   "ZAT3_SIG_D26","SwUnused10","ZV_ZU_HECK_D16","SwUnused11","SwUnused12","SwUnused13","SwUnused14","AN_VORHALT4_C11",
                   "ZAT4_SIG_D11","SwUnused15","SwUnused16","SwUnused17","SwUnused18","SwUnused19","SwUnused20","AN_VORHALT1_C24",
                   "SwUnused21","SwUnused22","SwUnused23","ZZH_AUS_IN_D32","SwUnused24","SwUnused25","AV_VORHALT5_C27","SwUnused26",
                   "ZAT_ALL","HW_C22","SwUnused27","SwUnused28","SwUnused29","SwUnused30","AN_VORHALT3_C28","AN_VORHALT6_C26"]

_nameList_PT    = ["KAPPASENSOR_HRE_E12","PtUnused0","PtUnused1","KAPPASENSOR_HLI_E13","PtUnused2","PtUnused3","KAPPASENSOR_VRE_E14","PtUnused4",
                     "PtUnused5","KAPPASENSOR_VLI_E15","PtUnused6","PtUnused7","PtUnused8","PtUnused9","PtUnused10","PtUnused11",
                     "PtUnused12","PtUnused13","PtUnused14","PtUnused15","PtUnused16","PtUnused17","PtUnused18","PtUnused19"]

_nameList_HL     = ["AN_VORHALT7_C23","AN_VORHALT7_C23_INT","HECKKLAPPE_HR_D28","HECKKLAPPE_HR_D28_INT","HwUnused0","HwUnused0_INT","POS_HALL_2D_C09","POS_HALL_2D_C09_INT",
                             "STELLING_P_D14","STELLING_P_D14_INT","HECKKLAPPE_1_D29","HECKKLAPPE_1_D29_INT","HwUnused1","HwUnused1_INT","POS_HALL_2D_PLUS_C25","POS_HALL_2D_PLUS_C25_INT",
                             "HwUnused2","HwUnused2_INT","HECKKLAPPE_1_D29","HECKKLAPPE_1_D29_INT","HwUnused3","HwUnused3_INT","HwUnused4","HwUnused4_INT",
                             "HwUnused5","HwUnused5_INT","HECKKLAPPE_2_D13","HECKKLAPPE_2_D13_INT","HwUnused6","HwUnused6_INT","HwUnused7","HwUnused7_INT",
                             "ZZH_EIN_IN_D31","ZZH_EIN_IN_D31_INT","HECKKLAPPE_SFT_D30","HECKKLAPPE_SFT_D30_INT","HwUnused8","HwUnused8_INT","HwUnused9","HwUnused9_INT",
                             "HECKROLLO_HALL_E04","HECKROLLO_HALL_E04_INT","HwUnused10","HwUnused10_INT","HwUnused11","HwUnused11_INT","HwUnused12","HwUnused12_INT"]

_nameList_RC    = ["RcUnused00_INT","RcUnused01_INT","RcUnused02_INT","RcUnused03_INT","RcUnused04_INT","RcUnused05_INT",
                    "RcUnused00","RcUnused01","RcUnused02","RcUnused03","RcUnused04","RcUnused05",
                    "RcUnused06","RcUnused07","RcUnused08","RcUnused09","RcUnused10","RcUnused11",
                    "RcUnused12","RcUnused13","RcUnused14","RcUnused15","RcUnused16","RcUnused17",
                    "RcUnused18","RcUnused19","RcUnused20","RcUnused21","RcUnused22","RcUnused23",
                    "RcUnused06_INT","RcUnused07_INT","RcUnused08_INT","RcUnused09_INT","RcUnused10_INT","RcUnused11_INT",
                    "RcUnused24","RcUnused25","RcUnused26","RcUnused27","RcUnused28","RcUnused29",
                    "RcUnused30","RcUnused31","RcUnused32","RcUnused33","RcUnused34","RcUnused35",
                    "RcUnused36","RcUnused37","RcUnused38","RcUnused39","RcUnused40","RcUnused41",
                    "RcUnused42","RcUnused43","RcUnused44","RcUnused45","RcUnused46","RcUnused47"]


def MTB_Init_Port():
        #Open RS232 port function. Port number (port), baudrate, number of data bits , number of stop bits and parity cand be foun in device manager.       
        global cfg
        global serTx
        cfg=ConfigParser.RawConfigParser()
        cfg.read("D:\PLAST\SW_AUT_ITS\Software\Library\Workspace\PLAST_wa\Test_MaBa\config_testbox.cfg")
        #serTx=serial.Serial()
        
        serTx.port = "COM"+cfg.get("TESTBOX","com")
        serTx.baudrate = int(cfg.get("TESTBOX","baud"))
        serTx.bytesize = int(cfg.get("TESTBOX","databit"))
        serTx.parity = cfg.get("TESTBOX","parity")[0]
        serTx.stopbits = int(cfg.get("TESTBOX","stopbit"))
        if cfg.get("TESTBOX","handshake")=="Rts/Cts":
            serTx.rtscts = 1
        if cfg.get("TESTBOX","handshake")=="Xon/Xoff":
            serTx.xonxoff = 1
        serTx.open()
        if DEBUG==1:
            print "Port "+serTx.port+" configuration succesful!"
            
def ComputeChecksum(data,length):
    CS=data[0]
    for i in range(1,length):
        CS=CS^data[i]
    return CS
    CS=0

def SetBit(byte,position):
    mask =1
    if position<0 or position>7: 
        print "SetBit: bit postion invalid !"
    mask=mask<<position
    byte=int(byte)|mask
    print "Set byte sent."
    return byte
       
def ResetBit(byte,position):
    mask =1
    if position<0 or position>7: 
        print "SetBit: bit postion invalid !"
    mask=mask<<position
    mask=~mask
    (byte)=(byte) & mask
    print "Reset byte sent."
    return byte

class _Button:
    
    def __init__(self, byte = None, bit = None, switchType = None):  
        self.byte=byte
        self.bit=bit                                                          
        self.switchType=switchType

class TBox:
    buttons_SW = [[None for _ in range(8)] for _ in range(6)] 
    buttons_HL = [[None for _ in range(8)] for _ in range(6)]
    buttons_RC = [[None for _ in range(6)] for _ in range(10)] 
    buttons_PT = [[None for _ in range(16)] for _ in range(3)] 
 
    def __init__(self): 
        for i in range(6):
            for j in range(8):
                self.buttons_SW[i][j] = _Button(i,j,TYPE_STANDARD_SWITCH)
        for i in range(6):
            for j in range(8):
                self.buttons_HL[i][j] = _Button(i,j,TYPE_HALL_SWITCH)
        for i in range(10):
            for j in range(6):
                self.buttons_RC[i][j] = _Button(i,j,TYPE_RESISTOR_CODED)
        for i in range(3):
            for j in range(16):
                self.buttons_PT[i][j] = _Button(i,j,TYPE_POTENTIOMETER)
        self.Code_Reset()
    
    def Code_Reset(self):
        del Front_SW_States[0:5]
        del Front_Hall_States[0:5]
        del Front_RC_States[0:9]
        del Front_PT_States[0:2]
        Front_SW_States.append(0)  
        Front_SW_States.append(0)
        Front_SW_States.append(0)
        Front_SW_States.append(0)
        Front_SW_States.append(0)
        Front_SW_States.append(0)  
        Front_Hall_States.append(0)
        Front_Hall_States.append(0)
        Front_Hall_States.append(0)
        Front_Hall_States.append(0)  
        Front_Hall_States.append(0)
        Front_Hall_States.append(0)
        Front_RC_States.append(0)
        Front_RC_States.append(0)
        Front_RC_States.append(0)
        Front_RC_States.append(0)
        Front_RC_States.append(0)
        Front_RC_States.append(0)
        Front_RC_States.append(0)
        Front_RC_States.append(0)
        Front_RC_States.append(0)
        Front_RC_States.append(0)
        Front_PT_States.append(0)
        Front_PT_States.append(0)
        Front_PT_States.append(0)
        
        if DEBUG == 1:
            pass
#             print "Code reset, all bits are set to 0."    
                
    def SetSwitch(self,name,state,switchType):
        found = 0      
        i=0
        j=0
        if switchType == TYPE_STANDARD_SWITCH: 
            for i in range(48):
                if name == _nameList_SW[i]:
                    print "Name found:\n" + name
                    found = 1
                    break
            if found==0:
                print "ERROR. THE GIVEN BUTTON NAME IS INVALID"
                return 1
            if i!=0:
                k=i
                if k<8:
                    i=0
                    j=k%8
                elif k>7 and k<16:
                    i=1
                    j=k%16-8
                elif k>15 and k<24:
                    i=2
                    j=k%24-16
                elif k>23 and k<32:
                    i=3
                    j=k%32-24
                elif k>31 and k<40:
                    i=4
                    j=k%40-32
                elif k>39:
                    i=5
                    j=k%48-40
                else:
                    print "Error, bit position invalid!"
            else:
                i=0
                j=0
        elif switchType == TYPE_HALL_SWITCH:
            for i in range(48):
                if name == _nameList_HL[i]:
                    print "Name found:\n" + name
                    found = 1
                    break
            if found==0:
                print "ERROR. THE GIVEN BUTTON NAME IS INVALID"
                return 1
            if i!=0:
                k=i
                if k<8:
                    i=0
                    j=k%8
                elif k>7 and k<16:
                    i=1
                    j=k%16-8
                elif k>15 and k<24:
                    i=2
                    j=k%24-16
                elif k>23 and k<32:
                    i=3
                    j=k%32-24
                elif k>31 and k<40:
                    i=4
                    j=k%40-32
                elif k>39:
                    i=5
                    j=k%48-40
                else:
                    print "Error, bit position invalid!"
        elif switchType == TYPE_RESISTOR_CODED:
            for i in range(60):
                if name == _nameList_RC[i]:
                    print "Name found:\n" + name
                    found = 1
                    break
            if found==0:
                print "ERROR. THE GIVEN BUTTON NAME IS INVALID"
                return 1
            if i!=0:
                k=i
                if k<6:
                    i=0
                    j=k%6
                elif k>5 and k<12:
                    i=1
                    j=k%12-6
                elif k>11 and k<18:
                    i=2
                    j=k%18-12
                elif k>17 and k<24:
                    i=3
                    j=k%24-18
                elif k>23 and k<30:
                    i=4
                    j=k%30-24
                elif k>29 and k<36:
                    i=5
                    j=k%36-30
                elif k>35 and k<42:
                    i=6
                    j=k%42-36
                elif k>41 and k<48:
                    i=7
                    j=k%48-42
                elif k>47 and k<54:
                    i=8
                    j=k%54-48
                elif k>52 and k<60:
                    i=9
                    j=k%60-54
                else:
                    print "Error, bit position invalid!"
            else:
                i=0
                j=0
        elif switchType == TYPE_POTENTIOMETER:
            for i in range(48):
                    if name == _nameList_PT[i]:
                        print "Name found:\n" + name
                        found = 1
                        break
            if found==0:
                print "ERROR. THE GIVEN BUTTON NAME IS INVALID??"
                return 1
            if i!=0:
                k=i
                if k<16:
                    i=0
                    j=k%16
                elif k>15 and k<32:
                    i=1
                    j=k%32-16
                elif k>31 and k<48:
                    i=2
                    j=k%48-32
                else:
                    print "Error, bit position invalid!"
            else:
                i=0
                j=0
        else:
            print "ERROR. THE GIVEN BUTTON NAME IS INVALID.CHECK IF THE CONFIG FILE IS RIGHT."        
        found=0
        if switchType == TYPE_STANDARD_SWITCH:
            if state==ACTIVE:
                Front_SW_States[i]=SetBit(Front_SW_States[self.buttons_SW[i][j].byte], self.buttons_SW[i][j].bit)
            else:
                Front_SW_States[i]=ResetBit(Front_SW_States[self.buttons_SW[i][j].byte], self.buttons_SW[i][j].bit)
            self.MTB_Set_Front_SW_States(SEND)
                
        elif switchType == TYPE_HALL_SWITCH:
            if state==ACTIVE:
                Front_Hall_States[i]=SetBit(Front_Hall_States[self.buttons_HL[i][j].byte], self.buttons_HL[i][j].bit)
            else:
                Front_Hall_States[i]=ResetBit(Front_Hall_States[self.buttons_HL[i][j].byte], self.buttons_HL[i][j].bit)
            self.MTB_Set_Front_Hall_States(SEND)
                
        elif switchType == TYPE_RESISTOR_CODED:
            if state==ACTIVE:
                Front_RC_States[i]=SetBit(Front_RC_States[self.buttons_RC[i][j].byte], self.buttons_RC[i][j].bit)
            else:
                Front_RC_States[i]=ResetBit(Front_RC_States[self.buttons_RC[i][j].byte], self.buttons_RC[i][j].bit)
            self.MTB_Set_Front_RC_States(SEND)
                
        elif switchType == TYPE_POTENTIOMETER:
            if state==ACTIVE:
                Front_PT_States[i]=SetBit(Front_PT_States[self.buttons_PT[i][j].byte], (self.buttons_PT[i][j].bit)/2)
            else:
                Front_PT_States[i]=ResetBit(Front_PT_States[self.buttons_PT[i][j].byte], (self.buttons_PT[i][j].bit)/2)
            self.MTB_Set_Front_PT_States(SEND)
        i=0
        return 0
 
    def Check_MTB_Answer (self,receivedbuffer,number):
        if number>0:
            if len(receivedbuffer)>1:
                if SendBufRS232[1]+receivedbuffer[1]!=0xFF:
                    print "Invalid complementary function code received"
                    return "ERROR"
            if len(receivedbuffer)>2:
                if SendBufRS232[1] == CMD_MTB_RESET or SendBufRS232[1]== CMD_SET_DIAGLEVEL:
                    if receivedbuffer[2]!=0xAA:
                        print "Negative response received from MTB"
                        return "ERROR"
        return "NO_ERROR"                  
    
    def SerialRecieved(self,number):
        time.sleep(0.6)
        bufer=[]
        number=serTx.readinto(bufer)
        if DEBUG==1:
            print "Data Recieved:"
            print bufer
        if len(bufer)>0:
            if self.Check_MTB_Answer(bufer, number) == "ERROR":
                print "ERROR: invalid answer from MTB"
        return bufer
    
    def SendData(self,bufer):
        global serTx
        serTx.write(bufer)
        if DEBUG==1:
            print "Data Sent(SendData function):"
            print bufer  #serTx.close()       
        
    def MTB_Set_Remote_Control(self):

        bufer = "\x03\x04\xE1\xE6"
        self.SendData(bufer)
        if DEBUG == 1:
            print "MTB_Set_Remote_Control is now on"
            
    def MTB_Set_Manual_Control(self):
        
        bufer = "\x03\x04\x00\x07"     
        serTx.write(bufer)
        print bufer
        serTx.close()
        if DEBUG==1:
            print "MTB_Set_Manual_Control is now on" 
            
    def MTB_Reset(self):
        del SendBufRS232[0:len(SendBufRS232)]
        SendBufRS232.append(3)              
        SendBufRS232.append(CMD_MTB_RESET)  
        SendBufRS232.append(0x00)           
        SendBufRS232.append(0x01)        
        self.SendData(SendBufRS232)
        if DEBUG==1:
            print "MTB_Reset called, remote control reseted."
  
    def MTB_Set_Multiple(self, switchType):
        if DEBUG==1:
            print "MTB_Set_Multiple"
        if type == SEND:
            del SendBufRS232[0:len(SendBufRS232)]
            SendBufRS232.append( 23) 
            SendBufRS232.append( CMD_SET_SWITCHES)    
            SendBufRS232.append( 0x80)                   
            SendBufRS232.append( Front_SW_States[0])
            SendBufRS232.append( Front_SW_States[1])
            SendBufRS232.append( Front_SW_States[2])
            SendBufRS232.append( Front_SW_States[3])
            SendBufRS232.append( Front_SW_States[4])
            SendBufRS232.append( Front_SW_States[5])   
            SendBufRS232.append( Front_Hall_States[0])
            SendBufRS232.append( Front_Hall_States[1])
            SendBufRS232.append( Front_Hall_States[2])
            SendBufRS232.append( Front_Hall_States[3])
            SendBufRS232.append( Front_Hall_States[4])
            SendBufRS232.append( Front_Hall_States[5])
            SendBufRS232.append( Front_RC_States[0])
            SendBufRS232.append( Front_RC_States[1])
            SendBufRS232.append( Front_RC_States[2])
            SendBufRS232.append( Front_RC_States[3])
            SendBufRS232.append( Front_RC_States[4])
            SendBufRS232.append( Front_RC_States[5])
            SendBufRS232.append( Front_RC_States[6])
            SendBufRS232.append( Front_RC_States[7]) 
            SendBufRS232.append(ComputeChecksum(SendBufRS232,23))    
            self.SendData(SendBufRS232)

    def MTB_Set_Front_SW_States(self,switchType): #This function will set the front switches states.
        del SendBufRS232[0:len(SendBufRS232)]
        SendBufRS232.append(9)                   #Command length.
        SendBufRS232.append(CMD_SET_SWITCHES)     #Function code.
        SendBufRS232.append(0x81)                 #Option.
        SendBufRS232.append(Front_SW_States[0])
        SendBufRS232.append(Front_SW_States[1])
        SendBufRS232.append(Front_SW_States[2])
        SendBufRS232.append(Front_SW_States[3])
        SendBufRS232.append(Front_SW_States[4])
        SendBufRS232.append(Front_SW_States[5])        
        SendBufRS232.append(ComputeChecksum(SendBufRS232,9)) #Checksum calculation       
        if switchType == SEND:
            self.SendData(SendBufRS232)
        if DEBUG==1:
            print "MTB_Set_Front_SW_States called, bits sent."
    
    def MTB_Set_Front_Hall_States(self, switchType):#This function will set the Hall switches states.
        del SendBufRS232[0:len(SendBufRS232)]
        SendBufRS232.append( 9)                    #Command length.
        SendBufRS232.append( CMD_SET_SWITCHES)     #Function code.
        SendBufRS232.append( 0x82)                 #Option.
        SendBufRS232.append( Front_Hall_States[0])
        SendBufRS232.append( Front_Hall_States[1])
        SendBufRS232.append( Front_Hall_States[2])
        SendBufRS232.append( Front_Hall_States[3])
        SendBufRS232.append( Front_Hall_States[4])
        SendBufRS232.append( Front_Hall_States[5])
        SendBufRS232.append( ComputeChecksum(SendBufRS232,9)) #Checksum calculation
        if switchType == SEND:
            self.SendData(SendBufRS232)
        if DEBUG==1:
            print "MTB_Set_Front_Hall_States called, bits sent."

    def MTB_Set_Front_RC_States(self, switchType):#This function will set the Resistor-Coded switches states.
        del SendBufRS232[0:len(SendBufRS232)]
        SendBufRS232.append( 0xD)                    #Command length.
        SendBufRS232.append( CMD_SET_SWITCHES)      #Function code.
        SendBufRS232.append( 0x83)                  #Option.
        SendBufRS232.append( Front_RC_States[0])
        SendBufRS232.append( Front_RC_States[1])
        SendBufRS232.append( Front_RC_States[2])
        SendBufRS232.append( Front_RC_States[3])
        SendBufRS232.append( Front_RC_States[4])
        SendBufRS232.append( Front_RC_States[5])
        SendBufRS232.append( Front_RC_States[6])
        SendBufRS232.append( Front_RC_States[7])
        SendBufRS232.append( Front_RC_States[8])
        SendBufRS232.append( Front_RC_States[9])
        SendBufRS232.append( ComputeChecksum(SendBufRS232,0xD)) #Checksum calculation
        if switchType == SEND:
            self.SendData(SendBufRS232)
        if DEBUG==1:
            print "MTB_Set_Front_RC_States called, bits sent."
            
    def MTB_Set_Front_PT_States(self, switchType):#This function will set the Front resistor standar switches states.
        del SendBufRS232[0:len(SendBufRS232)]
        SendBufRS232.append( 6)                    #Command length.
        SendBufRS232.append( CMD_SET_SWITCHES)      #Function code.
        SendBufRS232.append( 0x84)                  #Option.
        SendBufRS232.append( Front_PT_States[0])
        SendBufRS232.append( Front_PT_States[1])
        SendBufRS232.append( Front_PT_States[2])
        SendBufRS232.append( ComputeChecksum(SendBufRS232,6)) #Checksum calculation        
        if switchType == SEND:
            self.SendData(SendBufRS232)
        if DEBUG==1:
            print "MTB_Set_Front_PT_States called, bits sent."

Testbox = TBox()

def StartTestbox():
    MTB_Init_Port()
    Testbox.MTB_Set_Remote_Control()
    
def StopTestbox():
    Testbox.MTB_Set_Manual_Control()