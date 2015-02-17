import pyglet
import random
import math

WINDOW_X = 640
WINDOW_Y = 480

def centerAnchor(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

snakeHead_image = pyglet.image.load('snake_heads.png')
snakeTail_image = pyglet.image.load('snake_tails.png')
snakeSeg_image = pyglet.image.load('snake_segs.png')
apple_image = pyglet.image.load('apple.png')
segments = pyglet.image.ImageGrid(snakeSeg_image, 3, 2).get_texture_sequence()
heads = pyglet.image.ImageGrid(snakeHead_image, 2, 2).get_texture_sequence()
tails = pyglet.image.ImageGrid(snakeTail_image, 2, 2).get_texture_sequence()

segmentsDict = {}
segmentsDict['DownRight'] = segments[0]
segmentsDict['LeftUp'] = segments[0]
segmentsDict['DownLeft'] = segments[1]
segmentsDict['RightUp'] = segments[1]
segmentsDict['UpRight'] = segments[2]
segmentsDict['LeftDown'] = segments[2]
segmentsDict['UpLeft'] = segments[3]
segmentsDict['RightDown'] = segments[3]
segmentsDict['Up'] = segments[4]
segmentsDict['Down'] = segments[4]
segmentsDict['Left'] = segments[5]
segmentsDict['Right'] = segments[5]
segmentsDict['HeadLeft'] = heads[0]
segmentsDict['HeadDown'] = heads[1]
segmentsDict['HeadUp'] = heads[2]
segmentsDict['HeadRight'] = heads[3]
segmentsDict['TailLeft'] = tails[0]
segmentsDict['TailDown'] = tails[1]
segmentsDict['TailUp'] = tails[2]
segmentsDict['TailRight'] = tails[3]

for segment in segmentsDict:
    centerAnchor(segmentsDict[segment])
centerAnchor(apple_image)   

#-------------------------------------------------------------------------------
class World():
    appleImage = apple_image
    
    def __init__(self, snake):
        self.snake = snake
        self.score = 0
        self.apple = self.findAppleXY()
        self.keyPressed = False
      
        
    def draw(self):
        self.snake.draw()
        self.appleImage.blit(self.apple.x, self.apple.y)
        pyglet.text.Label(str(self.score), font_size=14, x= 30, y = 20).draw()
        
        
    def findAppleXY(self):
        newX = random.randrange(20, WINDOW_X, 20)
        newY = random.randrange(20, WINDOW_Y, 20)
        newApple = Apple(newX, newY)
        if self.snake.detectCollision(newApple):
            return self.findAppleXY()
        return newApple
    
    
    def keyPress(self, symbol):
        if not self.keyPressed:
            self.keyPressed = True
            currentDir = self.snake.direction
            if symbol == pyglet.window.key.UP and currentDir != "Down":
                self.snake.direction = "Up"
            if symbol == pyglet.window.key.RIGHT and currentDir != "Left":
                self.snake.direction = "Right"
            if symbol == pyglet.window.key.LEFT and currentDir != "Right":
                self.snake.direction = "Left"
            if symbol == pyglet.window.key.DOWN and currentDir != "Up":
                self.snake.direction = "Down"
    
    
    def onTick(self):
        self.keyPressed = False
        if self.snake.onTick():
            self.snake = Snake(WINDOW_X // 2, 480 // 2, 5)
            self.apple = self.findAppleXY()
            self.score = 0
        if self.snake.collision(self.snake.head, self.apple):
            self.snake.length += int(self.snake.length * 0.3)
            self.apple = self.findAppleXY()
            self.score += self.snake.length
        
#-------------------------------------------------------------------------------
class Snake():
    imageDict = segmentsDict
    #directions:
        # "Up"
        # "Right"
        # "Down"
        # "Left"
    
    def __init__(self, x, y, length):
        self.direction = "Up"
        self.head = SnakeSegment(x, y, self.direction, self.imageDict["Up"])
        self.length = length
        
        
    def addSegment(self, segment):
        segment.next = self.head
        self.head = segment
        
        
    def removeTail(self):
        count = self.length
        curr = self.head
        while count > 0 and curr.next != None:
            lastDir = curr.direction
            curr = curr.next
            count -= 1
        if lastDir == "Left":
            newTail = self.imageDict["TailRight"]
        elif lastDir == "Up":
            newTail = self.imageDict["TailDown"]
        elif lastDir == "Right":
            newTail = self.imageDict["TailLeft"]
        else:
            newTail = self.imageDict["TailUp"]
        curr.image = newTail
        curr.next = None
        
        
    def onTick(self):
        if self.direction == "Up":
            delta_x = 0
            delta_y = 20
        if self.direction == "Right":
            delta_x = 20
            delta_y = 0
        if self.direction == "Down":
            delta_x = 0
            delta_y = -20
        if self.direction == "Left":
            delta_x = -20
            delta_y = 0

        self.head.image = self.imageDict[self.direction]
        newImage = self.imageDict["Head" + self.direction]
            
        self.head.image = self.newNeckImage(self.head.direction, self.direction)
        self.addSegment(SnakeSegment(self.head.x + delta_x, 
                                     self.head.y + delta_y, 
                                     self.direction,
                                     newImage))
        self.removeTail()
        if self.detectCollision(self.head):
            return True
        return self.head.x > WINDOW_X + 40 or self.head.x < 0 - 40 or self.head.y > WINDOW_Y + 40 or self.head.y < 0 - 40
    
    
    def newNeckImage(self, oldDir, newDir):
        if oldDir == newDir:
            newDir = ""
        return self.imageDict[oldDir + newDir]
        
        
    def detectCollision(self, item):
        current = self.head
        if item == self.head:
            current = self.head.next
        while current != None:
            if self.collision(item, current):
                return True
            current = current.next
        return False
        
        
    def collision(self, item1, item2):
        return item1.x == item2.x and item1.y == item2.y
        
        
    def draw(self):
        current = self.head
        while current != None:
            current.draw()
            current = current.next

#-------------------------------------------------------------------------------
class SnakeSegment():
    
    def __init__(self, x, y, direction, image):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = image
        self.next = None

    def draw(self):
        self.image.blit(self.x, self.y)

#-------------------------------------------------------------------------------        
class Apple():

    def __init__(self, x, y):
        self.x = x
        self.y = y

#-------------------------------------------------------------------------------

window = pyglet.window.Window(WINDOW_X, 480)
snake = Snake(WINDOW_X // 2, 480 // 2, 5)
world = World(snake)
clock = 0.0

@window.event
def on_key_press(symbol, modifiers):
    world.keyPress(symbol)

@window.event
def on_draw():
    window.clear()
    world.draw()

def update(delta_time):
    global clock
    if clock >= 0.10:
        world.onTick()
        clock = 0.0
    clock += delta_time


pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
