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


#1 inch is equal to 10 pixels
table_size = (900,510)
margins = ((dimensions[0]-table_size[0])/2,(dimensions[1]-table_size[1])/2)

#(X,Y)
points = [30, 0, 415, 0, 405, 35, 65, 
    35]
for i in range(len(points)/2):
    points[2*i] += margins[0]
    points[2*i+1] += margins[1]
    
points_2 = [455, 0, 870, 0, 835, 35, 465, 
    35]
for i in range(len(points_2)/2):
    points_2[2*i] += margins[0]
    points_2[2*i+1] += margins[1]
    
points_3 = [30, 510, 415, 510, 405, 475, 65, 
    475]
for i in range(len(points_2)/2):
    points_3[2*i] += margins[0]
    points_3[2*i+1] += margins[1]
    
points_4 = [455, 510, 870, 510, 835, 475, 465, 
    475]
for i in range(len(points_2)/2):
    points_4[2*i] += margins[0]
    points_4[2*i+1] += margins[1]
    
points_5 = [0, 30, 0, 485, 35, 450, 35, 
    65]
for i in range(len(points_2)/2):
    points_5[2*i] += margins[0]
    points_5[2*i+1] += margins[1]
    
points_6 = [900, 30, 900, 485, 865, 450, 865, 
    65]
for i in range(len(points_2)/2):
    points_6[2*i] += margins[0]
    points_6[2*i+1] += margins[1]
balls = []
vels = []
pocket =[]

def create_ball(radius, color, x_pos, y_pos):
    balls.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius, fill = color))
    vels.append([5, 5])

def animate():
    for i in range(len(balls)):
        canvas.move(balls[i], vels[i][0], vels[i][1])

def create_pocket(radius, color, x_pos, y_pos):
    pocket.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos +radius, y_pos + radius, fill = color))
    

def start():
    canvas.create_rectangle(margins[0],margins[1],margins[0]+table_size[0],margins[1]+table_size[1],fill='#1e7228')
    canvas.create_polygon(points, fill='#1f822a', outline='#000000')
    canvas.create_polygon(points_2, fill='#1f822a', outline='#000000')
    canvas.create_polygon(points_3, fill='#1f822a', outline='#000000')
    canvas.create_polygon(points_4, fill='#1f822a', outline='#000000')
    canvas.create_polygon(points_5, fill='#1f822a', outline='#000000')
    canvas.create_polygon(points_6, fill='#1f822a', outline='#000000')
    create_pocket(25, '#000000', 30, 0)
    create_ball(20, '#000000', 500, 250)

def restart():
    create_ball(20, '#000000', 500, 250)
    
#Buttons
start_button = TK.Button(root, text='New Game', command=start)
start_button.grid(row=1, column=0)
restart_button = TK.Button(root, text='Reset', command=restart)
restart_button.grid(row=1, column=2)

#Load Logo
__dir__ = os.path.dirname(os.path.abspath(__file__))  
filename = os.path.join(__dir__, 'MiniPool Logo.png')

logo = PIL.Image.open(filename)
w, h = 600, 112

logo = logo.resize((w,h))
tkimg = PIL.ImageTk.PhotoImage(logo)
canvas.img = tkimg
try:
    canvas_imageID = canvas.create_image(w/2, h/2, image=tkimg)
except:
        pass

animate()        
root.mainloop()