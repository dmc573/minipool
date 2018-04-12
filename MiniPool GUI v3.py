import Tkinter as TK
import math
import PIL
from PIL import ImageTk
import os.path
import winsound

root = TK.Tk()
root.wm_title('MiniPool')

dimensions = (1280,720)
canvas = TK.Canvas(root, width=dimensions[0], height=dimensions[1], background='#FFFFFF')
canvas.grid(row=0, column=0, columnspan=4)


#1 inch is equal to 10 pixels
table_size = (900,510)
margins = ((dimensions[0]-table_size[0])/2,4*(dimensions[1]-table_size[1])/5)

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
pockets = []
startcircle = []

def round_rectangle(x1, y1, x2, y2, radius, clr, outln):

    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, fill = clr, outline = outln, smooth=True)
'''https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
    SneakyTurtle, stack overflow'''

def create_diamond(x_pos, y_pos, orientation):
    if orientation == 'h':
        x_offset = 5
        y_offset = 2
    else:
        x_offset = 2
        y_offset = 5
    d1 = [x_pos, y_pos+y_offset, x_pos+x_offset, y_pos, x_pos, y_pos-y_offset, x_pos-x_offset, y_pos]

    canvas.create_polygon(d1, fill='#ffffff', outline='#ffffff')

def create_ball(radius, color, x_pos, y_pos):
    balls.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius, fill = color))
    vels.append([5, 5])

def create_pocket(radius, color, x_pos, y_pos):
    pockets.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos +radius, y_pos + radius, fill = color))
    
def create_startcircle(radius, color, x_pos, y_pos):
    startcircle.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos +radius, y_pos + radius, fill = color, outline = color))
    
def create_table():
    round_rectangle(150, 128, 1130, 718, 100, '#727272', '#727272')
    canvas.create_rectangle(margins[0]+20,margins[1]+20,margins[0]+table_size[0]-20,margins[1]+table_size[1]-20,fill='#60B0F4')
    canvas.create_polygon(points, fill='#475F6C', outline='#000000')
    canvas.create_polygon(points_2, fill='#475F6C', outline='#000000')
    canvas.create_polygon(points_3, fill='#475F6C', outline='#000000')
    canvas.create_polygon(points_4, fill='#475F6C', outline='#000000')
    canvas.create_polygon(points_5, fill='#475F6C', outline='#000000')
    canvas.create_polygon(points_6, fill='#475F6C', outline='#000000')
    create_diamond(margins[0]+25+103, 150, 'v')
    create_diamond(margins[0]+25+205, 150, 'v')
    create_diamond(margins[0]+25+308, 150, 'v')
    create_diamond(dimensions[0]-margins[0]-25-103, 150, 'v')
    create_diamond(dimensions[0]-margins[0]-25-205, 150, 'v')
    create_diamond(dimensions[0]-margins[0]-25-308, 150, 'v')
    create_diamond(margins[0]+103, 700, 'v')
    create_diamond(margins[0]+205, 700, 'v')
    create_diamond(margins[0]+308, 700, 'v')
    create_diamond(dimensions[0]-margins[0]-25-103, 700, 'v')
    create_diamond(dimensions[0]-margins[0]-25-205, 700, 'v')
    create_diamond(dimensions[0]-margins[0]-25-308, 700, 'v')
    create_diamond(170, margins[1]+25+115, 'h')
    create_diamond(170, margins[1]+25+230, 'h')
    create_diamond(170, margins[1]+25+345, 'h')
    create_diamond(1110, margins[1]+25+115, 'h')
    create_diamond(1110, margins[1]+25+230, 'h')
    create_diamond(1110, margins[1]+25+345, 'h')
    create_startcircle(5, '#aaaaaa', dimensions[0]-margins[0]-25-205, margins[1]+25+230)
    create_pocket(25, '#000000', 215, 193)
    create_pocket(25, '#000000', 625, 183)
    create_pocket(25, '#000000', 1065, 193)
    create_pocket(25, '#000000', 215, 653)
    create_pocket(25, '#000000', 625, 663)
    create_pocket(25, '#000000', 1065, 653)

def start():
    create_ball(15, '#000000', 500, 250)

def restart():
    create_ball(15, '#000000', 500, 250)
    
def new_game():
    create_table()
    start()
    
def in_pocket(ball_i):
    x1, y1, x2, y2 = canvas.coords(balls[ball_i])
    pocket_center = [(x1+x2)/2, (y1+y2)/2]
    for pocket in pockets:
        x1, y1, x2, y2 = canvas.coords(pocket)
        ball_center = [(x1+x2)/2, (y1+y2)/2]
        pocket_radius = (x2-x1)/2
        radial_distance = math.hypot(pocket_center[0]-ball_center[0],pocket_center[1]-ball_center[1])
        if radial_distance < pocket_radius:
            balls[ball_i].grid_remove()
    
#Buttons
start_button = TK.Button(root, text='New Game', command=new_game)
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
        
root.mainloop()