import pyglet

# super simple "game" to test out using pyglet
window = pyglet.window.Window(640, 480)

MIN_LABEL_Y = 0
MAX_LABEL_Y = 480 - 14
COORDS_PER_SECOND = 200

label = pyglet.text.Label('Hello, world!', font_size=14, x=320   , y=MIN_LABEL_Y)

def change_dir():
    global COORDS_PER_SECOND
    COORDS_PER_SECOND *= -1

@window.event
def on_draw():
    window.clear()
    label.draw()

@window.event
def on_key_press(symbol, modifiers):
    global COORDS_PER_SECOND
    if symbol == pyglet.window.key.SPACE:
        change_dir()
    
ycoord = MIN_LABEL_Y

def update(dt):
    global ycoord
    global COORDS_PER_SECOND
    ycoord += COORDS_PER_SECOND * dt
    label.y = int(ycoord)
    if label.y > MAX_LABEL_Y or label.y < MIN_LABEL_Y:
        change_dir()
        


pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
