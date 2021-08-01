#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  GPIO_Tkinter_without_Class.py
# 
#  OS : Win 10  
# Tkinter
# Erzeugung von Schaltern ohne Verwendung einer Klasse

try:
	from Tkinter import * # Python 2
except:
	from tkinter import * # Python 3


root = Tk()
# Hauptfenster -> width x height + x_offset + y_offset:
root.geometry("500x600+30+30")

#Variablen fuer die Radiobutton der Schalter 
gpio_04 = IntVar()
gpio_07 = IntVar()
gpio_08 = IntVar()
gpio_09 = IntVar()
gpio_10 = IntVar()
gpio_11 = IntVar()
gpio_14 = IntVar()

# Definition des Symbolfensters fuer die Grafik
canvas_width = 40
canvas_height = 40

# Definition der Bilder 
sqr_gry_arrow_red_img = PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Pfeil_rot_klein.gif")
sqr_gry_circle_grn_img = PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Kreis_durchstrichen_gruen_klein.gif")


# Ueberschrifts Label 
Label(root, 
		text="""Set GPIO:""",
		justify = LEFT,
		padx = 20).place(x = 200, y = 10, width=100, height=30)

#GPIO 4
def upper_radio_button_pressed_S1():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 200, y = 40, width=40, height=40)  
def lower_radio_button_pressed_S1():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 200, y = 40, width=40, height=40)
#GPIO 7  
def upper_radio_button_pressed_S2():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 200, y = 110, width=40, height=40)
def lower_radio_button_pressed_S2():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 200, y = 110, width=40, height=40)
#GPIO 8
def upper_radio_button_pressed_S3():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 200, y = 180, width=40, height=40)
def lower_radio_button_pressed_S3():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 200, y = 180, width=40, height=40)
#GPIO 9
def upper_radio_button_pressed_S4():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 200, y = 250, width=40, height=40)
def lower_radio_button_pressed_S4():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 200, y = 250, width=40, height=40)
#GPIO 10
def upper_radio_button_pressed_S5():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 200, y = 320, width=40, height=40)
def lower_radio_button_pressed_S5():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 200, y = 320, width=40, height=40)
#GPIO 11
def upper_radio_button_pressed_S6():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 200, y = 390, width=40, height=40)
def lower_radio_button_pressed_S6():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 200, y = 390, width=40, height=40)
#GPIO 14
def upper_radio_button_pressed_S7():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
	canvas.place(x = 200, y = 460, width=40, height=40)  
def lower_radio_button_pressed_S7():
	canvas = Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
	canvas.place(x = 200, y = 460, width=40, height=40)








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
            text="GPIO 4 ON",
            padx = 10, 
            variable=gpio_04, 
            value=1,
            command=upper_radio_button_pressed_S1).place(x = 20, y = 30, width=100, height=30)
	Radiobutton(root, 
            text="GPIO 4 OFF",
            padx = 10, 
            variable=gpio_04, 
            value=2,
            command=lower_radio_button_pressed_S1).place(x = 20, y = 60, width=100, height=30)

	Radiobutton(root, 
            text="GPIO 7 ON",
            padx = 10, 
            variable=gpio_07, 
            value=3,
            command=upper_radio_button_pressed_S2).place(x = 20, y = 100, width=100, height=30)
	Radiobutton(root, 
            text="GPIO 7 OFF",
            padx = 10, 
            variable=gpio_07, 
            value=4,
            command=lower_radio_button_pressed_S2).place(x = 20, y = 130, width=100, height=30)

	Radiobutton(root, 
            text="GPIO 8 ON",
            padx = 10, 
            variable=gpio_08, 
            value=5,
            command=upper_radio_button_pressed_S3).place(x = 20, y = 170, width=100, height=30)
	Radiobutton(root, 
            text="GPIO 8 OFF",
            padx = 10, 
            variable=gpio_08, 
            value=6,
            command=lower_radio_button_pressed_S3).place(x = 20, y = 200, width=100, height=30)

	Radiobutton(root, 
            text="GPIO 9 ON",
            padx = 10, 
            variable=gpio_09, 
            value=7,
            command=upper_radio_button_pressed_S4).place(x = 20, y = 240, width=100, height=30)
	Radiobutton(root, 
            text="GPIO 9 OFF",
            padx = 10, 
            variable=gpio_09, 
            value=8,
            command=lower_radio_button_pressed_S4).place(x = 20, y = 270, width=100, height=30)

	Radiobutton(root, 
            text="GPIO 10 ON",
            padx = 10, 
            variable=gpio_10, 
            value=9,
            command=upper_radio_button_pressed_S5).place(x = 20, y = 310, width=100, height=30)
	Radiobutton(root, 
            text="GPIO 10 OFF",
            padx = 10, 
            variable=gpio_10, 
            value=10,
            command=lower_radio_button_pressed_S5).place(x = 20, y = 340, width=100, height=30)

	Radiobutton(root, 
            text="GPIO 11 ON",
            padx = 10, 
            variable=gpio_11, 
            value=11,
            command=upper_radio_button_pressed_S6).place(x = 20, y = 380, width=100, height=30)
	Radiobutton(root, 
            text="GPIO 11 OFF",
            padx = 10, 
            variable=gpio_11, 
            value=12,
            command=lower_radio_button_pressed_S6).place(x = 20, y = 410, width=100, height=30)

	Radiobutton(root, 
            text="GPIO 14 ON",
            padx = 10, 
            variable=gpio_14, 
            value=13,
            command=upper_radio_button_pressed_S7).place(x = 20, y = 450, width=100, height=30)
	Radiobutton(root, 
            text="GPIO 14 OFF",
            padx = 10, 
            variable=gpio_14, 
            value=14,
            command=lower_radio_button_pressed_S7).place(x = 20, y = 480, width=100, height=30)




	app = App(root)
	root.mainloop()
      
     
if __name__ == '__main__':
	main()




