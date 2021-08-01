#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  unbenannt.py
#  
#  Copyright 2017 Holger Lech 
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
#  

import First_Try_Win

def main():
	
	x = 42
	
	print(First_Try_Win.funk())
	
	First_Try_Win.User_input()
	
	f = open('text.txt','r')
	
	print(f.readline())
	
	

	
	return 0

if __name__ == '__main__':
	main()

