
import RPi.GPIO as GPIO
import time 

#hier wird zuerst die GPIO zurückgesetz
GPIO.cleanup

#setmode ermoeglicht die Einstellung welche GPIO- Bezeichnung verwendet werden soll,
#hier werden die Pinnummern der Stiftleiste benutzt
GPIO.setmode(GPIO.BOARD) 

#setup setzt die Funktion des Bezeichneten GPIO, hier 11 als Ausgang
GPIO.setup(11,GPIO.OUT) 


for i in range (0,1000):

	#outputsetzt den Pegel des GPIO,hier GPIO11 auf high 
	GPIO.output(11, GPIO.HIGH)
	
	print ("GPIO HIGH")
	
	time.sleep(10)

	GPIO.output(11, GPIO.LOW)
	
	print( "GPIO LOW")


GPIO.cleanup

print( "finish GPIO test")
 



