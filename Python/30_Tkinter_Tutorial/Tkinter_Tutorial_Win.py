# OS : Win 10
# C:\LegacyApp\Python36\python
# Erstes Fenster des Tkinter
# aus https://www.python-kurs.eu/tkinter_labels.php

try:
	from Tkinter import * # Python 2
except :
	from tkinter import * # Python 3



# definition of function upper radio button pressed which creates a picture in the window. The picture is in file  Rechteck_gelb_mit_Punkt_blau.gif
# see definiton of blue_img on the bottom of this script 
def upper_radio_button_pressed():
  canvas.create_image(20,20, anchor=NW, image=blue_img)
 
 # definition of function upper radio button pressed which creates a picture in the window. The picture is in file  Rechteck_gelb_mit_Punkt_rot.gif
# see definiton of red_img on the bottom of this script  
def lower_radio_button_pressed():
  canvas.create_image(20,20, anchor=NW, image=red_img)


# definition of class App which is handling the Quit  and the hello Button
class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.pack(side=LEFT)
    
    self.slogan = Button(frame,
                         text="Hello",
                         command=self.write_slogan)
    self.slogan.pack(side=LEFT)
    
  def write_slogan(self): # definition of function write slogan. The text is written in the command line box only if the button Hello is pressed.
    print ("Tkinter is easy to use!")

# Tkinter window definition
root = Tk() 
root.title("First python Tkinter window") 

# width x height + x_offset + y_offset:
root.geometry("500x600+30+30") 

# define red label inside the window with text  "red Label"
w = Label(root, text="Red Label", bg="red", fg="white")

# automatic managing of geometrie ( pack manager )of label w  inside of the window
# means x coordinate is done automatically and Y coordinate is given ( for x use padx =...) 
w.pack(fill=X,pady=10)

# integer variable definition 
v = IntVar()

entry1 = Entry(root)
entry2 = Entry(root)


# definition of Label "Choose a programming language"
Label(root, 
      text="""Choose a 
programming language:""",
      justify = LEFT,
      padx = 20).pack()

      
 # definition of pushable radiobuttons with text  Phyton or Perl
Radiobutton(root, 
            text="Python",
            padx = 20, 
            variable=v, 
            value=1,
            command=upper_radio_button_pressed).pack(anchor=W) # call the function upper_radio_button pressed
            
Radiobutton(root, 
            text="Perl",
            padx = 20, 
            variable=v, 
            value=2,
            command=lower_radio_button_pressed).pack(anchor=W)# call the function upper_radio_button pressed

# a canvas is a graphical object, here blue_img and red_img 
# define the dimensions of the pictures  inside of the window and that it is shown inside of the window root 

canvas_width = 200
canvas_height = 100
canvas = Canvas(root, 
           width=canvas_width, 
           height=canvas_height)
canvas.pack()


#definition of picture blue_img 
blue_img = PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Zeiger_gruen_links.PPM") 

#definition of picture red_img 
red_img = PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Zeiger_rot_links.PPM")



# call of the class App with parameter root for the window
app = App(root)

Label(root,text="Vorname:").pack()
vorname = entry1.pack()

Label(root,text="Nachnahme:").pack()
nachname = entry2.pack()

#start window loop
root.mainloop()

print(vorname)
print(nachname)
