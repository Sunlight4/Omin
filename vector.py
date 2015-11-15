import math
print "Init vectors"
class Vector(object):
    x=0
    y=0
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def _magnitude(self):
        return math.sqrt(self.x*self.x+self.y*self.y)
    magnitude=property(_magnitude)
    def angle(self, other):
        return math.acos(self.normalize()*other.normalize())
    def __mul__(self, other):
        try:return self.x*other.x+self.y*other.y
        except:
            return Vector(self.x*other, self.y*other)
    def normalize(self):
        if self.magnitude==0:return Vector(0,0)
        return Vector(self.x/self.magnitude, self.y/self.magnitude)
    def truncate(self,maximum):
        if self.magnitude>maximum:
            return self.normalize()*maximum
        else:
            return Vector(self.x, self.y)
    def __str__(self):
        return "<%s, %s>" %(self.x, self.y)
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
    def __truediv__(self, other):
        return Vector(float(self.x)/float(other), float(self.y)/float(other))
    def __div__(self, other):
        return Vector(float(self.x)/float(other), float(self.y)/float(other))
    def __neg__(self):
        return Vector(-self.x, -self.y)
    def distSquare(self, other):
        return (self.x-other.x)*(self.x-other.x)+(self.y-other.y)*(self.y-other.y)
    def __str__(self):
        return "<"+str(self.x)+","+str(self.y)+">"
    def dist(self, other):
        return math.sqrt((self.x-other.x)*(self.x-other.x)+(self.y-other.y)*(self.y-other.y))
    def _direction(self):
        return math.atan2(float(self.y),float(self.x))
    direction=property(_direction)