import pyglet
import math



PADDLE_SPEED = 500
PADDLE_SEGMENTS = 8
START_BALL_SPEED = 200
WINDOW_X = 640
WINDOW_Y = 480


window = pyglet.window.Window(WINDOW_X, WINDOW_Y)

# Classes
#-------------------------------------------------------------------------------
class World(object):
    """The current state of the game"""
    
    label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=10, y=10)
    
    def __init__(self, listOfPaddles, ball, speedPerSecond):
        self.listOfPaddles = listOfPaddles
        self.ball = ball
        self.speed = speedPerSecond
        self.score1 = 0
        self.score2 = 0
        
    def onTick(self, dt):

        for paddle in self.listOfPaddles:
            paddle.onTick(dt)
        self.ball.onTick(self.speed, dt)

        rPaddle = self.listOfPaddles[1]
        lPaddle = self.listOfPaddles[0]
        paddleHeight = (rPaddle.paddleSegHeight * PADDLE_SEGMENTS)

        if self.ball.x >= WINDOW_X - self.ball.ballWidth - rPaddle.paddleSegWidth:
            rPaddleMid = rPaddle.y + (paddleHeight // 2)
            if abs(self.ball.y - rPaddleMid) <= paddleHeight // 2:
               
                self.ball.x = WINDOW_X - self.ball.ballWidth - rPaddle.paddleSegWidth
                self.ball.dir_x *= -1.15
                self.ball.dir_y = (self.ball.y - rPaddleMid) / rPaddle.paddleSegHeight
                
        elif self.ball.x <= 0 + self.ball.ballWidth + lPaddle.paddleSegWidth:
            lPaddleMid = lPaddle.y + (paddleHeight // 2)
            if abs(self.ball.y - lPaddleMid) <= paddleHeight // 2:
               
                self.ball.x = 0 + ball.ballWidth + rPaddle.paddleSegWidth
                self.ball.dir_x *= -1.15
                self.ball.dir_y = (self.ball.y - lPaddleMid) / lPaddle.paddleSegHeight
                
        if self.ball.x < 0:
            self.score2 += 1
            self.ball.x = WINDOW_X // 2
            self.ball.y = WINDOW_Y // 2
            self.ball.dir_y = 0
            self.ball.dir_x = 1
        elif self.ball.x > WINDOW_X:
            self.score1 += 1
            self.ball.x = WINDOW_X // 2
            self.ball.y = WINDOW_Y // 2
            self.ball.dir_y = 0
            self.ball.dir_x = -1
        
    def draw(self):
        for paddle in self.listOfPaddles:
            paddle.draw()
        self.ball.draw()
        pyglet.text.Label(str(self.score1), font_size=14, x= 30, y = 20).draw()
        pyglet.text.Label(str(self.score2), font_size=14, x = WINDOW_X - 30, y = 20).draw()
        
    def keyPress(self, symbol, isPressed):
        # use isPress? to toggle keyup and key down so we can have 
        # smooth movement
        if symbol == pyglet.window.key.Q:
            self.listOfPaddles[0].move(1, isPressed)
        elif symbol == pyglet.window.key.A:
            self.listOfPaddles[0].move(-1, isPressed)
        elif symbol == pyglet.window.key.O:
            self.listOfPaddles[1].move(1, isPressed)
        elif symbol == pyglet.window.key.L:
            self.listOfPaddles[1].move(-1, isPressed)


#-------------------------------------------------------------------------------    
class Ball(object):
    """The current state of the ball"""
    ballImage = pyglet.image.load('ball.png')
    ballHeight = ballImage.height // 2
    ballWidth = ballImage.width // 2
    pyglet.image.anchor_x = ballWidth
    pyglet.image.anchor_y = ballHeight
    
    def __init__(self, x, y, dir_x):
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = 0.0
        
    def draw(self):
        self.ballImage.blit(self.x, self.y)
        
    def onTick(self, speed, dt):
        #dt lets us know how much of an actual tick has occured
        self.x += int(self.dir_x * speed * dt)
        self.y += int(self.dir_y * speed * dt)
        if self.y > WINDOW_Y - self.ballHeight:
            self.y = WINDOW_Y - self.ballHeight
            self.dir_y *= -1
        elif self.y < 0:
            self.y = self.ballHeight
            self.dir_y *= -1
        
 #-------------------------------------------------------------------------------       
class Paddle(object):
    """One of the two paddles on the screen"""
    paddleSeg = pyglet.image.load('paddleSeg.png')
    paddleSegWidth = paddleSeg.width
    paddleSegHeight = paddleSeg.height
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moving = 0
        
    def move(self, direction, isPressed):
        if isPressed == True:
            self.moving = direction
        elif isPressed == False and self.moving == direction:
            self.moving = 0
    
    def onTick(self, dt):
        #dt lets us know how much of an actual tick has occured
        self.y += int(self.moving * PADDLE_SPEED * dt)
        if self.y + (PADDLE_SEGMENTS * self.paddleSegHeight) > WINDOW_Y:
            self.y = WINDOW_Y - (PADDLE_SEGMENTS * self.paddleSegHeight)
        if self.y < 0:
            self.y = 0
    
    def draw(self):
        for i in range(PADDLE_SEGMENTS):
            self.paddleSeg.blit(self.x, self.y + (i * self.paddleSegHeight))


#-------------------------------------------------------------------------------
# Initialize World, paddles, and the ball
paddles = [Paddle(0, WINDOW_Y // 2), 
           Paddle(WINDOW_X - 10, WINDOW_Y // 2)]
ball = Ball(WINDOW_X // 2, WINDOW_Y // 2, 1)
world = World(paddles, ball, START_BALL_SPEED)


# pass Pyglet on_draw(), key_press(), and onTick()
@window.event
def on_draw():
    window.clear()
    world.draw()

@window.event
def on_key_press(symbol, modifiers):
    world.keyPress(symbol, True)
    
@window.event
def on_key_release(symbol, modifiers):
    world.keyPress(symbol, False)

# dt is the change in time since last update (not really a tick)
def tick(dt):
    world.onTick(dt)
        
pyglet.clock.schedule_interval(tick, 1/60.0)

# launch
pyglet.app.run()
