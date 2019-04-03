import pygame
import math
import random
from pygame.locals import *
from constants import *
from Box import *
from GameMenu import *
from IARandom import *
from IAMinMax import *
from pprint import pprint
import copy

class Game(object):
    def otherInit(self,args):
        self.isOnePlayer = args['isOnePlayer']
        self.__player1 = args['player1']
        self.__player2 = args['player2']
        self.n = args['n']
        self.__isHumanTurn = args['isHumanTurn']
        self.__playAgain = args['playAgain']
        self.__scoreOne = args['scoreOne']
        self.__scoreTwo = args['scoreTwo']
        self.__availableLines = copy.deepcopy(args['availableLines'])
        self.__plateau = [[Box(i,j,self) for i in range(self.n)] for j in range(self.n)]

        #Copie du plateau de jeu
        for x,row in enumerate(self.__plateau):
            for y,box in enumerate(row):
                box.setFilledBy(args['plateau'][x][y].getOwner())
                box.top.setPlayer(args['plateau'][x][y].top.getPlayer())
                box.right.setPlayer(args['plateau'][x][y].right.getPlayer())
                box.bottom.setPlayer(args['plateau'][x][y].bottom.getPlayer())
                box.left.setPlayer(args['plateau'][x][y].left.getPlayer())


    def __init__(self,otherInitArgs = False):
        if otherInitArgs != False:
            self.isOnePlayer = None
            self.__player1 = None
            self.__player2 = None
            self.n = None
            self.__isHumanTurn = None
            self.__playAgain = None
            self.__scoreOne = None
            self.__scoreTwo = None
            self.__availableLines = None
            self.__plateau = None
            self.otherInit(otherInitArgs)
        else:
            # Pygame inits
            pygame.init()

            #Menu 1
            screen = pygame.display.set_mode((LARGEUR+LARGEUR_INFOS, LARGEUR))
            menu_items = ("3x3 - Press a", "5x5 - Press z", "7x7 - Press e", "9x9 - Press r")
            pygame.display.set_caption("4AIT - Jeu du carré")
            gm = GameMenu(screen, menu_items)
            n=gm.menu1()

            # Menu 2
            screen = pygame.display.set_mode((LARGEUR+LARGEUR_INFOS, LARGEUR))
            menu_items = ("1 player - Press a", "IA vs IA - Press z")
            pygame.display.set_caption("4AIT - Jeu du carré")
            gm = GameMenu(screen, menu_items)
            self.isOnePlayer = gm.menu2()
            self.__player1 = self.definePlayer1()
            self.__player2 = self.definePlayer2()

            self.n = n
            self.boxSize = LARGEUR / n
            self.__plateau = [[Box(i,j,self) for i in range(n)] for j in range(n)]

            # les lignes disponibles sont représentées par un tableau a 3 dimensions [x][y]['horizontal ou vertical'] = True
            self.__availableLines = [[{'horizontal': True,'vertical':True} for i in range(n+1)] for j in range(n+1)]
            #On supprime les lignes qui n'xistent pas (bord droit - lignes horizontales et bas - lignes verticales)
            del(self.__availableLines[n][n])
            for i in range(n):
                del(self.__availableLines[i][n]['vertical'])
                del(self.__availableLines[n][i]['horizontal'])

            self.__linecolor = LINECOLOR
            self.__paintedColor = Color("white")
            self.__lineHoverColor = HOVERCOLOR
            self.__lineWidth = LINEWIDTH
            self.__lineHovered = False
            self.__isHumanTurn = True
            self.__playAgain = False
            self.__scoreOne = 0
            self.__scoreTwo = 0


            self.fenetre = pygame.display.set_mode((LARGEUR+(MARGE*(n+1))+self.__lineWidth+400, LARGEUR+(MARGE*(n+1))+self.__lineWidth))
            pygame.display.set_caption("4AIT - Jeu du carré")
            self.drawInfos()


    def definePlayer1(self):
        if self.isOnePlayer:
            return Player.HUMAN
        else:
            #return IARandom(self,Player.HUMAN)
            return self.defineIA(Player.HUMAN,"Define player 1")

    def definePlayer2(self):
        #return IARandom(self,Player.COMPUTER)
        return self.defineIA(Player.COMPUTER,"Define player 2")


    def defineIA(self,player,choose_text):
        screen = pygame.display.set_mode((LARGEUR + LARGEUR_INFOS, LARGEUR))
        menu_items = (choose_text,"IA Random - Press a", "IA MinMax - Press z")
        pygame.display.set_caption("4AIT - Jeu du carré")
        gm = GameMenu(screen, menu_items)
        return gm.menu3(self,player)


    def drawInfos(self):
        # same thing here
        myfont64 = pygame.font.SysFont("comicsansms", 64)
        myfont20 = pygame.font.SysFont("comicsansms", 20)

        scoreme = myfont64.render(str(self.__scoreOne), 1, (255, 255, 255))
        scoreother = myfont64.render(str(self.__scoreTwo), 1, (255, 255, 255))
        scoretextme = myfont20.render("You" if self.isOnePlayer else self.__player1.getName(), 1, (255, 255, 255))
        scoretextother = myfont20.render(self.__player2.getName(), 1, (255, 255, 255))

        self.fenetre.fill(Color('black'))
        self.fenetre.blit(scoretextme, (LARGEUR + LARGEUR_INFOS/2, 10))
        self.fenetre.blit(scoreme, (LARGEUR + LARGEUR_INFOS/2, 30))
        self.fenetre.blit(scoretextother, (LARGEUR + LARGEUR_INFOS/2, LARGEUR/2))
        self.fenetre.blit(scoreother, (LARGEUR + LARGEUR_INFOS/2, LARGEUR/2+20))

    def incrementScore(self,player):
        if player == Player.HUMAN:
            self.__scoreOne += 1
        else:
            self.__scoreTwo += 1

    def canPlayAgain(self):
        return self.__playAgain

    def setPlayAgain(self,val):
        self.__playAgain = val

    def isHumanTurn(self):
        return self.__isHumanTurn

    def getPlateau(self):
        return self.__plateau

    def getBox(self,x,y):
        box = False
        try:
            if y>=0 and x>=0:
                box = self.__plateau[y][x]
        except:
            pass
        return box

    def getAvailableLines(self):
        return self.__availableLines



    def noLongerAvailableLine(self,x,y,isHorizontal):
        if isHorizontal:
            del(self.__availableLines[x][y]['horizontal'])
        else:
            del(self.__availableLines[x][y]['vertical'])


    #Return true si toutes les box sont remplies
    def isOver(self):
        for row in self.getPlateau():
            for box in row:
                if not box.isFilled():
                    return False
        return True




    def drawBoard(self):
        for index,row in enumerate(self.getPlateau()):
            for indexBox,box in enumerate(row):
                #On peint les lignes
                #Affiche la ligne du haut du carré
                pygame.draw.line(self.fenetre,self.__paintedColor if box.top.isPainted() else (self.__lineHoverColor if box.top.isHovered() else self.__linecolor),(box.x*self.boxSize + MARGE*self.n,box.y*self.boxSize + MARGE*self.n),(box.x*self.boxSize + self.boxSize,box.y*self.boxSize + MARGE*self.n),self.__lineWidth)
                #Affiche la ligne de gauche du carré
                pygame.draw.line(self.fenetre,self.__paintedColor if box.left.isPainted() else (self.__lineHoverColor if box.left.isHovered() else self.__linecolor),(2+box.x*self.boxSize + MARGE*self.n,box.y*self.boxSize + MARGE*self.n),(2+box.x*self.boxSize + MARGE*self.n,box.y*self.boxSize + self.boxSize),self.__lineWidth)
                #Affiche la ligne du bas du carré, seulement pour la dernière row
                if index == self.n-1:
                    pygame.draw.line(self.fenetre, self.__paintedColor if box.bottom.isPainted() else (self.__lineHoverColor if box.bottom.isHovered() else self.__linecolor),(box.x * self.boxSize, box.y*self.boxSize + self.boxSize),(box.x*self.boxSize + self.boxSize, box.y * self.boxSize + self.boxSize),self.__lineWidth)
                # Affiche la ligne de droite du carré, seulement pour la dernière colonne
                if indexBox == self.n - 1:
                    pygame.draw.line(self.fenetre,self.__paintedColor if box.right.isPainted() else (self.__lineHoverColor if box.right.isHovered() else self.__linecolor),(box.x*self.boxSize + self.boxSize, box.y*self.boxSize + MARGE*self.n),(box.x*self.boxSize + self.boxSize, box.y*self.boxSize + self.boxSize),self.__lineWidth)

                if box.isFilled():
                    #On peint le carré rempli
                    rect = pygame.Rect(box.x*self.boxSize+LINEWIDTH, box.y*self.boxSize+LINEWIDTH, self.boxSize-LINEWIDTH, self.boxSize-LINEWIDTH)
                    pygame.draw.rect(self.fenetre, PLAYER_COLOR if box.getOwner() == Player.HUMAN else COMPUTER_COLOR, rect)







    #Permet de peindre le doublon de la ligne
    def paintDoubleLine(self,line,player):
        #Il n'existe pas de doublon pour les lignes du bas et de droite car normalement
        # les seules lignes droite et bas qu'on peint sont celles des carrés sur les bords

        if line.getPosition() == Position.TOP: #On doit peindre la ligne du bas du carré du dessus
            if line.getBox().hasTopBox(): #On n'est pas sur la première ligne, donc il existe un carré au dessus
                line.getBox().getTopBox().bottom.setPaintedBy(player,True)

        elif line.getPosition() == Position.LEFT: #On doit peindre la ligne de droite du carré de gauche
            if line.getBox().hasLeftBox():  # On n'est pas sur la première colonne, donc il existe un carré à gauche
                line.getBox().getLeftBox().right.setPaintedBy(player,True)




    def paintHoveredLine(self):
        #On peint la ligne survolée et le doublon
        self.__lineHovered.setPaintedBy(Player.HUMAN,False)
        self.paintDoubleLine(self.__lineHovered,Player.HUMAN)

        #On libère la ligne courante de la grille
        self.__lineHovered.setHover(False)
        self.__lineHovered = False


    #fonction debug pour voir quelles sont les lignes peintes
    def paintedLines(self):
        for row in self.getPlateau():
            for box in row:
                if box.top.isPainted():
                    print(box,"top")
                if box.bottom.isPainted():
                    print(box,"bottom")
                if box.right.isPainted():
                    print(box,"right")
                if box.left.isPainted():
                    print(box,"left")


    def play(self):
        continuer = True
        while not self.isOver() and continuer:
            # Limitation de vitesse de la boucle
            pygame.time.Clock().tick(60)
            self.drawInfos()
            self.drawBoard()
            # Rafraichissement
            pygame.display.flip()

            if(self.isOnePlayer): #Humain contre IA
                if self.isHumanTurn():
                    self.humanTurn()
                else:
                    self.computerTurn(self.__player2)

            else: #IA contre IA
                if self.isHumanTurn():
                    self.computerTurn(self.__player1)
                else:
                    self.computerTurn(self.__player2)

            self.setPlayAgain(False)
        if(self.isOver()):
            quit = False
            while(not quit):
                self.drawInfos()
                self.drawBoard()
                self.drawEnd()
                # Rafraichissement
                pygame.display.flip()
                for event in pygame.event.get():
                    # Si l'utilisateur quitte ou appuie sur échap on sort du programme
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        quit = True
                        break


    #Affiche la fin de jeu
    def drawEnd(self):
        textGameOver = ""
        if self.isOnePlayer:
            textGameOver = "You won" if self.__scoreOne > self.__scoreTwo else "You lose"
        else:
            textGameOver = self.__player1.getName()+" won" if self.__scoreOne > self.__scoreTwo else self.__player2.getName()+" won"
        colorGameOver = Color('green') if self.__scoreOne > self.__scoreTwo else Color('red')
        if self.__scoreOne == self.__scoreTwo:
            colorGameOver = Color('gray')
        end = pygame.font.SysFont("comicsansms", 64).render("Game over", 1, colorGameOver)
        result = pygame.font.SysFont("comicsansms", 48).render(textGameOver, 1, colorGameOver)
        self.fenetre.blit(end, (LARGEUR + LARGEUR_INFOS / 4, LARGEUR/3*2))
        self.fenetre.blit(result, (LARGEUR + LARGEUR_INFOS / 4, LARGEUR / 5 * 4))


    #l'IA joue son coup
    def computerTurn(self,ia):
        pygame.time.wait(100)
        pygame.event.clear(MOUSEBUTTONUP)#Pour éviter que l'utilisateur ne rajoute un event dans la queue pendant que c'est à l'IA de jouer
        ia.nextMove()
        if not self.canPlayAgain():
            self.changeTurn() #au tour de l'autre joueur


    #Au tour de l'humain, gère le hover de la souris et le clic
    def humanTurn(self):
        for event in pygame.event.get():
            # Si l'utilisateur quitte ou appuie sur échap on sort du programme
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                continuer = False
                break
            elif event.type == KEYDOWN and event.key == K_SPACE:
                pprint(self.getAvailableChoices())
            elif event.type == MOUSEMOTION:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                xpos = int(math.ceil((mouseX - (self.boxSize / 2)) / self.boxSize))
                ypos = int(math.ceil((mouseY - (self.boxSize / 2)) / self.boxSize))
                is_horizontal = abs(mouseY - ypos * self.boxSize) < abs(mouseX - xpos * self.boxSize)
                ypos = ypos - 1 if mouseY - ypos * self.boxSize < 0 and not is_horizontal else ypos
                xpos = xpos - 1 if mouseX - xpos * self.boxSize < 0 and is_horizontal else xpos

                # xpos et ypos représentent les coordonnées du carré qu'on pointe et horizontal si on pointe le haut ou la gauche

                if xpos < self.n and ypos < self.n:  # On est pas aux bords de la grille
                    box = self.getBox(xpos, ypos)
                    if self.__lineHovered != False:
                        self.__lineHovered.setHover(False)
                    if box != False:
                        self.__lineHovered = box.top if is_horizontal else box.left
                        self.__lineHovered.setHover(True)
                else:  # on est au bord de la grille, soit en bas soit à droite
                    if (ypos >= self.n):
                        ypos -= 1
                    if (xpos >= self.n):
                        xpos -= 1
                    box = self.getBox(xpos, ypos)
                    if self.__lineHovered != False:
                        self.__lineHovered.setHover(False)
                    if box != False:
                        self.__lineHovered = box.bottom if is_horizontal else box.right
                        self.__lineHovered.setHover(True)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1 and self.__lineHovered != False and not self.__lineHovered.isPainted():
                    self.paintHoveredLine()  # peint la ligne survolée et son doublon
                    if not self.canPlayAgain():
                        self.__isHumanTurn = False #On passe le tour à l'ordinateur si on n'a pas marqué de point





    #Peint la ligne correspondant aux coordonnées et à l'orientation, ainsi que ses doublons.
    def paintLineAndDouble(self,x,y,isHorizontal,player):
        if x < self.n and y < self.n:  # On est pas aux bords de la grille
            box = self.getBox(x, y)
            line = box.top if isHorizontal else box.left
        else: # on est au bord de la grille, soit en bas soit à droite
            y = y - 1 if (y >= self.n) else y
            x = x - 1 if (x >= self.n) else x
            box = self.getBox(x, y)
            line = box.bottom if isHorizontal else box.right

        #On a trouvé la ligne, on la peint et son doublon aussi
        line.setPaintedBy(player,False)
        self.paintDoubleLine(line, player)


    #Renvoie la liste de coups possibles pour la partie actuelle
    def getAvailableChoices(self):
        choices = []
        for x,row in enumerate(self.getAvailableLines()):
            for y,box in enumerate(row):
                for position in box:
                    choices.append([x,y,position])
        return choices

    # a supprimer : Fonction debug, pour afficher les lignes dispos
    def printAvailableLines(self):
        for x,row in enumerate(self.getAvailableLines()):
            for y,box in enumerate(row):
                for position in box:
                    print("Position : ", position, " x : ",x, "y : ",y)


    #Joue le coup passé en paramètre pour le joueur donné, est appelé seulement par les IA pour simuler les possibilités
    #Le paramètre real permet de différencier le vrai coup joué des coups simulés sur les faux plateaux
    def playMove(self,move,player,real=False):
        playerstats = "HUMAN" if player == Player.HUMAN else "COMPUTER"
        if move[2] == "horizontal":
            move[2] = True
        elif move[2] == "vertical":
            move[2] = False
        self.paintLineAndDouble(move[0], move[1], move[2], player)

        #Pour les simulations : on change le tour des joueurs manuellement vu que normalement c'est fait dans la fonction play
        if not real:
            if not self.canPlayAgain():
                self.changeTurn()
            self.__playAgain = False



    #Retourne le gagnant si la partie est terminée, sinon False
    def getWinner(self):
        if not self.isOver():
            return False
        return Player.HUMAN if self.__scoreOne > self.__scoreTwo else Player.COMPUTER

    #Retourne le score du joueur passé en paramètre
    def getScore(self,player):
        return self.__scoreOne if player == Player.HUMAN else self.__scoreTwo

    #Retourne le score de l'adversaire du joueur passé en paramètre
    def getOtherScore(self,player):
        return self.__scoreTwo if player == Player.HUMAN else self.__scoreOne


    def getCurrentTurnPlayer(self):
        return Player.HUMAN if self.__isHumanTurn else Player.COMPUTER

    def changeTurn(self):
        self.__isHumanTurn = not self.__isHumanTurn


    def copyBoard(self):
        otherInitArgs = {
            'isOnePlayer':self.isOnePlayer,
            'player1':self.__player1,
            'player2':self.__player2,
            'n':self.n,
            'isHumanTurn':self.isHumanTurn(),
            'playAgain':self.__playAgain,
            'scoreOne':self.__scoreOne,
            'scoreTwo':self.__scoreTwo,
            'availableLines':self.__availableLines,
            'plateau':self.__plateau,
                         }
        return Game(otherInitArgs)