import Tkinter as TK
import math

root = TK.Tk()
root.wm_title('MiniPool')

dimensions = (1280,720)
canvas = TK.Canvas(root, width=dimensions[0], height=dimensions[1], background='#FFFFFF')
canvas.grid(row=0, column=0, columnspan=4)

table_size = (1000,500)
margins = ((dimensions[0]-table_size[0])/2,(dimensions[1]-table_size[1])/2)
canvas.create_rectangle(margins[0],margins[1],margins[0]+table_size[0],margins[1]+table_size[1],fill='#1e7228')


'''
class BallVel:
    def __init__(self, x, y):
        self.x, self.y = (x,y)
'''

balls = []
vels = []

def create_ball(radius, color, x_pos, y_pos):
    balls.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius ,fill = color))
    vels.append([5, 5])
    
create_ball(20, '#000000', 500, 250)

def animate():
    for i in range(len(balls)):
        canvas.move(balls[i], vels[i][0], vels[i][1])
        
root.mainloop()
animate()