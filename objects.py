import cocos, math, os, random
from vector import Vector
autoscrolling=1
class Atomic(cocos.sprite.Sprite):
    def __init__(self, x, y, image):
        super(Atomic, self).__init__(image, (x, y))
    def remove(self):
        self.kill()
    def moveto(self, x, y):
        self.position=(x, y)
    def render(self):
        pass
    def update(self, args):
        pass
    def _cshape(self):
        left=int(self.position[0]-(self.width/2.0))
        top=int(self.position[1]-(self.height/2.0))
        return cocos.collision_model.AARectShape((left, top), (self.width/2.0), (self.height/2.0))
class Object(Atomic): # Base class
    props={"x":"int", "y":"int", "image":"image", "mass":"int", "fixed":"bool"}
    defs={"x":0, "y":0, "image":"Wall.png", "mass":50, "fixed":False}
    grounded=None
    def __init__(self, x=0, y=0, image="Wall.png", mass=50, fixed=False, *args):
        "Create an object with specified x, y, image, and mass. Calculate rect and mask for later, and make pos and velocity vectors"
        super(Object, self).__init__(x, y, image, *args)
        self.forces=[]
        self.fixed=fixed
        self.velocity=Vector(0,0)
        self.pos=Vector(x+(self.rect.width/2.0), y+(self.rect.height/2.0))
        self.mass=mass
        self.path=image
    def update(self, args):           
        "Check our forces, and change velocity accordingly, then change our position"
        super(Object, self).update(args)
        self.grounded=None
        if not self.fixed:
            total_force=Vector(0,0)
            for f in self.forces:total_force+=f
            vel_change=total_force/float(self.mass)
            self.velocity+=vel_change
            self.pos+=self.velocity
        self.forces=[]
        self.moveto(self.pos.x, self.pos.y)
    def addforce(self, v):
        self.forces.append(v)
    def _rect(self):
        return self.get_rect()
    rect=property(_rect)
    def _x(self):return self.pos.x
    def _y(self):return self.pos.y
    x=property(_x)
    y=property(_y)

    
    
class Wall(Object):
    props={"bouncy":"int", "x":"int", "y":"int", "image":"image", "mass":"int", "fixed":"bool", "friction":"int"}
    defs={"x":0, "y":0, "image":"Wall.png", "mass":0, "fixed":True, "bouncy":1, "friction":0.5}
    def __init__(self, x, y, image, bouncy=1, friction=0.5, **kw):
        "Create a wall with specified bounciness, rotated by the given amount of degrees"
        self.bouncy=bouncy
        self.friction=friction
        super(Wall, self).__init__(x, y, image, **kw)
    def update(self, args):
        "Handle wall-object collisions: use our normal function, then move the object out of us, then do bounciness pushback"
        #TODO:Bounciness
        super(Object, self).update(args)
        sprites=args["collider"].objs_colliding(self)
        if sprites==None:return
        for spr in sprites:
            if isinstance(spr, Wall):continue
            
            spr.addforce((-spr.velocity)*self.friction)
            #get normal force
            angle=math.degrees((spr.pos-self.pos).direction)
            normal=self.normal((angle) % 360)
            a=(-normal).angle(spr.velocity)
            mN = math.cos(a) * spr.velocity.magnitude * self.bouncy * spr.mass
            spr.addforce(normal*mN)
            
            opos=spr.pos
            
            #enforce non-penetration constant
            while pygame.sprite.collide_rect(self, spr):
                spr.pos+=normal
                
                
                spr.moveto(spr.pos.x, spr.pos.y)
            
            spr.grounded=self
            #TODO:fix this
        

    def normal(self, angle):
        "Default normal function: simply return up vector"
        return Vector(0, -1)

class CircleWall(Wall):
    "Special class for circle walls. Simply changes the normal function to pushback based on the exact angle"
    def normal(self, angle):
        a=math.radians(angle) 
        
        return Vector(math.cos(a), math.sin(a))
class SquareWall(CircleWall):
    "Special class for square walls. Rounds angle, then passes it to the circle normal function."
    def normal(self, angle):
        a=angle
        if a<45:
            a=0
        elif 45<=a<=135:
            a=90
        elif 135<=a<=225:
            a=180
        elif 225<=a<=315:
            a=270
        else:
            a=0
        return super(SquareWall, self).normal(a)
class RightTriangleWall(CircleWall):
    def normal(self, angle):
        a=(angle+90)%360
        if a<135:a=45
        if 135<=a<=225:
            a=180
        if 225<=a<=315:
            a=270
        else:
            a=45
        return super(RightTriangleWall, self).normal(a)
class Gravity(object):
    props={"strength":"Vector"}
    defs={"strength":Vector(0, -1)}
    def __init__(self, strength=Vector(0,-1)):
        super(Gravity, self).__init__()
        self.strength=strength
    def update(self, args):
        for spr in args["updated"].get_children():
            spr.addforce(self.strength*spr.mass)
        
        
