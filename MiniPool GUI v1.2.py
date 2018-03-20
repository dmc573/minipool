import Tkinter as TK
import math
import PIL
from PIL import ImageTk
import os.path

root = TK.Tk()
root.wm_title('MiniPool')

dimensions = (1280,720)
canvas = TK.Canvas(root, width=dimensions[0], height=dimensions[1], background='#FFFFFF')
canvas.grid(row=0, column=0, columnspan=4)

table_size = (1000,500)
margins = ((dimensions[0]-table_size[0])/2,(dimensions[1]-table_size[1])/2)

MAX = 800

balls = []
vels = []

def create_ball(radius, color, x_pos, y_pos):
    balls.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius ,fill = color))
    vels.append([5, 5])

def animate():
    for i in range(len(balls)):
        canvas.move(balls[i], vels[i][0], vels[i][1])

def start():
    canvas.create_rectangle(margins[0],margins[1],margins[0]+table_size[0],margins[1]+table_size[1],fill='#1e7228')
    create_ball(20, '#000000', 500, 250)

#Load Logo
__dir__ = os.path.dirname(os.path.abspath(__file__))  
filename = os.path.join(__dir__, 'MiniPool Logo.png')
filename_2 = os.path.join(__dir__, 'GLHF.png')
'''
startimage = PIL.Image.open(filename_2)

tkimg = PIL.ImageTk.PhotoImage(startimage)
canvas.img = tkimg
'''
#Buttons
start_button = TK.Button(root, text='start', command=start)
start_button.grid(row=0, column=0)

#Images
logo = PIL.Image.open(filename)
w, h = 600, 112

logo = logo.resize((w,h))
tkimg = PIL.ImageTk.PhotoImage(logo)
canvas.img = tkimg


animate()        
root.mainloop()