import Tkinter as TK
import math

root = TK.Tk()
root.wm_title('MiniPool')

dimensions = (1600,900)
canvas = TK.Canvas(root, width=dimensions[0], height=dimensions[1], background='#FFFFFF')
canvas.grid(row=0, column=0, columnspan=4)

table_size = (1200,600)
margins = ((dimensions[0]-table_size[0])/2,(dimensions[1]-table_size[1])/2)
cushion = {'left':margins[0],'top':margins[1],'right':margins[0]+table_size[0],'bottom':margins[1]+table_size[1]}
canvas.create_rectangle(cushion['left'],cushion['top'],cushion['right'],cushion['bottom'],fill='#1e7228')

balls = []
vels = []
hit_x_cushion = []
hit_y_cushion = []

def create_ball(radius, color, x_pos, y_pos, x_vel, y_vel):
    balls.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius ,fill = color))
    vels.append([float(x_vel), float(y_vel)])
    hit_x_cushion.append(False)
    hit_y_cushion.append(False)
    
create_ball(20, '#000000', 500, 400, 0, 10)
create_ball(20, '#FF0000', 500, 700, -0, -10)
cushion_deflection = .9
rolling_friction = .98
min_vel = .4

def arctan(x, y):
    if x == 0:
        angle = math.pi/2
    else:
        angle = math.atan(y/x)
    return angle

def ball_collision(ball_i):
    x1, y1, x2, y2 = canvas.coords(balls[ball_i])
    x1 += vels[ball_i][0]/2
    x2 += vels[ball_i][0]/2
    y1 += vels[ball_i][1]/2
    y2 += vels[ball_i][1]/2
    ball_center = [(x1+x2)/2, (y1+y2)/2]
    ball_radius = (x2-x1)/2
    for i in range(ball_i+1, len(balls)):
        x1, y1, x2, y2 = canvas.coords(balls[i])
        x1 += vels[i][0]/2
        x2 += vels[i][0]/2
        y1 += vels[i][1]/2
        y2 += vels[i][1]/2
        other_center = [(x1+x2)/2, (y1+y2)/2]
        other_radius = (x2-x1)/2
        radial_distance = math.hypot(ball_center[0]-other_center[0],ball_center[1]-other_center[1])
        if ball_radius + other_radius >= radial_distance:
            contact_angle = arctan(ball_center[0]-other_center[0],ball_center[1]-other_center[1])
            collide_balls(ball_i, i, contact_angle)

def collide_balls(ball_i, other_i, phi):
    vx1i, vy1i = vels[ball_i]
    vx2i, vy2i = vels[other_i]
    v1i = math.hypot(vx1i, vy1i)
    v2i = math.hypot(vx2i, vy2i)
    a1i = arctan(vx1i, vy1i)
    a2i = arctan(vx2i, vy2i)
    vx1f = v2i*math.cos(a2i-phi)*math.cos(phi)-v1i*math.sin(a1i-phi)*math.sin(phi)
    vy1f = v2i*math.cos(a2i-phi)*math.sin(phi)+v1i*math.sin(a1i-phi)*math.cos(phi)
    vx2f = v1i*math.cos(a1i-phi)*math.cos(phi)-v2i*math.sin(a2i-phi)*math.sin(phi)
    vy2f = v1i*math.cos(a1i-phi)*math.sin(phi)+v2i*math.sin(a2i-phi)*math.cos(phi)
    vels[ball_i] = [vx1f, vy1f]
    vels[other_i] = [vx2f, vy2f]
                               

def animate():
    for i in range(len(balls)):
        x1, y1, x2, y2 = canvas.coords(balls[i])
        if x1+vels[i][0]/2 <= cushion['left'] or x2+vels[i][0]/2 >= cushion['right']:
            if hit_x_cushion[i] == False:
                vels[i][0] = -cushion_deflection*vels[i][0]
                hit_x_cushion[i] = True
        else:
            hit_x_cushion[i] = False
        if y1+vels[i][1]/2 <= cushion['top'] or y2+vels[i][1]/2 >= cushion['bottom']:
            if hit_y_cushion[i] == False:
                vels[i][1] = -cushion_deflection*vels[i][1]
                hit_y_cushion[i] = True
        else:
            hit_y_cushion[i] = False
        ball_collision(i)
        canvas.move(balls[i], vels[i][0], vels[i][1])
            
    for i in range(len(vels)):
        #vels[i] = [rolling_friction*vels[i][0], rolling_friction*vels[i][1]]
        if math.hypot(vels[i][0],vels[i][1]) < min_vel:
            vels[i] = [0,0]
    canvas.after(10, animate)

animate()
root.mainloop()

