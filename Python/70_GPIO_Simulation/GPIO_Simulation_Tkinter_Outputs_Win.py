
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  GPIO_Simulation_Win.py
#  
#  Copyright 2020 uid02589 <uid02589@RBL7YK4G>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  OS : Win 10 
#  Simulation der GPIOs auf einem Windows PC
#  Anzeige der GPIO Zustaende

try:
	from Tkinter import * # Python 2
except:
	from tkinter import * # Python 3


root = Tk()
root.title("Set GPIO switches simulation") 
# Hauptfenster -> width x height + x_offset + y_offset:
root.geometry("500x600+30+30")

#Variablen fuer die Radiobutton der Schalter 
schalter_eins = IntVar()
schalter_zwei = IntVar()
schalter_drei = IntVar()
schalter_vier = IntVar()
schalter_fuenf = IntVar()
schalter_sechs = IntVar()
schalter_sieben = IntVar()

# Definition des Symbolfensters fuer die Grafik
canvas_width = 40
canvas_height = 40

# Definition der Bilder 
sqr_gry_arrow_red_img = PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Pfeil_rot_klein.gif")
sqr_gry_circle_grn_img = PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Kreis_durchstrichen_gruen_klein.gif")


# Ueberschrifts Label 
Label(root, 
		text="""Set switch:""",
		justify = LEFT,
		padx = 20).place(x = 200, y = 10, width=100, height=30)

#Schalter 1
def upper_radio_button_pressed_S1():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 40, width=40, height=40) 
def lower_radio_button_pressed_S1():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 40, width=40, height=40)   
#Schalter 2  
def upper_radio_button_pressed_S2():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 110, width=40, height=40)
def lower_radio_button_pressed_S2():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 110, width=40, height=40)
#Schalter 3
def upper_radio_button_pressed_S3():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 180, width=40, height=40)
def lower_radio_button_pressed_S3():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 180, width=40, height=40)
#Schalter 4
def upper_radio_button_pressed_S4():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 250, width=40, height=40)
def lower_radio_button_pressed_S4():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 250, width=40, height=40)
#Schalter 5
def upper_radio_button_pressed_S5():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 320, width=40, height=40)
def lower_radio_button_pressed_S5():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 320, width=40, height=40)
#Schalter 6
def upper_radio_button_pressed_S6():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 390, width=40, height=40)
def lower_radio_button_pressed_S6():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 390, width=40, height=40)
#Schalter 7
def upper_radio_button_pressed_S7():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 460, width=40, height=40)  
def lower_radio_button_pressed_S7():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 460, width=40, height=40)  




class App:
  def __init__(self, master):
    frame = Frame(master)
    frame.place(x = 15, y = 550, width=80, height=80)
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.place(x = 10, y = 10, width=70, height=30)

    

def main():
	
#print ("Debug Schalter ")

	lower_radio_button_pressed_S1()
	lower_radio_button_pressed_S2()
	lower_radio_button_pressed_S3()
	lower_radio_button_pressed_S4()
	lower_radio_button_pressed_S5()
	lower_radio_button_pressed_S6()
	lower_radio_button_pressed_S7()


	Radiobutton(root, 
            text="Schalter 1 ON",
            padx = 10, 
            variable=schalter_eins, 
            value=1,
            command=upper_radio_button_pressed_S1).place(x = 20, y = 30, width=100, height=30)
	Radiobutton(root, 
            text="Schalter 1 OFF",
            padx = 10, 
            variable=schalter_eins, 
            value=2,
            command=lower_radio_button_pressed_S1).place(x = 20, y = 60, width=100, height=30)

	Radiobutton(root, 
            text="Schalter 2 ON",
            padx = 10, 
            variable=schalter_zwei, 
            value=3,
            command=upper_radio_button_pressed_S2).place(x = 20, y = 100, width=100, height=30)
	Radiobutton(root, 
            text="Schalter 2 OFF",
            padx = 10, 
            variable=schalter_zwei, 
            value=4,
            command=lower_radio_button_pressed_S2).place(x = 20, y = 130, width=100, height=30)

	Radiobutton(root, 
            text="Schalter 3 ON",
            padx = 10, 
            variable=schalter_drei, 
            value=5,
            command=upper_radio_button_pressed_S3).place(x = 20, y = 170, width=100, height=30)
	Radiobutton(root, 
            text="Schalter 3 OFF",
            padx = 10, 
            variable=schalter_drei, 
            value=6,
            command=lower_radio_button_pressed_S3).place(x = 20, y = 200, width=100, height=30)

	Radiobutton(root, 
            text="Schalter 4 ON",
            padx = 10, 
            variable=schalter_vier, 
            value=7,
            command=upper_radio_button_pressed_S4).place(x = 20, y = 240, width=100, height=30)
	Radiobutton(root, 
            text="Schalter 4 OFF",
            padx = 10, 
            variable=schalter_vier, 
            value=8,
            command=lower_radio_button_pressed_S4).place(x = 20, y = 270, width=100, height=30)

	Radiobutton(root, 
            text="Schalter 5 ON",
            padx = 10, 
            variable=schalter_fuenf, 
            value=9,
            command=upper_radio_button_pressed_S5).place(x = 20, y = 310, width=100, height=30)
	Radiobutton(root, 
            text="Schalter 5 OFF",
            padx = 10, 
            variable=schalter_fuenf, 
            value=10,
            command=lower_radio_button_pressed_S5).place(x = 20, y = 340, width=100, height=30)

	Radiobutton(root, 
            text="Schalter 6 ON",
            padx = 10, 
            variable=schalter_sechs, 
            value=11,
            command=upper_radio_button_pressed_S6).place(x = 20, y = 380, width=100, height=30)
	Radiobutton(root, 
            text="Schalter 6 OFF",
            padx = 10, 
            variable=schalter_sechs, 
            value=12,
            command=lower_radio_button_pressed_S6).place(x = 20, y = 410, width=100, height=30)

	Radiobutton(root, 
            text="Schalter 7 ON",
            padx = 10, 
            variable=schalter_sieben, 
            value=13,
            command=upper_radio_button_pressed_S7).place(x = 20, y = 450, width=100, height=30)
	Radiobutton(root, 
            text="Schalter 7 OFF",
            padx = 10, 
            variable=schalter_sieben, 
            value=14,
            command=lower_radio_button_pressed_S7).place(x = 20, y = 480, width=100, height=30)




	app = App(root)
	root.mainloop()
      
     
if __name__ == '__main__':
	main()

# GPIO Belegung 
# GPIO 4  - Board Pin 7
# GPIO 7  - Board Pin 26
# GPIO 8  - Board Pin 24
# GPIO 11 - Board Pin 23
# GPIO 9  - Board Pin 21
# GPIO 10 - Board Pin 19
# GPIO 14 - Board Pin 8
# GPIO 15 - Board Pin 10
# GPIO 17 - Board Pin 11
# GPIO 18 - Board Pin 12
# GPIO 22 - Board Pin 15
# GPIO 13 - Board Pin 16
# GPIO 24 - Board Pin 18
# GPIO 25 - Board Pin 22


