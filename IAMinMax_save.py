from IA import *
import random
from pprint import pprint


class IAMinMax(IA):

    def __init__(self,game,player):
        IA.__init__(self,game,player,"IA MinMax")

    def nextMove(self):
        max = -100000
        coupMax = 0
        value = 0
        profondeur = 1

        #Parcours de l'ensemble des coups possibles
        for move in self.getGame().getAvailableChoices():
            gameCopy = self.getGame().copyBoard()
            print()
            print('Test du coup : ', move)
            gameCopy.playMove(move,self.getPlayerType())

            if gameCopy.getCurrentTurnPlayer() != self.getPlayerType():
                value = self.min(gameCopy,profondeur)
            else:
                value = self.max(gameCopy, profondeur)
            print('Fin du test. valeur : ',value)
            print()
            if value > max or (value == max and random.randint(0,9) >= 8):
                max = value
                coupMax = move


        #print('coup max = ', coupMax)
        #On joue le coup le mieux côté
        self.playMove(coupMax)



    #Fonction récursive min de l'algorithme minmax
    def min(self,game,profondeur):
        if profondeur == 0 or game.isOver():
            return self.eval(game)

        value = 0
        min = 100000
        max = -100000

        for move in game.getAvailableChoices():
            gameCopy = game.copyBoard()
            gameCopy.playMove(move, gameCopy.getCurrentTurnPlayer())

            if gameCopy.getCurrentTurnPlayer() != self.getPlayerType():  # L'ia va rejouer, on cherche donc le max
                value = self.min(gameCopy, profondeur - 1)
                if value > max or (value == max and random.randint(0, 9) >= 8):
                    max = value
            else:
                value = self.max(gameCopy,profondeur-1)
                if value < min or (value == min and random.randint(0,9) >= 8):
                    min = value
        return max if self.getGame().getCurrentTurnPlayer() != self.getPlayerType() else min





    #Fonction récursive max de l'algorithme minmax
    def max(self,game,profondeur):
        if profondeur == 0 or game.isOver():
            return self.eval(game)

        value = 0
        max = -100000
        min = 100000

        for move in game.getAvailableChoices():
            gameCopy = game.copyBoard()
            gameCopy.playMove(move, gameCopy.getCurrentTurnPlayer())

            if gameCopy.getCurrentTurnPlayer() == self.getPlayerType(): # L'ia va rejouer, on cherche donc le max
                value = self.max(gameCopy, profondeur - 1)
                if value < min or (value == min and random.randint(0, 9) >= 8):
                    min = value
            else:
                value = self.min(gameCopy,profondeur-1)
                if value > max or (value == max and random.randint(0,9) >= 8):
                    max = value
        return max if self.getGame().getCurrentTurnPlayer() == self.getPlayerType() else min


    #Fonction heuristique de l'algorithme minmax
    def eval(self,game):
        if game.isOver():
            if game.getWinner() == self.getPlayerType():
                return 1000 - game.getOtherScore(self.getPlayerType()) # On gagne la partie, grosse valeur
            else:
                return - 1000 + game.getScore(self.getPlayerType()) # On perd la partie, on doit avoir le + de carrés possibles

        return int(game.getScore(self.getPlayerType()) - game.getOtherScore(self.getPlayerType()))