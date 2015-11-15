import cocos, pyglet, this
from cocos.director import director
from objects import *
from vector import Vector
from utils import *
kinds={"Object":Object, "Wall":Wall, "SquareWall":SquareWall, "CircleWall":CircleWall}
inputtool=raw_input
def tool_donothing(x, y):pass
def make_tool_basiccreate(kind, image):
    def tool_create(x, y):
        new=kind(x//24*24, y//24*24, image)
        world.updated.add(new)
        world.collider.add(new)
    return tool_create
class EditorLayer(GameLayer):
    is_event_handler = True
    focus=[320,240]
    updating=0
    def __init__(self, *args):
        super(EditorLayer, self).__init__(*args)
        self.tool=tool_donothing
        
        
    def on_key_press(self, key, modifiers):
        if key==pyglet.window.key.LEFT:
            self.focus[0]-=10
        elif key==pyglet.window.key.RIGHT:
            self.focus[0]+=10
        elif key==pyglet.window.key.UP:
            self.focus[1]-=10
        elif key==pyglet.window.key.DOWN:
            self.focus[1]+=10
        elif key==pyglet.window.key.G:
            self.forces.add(Gravity())
        elif key==pyglet.window.key.SPACE:
            if not self.updating:
                self.updating=1
                self.schedule(self.update)
            else:
                self.unschedule(self.update)
                self.updating=0
        elif key==pyglet.window.key.C:
            kind=kinds[inputtool("What kind of object? ")]
            image=pyglet.image.load(inputtool("Image Path? "))
            self.tool=make_tool_basiccreate(kind, image)
        mainlayer.force_focus(*self.focus)
    def on_mouse_press(self, x, y, buttons, modifiers):
        if pyglet.window.mouse.LEFT == buttons:
            pos=mainlayer.pixel_from_screen(x, y)
            self.tool(*pos)
    def update(self, *args):
        if not self.updating:return
        super(EditorLayer, self).update(*args)
director.init()
mainlayer=cocos.layer.scrolling.ScrollingManager()
world=EditorLayer()
mainlayer.add(world)
scene=cocos.scene.Scene(mainlayer)
cocos.director.director.run(scene)

