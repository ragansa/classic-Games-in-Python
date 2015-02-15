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
centerAnchor(apple_image)
segments = pyglet.image.ImageGrid(snakeSeg_image, 3, 2).get_texture_sequence()
heads = pyglet.image.ImageGrid(snakeHead_image, 2, 2).get_texture_sequence()
tails = pyglet.image.ImageGrid(snakeTail_image, 2, 2).get_texture_sequence()

snake_segments = [segment for segment in segments]
snake_segments += [head for head in heads]
snake_segments += [tail for tail in tails]

for segment in snake_segments:
    centerAnchor(segment)
    

class World():

    def __init__(self, snake):
        self.snake = snake
        self.score = 0
        self.apple = self.findAppleXY()
        
    def draw(self):
        self.snake.draw()
        apple_image.blit(self.apple.x, self.apple.y)
        pyglet.text.Label(str(self.score), font_size=14, x= 30, y = 20).draw()
        
    def findAppleXY(self):
        newX = random.randrange(0, WINDOW_X, 20)
        newY = random.randrange(0, WINDOW_Y, 20)
        apple = Apple(newX, newY)
        if self.snake.detectCollision(apple):
            return self.findAppleXY()
        return apple
    
    def keyPress(self, symbol):
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
        if self.snake.onTick():
            self.snake = Snake(WINDOW_X // 2, 480 // 2, 5)
            self.apple = self.findAppleXY()
            self.score = 0
        if self.snake.collision(self.snake.head, self.apple):
            self.snake.length += int(self.snake.length * 0.3)
            self.apple = self.findAppleXY()
            self.score += self.snake.length
        

class Snake():
    image = snake_segments
    # image[0] - bend:top-right
    # image[1] - bend:top-left
    # image[2] - bend:bottom-right
    # image[3] - bend:bottom-left
    # image[4] - body: up-down
    # image[5] - body: left-right
    # image[6] - head: left
    # image[7] - head: down
    # image[8] - head: up
    # image[9] - head: right
    # image[10] - tail: left
    # image[11] - tail: down
    # image[12] - tail: right
    # image[13] - tail: up
    
    #directions:
        # "Up"
        # "Right"
        # "Down"
        # "Left"
    
    def __init__(self, x, y, length):
        self.direction = "Up"
        self.head = SnakeSegment(x, y, self.direction, self.image[8])
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
            newTail = self.image[13]
        elif lastDir == "Up":
            newTail = self.image[11]
        elif lastDir == "Right":
            newTail = self.image[10]
        else:
            newTail = self.image[12]
        curr.image = newTail
        curr.next = None
        
    def onTick(self):
        if self.direction == "Up":
            delta_x = 0
            delta_y = 20
            newImage = self.image[8]
        if self.direction == "Right":
            delta_x = 20
            delta_y = 0
            newImage = self.image[9]
            self.head.image = self.image[4]
        if self.direction == "Down":
            delta_x = 0
            delta_y = -20
            newImage = self.image[7]
            self.head.image = self.image[4]
        if self.direction == "Left":
            delta_x = -20
            delta_y = 0
            newImage = self.image[6]
            self.head.image = self.image[4]
            
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
        if oldDir == "Up":
            if newDir == "Right":
                return self.image[2]
            if newDir == "Left":
                return self.image[3]
            else:
                return self.image[4]
        if oldDir == "Down":
            if newDir == "Right":
                return self.image[0]
            if newDir == "Left":
                return self.image[1]
            else:
                return self.image[4]
        if oldDir == "Right":
            if newDir == "Up":
                return self.image[1]
            if newDir == "Down":
                return self.image[3]
            else:
                return self.image[5]
        if oldDir == "Left":
            if newDir == "Up":
                return self.image[0]
            if newDir == "Down":
                return self.image[2]
            else:
                return self.image[5]
        
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

class SnakeSegment():
    
    def __init__(self, x, y, direction, image):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = image
        self.next = None

    def draw(self):
        self.image.blit(self.x, self.y)
        
class Apple():

    def __init__(self, x, y):
        self.x = x
        self.y = y


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
