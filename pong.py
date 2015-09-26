import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]
paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [random.randrange(120, 240)/60, random.randrange(60, 180)/60]

    if direction == RIGHT:
        ball_vel[0] = ball_vel[0]
        ball_vel[1] = ball_vel[1]
        
    elif direction == LEFT:
        ball_vel[0] = -1 * ball_vel[0]
        ball_vel[1] = -1 * ball_vel[1]
 
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    ball_pos = [WIDTH/2, HEIGHT/2]
    direction = random.choice([RIGHT, LEFT])
    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel

        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
 
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]

    elif ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH + 3 ):
        if (paddle1_pos + PAD_HEIGHT) >= ball_pos[1] >= paddle1_pos:
            ball_vel[0] = -ball_vel[0] * 1.1  
            ball_vel[1] *= 1.1
          
        else: 
            score2 += 1
            spawn_ball(RIGHT)
    
    elif ball_pos[0] >= ((WIDTH-1)-BALL_RADIUS-PAD_WIDTH):
        if (paddle2_pos + PAD_HEIGHT) >= ball_pos[1] >= paddle2_pos:
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
              
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Yellow", "Green")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    if ((paddle1_pos + paddle1_vel) >= PAD_HEIGHT) and ((paddle1_pos + paddle1_vel) <= (HEIGHT - PAD_HEIGHT)):
        paddle1_pos += paddle1_vel
    elif (paddle1_pos + paddle1_vel) > (HEIGHT - PAD_HEIGHT):
        paddle1_pos = HEIGHT - PAD_HEIGHT
        paddle1_vel = 0
    elif (paddle1_pos + paddle1_vel) < 0:
        paddle1_pos = 0 
        paddle1_vel = 0
        
    if ((paddle2_pos + paddle2_vel) >= PAD_HEIGHT) and ((paddle2_pos + paddle2_vel) <= (HEIGHT - PAD_HEIGHT)):
        paddle2_pos += paddle2_vel
    elif (paddle2_pos + paddle2_vel) > (HEIGHT - PAD_HEIGHT):
        paddle2_pos = HEIGHT - PAD_HEIGHT
        paddle2_vel = 0
    elif (paddle2_pos + paddle2_vel) < 0:
        paddle2_pos = 0
        paddle2_vel = 0

  # draw paddles
    canvas.draw_polygon([(0, paddle1_pos),                               
                      (0, paddle1_pos + PAD_HEIGHT),                  
                      (PAD_WIDTH, paddle1_pos + PAD_HEIGHT),          
                      (PAD_WIDTH, paddle1_pos)], 2, "Blue", "Blue")
    canvas.draw_polygon([(WIDTH-PAD_WIDTH, paddle2_pos),  #A                             
                      (WIDTH-PAD_WIDTH, paddle2_pos + PAD_HEIGHT), #D                 
                      (WIDTH-1, paddle2_pos + PAD_HEIGHT), #C          
                      (WIDTH - 1, paddle2_pos)], 2, "Red", "Red") #B
    # draw scores
    canvas.draw_text(str(score1), (200, 100),30, "Green")
    canvas.draw_text(str(score2), ( 400, 100), 30, "Green")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 3
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel -=acc
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0

def button_handler():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
button = frame.add_button('Restart', button_handler)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()