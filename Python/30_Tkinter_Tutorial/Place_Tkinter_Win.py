
# Tkinter
# Verwendung von Place

from Tkinter import *

def upper_radio_button_pressed():
  canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
  canvas.place(x = 150, y = 40, width=50, height=50)

  
  
def lower_radio_button_pressed():
  canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
  canvas.place(x = 150, y = 40, width=50, height=50)
 


class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.place(x = 15, y = 80, width=80, height=80)
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.place(x = 10, y = 10, width=50, height=30)
    
root = Tk()

v = IntVar()
#z = IntVar()

# width x height + x_offset + y_offset:
root.geometry("500x200+30+30") 


Label(root, 
      text="""Set switch:""",
      justify = LEFT,
      padx = 20).place(x = 200, y = 20, width=100, height=30)
Radiobutton(root, 
            text="Schalter ON",
            padx = 10, 
            variable=v, 
            value=1,
            command=upper_radio_button_pressed).place(x = 20, y = 30, width=100, height=30)
Radiobutton(root, 
            text="Schalter OFF",
            padx = 10, 
            variable=v, 
            value=2,
            command=lower_radio_button_pressed).place(x = 20, y = 50, width=100, height=30)

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
