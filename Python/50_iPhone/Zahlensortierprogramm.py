
# Zahlensortierprogramm fuer das iPhone
 
print("Zahlensortierprogramm")

elemente = 10
zahlen = [11,12,13,14,15,16,17,18,19,20]

for i in range(0,9):
	print (i)
	zahlen[i]= input ("Eingabe einer Zahl : \n")
	print ("Die eing. Zahl war")
	print (zahlen[i])
print (zahlen)

def bubblesort(list_):
    """
    Idea: The maximum value floats at the end of the list in every outer
          iteration.
    """
    n = len(list_)
    something_changed = True
    for i in range(0, n):
        something_changed = False
        for j in range(0, n-i-1):
            if list_[j] > list_[j+1]:
                # Swap
                list_[j], list_[j+1] = list_[j+1], list_[j]
                something_changed = True
        if not something_changed:
            break

    return list_
    
    
bubblesort(zahlen)
print (zahlen )
