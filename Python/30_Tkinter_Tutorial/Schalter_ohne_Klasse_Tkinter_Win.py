
# Tkinter
# Erzeugung von Schaltern ohne Verwendung einer Klasse

try:
    # Tkinter for Python 2.xx
    import Tkinter as tk
except:
    # Tkinter for Python 3.xx
    import tkinter as tk

root = tk.Tk()
# Hauptfenster -> width x height + x_offset + y_offset:
root.geometry("500x600+30+30")

#Variablen fuer die Radiobutton der Schalter 
schalter_eins = tk.IntVar()
schalter_zwei = tk.IntVar()
schalter_drei = tk.IntVar()
schalter_vier = tk.IntVar()
schalter_fuenf = tk.IntVar()
schalter_sechs = tk.IntVar()
schalter_sieben = tk.IntVar()

# Definition des Symbolfensters fuer die Grafik
canvas_width = 40
canvas_height = 40

# Definition der Bilder 
sqr_gry_arrow_red_img = tk.PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Pfeil_rot_klein.gif")
sqr_gry_circle_grn_img = tk.PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Kreis_durchstrichen_gruen_klein.gif")


# Ueberschrifts Label 
tk.Label(root, 
		text="""Set switch:""",
		justify = 'left',
		padx = 20).place(x = 200, y = 10, width=100, height=30)

#Schalter 1
def upper_radio_button_pressed_S1():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 40, width=40, height=40)
def lower_radio_button_pressed_S1():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 40, width=40, height=40)
#Schalter 2  
def upper_radio_button_pressed_S2():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 110, width=40, height=40)
def lower_radio_button_pressed_S2():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 110, width=40, height=40)
#Schalter 3
def upper_radio_button_pressed_S3():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 180, width=40, height=40)
def lower_radio_button_pressed_S3():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 180, width=40, height=40)
#Schalter 4
def upper_radio_button_pressed_S4():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 250, width=40, height=40)
def lower_radio_button_pressed_S4():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 250, width=40, height=40)
#Schalter 5
def upper_radio_button_pressed_S5():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 320, width=40, height=40)
def lower_radio_button_pressed_S5():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 320, width=40, height=40)
#Schalter 6
def upper_radio_button_pressed_S6():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 390, width=40, height=40)
def lower_radio_button_pressed_S6():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 390, width=40, height=40)
#Schalter 7
def upper_radio_button_pressed_S7():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_arrow_red_img)
	canvas.place(x = 150, y = 460, width=40, height=40)  
def lower_radio_button_pressed_S7():
	canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
	canvas.create_image(10,10, anchor='nw', image=sqr_gry_circle_grn_img)
	canvas.place(x = 150, y = 460, width=40, height=40)








class App:
  def __init__(self, master):
    frame = tk.Frame(master)
    frame.place(x = 15, y = 550, width=80, height=80)
    self.button = tk.Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.place(x = 10, y = 10, width=70, height=30)

    

def main():
	
#print ("Debug Schalter ")
	schalter_eins  = 2
	lower_radio_button_pressed_S1()
	schalter_zwei  = 4
	lower_radio_button_pressed_S2()
	schalter_drei  = 6
	lower_radio_button_pressed_S3()
	schalter_vier  = 8
	lower_radio_button_pressed_S4()
	schalter_fuenf  = 10
	lower_radio_button_pressed_S5()
	schalter_sechs  = 12
	lower_radio_button_pressed_S6()
	schalter_sieben  = 14
	lower_radio_button_pressed_S7()


	tk.Radiobutton(root, 
            text="Schalter 1 ON",
            padx = 10, 
            variable=schalter_eins, 
            value=1,
            command=upper_radio_button_pressed_S1).place(x = 20, y = 30, width=100, height=30)
	tk.Radiobutton(root, 
            text="Schalter 1 OFF",
            padx = 10, 
            variable=schalter_eins, 
            value=2,
            command=lower_radio_button_pressed_S1).place(x = 20, y = 60, width=100, height=30)

	tk.Radiobutton(root, 
            text="Schalter 2 ON",
            padx = 10, 
            variable=schalter_zwei, 
            value=3,
            command=upper_radio_button_pressed_S2).place(x = 20, y = 100, width=100, height=30)
	tk.Radiobutton(root, 
            text="Schalter 2 OFF",
            padx = 10, 
            variable=schalter_zwei, 
            value=4,
            command=lower_radio_button_pressed_S2).place(x = 20, y = 130, width=100, height=30)

	tk.Radiobutton(root, 
            text="Schalter 3 ON",
            padx = 10, 
            variable=schalter_drei, 
            value=5,
            command=upper_radio_button_pressed_S3).place(x = 20, y = 170, width=100, height=30)
	tk.Radiobutton(root, 
            text="Schalter 3 OFF",
            padx = 10, 
            variable=schalter_drei, 
            value=6,
            command=lower_radio_button_pressed_S3).place(x = 20, y = 200, width=100, height=30)

	tk.Radiobutton(root, 
            text="Schalter 4 ON",
            padx = 10, 
            variable=schalter_vier, 
            value=7,
            command=upper_radio_button_pressed_S4).place(x = 20, y = 240, width=100, height=30)
	tk.Radiobutton(root, 
            text="Schalter 4 OFF",
            padx = 10, 
            variable=schalter_vier, 
            value=8,
            command=lower_radio_button_pressed_S4).place(x = 20, y = 270, width=100, height=30)

	tk.Radiobutton(root, 
            text="Schalter 5 ON",
            padx = 10, 
            variable=schalter_fuenf, 
            value=9,
            command=upper_radio_button_pressed_S5).place(x = 20, y = 310, width=100, height=30)
	tk.Radiobutton(root, 
            text="Schalter 5 OFF",
            padx = 10, 
            variable=schalter_fuenf, 
            value=10,
            command=lower_radio_button_pressed_S5).place(x = 20, y = 340, width=100, height=30)

	tk.Radiobutton(root, 
            text="Schalter 6 ON",
            padx = 10, 
            variable=schalter_sechs, 
            value=11,
            command=upper_radio_button_pressed_S6).place(x = 20, y = 380, width=100, height=30)
	tk.Radiobutton(root, 
            text="Schalter 6 OFF",
            padx = 10, 
            variable=schalter_sechs, 
            value=12,
            command=lower_radio_button_pressed_S6).place(x = 20, y = 410, width=100, height=30)

	tk.Radiobutton(root, 
            text="Schalter 7 ON",
            padx = 10, 
            variable=schalter_sieben, 
            value=13,
            command=upper_radio_button_pressed_S7).place(x = 20, y = 450, width=100, height=30)
	tk.Radiobutton(root, 
            text="Schalter 7 OFF",
            padx = 10, 
            variable=schalter_sieben, 
            value=14,
            command=lower_radio_button_pressed_S7).place(x = 20, y = 480, width=100, height=30)




	app = App(root)
	root.mainloop()
      
     
if __name__ == '__main__':
	main()




