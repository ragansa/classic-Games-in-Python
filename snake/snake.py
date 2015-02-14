import pyglet


snakeHead_image = pyglet.image.load('snake_heads.png')
snakeSeg_image = pyglet.image.load('snake_segs.png')
segments = pyglet.image.ImageGrid(snakeSeg_image, 3, 2).get_texture_sequence()
heads = pyglet.image.ImageGrid(snakeHead_image, 2, 2).get_texture_sequence()

snake_segments = [segment for segment in segments]
snake_segments += [head for head in heads]

for segment in snake_segments:
    segment.anchor_x = segment.width // 2
    segment.anchor_y = segment.height // 2
    
class World():

    def __init__(self, snake):
        self.snake = snake
        
    def draw():
        collision = self.snake.drawAndDetect()
        

class Snake():
    
    snake_segments = snake_segments
    # snake_segments[0] - bend:top-right
    # snake_segments[1] - bend:top-left
    # snake_segments[2] - bend:bottom-right
    # snake_segments[3] - bend:bottom-left
    # snake_segments[4] - body: up-down
    # snake_segments[5] - body: left-right
    # snake_segments[6] - head: left
    # snake_segments[7] - head: right
    # snake_segments[8] - head: up
    # snake_segments[9] - head: down
    
    def __init__(self):
        self.head = None
        
    def addSegment(self, segment):
        segment.next = self.head
        self.head = segment
        
    def drawAndDetect(self):
        current = self.head
        collision = False
        while current != None:
            current.draw()
            if collision(self.head, current):
                collision = True
            current = current.next
        return collision

class SnakeSegment():
    
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.next = None

    def draw():
        self.image.blit(x, y)

window = pyglet.window.Window(640, 480)
snake = Snake()

@window.event
def on_draw():
    window.clear()
    world.draw()

def update(delta_time):
    snake.draw()
    


pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
