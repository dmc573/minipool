#####
# bouncing_ball.py
# 
# Creates a Scale and a Canvas. Animates a circle based on the Scale
# (c) 2013 PLTW
# version 11/1/2013
####

import Tkinter #often people import Tkinter as *
import random
import math

def hexstring(slider_int):
    '''A function to prepare data from controller's widget for view's consumption
    
    slider_intvar is an IntVar between 0 and 255, inclusive
    hexstring() returns a string representing two hexadecimal digits
    '''
    
    slider_hex = hex(slider_int)
    # Drop the 0x at the beginning of the hex string
    slider_hex_digits = slider_hex[2:] 
    # Ensure two digits of hexadecimal:
    if len(slider_hex_digits)==1:
        slider_hex_digits = '0' + slider_hex_digits 
    return slider_hex_digits

def color(r,g,b):
    '''Takes three IntVar and returns a color Tkinter string like #FFFFFF.        
    '''
    rx=hexstring(r)
    gx=hexstring(g)
    bx=hexstring(b)
    return '#'+rx+gx+bx

#####
# Create root window 
####
root = Tkinter.Tk()

#####
# Create Model
######
speed_intvar = Tkinter.IntVar()
speed_intvar.set(3) # Initialize y coordinate
# radius and x-coordinate of circle
r = 10
directions = [] # radians of angle in standard position, ccw from positive x axis
 
######
# Create Controller
#######
# Instantiate and place slider
speed_slider = Tkinter.Scale(root, from_=20, to=1, variable=speed_intvar,    
                              label='speed')
speed_slider.grid(row=1, column=0, sticky=Tkinter.W)
# Create and place directions for the user
text = Tkinter.Label(root, text='Drag slider \nto adjust\nspeed.')
text.grid(row=0, column =0)

######
# Create View
#######
# Create and place a canvas
canvas = Tkinter.Canvas(root, width=600, height=600, background='#FFFFFF')
canvas.grid(row=0, rowspan=2, column=1)

# Create a circle on the canvas to match the initial model

amount = 20

def rand8bit():
    return random.randint(0,255)

def randpos():
    return random.randint(r, 600-r)

circles = []

for i in range(amount):
    x = randpos()
    y = randpos()
    circles.append(canvas.create_oval(x-r, y-r, x+r, y+r, 
                                 outline='#000000', fill=color(rand8bit(),rand8bit(),rand8bit())))
    directions.append(random.uniform(0,2*math.pi))

def animate():
    for i in range(amount):
        global directions
        # Get the slider data and create x- and y-components of velocity
        velocity_x = speed_intvar.get() * math.cos(directions[i]) # adj = hyp*cos()
        velocity_y = speed_intvar.get() * math.sin(directions[i]) # opp = hyp*sin()
        # Change the canvas item's coordinates
        canvas.move(circles[i], velocity_x, velocity_y)
        
        # Get the new coordinates and act accordingly if ball is at an edge
        x1, y1, x2, y2 = canvas.coords(circles[i])
        # If crossing left or right of canvas
        if x2>canvas.winfo_width() or x1<0: 
            directions[i] = math.pi - directions[i]
        # If crossing top or bottom of canvas
        if y2>canvas.winfo_height() or y1<0: 
            directions[i] = -1 * directions[i] # Reverse the y-component of velocity
        
        # Create an event in 1 msec that will be handled by animate(),
        # causing recursion        
    canvas.after(amount, animate)
# Call function directly to start the recursion
animate()

#######
# Event Loop
#######
root.mainloop()