import Tkinter as TK
import math

root = TK.Tk()
root.wm_title('MiniPool')

dimensions = (1280,720)
canvas = TK.Canvas(root, width=dimensions[0], height=dimensions[1], background='#FFFFFF')
canvas.grid(row=0, column=0, columnspan=4)

table_size = (1000,500)
margins = ((dimensions[0]-table_size[0])/2,(dimensions[1]-table_size[1])/2)
cushion = {'left':margins[0],'top':margins[1],'right':margins[0]+table_size[0],'bottom':margins[1]+table_size[1]}
canvas.create_rectangle(cushion['left'],cushion['top'],cushion['right'],cushion['bottom'],fill='#1e7228')

balls = []
vels = []
hit_x_cushion = []
hit_y_cushion = []

def create_ball(radius, color, x_pos, y_pos):
    balls.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius ,fill = color))
    vels.append([50, 5])
    hit_x_cushion.append(False)
    hit_y_cushion.append(False)
    
create_ball(20, '#000000', 500, 250)

cushion_deflection = .9
rolling_friction = .98
min_vel = .5


def animate():
    for i in range(len(balls)):
        canvas.move(balls[i], vels[i][0], vels[i][1])
        x1, y1, x2, y2 = canvas.coords(balls[i])
        if x1 < cushion['left'] or x2 > cushion['right']:
            if hit_x_cushion[i] == False:
                vels[i][0] = -cushion_deflection*vels[i][0]
                hit_x_cushion[i] = True
        else:
            hit_x_cushion[i] = False
        if y1 < cushion['top'] or y2 > cushion['bottom']:
            if hit_y_cushion[i] == False:
                vels[i][1] = -cushion_deflection*vels[i][1]
                hit_y_cushion[i] = True
        else:
            hit_y_cushion[i] = False
    canvas.after(len(balls), animate)
    for i in range(len(vels)):
        vels[i] = [rolling_friction*vels[i][0], rolling_friction*vels[i][1]]
        if vels[i][0]**2 + vels[i][1]**2 < min_vel**2:
            vels[i] = [0,0]

animate()
root.mainloop()

