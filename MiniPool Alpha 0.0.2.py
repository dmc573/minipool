import Tkinter as TK
import math
import time
import PIL
from PIL import ImageTk
import os.path
import winsound

'''
MiniPool Alpha 0.1
Made by Derek Cantor and Shane Kirk
March 16 to April 19, 2018
'''

# timer (used to track the length of each frame)

stop = -1
stopped = 0
cue_ball_exists = 0
still = 0
trajectory_indicators = []


def timer(start_time):
    return (time.time() - start_time)

'''
    GUI Functions
'''
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

def create_diamond(x_pos, y_pos, orientation):    # creates a small white diamond
    x_pos += margins[0]
    y_pos += margins[1]
    if orientation == 'h':  # horizontal
        x_offset = 5
        y_offset = 2
    else:                   # vertical
        x_offset = 2
        y_offset = 5
    d1 = [x_pos, y_pos+y_offset, x_pos+x_offset, y_pos, x_pos, y_pos-y_offset, x_pos-x_offset, y_pos]

    canvas.create_polygon(d1, fill='#F2F2F2', outline='#F2F2F2')

def create_ball(radius, color, x_pos, y_pos, x_vel, y_vel):     # creates a billiard ball and places it on the table
    x_pos += margins[0]
    y_pos += margins[1]
    balls.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius ,fill = color,outline = color))
    vels.append([float(x_vel), float(y_vel)])

def create_cue_ball():     # creates a billiard ball and places it on the table
    global cue_ball, cue_ball_vel, cue_ball_exists
    cue_ball = canvas.create_oval(185+margins[0], 240+margins[1], 215+margins[0], 270+margins[1], fill = '#ffffff', outline = '#ffffff')
    cue_ball_vel = [0.0,0.0]
    cue_ball_exists = 1

def create_pocket(radius, x_pos, y_pos):                 # creates a pocket to be placed near the edge of the table
    x_pos += margins[0]
    y_pos += margins[1]
    pockets.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius, fill = '#000000'))
    
def ball_score(radius, color, x_pos, y_pos):             # creates placeholders for pocketed balls
    score.append(canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius, fill = color, outline = color))
    
def create_startcircle(radius, color, x_pos, y_pos):     # places indicator circle on pool table
    global startcircle
    x_pos += margins[0]
    y_pos += margins[1]
    startcircle = canvas.create_oval(x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius, fill = color, outline = color)
    
def create_table():                                      # creates the entire table
    global pool_table
    pool_table = True
    # border for pocketed ball zone
    round_rectangle(DIMENSIONS[0]-margins[0]-235, 30, DIMENSIONS[0]-margins[0], 80, 10, '#f9d49f', '#000000')
    
    # placeholders for pocketed balls
    ball_score(15, '#bbbbbb', DIMENSIONS[0]-395, 55)
    ball_score(15, '#bbbbbb', DIMENSIONS[0]-360, 55)
    ball_score(15, '#bbbbbb', DIMENSIONS[0]-325, 55)
    ball_score(15, '#bbbbbb', DIMENSIONS[0]-290, 55)
    ball_score(15, '#bbbbbb', DIMENSIONS[0]-255, 55)
    ball_score(15, '#bbbbbb', DIMENSIONS[0]-220, 55)
    
    # pool table border
    round_rectangle(margins[0]-40, margins[1]-40, margins[0]+TABLE_SIZE[0]+40, margins[1]+TABLE_SIZE[1]+40, 100, '#6b2c00', '#6b2c00')
    
    # pool felt
    canvas.create_rectangle(margins[0]+10,margins[1]+10,margins[0]+TABLE_SIZE[0]-10,margins[1]+TABLE_SIZE[1]-10,fill='#1e7228')
    
    # pool cushions
    canvas.create_polygon(points_1, fill='#1f822a', outline='#000000')
    canvas.create_polygon(points_2, fill='#1f822a', outline='#000000')
    canvas.create_polygon(points_3, fill='#1f822a', outline='#000000')
    canvas.create_polygon(points_4, fill='#1f822a', outline='#000000')
    canvas.create_polygon(points_5, fill='#1f822a', outline='#000000')
    canvas.create_polygon(points_6, fill='#1f822a', outline='#000000')
    
    # diamond markers
    create_diamond(120, -20, 'v')
    create_diamond(230, -20, 'v') 
    create_diamond(340, -20, 'v')
    create_diamond(TABLE_SIZE[0]-120, -20, 'v')
    create_diamond(TABLE_SIZE[0]-230, -20, 'v')
    create_diamond(TABLE_SIZE[0]-340, -20, 'v')
    create_diamond(120, TABLE_SIZE[1]+20, 'v')
    create_diamond(230, TABLE_SIZE[1]+20, 'v')
    create_diamond(340, TABLE_SIZE[1]+20, 'v')
    create_diamond(TABLE_SIZE[0]-120, TABLE_SIZE[1]+20, 'v')
    create_diamond(TABLE_SIZE[0]-230, TABLE_SIZE[1]+20, 'v')
    create_diamond(TABLE_SIZE[0]-340, TABLE_SIZE[1]+20, 'v')
    create_diamond(-20, 135, 'h')
    create_diamond(-20, 255, 'h')
    create_diamond(-20, 375, 'h')
    create_diamond(TABLE_SIZE[0]+20, 135, 'h')
    create_diamond(TABLE_SIZE[0]+20, 255, 'h')
    create_diamond(TABLE_SIZE[0]+20, 375, 'h')
    
    # indicator circle
    create_startcircle(8, '#888888', TABLE_SIZE[0]-25-205, 25+230)
    
    # six pockets
    create_pocket(25, 25, 25)
    create_pocket(25, 450, 15)
    create_pocket(25, 875, 25)
    create_pocket(25, 25, 485)
    create_pocket(25, 450, 495)
    create_pocket(25, 875, 485)

def rack_6ball():
    x,y = TABLE_SIZE[0]-25-205, 25+230
    create_ball(15, '#ffe01c', x, y, 0, 0)
    create_ball(15, '#2f2fe2', x+27, y+16, 0, 0)
    create_ball(15, '#d81111', x+27, y-16, 0, 0)
    create_ball(15, '#6e1fa3', x+54, y+32, 0, 0)
    create_ball(15, '#ff880a', x+54, y, 0, 0)
    create_ball(15, '#0c890c', x+54, y-32, 0, 0)
    
def new_game(): # creates table with cue ball
    global start_time, times, stop, balls, vels, collided, cushioned, pockets, score, scored, balls_to_delete, trajectory_indicators, aiming, still
    if stop == 0:
        stop = 1
    if stopped == 1:
        canvas.delete("all")
    balls = []              # stores the Tkinter ball objects
    vels = []               # stores the velocities of each ball
    collided = []           # stores pairs of balls that have just collided
    cushioned = []          # stores balls that have just bounced off a cushion
    pockets = []            # stores the Tkinter pocket objects
    score = []              # stores pocket ball placeholders
    scored = []             # stores pocketed balls
    balls_to_delete = []    # stacks items to be deleted
    trajectory_indicators = []  # stores Tkinter circle objects for the trajectory path
    still = 1
    aiming = 1
    create_table()
    create_cue_ball()
    rack_6ball()
    start_time = time.time()
    times = [0]
    animate()
    
def in_pocket(ball_i):
    if ball_i == 'c':
        x1, y1, x2, y2 = canvas.coords(cue_ball)
        ball_center = [(x1+x2)/2, (y1+y2)/2]
        for pocket in pockets:
            x1, y1, x2, y2 = canvas.coords(pocket)
            pocket_center = [(x1+x2)/2, (y1+y2)/2]
            pocket_radius = (x2-x1)/2
            radial_distance = math.hypot(pocket_center[0]-ball_center[0],pocket_center[1]-ball_center[1])
            if radial_distance < pocket_radius:
                delete_cue_ball()
        if ball_center[0] < margins[0] or ball_center[0] > margins[0]+TABLE_SIZE[0] or ball_center[1] < margins[1] or ball_center[1] > margins[1]+TABLE_SIZE[1]:
            delete_cue_ball()
    else: 
        x1, y1, x2, y2 = canvas.coords(balls[ball_i])
        ball_center = [(x1+x2)/2, (y1+y2)/2]
        for pocket in pockets:
            x1, y1, x2, y2 = canvas.coords(pocket)
            pocket_center = [(x1+x2)/2, (y1+y2)/2]
            pocket_radius = (x2-x1)/2
            radial_distance = math.hypot(pocket_center[0]-ball_center[0],pocket_center[1]-ball_center[1])
            if radial_distance < pocket_radius:
                balls_to_delete.append(ball_i)
        if ball_center[0] < margins[0] or ball_center[0] > margins[0]+TABLE_SIZE[0] or ball_center[1] < margins[1] or ball_center[1] > margins[1]+TABLE_SIZE[1]:
            balls_to_delete.append(ball_i)

def delete_ball(ball_i):
    pos = len(scored)
    scored.append(ball_score(15, canvas.itemcget(balls[ball_i], 'fill'), DIMENSIONS[0]-395+35*pos, 55))
    canvas.delete(balls[ball_i])
    balls.pop(ball_i)
    vels.pop(ball_i)

def delete_cue_ball():
    global cue_ball_exists
    canvas.delete(cue_ball)
    cue_ball_exists = 0

def adjust_trajectory(dummy):
    global trajectory_indicators, aiming
    if still:
        aiming = 1
        direction = (direction_intvar.get()-360)*math.pi/360.
        speed = speed_intvar.get()
        try:
            x1, y1, x2, y2 = canvas.coords(cue_ball)
        except NameError:
            x1, y1, x2, y2 = 185+margins[0], 240+margins[1], 215+margins[0], 270+margins[1]
        ball_center = [(x1+x2)/2., (y1+y2)/2.]
        interval = [speed/10.*math.cos(direction), speed/10.*math.sin(direction)]
        for item in trajectory_indicators:
            canvas.delete(item)
        trajectory_indicators = []
        for i in range(1,6):
            x, y = add_vectors(ball_center, scalar_product(i, interval))
            trajectory_indicators.append(canvas.create_oval(x-5, y-5, x+5, y+5, fill = '#bbbbbb', outline = '#bbbbbb'))

def shoot():
    global aiming, cue_ball_vel
    direction = (direction_intvar.get()-360)*math.pi/360.
    speed = speed_intvar.get()
    cue_ball_vel = [speed*math.cos(direction), speed*math.sin(direction)]
    aiming = 0
    pass

'''
    Physics Functions
'''

def rotate(x, y, angle):
    # Rotates point ('x','y') 'angle' radians about origin.
    magnitude = math.hypot(x,y)
    direction = arctan(x,y)
    direction += angle
    x = magnitude*math.cos(direction)
    y = magnitude*math.sin(direction)
    return (x,y)

def arctan(x, y):
    # Computes angle based on horizontal and vertical component
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
    # Finds the dot product of two vectors.
    if len(v1) == len(v2):
        t = 0
        for i in range(len(v1)):
            t += v1[i]*v2[i]
        return t
    else:
        raise IndexError('Input lists are unequal in length.')

def scalar_product(scalar, vector):
    # Multiplies a vector by a scalar.
    v = []
    for d in vector:
        v.append(d*scalar)
    return v

def add_vectors(v1, v2):
    # Adds two vectors term-by-term.
    if len(v1) == len(v2):
        v = []
        for i in range(len(v1)):
            v.append(v1[i]+v2[i])
        return v
    else:
        raise IndexError('Input lists are unequal in length.')

def subtract_vectors(v1, v2):
    # Subtracts vectors term-by-term.
    if len(v1) == len(v2):
        v = []
        for i in range(len(v1)):
            v.append(v1[i]-v2[i])
        return v
    else:
        raise IndexError('Input lists are unequal in length.')

def square_sum(v):
    # Computes the sum of the squares of each term in a list.
    t = 0
    for d in v:
        t += d**2
    return t

def ball_cushion(ball_i):
    global cue_ball, cue_ball_vel
    # Computes any reflections off cushions with 'ball_i'.
    if ball_i == 'c':                                                      # Check for collisions with cue ball
        x1, y1, x2, y2 = canvas.coords(cue_ball)
        ball_center = [(x1+x2)/2., (y1+y2)/2.]
        ball_radius = (x2-x1)/2.
        for i in range(len(walls)):
            wall = walls[i]
            x1, y1, x2, y2 = wall
            x0, y0 = ball_center
            orientation = orientations[i]
            if orientation == 'h':                                             # Cushion is horizontal
                if x0 == sorted([x0, x1, x2])[1] and abs(y1-y0) <= ball_radius:
                    if (ball_i, i) not in cushioned:
                        cushioned.append((ball_i, i))
                        vx, vy = cue_ball_vel
                        cue_ball_vel = scalar_product(CUSHION_LOSS, [vx, -vy]) # Reverse y direction
                else:
                    while (ball_i, i) in cushioned:
                        cushioned.remove((ball_i, i))
            elif orientation == 'v':                                           # Cushion is horizontal
                if y0 == sorted([y0, y1, y2])[1] and abs(x1-x0) <= ball_radius:
                    if (ball_i, i) not in cushioned:
                        cushioned.append((ball_i, i))
                        vx, vy = cue_ball_vel
                        cue_ball_vel = scalar_product(CUSHION_LOSS, [-vx, vy]) # reverse x direction
                else:
                    while (ball_i, i) in cushioned:
                        cushioned.remove((ball_i, i))
            elif orientation == 'l':
                
    else:
        x1, y1, x2, y2 = canvas.coords(balls[ball_i])
        ball_center = [(x1+x2)/2., (y1+y2)/2.]
        ball_radius = (x2-x1)/2.
        for i in range(len(walls)):
            wall = walls[i]
            x1, y1, x2, y2 = wall
            x0, y0 = ball_center
            orientation = orientations[i]
            if orientation == 'h':
                if x0 == sorted([x0, x1, x2])[1] and abs(y1-y0) <= ball_radius:
                    if (ball_i, i) not in cushioned:
                        cushioned.append((ball_i, i))
                        vx, vy = vels[ball_i]
                        vels[ball_i] = vx, -vy
                else:
                    while (ball_i, i) in cushioned:
                        cushioned.remove((ball_i, i))
            elif orientation == 'v':
                if y0 == sorted([y0, y1, y2])[1] and abs(x1-x0) <= ball_radius:
                    if (ball_i, i) not in cushioned:
                        cushioned.append((ball_i, i))
                        vx, vy = vels[ball_i]
                        vels[ball_i] = -vx, vy
                else:
                    while (ball_i, i) in cushioned:
                        cushioned.remove((ball_i, i))
            else:
                angle = arctan((y2-y1),(x2-x1))
                x1, y1 = rotate(x1,y1,-angle)
                x2, y2 = rotate(x2,y2,-angle)
                x0, y0 = rotate(ball_center[0],ball_center[1],-angle)
                if abs(y1 - y2) > .5:
                    raise ArithmeticError('Rotating was unsuccessful')
                if x0 == sorted([x0, x1, x2])[1] and abs(y1-y0) <= ball_radius:
                    if (ball_i, i) not in cushioned:
                        cushioned.append((ball_i, i))
                        vx, vy = vels[ball_i]
                        vm = math.hypot(vx, vy)
                        vai = arctan(vx, vy)
                        incidence = vai-angle
                        while incidence >= math.pi:
                            incidence -= math.pi 
                        va = vai-incidence+math.pi-incidence
                        vels[ball_i] = [-vm*math.cos(va), -vm*math.sin(va)]
                else:
                    while (ball_i, i) in cushioned:
                        cushioned.remove((ball_i, i))
    
def ball_collision(ball_i):
    global cue_ball, cue_ball_vel
    # Computes any collisions with 'ball_i'.
    if ball_i == 'c':
        x1, y1, x2, y2 = canvas.coords(cue_ball)
        ball_center = [(x1+x2)/2., (y1+y2)/2.]
        ball_radius = (x2-x1)/2.
        for other_i in range(0, len(balls)):
            x1, y1, x2, y2 = canvas.coords(balls[other_i])
            other_center = [(x1+x2)/2., (y1+y2)/2.]
            other_radius = (x2-x1)/2.
            if test_collision(ball_center, ball_radius, other_center, other_radius): # If two balls are touching:
                if sorted((ball_i, other_i)) not in collided:                       # If the balls are not currently in a collision, then initiate the collision.
                    cue_ball_vel, vels[other_i] = calculate_collision(ball_center, cue_ball_vel, other_center, vels[other_i])
                    collided.append(sorted((ball_i, other_i)))
            else:                                                                   # Wait until the balls are separated, then terminate the collision. 
                while sorted((ball_i, other_i)) in collided:
                    collided.remove(sorted((ball_i, other_i)))
    else:
        x1, y1, x2, y2 = canvas.coords(balls[ball_i])
        ball_center = [(x1+x2)/2., (y1+y2)/2.]
        ball_radius = (x2-x1)/2.
        for other_i in range(0, len(balls)):
            if ball_i != other_i:
                x1, y1, x2, y2 = canvas.coords(balls[other_i])
                other_center = [(x1+x2)/2., (y1+y2)/2.]
                other_radius = (x2-x1)/2.
                if test_collision(ball_center, ball_radius, other_center, other_radius): # If two balls are touching:
                    if sorted((ball_i, other_i)) not in collided:                       # If the balls are not currently in a collision, then initiate the collision.
                        vels[ball_i], vels[other_i] = calculate_collision(ball_center, vels[ball_i], other_center, vels[other_i])
                        collided.append(sorted((ball_i, other_i)))
                else:                                                                   # Wait until the balls are separated, then terminate the collision. 
                    while sorted((ball_i, other_i)) in collided:
                        collided.remove(sorted((ball_i, other_i)))

def test_collision(center1, radius1, center2, radius2):
    # Checks to see if one of the balls is touching the other.
    radial_distance = math.hypot(center1[0]-center2[0],center1[1]-center2[1])
    return (radius1 + radius2 >= radial_distance)

def calculate_collision(x1, v1, x2, v2):
    # Uses vector math to compute the new velocities after the collision has commenced.
    v1f = scalar_product(COLLISION_LOSS, subtract_vectors(v1,scalar_product(float(dot_product(subtract_vectors(v1,v2),subtract_vectors(x1,x2)))/float(square_sum(subtract_vectors(x1,x2))),subtract_vectors(x1,x2))))
    v2f = subtract_vectors(add_vectors(v1,v2),v1f)  # Conservation of momentum
    return [v1f, v2f]

root = TK.Tk()
root.wm_title('MiniPool')

DIMENSIONS = (1280,720)
canvas = TK.Canvas(root, width=DIMENSIONS[0], height=DIMENSIONS[1], background='#FFFFFF')
canvas.grid(row=0, column=0, columnspan=4)

#1 inch is equal to 10 pixels
TABLE_SIZE = (900,510)
margins = ((DIMENSIONS[0]-TABLE_SIZE[0])/2,4*(DIMENSIONS[1]-TABLE_SIZE[1])/5)

COLLISION_LOSS = .9         # amount of momentum lost in collision
CUSHION_LOSS = .8           # amount of momentum lost in collision
ROLLING_FRICTION = .6       # amount of momentum lost to friction
MIN_VEL = 10                # lowest velocity a ball can go until stopping completely

#(X,Y)
points_1 = [33, 0, 430, 0, 420, 35, 68, 
    35]
for i in range(len(points_1)/2):
    points_1[2*i] += margins[0]
    points_1[2*i+1] += margins[1]
    
points_2 = [470, 0, 867, 0, 832, 35, 480, 
    35]
for i in range(len(points_2)/2):
    points_2[2*i] += margins[0]
    points_2[2*i+1] += margins[1]
    
points_3 = [33, 510, 430, 510, 420, 475, 68, 
    475]
for i in range(len(points_3)/2):
    points_3[2*i] += margins[0]
    points_3[2*i+1] += margins[1]
    
points_4 = [470, 510, 867, 510, 832, 475, 480, 
    475]
for i in range(len(points_4)/2):
    points_4[2*i] += margins[0]
    points_4[2*i+1] += margins[1]
    
points_5 = [0, 33, 0, 477, 35, 442, 35, 
    68]
for i in range(len(points_5)/2):
    points_5[2*i] += margins[0]
    points_5[2*i+1] += margins[1]
    
points_6 = [900, 33, 900, 477, 865, 442, 865, 
    68]
for i in range(len(points_6)/2):
    points_6[2*i] += margins[0]
    points_6[2*i+1] += margins[1]

walls = [[points_1[0],points_1[1],points_1[6],points_1[7]],[points_1[6],points_1[7],points_1[4],points_1[5]],[points_1[4],points_1[5],points_1[2],points_1[3]]
        ,[points_2[0],points_2[1],points_2[6],points_2[7]],[points_2[6],points_2[7],points_2[4],points_2[5]],[points_2[4],points_2[5],points_2[2],points_2[3]]
        ,[points_3[2],points_3[3],points_3[4],points_3[5]],[points_3[4],points_3[5],points_3[6],points_3[7]],[points_3[6],points_3[7],points_3[0],points_3[1]]
        ,[points_4[2],points_4[3],points_4[4],points_4[5]],[points_4[4],points_4[5],points_4[6],points_4[7]],[points_4[6],points_4[7],points_4[0],points_4[1]]
        ,[points_5[2],points_5[3],points_5[4],points_5[5]],[points_5[4],points_5[5],points_5[6],points_5[7]],[points_5[6],points_5[7],points_5[0],points_5[1]]
        ,[points_6[0],points_6[1],points_6[6],points_6[7]],[points_6[6],points_6[7],points_6[4],points_6[5]],[points_6[4],points_6[5],points_6[2],points_6[3]]
        ]

orientations = 'lhvvhrrhvvhlrvllvr'

speed_intvar = TK.IntVar()
speed_intvar.set(0)
direction_intvar = TK.IntVar()
direction_intvar.set(360)

#Buttons
start_button = TK.Button(root, text='New Game', command=new_game)
start_button.grid(row=1, column=0)
shoot_button = TK.Button(root, text='Shoot', command=shoot, state=TK.ACTIVE, disabledforeground='#000000')
shoot_button.grid(row=1, column=3)
direction_slider = TK.Scale(root, from_=0, to=720, orient=TK.HORIZONTAL, length = 760, variable=direction_intvar,
                                label='Direction', command=adjust_trajectory, showvalue=0)
direction_slider.grid(row=1, column=1)
direction_slider.set(360)
speed_slider = TK.Scale(root, from_=1000, to=0, variable=speed_intvar,
                                label='Speed', command=adjust_trajectory, showvalue=0)
speed_slider.grid(row=1, column=2)

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
                        
def animate():
    global stop, stopped, aiming, trajectory_indicators, cue_ball_vel, balls_to_delete
    times.append(timer(start_time))
    ft = times[-1]-times[-2]
    if not aiming:
        for item in trajectory_indicators:
            canvas.delete(item)
        if trajectory_indicators != []:
            trajectory_indicators = []
        if cue_ball_exists:
            ball_collision('c')
            ball_cushion('c')
            in_pocket('c')
            canvas.move(cue_ball, cue_ball_vel[0]*ft, cue_ball_vel[1]*ft)
            cue_ball_vel = [cue_ball_vel[0]*(ROLLING_FRICTION**ft), cue_ball_vel[1]*(ROLLING_FRICTION**ft)]
            if math.hypot(cue_ball_vel[0],cue_ball_vel[1]) < MIN_VEL:
                cue_ball_vel = [0.0,0.0]
        for i in range(len(balls)):
            ball_collision(i)
            ball_cushion(i)
            in_pocket(i)
            canvas.move(balls[i], vels[i][0]*ft, vels[i][1]*ft)    
        for i in range(len(vels)):
            vels[i] = [vels[i][0]*(ROLLING_FRICTION**ft), vels[i][1]*(ROLLING_FRICTION**ft)]
            if math.hypot(vels[i][0],vels[i][1]) < MIN_VEL:
                vels[i] = [0.0,0.0]
        while stop == 1:
            stopped = 1
            pass
        stopped = 0
        for i in balls_to_delete:
            delete_ball(i)
        balls_to_delete = []
        still = 1
        for vel in vels:
            if vel != [0.0, 0.0]:
                still = 0
                break
        if cue_ball_exists:
            if cue_ball_vel != [0.0, 0.0]:
                still = 0
        if still:
            shoot_button['state'] = TK.NORMAL
            speed_slider['state'] = TK.NORMAL
            direction_slider['state'] = TK.NORMAL
            aiming = 1
            if not cue_ball_exists:
                create_cue_ball()
        else:
            shoot_button['state'] = TK.DISABLED
            speed_slider['state'] = TK.DISABLED
            direction_slider['state'] = TK.DISABLED
            for i in balls_to_delete:
                delete_ball(i)
                balls_to_delete.pop(i)
                
    else:
        shoot_button['state'] = TK.NORMAL
    canvas.after(10, animate)
    
root.mainloop()