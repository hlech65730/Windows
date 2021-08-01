
# Tkinter
# Verwendung von Grid

from Tkinter import *

def upper_radio_button_pressed():
  canvas.create_image(20,20, anchor=NW, image=sqr_gry_arrow_red_img)
  canvas.grid(row=3, column=2)
  
  
def lower_radio_button_pressed():
  canvas.create_image(20,20, anchor=NW, image=sqr_gry_circle_grn_img)
  canvas.grid(row=3, column=2)
 


class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.grid(row=6, column=2)
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.grid(row=0, column=1)
    
root = Tk()

v = IntVar()
z = IntVar()

# width x height + x_offset + y_offset:
root.geometry("500x300+30+30") 


Label(root, 
      text="""Set switch:""",
      justify = LEFT,
      padx = 20).grid(row=2, column=2)
Radiobutton(root, 
            text="Schalter ON",
            padx = 20, 
            variable=v, 
            value=1,
            command=upper_radio_button_pressed).grid(row=3, column=1)
Radiobutton(root, 
            text="Schalter OFF",
            padx = 20, 
            variable=v, 
            value=2,
            command=lower_radio_button_pressed).grid(row=4, column=1)

canvas_width = 50
canvas_height = 50


canvas = Canvas(root, 
		width=canvas_width, 
		height=canvas_height)
		
sqr_gry_arrow_red_img = PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Pfeil_rot_klein.gif")
sqr_gry_circle_grn_img = PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Kreis_durchstrichen_gruen_klein.gif")

lower_radio_button_pressed()

app = App(root)


root.mainloop()
