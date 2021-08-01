# -*- coding: utf-8 -*-
try:
    # Tkinter for Python 2.xx
    import Tkinter as tk
except:
    # Tkinter for Python 3.xx
    import tkinter as tk

APP_TITLE = "Schalter"
APP_XPOS = 30
APP_YPOS = 30
APP_WIDTH = 300
APP_HEIGHT = 100

CANVAS_WIDTH = 50
CANVAS_HEIGHT = 50


class Schalter(tk.Frame):

    def __init__(self, app_win):
        self.app_win = app_win
        tk.Frame.__init__(self, app_win)
        
        self.sqr_gry_arrow_red_img = tk.PhotoImage(
            file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Pfeil_rot_klein.ppm")
        self.sqr_gry_circle_grn_img = tk.PhotoImage(
            file="D:\\uid_02589\\python\\30_Tkinter_Tutorial\\pictures\\Rechteck_grau_mit_Kreis_durchstrichen_gruen_klein.gif")
                
        radio_button_frame = tk.Frame(self)
        radio_button_frame.pack(side='left', expand=True)
        
        self.var = tk.IntVar()
        tk.Radiobutton(radio_button_frame, text="Schalter ON",padx=10, 
            variable=self.var, value=1, command=self.upper_radio_button_pressed
            ).pack(anchor='w')
            
        rb = tk.Radiobutton(radio_button_frame, text="Schalter OFF", padx=10,
            variable=self.var, value=2, command=self.lower_radio_button_pressed)
        rb.pack(anchor='w')

        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack(side='left', expand=True)
        
        self.canvas.create_image(10, 10, anchor='nw', tag="Schaltersymbol")
        
        rb.invoke()
        
    def lower_radio_button_pressed(self):
        self.canvas.itemconfig(
            "Schaltersymbol", image=self.sqr_gry_circle_grn_img)
        
    def upper_radio_button_pressed(self):
        self.canvas.itemconfig(
            "Schaltersymbol", image=self.sqr_gry_arrow_red_img)
                   
def main():
    app_win = tk.Tk()
    app_win.title(APP_TITLE)
    app_win.geometry("+{}+{}".format(APP_XPOS, APP_YPOS))
    #app_win.geometry("{}x{}".format(APP_WIDTH, APP_HEIGHT))
    
    app = Schalter(app_win)
    app.pack(fill='both', expand=True)
    
    app_win.mainloop()
 
 
if __name__ == '__main__':
    main()
