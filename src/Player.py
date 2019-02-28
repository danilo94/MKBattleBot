class Player(object):
    id=0
    position=0
    distance=0
    life = 0
    lado = 0
    debug = None
    timeAlive = 0

    def __init__(self,id,debug=False):
        self.id=id
        self.position=0
        self.distance=0
        self.life=0
        self.timeAlive=0
        self.lado = 0
        self.debug = debug


    def isDead(self):
        if(self.life>0):
            return False
        else:
            return True


    def updateLado(self,lado):
        self.lado = lado

    def updateposition(self,position):
        self.position=position

    def updateDistance(self,distance):
        self.distance=distance


    def updateLife(self,life):
        self.life=life


    def updateTimeAlive(self,alive):
        self.timeAlive = alive


    def getDistance(self):
        return self.distance

    def getPosition(self):
        return self.position

    def getLife(self):
        return self.life

    def getLado(self):
        return self.lado


    def updateData(self,dist,pos,life,timeAlive,lado):
        self.updateLife(life)
        self.updateDistance(dist)
        self.updateposition(pos)
        self.updateTimeAlive(timeAlive)
        self.updateLado(lado)
        if (self.debug==True):
            print("Player ID: ",self.id)
            print("Distancia: ",self.getDistance())
            print("Vida: ",self.getLife())
            print("Posicao: ",self.getPosition())