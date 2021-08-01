
#Zahleneingabeprogramm für das iPhone

print("Zahleneingabeprogramm")

# Array Initialisierung 

zahlen = [11,12,13,14,15,16,17,18,19,20]

# Array mit Werten füllen

for i in range (0,9):
	zahlen[i] = input ("Eingabe einer Zahl \n")
	print ("Die eingegebene Zahl ist")
	print (zahlen[i])
	
# Ausgabe der 
# eingegebenen Zahlen

for a in range (0,9):
	print ("Zahl",(a),"ist :\n")
	print (zahlen[a])
