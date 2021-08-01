import math
import subprocess

'''
The following parameters can be programmed and monitored via the serial communication port:

USAGE EXEMPLE

# sms = SMSInstance()
# sms.Reset(78)
# time.sleep(0.5) 
# sms.Inc(78)
# sms.Inc(78)
# sms.Dec(78)
# # sms.SetBlock(78, 1000, "HALF")
# # sms.SetPinch(78, 1500, "HALF")
#  
# x,y = sms.GetHallState(78)
# print x,y
# 
# print sms.GetPos(78)  

'''

class SMS:
        
    def SetPos(self,serNum,newPos):
        '''Sets the position of the device number serNum to newPos'''
        subprocess.check_output("sms open "+str(serNum)+" setpos "+str(newPos)+" close",stderr=subprocess.STDOUT,shell=False)
    
    def Reset(self,serNum):
        '''Resets the device number serNum to default values'''
        subprocess.check_output("sms open "+str(serNum)+" reset close",stderr=subprocess.STDOUT,shell=False)
    
    def Inc(self,serNum):
        '''Increment the actual motor position by one hall sensor edge'''
        subprocess.check_output("sms open "+str(serNum)+" inc close",stderr=subprocess.STDOUT,shell=False)
        
    def Dec(self,serNum):
        '''Decrement the actual motor position by one hall sensor edge'''
        subprocess.check_output("sms open "+str(serNum)+" dec close",stderr=subprocess.STDOUT,shell=False)
        
    def GetPos(self,serNum):
        '''Returns the position of the device number serNum'''
        p=subprocess.check_output("sms open "+str(serNum)+" RDPOS close",stderr=subprocess.STDOUT,shell=False)
        p=p[:-2]
        x,y=0,0
        for num in range(0,len(p)):
            if p[len(p)-num:len(p)-num+1].isdigit() == True:
                x=int(p[len(p)-num:len(p)-num+1])*math.pow(10,y)+x
                y=y+1
            else:
                if num>0:
                    break
        return int(x)
     
    def GetHallState(self,serNum):
        '''Returns the status of hall sensors of the device number serNum'''
        p=subprocess.check_output("sms open "+str(serNum)+" RDHALL close",stderr=subprocess.STDOUT,shell=False)
        a=p[len(p)-7:len(p)-6]
        b=p[len(p)-3:len(p)-2]
        a = int(a)
        b = int(b)
        return a,b
    
    def SetHallErr(self,serNum,string):
        '''Sets the status of hall sensors of the device number serNum
        "A 0" - will hold the hall sensor A at low level
        "A 1" - will hold the hall sensor A at high level
        "B 0" - will hold the hall sensor B at low level
        "B 1" - will hold the hall sensor B at high level
        "A=B" is only usefull for voltage type hall sensors. It will simulate a shortcut between the two hall
             sensor signal lines. If one hall sensor is low, both hall sensor signals will be held low.'''
        
        if(string == "noErr"):
            '''the hall sensor error simulation will be deactivated'''
            subprocess.check_output("sms open "+str(serNum)+" HALLERR close",stderr=subprocess.STDOUT,shell=False)
        else:        
            subprocess.check_output("sms open "+str(serNum)+" HALLERR"+string+"close",stderr=subprocess.STDOUT,shell=False)

    def SetBlock(self,serNum,blockPos,blockType):
        '''Blocking occours if the specified position is reached.
        Block mode:
        UP: Block only upwards moving, downward moving will be free.
        DOWN: Block only downwards moving, upward moving will be free.
        HALF: Block only against the initial moving direction, the other moving direction will be free.
        FULL: Block moving in any direction.'''
        subprocess.check_output("sms open "+str(serNum)+' setact pos='+str(blockPos)+" "+blockType+" block",stderr=subprocess.STDOUT,shell=False)
    
    def SetPinch(self,serNum,pinchPos,pinchType):    
        '''Pinching will be triggered if the specified position is reached.
        Pinch mode:
        UP: Pinch only if moving upwards.
        DOWN: Pinch only if moving downwards.
        HALF: Pinch against the actual moving direction.'''
            
        subprocess.check_output("sms open "+str(serNum)+' setact pos='+str(pinchPos)+" "+pinchType+" pinch 10",stderr=subprocess.STDOUT,shell=False)
        

# sms = SMSInstance()
# sms.Reset(78)
# time.sleep(0.5) 
# sms.Inc(78)
# sms.Inc(78)
# sms.Dec(78)
# # sms.SetBlock(78, 1000, "HALF")
# # sms.SetPinch(78, 1500, "HALF")
#  
# x,y = sms.GetHallState(78)
# print x,y
# 
# print sms.GetPos(78)    
