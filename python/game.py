#%%
import random 
from collections import Counter

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = [i for i in range(11)]
        self.crowns = 0
        self.strategy = "random"

    def playcard(self):
        if self.strategy == "random":
            card = random.choice(self.cards)
        elif self.strategy == "human":
            card = self.getcardinput()
        return card 

    def getcardinput(self):
        card = -1
        while card not in self.cards:
            print("Choose a card! Your cards are: " + str(self.cards))
            card = int(input())
        else:
            return card
            
    def removehighestcard(self):
        if(self.cards[-1] != 0):
            self.cards.pop()

    def removecard(self, card):
        index = self.cards.index(card)
        if(self.cards[index] != 0):
            self.cards.pop(index)
        

    def addcrown(self):
        self.crowns += 1
    
    def changename(self, newname):
        self.name = newname

    def reset(self):
        self.cards = [i for i in range(11)]
        self.crowns = 0

class Game:
    def __init__(self):
        self.players = []
        self.crownstowin = 2
        self.round = 0
        self.verbose = True

    def addplayer(self, name, human = False):
        player = Player(name)
        if human:
            player.strategy = "human"
        self.players.append(player)

    def reset(self):
        self.round = 0

    def printroundresults(self, roundresults, playedcards):
        print("roundresults:\n")
        for i, p in enumerate(self.players):
            print(str(p.name) + " played: " + str(playedcards[i]) + " - crowns: " + str(self.players[i].crowns))
        print("\n")


    def updateplayers(self, roundresults, playedcards):
        for index, roundresult in enumerate(roundresults):
            if(roundresult == "win"):
                cards = playedcards[index] - 1 #remove cards - 1 for win
                self.players[index].crowns += 1 #add crown
                [self.players[index].removehighestcard() for i in range(cards)]
            elif(roundresult == "loss"):
                cards = playedcards[index] # remove all cards for loss
                [self.players[index].removehighestcard() for i in range(cards)]
            elif(roundresult == "tie"):
                playercard = playedcards[index] # remove 1 card for tie
                self.players[index].removecard(playedcard)



        if self.verbose: #print console output
            self.printroundresults(roundresults, playedcards)


    def checkwin(self):
        for player in self.players:
            if player.crowns >= self.crownstowin:
                return True
        return False  

    def startgame(self):
        self.reset()
        nplayers = len(self.players)
        if nplayers < 2:
            print("Not enough players.")
        elif nplayers == 2:
            self.crownstowin = 3
        else:
            self.crownstowin = 2
        print("Welcome to Henriekow! Good luck.")
        gameover = self.checkwin()
        while gameover == False:
            self.runround()
            gameover = self.checkwin()
        else:
            print(str(self.findwinner().name) + " wins the game!")
            return


    def runround(self):
        self.round += 1
        playedcards = []
        for player in self.players:
            playedcards.append(player.playcard()) # play cards
        roundresults = self.getroundresults(playedcards) # evaluate round
        self.updateplayers(roundresults, playedcards) # update player cards and crowns

    def getroundresults(self, playedcards):
        rr = ["loss"] * len(playedcards)
        highestcard = max(playedcards)
        occurence = Counter(playedcards)[highestcard]
        if occurence == 1:
            index = playedcards.index(highestcard)
            rr[index] = "win"
        else:
            for i in range(len(rr)):
                if(playedcards == highestcard):
                    rr[i] = "tie"
        return rr

    def findwinner(self):
        for player in self.players:
            if player.crowns >= self.crownstowin:
                return player

#%%
game = Game()
game.addplayer("Niklas")
game.addplayer("Peter")
game.addplayer("Franz")
game.addplayer("Nata")
game.addplayer("Henrieke")
game.addplayer("Klaus")
game.addplayer("Bea")
game.addplayer("Hubertus")
game.addplayer("YOU", "human")

#%%
game.startgame()


# %%

