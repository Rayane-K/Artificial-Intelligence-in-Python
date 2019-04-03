from Line import *

class Box:
    def __init__(self,x,y,board):
        self.top = Line(self,Position.TOP)
        self.right = Line(self,Position.RIGHT)
        self.bottom = Line(self,Position.BOTTOM)
        self.left = Line(self,Position.LEFT)
        self.x = x
        self.y = y
        self.__owner = Player.NONE
        self.__board = board

    def isFilled(self):
        return self.top.isPainted() and self.right.isPainted() and self.bottom.isPainted() and self.left.isPainted()

    def setFilledBy(self,player):
        self.__owner = player

    def tryToFillBy(self,player):
        if self.isFilled() and self.getOwner() == Player.NONE:
            #Le joueur vient de remplir un carré
            self.setFilledBy(player)
            self.getBoard().setPlayAgain(True)
            self.getBoard().incrementScore(player)

    def getOwner(self):
        return self.__owner

    def getBoard(self):
        return self.__board

    def hasTopBox(self):
        if self.getBoard().getBox(self.x,self.y-1) != False:
            return True
        return False

    def hasLeftBox(self):
        if self.getBoard().getBox(self.x-1,self.y) != False:
            return True
        return False

    def getTopBox(self):
        return self.getBoard().getBox(self.x,self.y-1)

    def getLeftBox(self):
        return self.getBoard().getBox(self.x-1,self.y)

    def __repr__(self):
        return "Box({}, {})".format(self.x,self.y)
