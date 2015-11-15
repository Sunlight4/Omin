import cocos, cocos.collision_model as cm
from objects import *
from vector import Vector
class GameLayer(cocos.layer.scrolling.ScrollableLayer):
    def __init__(self):
        super(GameLayer, self).__init__()
        self.bg = None
        self.updated=cocos.cocosnode.CocosNode()
        self.updated.name="updated"
        self.forces=set()
        self.add(self.updated)
        self.collider=cm.CollisionManager()
        
    def update(self, dt):
        updated=self.updated
        for force in self.forces:
            force.update({"updated":updated, "collider":self.collider})
        for o in updated.get_children():
            o.update({"updated":updated, "collider":self.collider})
    def load(self, path):
        pass
class Level(cocos.layer.scrolling.ScrollingManager):
    def __init__(self, *args):
        super(LevelScene, self).__init__(*args)

def distance(x1,y1,x2,y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))
def getangle(x1,y1,x2,y2):
    a = x2-x1
    b = y2-y1

    h = math.sqrt(a**2+b**2)

    theta = math.asin(b/float(h))

    return math.degrees(theta)



    
            
        
