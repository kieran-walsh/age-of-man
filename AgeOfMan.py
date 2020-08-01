# AGE OF MAN: A TEXT ADVENTURE
# Created by Kieran Walsh (kawalsh)
# 15-110 Section O

#Citations:
#sys.exit(0) - found on  Stack Overflow - https://stackoverflow.com/questions/2823472/is-there-a-method-that-tells-my-program-to-quit
#clearScreen() - found on Stack Overflow - https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
#getTermSize() - found on Reddit - https://www.reddit.com/r/Python/comments/5q7b36/getting_terminal_size_in_python/
#time.sleep() - found on JournalDev - https://www.journaldev.com/15797/python-time-sleep

import os
import shutil
import math
import time
import sys

## Boot-Game Functions
def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')
    
def getTermSize():
    try:
        (width, height) = shutil.get_terminal_size()
    except: (width, height) = (80, 24)
    return (width, height)

def bootGame():
    clearScreen()
    width, height = getTermSize()
    print(("*"*width + "\n")*2)
    print(" "*(math.ceil(width/2)-14) + "AGE OF MAN: A TEXT ADVENTURE\n")
    print(("*"*width + "\n")*2)
    
    while True:
        response = input("Enter '(s)tart' to start the game, '(i)nst' to see instructions, '(c)redits' to see credits, '(e)xit' to exit" + "\n"*2 + ">")
        response = response.lower()
        print()
        if response == "start" or response == "s":
            clearScreen()
            startGame()
            break
        elif response == "inst" or response == "i":
            print("Instructions:")
            print('''You progress in the game by typing in commands for movement and actions. 
For example:''')
            print('''If you type 'north', you'll move to a northern part of the map. If you type
'take', you'll take an item if it's in the same location.''')
            print('''Any time you see a command with parentheses around it (ex. (s)tart), that means 
that you can perform the same command by typing either the whole command or only what's in the 
parentheses.''')
        elif response == "credits" or response == "c":
            print("Credits:")
            print("Fall 2018 15-110 Term Project (Section O)")
            print("Designed and Written by Kieran Walsh (kawalsh)")
            print("Title inspired by the song 'Age Of Man' by rock band Greta Van Fleet")
        elif response == "exit" or response == "e":
            print("Thank you for playing! Carpe Diem. :-)\n")
            break
        else:
            print ("'"+response+"'", "is not a valid instruction!")
        print()
        
## Miscellaneous
descriptionDict = {'branch':'Can be used to build fire or as a weapon'}
availCommands = set()
objectives = {0:"Collect two branches and something to use as tinder", 1:"Take the branches and tinder back to the cave",
              2: "Find some animals and hunt for food", 3: "Travel back to the cave to cook the meat by the fire",
              4: "Go and find more food to give to the nomads", 5:"Take the food back to the nomads"}
        
## Items
class Item(object):
    pass

rock = Item()
rock.name = "rock"

dryGrass = Item()
dryGrass.name = "pile of dry grass"

branch = Item()
branch.name = "branch"

spear = Item()
spear.name = "spear"

meat = Item()
meat.name = "meat"

nuts = Item()
nuts.name = "nut tree"

## Areas
class Area(object):
    pass
    
Cave = Area()
Cave.message = '''***CAVE***\nIt's dark in the cave, and the only thing you can see is the light coming from 
the entrance to the north.'''
Cave.shortMessage = '''***CAVE***\nThe only thing you can see is the light coming from the entrace to the north.'''
Cave.possibleCommands = set(["north"])
Cave.items = [branch]

Overlook = Area()
Overlook.message = '''***OVERLOOK***\nYou are on the hill overlooking the land. There are plains to the west, 
a forest to the east, and a river to the north.'''
Overlook.shortMessage = '''***OVERLOOK***\nYou are on the hill overlooking the land.'''
Overlook.possibleCommands = set(["north", "south", "east", "west"])
Overlook.items = []

Plains = Area()
Plains.message = "***PLAINS***\nA wide-open area of flat land. There's more fertile ground north of here."
Plains.shortMessage = '''***PLAINS***\nA wide-open area of flat land.'''
Plains.possibleCommands = set(["north", "east"])
Plains.items = []

Forest = Area()
Forest.message = "***FOREST***\nThe forest is full of tall, green trees. There's flatland to the north."
Forest.shortMessage = '''***FOREST***\nThe forest is full of tall, green trees.'''
Forest.possibleCommands = set(["north", "west"])
Forest.items = [branch]

FertileGround = Area()
FertileGround.message = '''***FERTILE GROUND***\nThe soil here is fertile. There are trees, bushes, and other plants here.
There's a river to the east.'''
FertileGround.shortMessage = '''***FERTILE GROUND***\nThere are trees, bushes, and other plants here.'''
FertileGround.possibleCommands = set(["south", "east"])
FertileGround.items = []

RiverBank = Area()
RiverBank.message = '''***RIVER BANK***\nYou're at the edge of a fairly small, shallow river. You think you
see animals to the north, on the other side. There's fertile ground to the west, and flatland to the east. '''
RiverBank.shortMessage = '''***RIVER BANK***\nYou're at the edge of a fairly small, shallow river.'''
RiverBank.possibleCommands = set(["north", "south", "east", "west"])
RiverBank.items = []

Flatland = Area()
Flatland.message = '''***FLATLAND***\nAnother open space with the river to the west. Nothing more than grass 
and a few rocks. There's a forest south of here.'''
Flatland.shortMessage = '''***FLATLAND***\nAnother open space. Nothing more than grass and a few rocks.'''
Flatland.possibleCommands = set(["south", "west"])
Flatland.items = [dryGrass]

BeyondRiver = Area()
BeyondRiver.message = '''***BEYOND RIVER***\nYou're in an area of plant life and animals roaming around. The
river is to the south.'''
BeyondRiver.shortMessage = '''***BEYOND RIVER***\nYou're in an area of plant life and animals roaming around.'''
BeyondRiver.possibleCommands = set(["south"])
BeyondRiver.items = []


gameMap = [[ None,  Plains,    FertileGround,  None],
            [ Cave,  Overlook,  RiverBank,      BeyondRiver],
            [ None,  Forest,     Flatland,       None]]

## Player
class Player(object):
    pass

player = Player()
player.location = [1, 0]
player.inventory = []
player.currentObjective = 0
player.visitedAreas = []
player.recentMoves = []
player.woke = False

########################################

def reflection():
    print("***Wait a minute***")
    print("As you're crossing the river to get back to the cave, you look down.")
    print("You notice your reflection in the water. It's the first time you have ever seen yourself.")
    time.sleep(7.00)
    print()
    print("You are in complete awe. You drop to your knees.")
    print("You realize that you're actually a living being.")
    time.sleep(7.00)
    print()
    print("You are experiencing feelings you have never known before.")
    print("You want to symbolize this idea, but you are not sure how.")
    time.sleep(7.00)
    print()
    print("All of a sudden, you feel compelled to make some kind of sound.\n")
    time.sleep(4.00)
    while True:
        speakResponse = input("Speak? ((y)es/(n)o)\n" + ">").lower()
        if speakResponse == "y" or speakResponse == "yes":
            break
        elif speakResponse == "n" or speakResponse == "no":
            print("\nYou are unsure at first, but you find the courage within yourself.")
            break
        else: print("\nNot a valid response. Please choose one of the options.\n")
    
    time.sleep(2.00)    
    print("\n...\n")
    time.sleep(2.00)
    print('''You gesture toward yourself and say "na". It is how you will refer 
to yourself from now on.''')
    time.sleep(5.00)
    print("Such a simple sound, with such profound meaning.\n")
    time.sleep(5.00)
    player.woke = True

def displayInventory():
    print("Inventory:")
    if len(player.inventory) == 0:
        print("Your inventory is currently empty.")
    for item in player.inventory:
        print(item.name[0].upper() + item.name[1:], end=" ")
        print()
    print()
    return

def displayHelp():
    print("Type '(inv)entory' to show your current inventory.")
    print("Type '(obj)ective' to show your current objective.")
    print("Type 'area' to learn about your current location again.")
    print("Type 'clear' to clear the screen.\n")
    print("**Possible commands for this area are:", availCommands, "")
    print("Type 'north', 'south', 'east', or 'west' to move around.")
    print("Type 'take' to take an item, if an item is there.")
    print("Type 'back' to reverse your most recent move.\n")
    return
    
## Objectives
def checkObjectives():
    #Objective: (if you go back to cave)
    if (player.currentObjective == 0 and player.inventory.count(branch) == 2 and 
                                         player.inventory.count(dryGrass) == 1):
        player.currentObjective += 1
        if (player.location == [1, 0]): checkObjectives()
        else: getObjective()
    
    #Objective: (if you build fire)
    elif (player.currentObjective == 1) and player.location == [1, 0]:
        while True:
            fireResponse = input("You have all the items to build a fire. Attempt to build it? ((y)es/(n)o)\n" + ">").lower()
            if fireResponse == "y" or fireResponse == "yes":
                print("\n***Fire successfully built!***")
                Cave.message = '''***CAVE***\nThe cave is now lit by the fire. You see strange symbols and figures on the 
walls, drawn with dirt.'''
                Cave.shortMessage = '''***CAVE***\nThe cave is now lit by the fire.'''
                print(Cave.message[10:])
                print()
                time.sleep(3.00)
                print("It looks like there may have been other nomads here recently. There are remnants from a previous fire,")
                print("and there's a spear lying here.\n")
                time.sleep(3.00)
                player.inventory = []
                Cave.items.append(spear)
                player.currentObjective += 1
                getObjective()
                break
            elif fireResponse ==  "n" or fireResponse == "no":
                print()
                break
            else:
                print("\nNot a valid response! Please choose one of the options.\n")        
    
    #Objective: (if you find animals)
    elif (player.currentObjective == 2) and (player.location == [1, 3]):
        while True:
            attackResponse = input("You see animals here. Attack? ((y)es/(n)o)\n" + ">").lower()
            if attackResponse == "y" or attackResponse == "yes":
                print("\nIt was a tough battle to fight on your own, but you manage to kill the beast.")
                print("You are feeling grateful to be alive.")
                print("You salvage all of the meat that you can and take it with you.\n")
                time.sleep(5.00)
                player.inventory.append(meat)
                player.currentObjective += 1
                getObjective()
                break
            elif attackResponse ==  "n" or attackResponse == "no":
                print()
                break
            else: print("\nNot a valid response! Please choose one of the options.\n")
        
    #Objective: (if you make it back to the cave)
    elif (player.currentObjective == 3 and player.location == [1, 0]):
        print('''When you make it back to the cave, you are not alone.
There is a group of nomads in the cave, and they are curious what you are doing in what seems to be "their cave."
To them, you are an enemy, and they are ready to fight.\n''')
        time.sleep(3.00)
        print("You remember that you are carrying meat with you.\n")
        while True:
            shareResponse = input("Give the meat to the nomads as a peace offering? ((y)es/(n)o)\n" + ">").lower()
            if shareResponse == "y" or shareResponse == "yes":
                print("\nThe nomads take the meat, but it is not enough for them to trust you.")
                print("In exchange for their trust, they want you to gather and bring them a plant food as well.\n ")
                time.sleep(4.00)
                FertileGround.items.append(nuts)
                player.inventory.remove(meat)
                player.currentObjective += 1
                getObjective()
                break
            elif shareResponse ==  "n" or shareResponse == "no":
                print("\nThe nomads do not waste time; they kill you.\n")
                time.sleep(2.00)
                width, height = getTermSize()
                print(("*"*width + "\n")*2)
                print(" "*(math.ceil(width/2)-7) + "YOU DIED\n")
                print(("*"*width + "\n")*2)
                time.sleep(3.00)
                print("Thanks for playing! Better luck next time. :-)\n")
                sys.exit(0)
                #break
            else: print("\nNot a valid response! Please choose one of the options.\n")
    
    #Objective: (if you take the nuts)
    elif (player.currentObjective == 4 and player.inventory.count(nuts) == 1):
        player.currentObjective += 1
        if (player.location == [1, 0]): checkObjectives()
        else: getObjective()
     
    #Objective: (if you make it back to the cave with the nuts)
    elif (player.currentObjective == 5 and player.location == [1, 0]):
        print("The nomads appreciate your gift of food and decide that you are trustworthy.")
        print("They welcome you into the cave. You are now one of them.\n")
        time.sleep(5.00)
        width, height = getTermSize()
        print(("*"*width + "\n")*2)
        print(" "*(math.ceil(width/2)-4) + "THE END!\n")
        print(("*"*width + "\n")*2)
        time.sleep(5.00)
        sys.exit(0)    
 
########################################    

def getArea(fullMessage=False):
    area = gameMap[player.location[0]][player.location[1]]
    global availCommands
    availCommands = area.possibleCommands
    
    if fullMessage == True:
        print(area.message)
    elif area in player.visitedAreas:
        print(area.shortMessage)
    else: 
        print(area.message)
        player.visitedAreas.append(area)
    if len(area.items) != 0:
        print("\nThere is a", area.items[0].name, "here.\n")
        availCommands.add("take")
    else: print()

def takeItem():
    area = gameMap[player.location[0]][player.location[1]]
    if len(area.items) != 0:
        if (area.items[0] == nuts): nuts.name = "nuts"
        print("You took the " + area.items[0].name + ".\n")
        player.inventory.append(area.items[0])
        gameMap[player.location[0]][player.location[1]].items.pop()
    else:
        print("There is no item to take!\n")
        
def goBack():
    if len(player.recentMoves) > 0:
        if player.recentMoves[-1] == "north":
            specificCommands("south", new=False)
        elif player.recentMoves[-1] == "south":
            specificCommands("north", new=False)
        elif player.recentMoves[-1] == "east":
            specificCommands("west", new=False)
        elif player.recentMoves[-1] == "west":
            specificCommands("east", new=False)
        player.recentMoves.pop()
    else: print("There are no moves to reverse!\n")

    
    
def specificCommands(response, new=True):
    if response in availCommands:
        if response == "north":
            if player.location == [1, 2] and spear not in player.inventory:
                print('''Being that you don't have any weapons, you 
decide that crossing the river is not a good idea right now.\n''')
                return
            else:
                player.location[1] += 1
        elif response == "south":
            if (player.currentObjective == 3) and (player.location == [1, 3] and player.woke == False):
                reflection()
            player.location[1] -= 1
        elif response == "east":
            player.location[0] += 1
        elif response == "west":
            player.location[0] -= 1
        if new == True: player.recentMoves.append(response)
        getArea()
        checkObjectives()
        
    elif (response not in availCommands) and (response == "north" or
            response == "south" or response == "west" or response == "east"):
        print("You can't go any further", response + ".\n")
    else: print("'" +response+"'", "is not a valid command!\n")
    
def checkCommands(response):
    if response == "inventory" or response == "inv":
        displayInventory()
    elif response == "back": goBack()
    elif response.startswith("take"):
        takeItem()
        checkObjectives()
    elif response == "help": displayHelp()
    elif response == "area": getArea(fullMessage=True)
    elif response == "clear": clearScreen()
    elif response == "exit": return
    elif response == "obj" or response == "objective":
        print("OBJECTIVE:", objectives[player.currentObjective], "\n")
    elif response == "f": print("Respects paid.\n")
    else: specificCommands(response)

def getInput():
    while True:
        response = input("Enter a command (or 'help' for some helpful commands): \n" + ">").lower()
        print()
        checkCommands(response)
        if response == "exit": break
        
def getObjective():
    print("NEW OBJECTIVE:", objectives[player.currentObjective])
    print()

def startGame():
    print("AGE OF MAN: A TEXT ADVENTURE")
    print()
    print("""   It's the crack of dawn. You wake up alone in a cave, cold and unable to
        see much. If only there was a way to solve this problem.""" + "\n")
    getObjective()
    getArea()
    getInput()

if __name__ == '__main__':
    bootGame()