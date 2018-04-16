import Tkinter as TK
import math
import time
import random

start_time = time.time()
times = [0]
def timer():
    return (time.time() - start_time)
    

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
collided = []

def create_ball(radius, color, x_pos, y_pos, x_vel, y_vel):
    balls.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius, fill = color, outline = color))
    vels.append([float(x_vel), float(y_vel)])
    hit_x_cushion.append(False)
    hit_y_cushion.append(False)
    
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

def rand8bit():
    return random.randint(0,255)
def randcolor():
    '''Takes three IntVar and returns a color Tkinter string like #FFFFFF.        
    '''
    r=hexstring(rand8bit())
    g=hexstring(rand8bit())
    b=hexstring(rand8bit())
    return '#'+r+g+b

def randpos():
    return [random.randint(margins[0]+20, dimensions[0]-margins[0]-20),random.randint(margins[1]+20, dimensions[1]-margins[1]-20)]

def randvel():
    return random.uniform(-200,200)

for i in range(20):
    x,y = randpos()
    create_ball(20, randcolor(), x, y, randvel(), randvel())
cushion_deflection = 1
rolling_friction = 1
min_vel = 1

def arctan(x, y):
    x = float(x)
    y = float(y)
    if x == 0:
        if y > 0:
            angle = math.pi/2
        elif y < 0:
            angle = -math.pi/2
        else:
            angle = 2*math.pi # Does not matter what value is
    elif y == 0:
        if x > 0:
            angle = 0.0
        else:
            angle = math.pi
    else:
        angle = math.atan(y/x)
    return angle

def dot_product(v1, v2):
    if len(v1) == len(v2):
        t = 0
        for i in range(len(v1)):
            t += v1[i]*v2[i]
        return t
    else:
        raise IndexError('Input lists are unequal in length.')

def scalar_product(scalar, vector):
    v = []
    for d in vector:
        v.append(d*scalar)
    return v

def add_vectors(v1, v2):
    if len(v1) == len(v2):
        v = []
        for i in range(len(v1)):
            v.append(v1[i]+v2[i])
        return v
    else:
        raise IndexError('Input lists are unequal in length.')

def subtract_vectors(v1, v2):
    if len(v1) == len(v2):
        v = []
        for i in range(len(v1)):
            v.append(v1[i]-v2[i])
        return v
    else:
        raise IndexError('Input lists are unequal in length.')

def square_sum(v):
    t = 0
    for d in v:
        t += d**2
    return t

def ball_collision(ball_i):
    x1, y1, x2, y2 = canvas.coords(balls[ball_i])
    ball_center = [(x1+x2)/2., (y1+y2)/2.]
    ball_radius = (x2-x1)/2.
    for other_i in range(0, len(balls)):
        if ball_i != other_i:
            x1, y1, x2, y2 = canvas.coords(balls[other_i])
            other_center = [(x1+x2)/2., (y1+y2)/2.]
            other_radius = (x2-x1)/2.
            if test_collision(ball_center, ball_radius, other_center, other_radius):
                if sorted((ball_i, other_i)) not in collided:
                    vels[ball_i], vels[other_i] = calculate_collision(ball_center, vels[ball_i], other_center, vels[other_i])
            else:
                while sorted((ball_i, other_i)) in collided:
                    collided.remove(sorted((ball_i, other_i)))
def test_collision(center1, radius1, center2, radius2):
    radial_distance = math.hypot(center1[0]-center2[0],center1[1]-center2[1])
    return (radius1 + radius2 >= radial_distance)

def calculate_collision(x1, v1, x2, v2):
    v1f = subtract_vectors(v1,scalar_product(float(dot_product(subtract_vectors(v1,v2),subtract_vectors(x1,x2)))/float(square_sum(subtract_vectors(x1,x2))),subtract_vectors(x1,x2)))
    v2f = subtract_vectors(add_vectors(v1,v2),v1f)
    return [v1f, v2f]

def animate():
    times.append(timer())
    ft = times[-1]-times[-2]
    for i in range(len(balls)):
        x1, y1, x2, y2 = canvas.coords(balls[i])
        if x1 <= cushion['left'] or x2 >= cushion['right']:
            if hit_x_cushion[i] == False:
                vels[i][0] = -cushion_deflection*vels[i][0]
                hit_x_cushion[i] = True
        else:
            hit_x_cushion[i] = False
        if y1 <= cushion['top'] or y2 >= cushion['bottom']:
            if hit_y_cushion[i] == False:
                vels[i][1] = -cushion_deflection*vels[i][1]
                hit_y_cushion[i] = True
        else:
            hit_y_cushion[i] = False
        ball_collision(i)
        canvas.move(balls[i], vels[i][0]*ft, vels[i][1]*ft)
            
    for i in range(len(vels)):
        vels[i] = [rolling_friction*vels[i][0], rolling_friction*vels[i][1]]
        if math.hypot(vels[i][0],vels[i][1]) < min_vel:
            vels[i] = [0,0]
            
    canvas.after(1, animate)

animate()
root.mainloop()

