
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
			
sqr_gry_arrow_red_img = tk.PhotoImage(file="D:\\Repositories\\Windows\\Python\\30_Tkinter_Tutorial\\20_Gif\\Rechteck_grau_mit_Pfeil_rot_klein.gif")
sqr_gry_circle_grn_img = tk.PhotoImage(file="D:\\Repositories\\Windows\\Python\\30_Tkinter_Tutorial\\20_Gif\\Rechteck_grau_mit_Kreis_durchstrichen_gruen_klein.gif")


class Schalter(tk.Frame):
	
	def __init__(self,app_win):
			self.app_win = app_win
			self.var = tk.IntVar()
			
			tk.Radiobutton(app_win, 
				text="Schalter ON",
				padx = 10, 
				variable= self.var, 
				value=1,
				command=self.upper_radio_button_pressed).place(x = 30,
				y = 30, width=100, height=30)
					
			tk.Radiobutton(app_win, 
				text="Schalter OFF",
				padx = 10, 
				variable=self.var, 
				value=2,
				command=self.lower_radio_button_pressed).place(x = 20,
				y = 70, width=120, height=30)
				
			self.canvas = tk.Canvas(app_win, width=canvas_width, height=canvas_height)
			self.canvas.create_image(10,10, anchor='nw', image=sqr_gry_circle_grn_img)
			self.canvas.place(x = 150, y = 40, width=50, height=50)
			
			self.var.set(2)
			
	def upper_radio_button_pressed(self):
			self.canvas.create_image(10,10, anchor='nw', image=sqr_gry_arrow_red_img)
            
	def lower_radio_button_pressed(self):
			self.canvas.create_image(10,10, anchor='nw', image=sqr_gry_circle_grn_img)


def main():

	app_win.title("Schalter")
		# width x height + x_offset + y_offset:
	app_win.geometry("500x200+30+30")
	schalter_1 = Schalter(app_win)
	app_win.mainloop()
	
	


if __name__ == '__main__':
	main()
