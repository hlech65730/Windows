
# OS : Win10
# Phyton 3 - self created simple functions 

# function create numeric array

Demoliste = []

def create_num_array(liste,xp=0):

	while xp != 0:
		liste += [0]
		xp = xp -1

create_num_array(Demoliste,10)

print(Demoliste)

# function create character array

charlist = ["0"]

def create_char_array(liste,cp=0):
	newchar = 'x'
	while cp != 0:
		liste.append(newchar)
		cp = cp -1

create_char_array(charlist,10)

print(charlist)

# function to open a textfile search and replace some text

testfile 		= 'Testfile.txt'
findtext		 = 'Ds'
replacetext = 'Das'

def replace_txt_in_file(textfile,suchtext,ersatztext):

	# Read in the file
	with open(textfile, 'r') as txtfile:
		filedata = txtfile.read()
		print (filedata.index(suchtext))
	# Replace the target string
	filedata = filedata.replace(suchtext, ersatztext)
	# Write the file out again
	with open(textfile, 'w') as file:
		file.write(filedata)
	txtfile.close()

replace_txt_in_file(testfile,findtext,replacetext)







