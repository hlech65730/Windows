
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  GPIO_Simulation_Win.py
#  
#  Verwendung von Tkinter für die GPIO Ausgabe
#  Verwendung von Place

GPIO_BOARD = 'BOARD'
GPIO_OUT = 1
GPIO_IN =  0
GPIO_HIGH = 1
GPIO_LOW =  0


def GPIO_setmode(setmodetxt):
	print(' Mode set to',setmodetxt)

def GPIO_setup(number,mode):
	if mode == 1:
		print('GPIO mode set to OUT')
	else:
		print('GPIO mode set to IN')

def GPIO_output(number,status):
	print('GPIO',number,'set to',status)
	
def GPIO_cleanup():
	print('GPIO cleant')
