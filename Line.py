
class Player:
    HUMAN = 1
    COMPUTER = 2
    NONE = 3

class Position:
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4

#Représente une ligne d'un carré, un carré possède 4 lignes.
class Line:
    def __init__(self,box,position):
        self.__player = Player.NONE
        self.__hovered = False
        self.__box = box
        self.__position = position

    def isHorizontal(self):
        return self.getPosition() == Position.TOP or self.getPosition() == Position.BOTTOM

    def getPlayer(self):
        return self.__player

    def setPaintedBy(self,player,isDoublon):
        self.__player = player
        self.getBox().tryToFillBy(player)

        #Si c'est pas un doublon, on enlève de la liste des lignes dispos cette ligne
        if not isDoublon:
            x = self.getBox().x + 1 if self.getPosition() == Position.RIGHT else self.getBox().x
            y = self.getBox().y + 1 if self.getPosition() == Position.BOTTOM else self.getBox().y
            self.getBox().getBoard().noLongerAvailableLine(x,y,self.isHorizontal())

    def isPainted(self) -> object:
        return self.__player != Player.NONE

    def isHovered(self):
        return self.__hovered

    def setHover(self,hover):
        self.__hovered=hover

    def getPosition(self):
        return self.__position

    def getBox(self):
        return self.__box

    #Fonction en plus pour faciliter la copie du jeu
    def setPlayer(self,player):
        self.__player = player