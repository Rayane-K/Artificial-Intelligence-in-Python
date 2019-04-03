from Line import Player

class IA(object):
    def __init__(self,game,player,name):
        self.__game = game
        self.__player = player
        self.__name = name

    def getGame(self):
        return self.__game

    def getName(self):
        return self.__name

    def getPlayerType(self):
        return self.__player

    def getOtherPlayerType(self):
        return Player.HUMAN if self.__player == Player.COMPUTER else Player.COMPUTER

    def nextMove(self):
        return NotImplemented("Pas encore implémentée ! c'est une classe mère")

    def playMove(self,move):
        self.getGame().playMove(move,self.getPlayerType(),True)