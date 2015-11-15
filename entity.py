import collections,pygame,vector
import objects,utils,move_repo
from move_repo import Jump, Walk
from vector import Vector
class AI(object):
    goals=[]
    def update_obj(self,e, args):
        pass
class DoNothingAI(AI):
    def update_obj(self, e, args):
        pass
class GeoJumperAI(AI):
    def update_obj(self, e, args):
        for event in args["events"]:
            if event.type==pygame.MOUSEBUTTONDOWN:
                move_repo.Jump.run(e)
class PlayerAI(AI):
    selected_move=0
    def update_obj(self, e, args):
        ngoals=[]
        for i in self.goals:
            i.update_obj(e, args)
            if not i.satisfied:ngoals.append(i)
        self.goals=ngoals
        for event in args["events"]:
            if event.type==pygame.MOUSEBUTTONDOWN:
                x, y=pygame.mouse.get_pos()
                if self.selected_move==0:
                    self.goals.append(MoveGoal(Vector(x, y)))
class MoveGoal(object):
    def __init__(self, target):
        self.target=target
    def update_obj(self, e, args):
        pass
    def satisfied(self, e):
        return (e.pos-self.target).magnitude<5
ai_dict={"basic/nothing":DoNothingAI, "test/geojumper":GeoJumperAI, "basic/playerai":PlayerAI}
class Entity(objects.Object):
    skills=collections.defaultdict(int)
    hp=0
    moves=[]
    energy=0
    ai=DoNothingAI
    def ondeath(self):return 1
    def __init__(self, x, y, who=""):
        f=file(who+".txt", "r")
        setup=f.read().split(',')
        for command in setup:
            key=command.split(':')
            if key[0]=="HP":
                self.hp=int(key[1])
            if key[0]=="IMG":
                image="res/sprites/"+key[1]+".png"
            if key[0]=="AI":
                self.ai=ai_dict[key[1]]()
            if key[0]=="MOVE":
                self.moves.append(move_repo.move_dict[key[1]])
        super(Entity, self).__init__(x=x, y=y, image=image)
    def update(self, args):
        self.energy+=1
        if self.hp==0:
            if self.ondeath():
                self.kill()
        self.ai.update_obj(self, args)
        super(Entity, self).update(args)
