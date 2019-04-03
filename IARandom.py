from IA import *
import random


class IARandom(IA):

    def __init__(self,game,player):
        IA.__init__(self,game,player,"IA Random")

    def nextMove(self):
        choice = random.choice(self.getGame().getAvailableChoices())
        self.playMove(choice)

