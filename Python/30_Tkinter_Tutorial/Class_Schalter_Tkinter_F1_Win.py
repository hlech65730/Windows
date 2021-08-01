
# Tkinter
# Definition einer Klasse Schalter

try:
    # Tkinter for Python 2.xx
    import Tkinter as tk
except:
    # Tkinter for Python 3.xx
    import tkinter as tk


canvas_width = 50
canvas_height = 50
	
app_win = tk.Tk()
			
			


class Schalter(tk.Frame):
	
	def __init__(self,app_win):
			self.lower_radio_button_pressed()
			sqr_gry_arrow_red_img = tk.PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Pfeil_rot_klein.gif")
			sqr_gry_circle_grn_img = tk.PhotoImage(file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Kreis_durchstrichen_gruen_klein.gif")
			v= tk.IntVar(self.var)
					
	def upper_radio_button_pressed(self):
			self.canvas = Canvas(app_win, width=canvas_width, height=canvas_height)
			self.canvas.create_image(10,10, anchor=NW, image=sqr_gry_arrow_red_img)
			self.canvas.place(x = 150, y = 40, width=50, height=50)
	
	#self.var = tk.IntVar()
	
	tk.Radiobutton(app_win, 
            text="Schalter ON",
            padx = 10, 
            variable= tk.Intvar(self), 
            value=1,
            command=upper_radio_button_pressed).place(x = 20,
            y = 30, width=100, height=30)
            
	def lower_radio_button_pressed(self):
			self.canvas = Canvas(app_win, width=canvas_width, height=canvas_height)
			self.canvas.create_image(10,10, anchor=NW, image=sqr_gry_circle_grn_img)
			self.canvas.place(x = 150, y = 40, width=50, height=50)
	
	tk.Radiobutton(app_win, 
            text="Schalter OFF",
            padx = 10, 
            variable=tk.Intvar(self), 
            value=2,
            command=lower_radio_button_pressed).place(x = 20,
            y = 70, width=120, height=30)

	
		

		
	
schalter_1 = Schalter()

def main():

	app_win.title("Schalter")
		# width x height + x_offset + y_offset:
	app_win.geometry("500x200+30+30")
	app_win.mainloop()
	
	


if __name__ == '__main__':
	main()
