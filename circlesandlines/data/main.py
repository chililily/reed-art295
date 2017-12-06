from room import Room, TriggerableRoom, LockedRoom, index
from player import Player
from item import Item
from monster import Monster, Special
from npc import *
from glossary_items import *
from battle import battle
import os
import updater
import random

player = Player()

def createWorld():
    """Rooms"""
    pondRoom = Room("You are in a circular room. There is a large mirror on the northern wall, and in the center is a raised platform with a strange pond. An exit to the south, adorned on top with an inscription, leads to a flight of stairs going up.")
    fork = Room("You are in a small room connected to two corridors. There's also a flight of stairs leading down.")
    Room.connectRooms(pondRoom, "up", fork, "down")
    #Quarters
    quarters = Room("You are in a corridor with a door on each side and one at the northern end.")
    quart_a = LockedRoom("It's just a large, empty room.", "It's locked.", rustykey, "You insert the key and turn. It takes a little fiddling around, but you eventually hear it click.", None, "Or, well, it would be if it weren't for that suspicious orb of light hovering around. Strange.")
    quart_b = Room("You are in someone's private quarters. It's quite large, but there isn't a lot of practical furniture. It's mostly filled with a bunch of trinkets and other oddities organized very neatly.")
    quart_c = TriggerableRoom("You are in someone's private quarters.", "Immediately, you notice that there's a tray of food on a table, and you realize that it's been a couple hours since you last ate. The food doesn't look spoiled for some reason. Maybe...?", "eat food", "You tentatively nibble at one of the bread rolls. It's cold, but it tastes pretty good. You gulp it down and wait a few seconds. When nothing happens, you tear into the rest of the roll./After a few minutes, you feel like you've eaten enough and rummage around for a bag so you can take the rest of the food with you. You find a pretty sizable one and stuff the food in after wrapping napkins around everything.", food)
    Room.connectRooms(quarters, "north", quart_a, "south")
    Room.connectRooms(quarters, "left", quart_b, "east")
    Room.connectRooms(quarters, "right", quart_c, "west")
    Room.connectRooms(fork, "north", quarters, "south")
    #Balcony
    southbalcony = Room("You are on a balcony overlooking what seems to be a fairly large hall. The balcony snakes along the southern wall, with doors on west and east sides leading north. The eastern door looks like it leads to more balcony.")
    eastbalcony = Room("You are on a balcony that lines the eastern wall of a large hall. There is a pair of sturdy doors halfway along the wall. At the northern end, the path turns east, and at the southern end is a door.")
    northbalcony = Room("You are on a balcony. On the lower level, there's a large hall to the west; the balcony itself overlooks a narrower hallway. Along its wall are three doors decorated with elaborate markings, each sporting a different design than the others. To the east is a staircase; to the west, the path turns a corner to the south.")
    Room.connectRooms(southbalcony, "east", eastbalcony, "south")
    Room.connectRooms(eastbalcony, "north", northbalcony, "south")
    Room.connectRooms(fork, "east", southbalcony, "west")
    #Storage
    storage1 = Room("The door is surprisingly heavy, but you manage to pull it open. You're disappointed to see a simple storage room. There is a stack of blank parchment and new inkwells sitting neatly on a table to your left and a line of closets opposite the door.")
    storage3 = Room("You are in a small storage room. There are several scorch marks on the walls and floor. It looks like someone tried to cover them up, but they weren't very thorough.")
    Room.connectRooms(northbalcony, "to first door", storage1, "north")
    Room.connectRooms(northbalcony, "to third door", storage3, "north")
    #Library
    lib_main = Room("You are in the library, a vast room with a high ceiling and countless shelves full of books.", None, "library")
    lib_a = Room("You are in the library, a vast room with a high ceiling and countless shelves full of books.")
    lib_b = Room("You are in the library, a vast room with a high ceiling and countless shelves full of books.")
    lib_c = Room("You are in the library, a vast room with a high ceiling and countless shelves full of books.")
    lib_d = Room("You are in the library, a vast room with a high ceiling and countless shelves full of books.")
    lib_e = Room("You are in the library, a vast room with a high ceiling and countless shelves full of books.")
    lib_f = Room("You are in the library, a vast room with a high ceiling and countless shelves full of books.")
    lib_g = Room("You are in the library, a vast room with a high ceiling and countless shelves full of books.")
    lib_h = Room("You are in the library, a vast room with a high ceiling and countless shelves full of books.")
    lib_i = Room("You are in the library, a vast room with a high ceiling and countless shelves full of books.")
    Room.connectRooms(lib_b, "west", lib_main, "east")
    Room.connectRooms(lib_b, "north", lib_a, "south")
    Room.connectRooms(lib_a, "east", lib_d, "west")
    Room.connectRooms(lib_d, "south", lib_e, "north")
    Room.connectRooms(lib_d, "east", lib_g, "west")
    Room.connectRooms(lib_e, "west", lib_b, "east")
    Room.connectRooms(lib_e, "south", lib_f, "north")
    Room.connectRooms(lib_e, "east", lib_h, "west")
    Room.connectRooms(lib_f, "west", lib_c, "east")
    Room.connectRooms(lib_c, "north", lib_b, "south")
    Room.connectRooms(lib_f, "east", lib_i, "west")
    Room.connectRooms(lib_i, "north", lib_h, "south")
    Room.connectRooms(lib_h, "north", lib_g, "south")
    Room.connectRooms(eastbalcony, "east", lib_main, "west")
    corridor = Room("You are in a corridor. There's a large pair of doors to the north and a staircase going up to the south. There's a dead end to the west, but the corridor opens up to the east.")
    thr = Room("You are in the throne room. At the far end is a dilapidated chair. On each side, there's a narrow corridor that leads downstairs.", None, "throne room")
    koroom = Room("You are in a circular room filled with concentric snaking waterways surrounding an island. A narrow walkway extends from the entrance to the island, where there appears to be someone sitting idly.", None, "ko's room")
    island = Room("You approach the island, stopping just before the two pillars in front.", "Now that you've moved closer, you can see that the island is covered in intricate engravings that extend onto the surrounding pillars./As your gaze returns to the center of the island, you notice that the cloaked figure sitting there is staring at you. You're a little surprised to see faint markings on their arms similar to the ones on the island.", "island")
    Room.connectRooms(northbalcony, "down", corridor, "up")
    Room.connectRooms(corridor, "north", thr, "south")
    Room.connectRooms(thr, "down", koroom, "up")
    Room.connectRooms(koroom, "to island", island, "back")
    ctyd = Room("You are in the courtyard. There's a quaint-looking gazebo in the center.", None, "courtyard")
    gazebo = Room("You walk up to the gazebo.It has north and south entrances, and a bench runs along its six sides.", None, "gazebo")
    bird = Room("You are on a small, open platform. Columns surround its perimeter and support an overhead dome. In the center stands a solitary basin. It looks a little like a birdbath.", "You walk to the edge of the platform and cautiously rest your hand against a nearby column. Gazing out from here, you realize that the castle stands atop a mountain that overlooks a vast swathe of land. The sheerness of it all overwhelms you - but at the same time, you can't seem to shake the feeling that something's off./And then it hits you./There's no sign of life anywhere.")
    Room.connectRooms(ctyd, "west", bird, "east")
    Room.connectRooms(ctyd, "to gazebo", gazebo, "to courtyard")
    """Items"""
    storage1.addItem(inkwell)
    storage1.addItem(parchment)
    fork.addItem(rustykey)
    """NPCs"""
    pond.place(pondRoom)
    pond.addOptions([("Dip your finger in.", "Remembering the pond in the woods, you peered more closely at the empty one in front of you. You warily reach out a finger to touch it.../...and nothing happens. It feels nice, though. You stir your finger around in it a bit, watching your reflection twist and distort."), ("Leave it alone.", "You leave the pond alone.")])
    mirror.place(pondRoom)
    inscription.place(pondRoom)
    closet.place(storage1)
    closet.addItem(animalplush)
    suspiciousorb.placeHidden(quart_a)
    Ko.place(island)
    throne.place(thr)
    throne.addItem(pinkcrystal)
    redpotion.putInRoom(storage3)
    """Monsters"""
    dustbunny = Monster("dust bunny", quart_b, 8, 3, 1, 0, 1, 8, 0.4)
    slime = Monster("slime", fork, 10, 5, 2, 0, 3, 10, 0.75)
    slime.addDrop(slimyboots)
    redslime = Monster("red slime", fork, 16, 11, 1, 0, 1, 17, 0.36, True, 10)
    redslime.addDrop(slimyboots)
    blueslime = Monster("blue slime", fork, 16, 0, 1, 11, 1, 0.36, True, 10)
    blueslime.addDrop(slimyboots)
    ichormoth = Monster("ichor moth", ctyd, 23, 4, 15, 2, 20, 19, 0.44)
    suspiciousorbmon = Special("suspicious orb", quart_a, 20, 0, 3, 10, 5, 20, False, None, True) #sounds like a digimon...
    spectre = Monster("spectre", lib_g, 40, 0, 5, 10, 12, 40, 0,32)
    minichimaera = Monster("miniature chimaera", storage3, 26, 14, 5, 0, 9, 26, .1)
    minichimaera.addDrop(crimsonscale)
    player.location = pondRoom

def clear():
    os.system('clear')

def initialize(): #initial scenario
    clear()
    print("\"Uhhh...\"")
    print()
    print("You groan as you come to, grimacing at every tiny movement of your aching body. As you struggle to sit upright, you realize that you had been lying sprawled on top of some steps. You stare blankly at the marble steps for a few moments, still somewhat disoriented.")
    print()
    print("Steps...?")
    print()
    print("Your eyes trace the stairs up to find that it leads rather disappointingly to what looks like a simple flat platform. You climb to the top anyway, and soon find yourself peering into a pond. Or, well, it would be a pond if it weren't carved out of stone and empty, except for the water. Not very exciting.")
    input()
    clear()
    print("You look up from the pseudo-pond to find that you're in some weird circular room. The only entrance lies to your right. There seems to be some kind of inscription on top, but you can't tell what it says from where you are.")
    print()
    print("To the left is a gigantic mirror. Peering at your small silhouette framed against the rest of this odd room, it suddenly hits you that you have absolutely no idea what is going on.")
    print()
    print("What is this place? Where is everyone? Why are you here?")
    print()
    print("Come to think of it, weren't you just messing around on a Saturday morning a minute ago?")
    input()
    clear()
    print("You had been walking around in the park nearby and had gone off the trail and into the woods for fun. Mostly it was just leaves and branches and spiders everywhere, but...")
    print()
    print("There had been a clearing. Just a little circular spot in the woods - almost TOO circular, actually - and there had been a pond in the center with a fish in it. Only one fish, actually. You had thought it must be pretty lonely, swimming around in that little pond with nothing else around. You remember wanting to reach out and touch it...")
    input()
    clear()
    print("\"I don't remember actually touching it, though...\"")
    print()
    print("You shivered. You had spoken out loud out of habit, and the sound hung strangely in the silence.")
    print()
    print("Sighing, you stand up and stretch a bit. It looks like you aren't getting back to someplace familiar any time soon, so you might as well explore. You should probably feel more panicked, but at this moment curiousity seems to trump panic. And this place has a sort of tranquil beauty to it, too - wherever it is.")
    print()
    input("Press enter to continue...")

def printSituation():
    clear()
    print(player.location.desc)
    print()
    player.location.initDesc()
    player.location.addNewDesc()
    if player.location.hasMonsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m.name)
        print()
    if player.location.hasItems():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()
    print("You can go in the following directions:")
    for e in player.location.exitNames():
        print(e)
    print()

def showHelp():
    clear()
    print("'go <direction>' -- moves you in the given direction")
    print("'go to <room>' -- moves you to the given room if it's adjacent to your current location")
    print("'go back' -- moves you to the adjacent room if your current location only has one exit")
    print("'leave' -- moves you to the adjacent room if the current room only has one exit")
    print("'back' or 'main' -- returns to the main screen")
    print("'inspect <target>' -- describes <target> or launches interaction with <target>")
    print("'talk to <NPC>' -- intitiates conversation with <NPC>")
    print("'[i]nventory' -- opens your inventory")
    print("'pickup' or 'take <item>' -- picks up the item")
    print("'drop <item>' -- drops the item")
    print("'use <item>' -- uses the item")
    print("'attack <monster>' -- initiates battle with <monster>")
    print("'quit' or 'exit' -- quits the game")
    print()
    input("Press enter to continue...")
createWorld()
playing = True
player.turns = 0
while playing and player.alive:
    if player.turns == 0:
        initialize()
    printSituation()
    commandSuccess = False
    timePasses = False
    while not commandSuccess:
        commandSuccess = True
        command = input("What now? ")
        commandWords = command.split()
        if isinstance(player.location, TriggerableRoom) and commandWords[0].lower() == player.location.trigger[0]: #can't handle non-verbatim commands
            for i in range(len(commandWords)):
                if commandWords[i].lower() != player.location.trigger[i]:
                    print("Not a valid command.")
                    commandSuccess = False
            if commandSuccess:
                player.location.triggerEvent(player)
        if not commandWords or (commandWords[0].lower() == "do" and commandWords[1].lower() == "nothing"):
            player.turns += 1
            print("You do nothing. At least whistle a song or something.")
            print()
            commandSuccess = False
        elif commandWords[0].lower() == "wait":
            turns += 1
            print("You wait.")
            print()
            commandSuccess = False
        elif commandWords[0].lower() == "go":
            if len(commandWords) > 1:
                if commandWords[1].lower() == "to":
                    destName = command[6:].lower()
                    destDir = command[3:].lower()
                    for room in player.location.adj:
                        if destName == room.name:
                            player.goDirection(direction)
                            timePasses = True
                        elif destDir in player.location.exitNames():
                            dest = player.location.getDestination(destDir)
                            if isinstance(dest, LockedRoom) and dest.locked:
                                print(dest.lockedDesc)
                                commandSuccess = False
                            else:
                                player.goDirection(destDir)
                                timePasses = True
                elif commandWords[1].lower() in player.location.exitNames():
                    dest = player.location.getDestination(commandWords[1].lower())
                    if isinstance(dest, LockedRoom) and dest.locked:
                            print(dest.lockedDesc)
                            commandSuccess = False
                    else:
                        if not journal in player.items:
                            clear()
                            print("As you turn to go down the steps, something on the ground catches your eye. You walk over to what appears to be a small journal and pick it up, turning it around a few times. You can tell it's seen a lot of use, but it's still in remarkably good condition. You flip through it, only to find it full of blank pages. Strange.")
                            print()
                            print("Well, might as well take it with you.")
                            print()
                            player.items.append(journal)
                            input()
                        player.goDirection(commandWords[1]) 
                    timePasses = True
                elif commandWords[1].lower() == "back": #if current room has one exit, moves through exit
                    if len(player.location.exits) == 1 and turns != 0:
                        player.goDirection(player.location.exitNames()[0])
                        timePasses = True
                if not timePasses:
                        print("Nothing like that is nearby.")
                        commandSuccess = False
            else:
                print("Go where?")
                commandSuccess = False
        elif commandWords[0].lower() == "me":
            player.showProfile()
        elif commandWords[0].lower() == "inspect": #checks 1. inventory/equips, 2. location, 3. for NPCs since interactive objects are classified as NPCs
            targetName = command[8:]
            found = False
            target = player.getItemByName(targetName)
            if target != False:
                target.describe()
                found = True
                commandSuccess = False
            else:
                target = player.location.getItemByName(targetName)
                if target != False:
                    target.describe()
                    commandSuccess = False
                else:
                    target = player.location.getNPCbyName(targetName)
                    if target != False:
                        target.interact()
                        timePasses = True
                    else:
                        print("There isn't anything like that around.")
                        commandSuccess = False
        elif commandWords[0].lower() == "pickup":
            targetName = command[7:]
            target = player.location.getItemByName(targetName)
            if target != False:
                player.pickup(target)
            else:
                print("No such item.")
                commandSuccess = False
        elif commandWords[0].lower() == "take":
            targetName = command[5:]
            target = player.location.getItemByName(targetName)
            if target != False:
                player.pickup(target)
            else:
                print("No such item.")
                commandSuccess = False
        elif commandWords[0].lower() == "drop":
                targetName = command[5:]
                found = False
                for i in player.items:
                    if i.name == targetName:
                        player.drop(target, player.location)
                        print("Dropped " + str(targetName) + ".")
                        found = True
                for i in list(player.equips.values()):
                    if i:
                        if i.name == targetName:
                            found = True
                            print("You need to unequip it first.")
                            commandSuccess = False
                if not found:
                    print("You're not carrying that.")
                    commandSuccess = False
        elif commandWords[0].lower() == "inventory" or commandWords[0].lower() == "i":
            player.showItems()
            commandSuccess = False
        elif commandWords[0].lower() == "use": #this is gonna get real hairy
            targetName = command[4:]
            found = False
            for i in player.items:
                if i.name == targetName and isinstance(i, useable):
                    if isinstance(i, Key):
                        for room in player.location.adj:
                            if isinstance(room, LockedRoom) and i == room.key:
                                room.unlock(player)
                                timePasses = True
                    else:
                        i.use()
                        player.items.remove(i)
                        print("Used " + str(targetName) + ".")
                    found = True
            if not found:
                print("You're not carrying that.")
                commandSuccess = False
        elif commandWords[0].lower() == "equip":
            targetName = command[6:]
            player.equipItem(targetName)
            player.showItems()
            commandSuccess = False
        elif commandWords[0].lower() == "unequip":
            targetName = command[8:]
            player.unequipItem(targetName)
            player.showItems()
            commandSuccess = False
        elif commandWords[0].lower() == "help":
            showHelp()
        elif commandWords[0].lower() == "back" or commandWords[0].lower() == "main":
            printSituation()
            commandSuccess = False
        elif commandWords[0].lower() == "quit" or commandWords[0].lower() == "exit":
            playing = False
        elif commandWords[0].lower() == "attack": #initiates battle with target
            targetName = command[7:]
            target = player.location.getMonsterByName(targetName)
            if target != False:
                battle(player, target, None)
                player.exp += target.exp
                if player.helper: player.helper.exp += target.exp
                target.drop()
                timePasses = True
            else:
                print("No such monster.")
                commandSuccess = False
        elif commandWords[0].lower() == "talk":
            targetName = command[8:] #assumes there's a preposition "to"
            target = player.location.getNPCbyName(targetName)
            if target != False:
                if isinstance(target, Helper):
                    target.interact(player)
                else:
                    target.init()
        elif commandWords[0].lower() == "whistle": #for whimsy
            success = random.randint(1, 10)
            if success > 3:
                if "song" in commandWords:
                    print()
                    print("You whistle a pretty tune. If only there were birds around to sing along...")
                    print()
                    commandSuccess = False
                else:
                    print()
                    print("You whistle. It sounds a bit harsh in the silence.")
                    print()
                    commandSuccess = False
            else:
                print()
                print("You try to whistle and fail miserably. At least no one else was around to hear that...right?")
                print()
                commandSuccess = False
        else:
            print("Not a valid command.")
            commandSuccess = False
    if timePasses == True:
        player.turns += 1
        updater.updateAll(player.turns)
    if player.turns == 1000: #time-sensitive; game over scenario
        clear()
        print("You take a step forward, only to find the ground crumble beneath your feet. Your heart leaps as you feel yourself falling forward into nothing...")
        input()
        clear()
        print("...only to be wrenched violently backwards and slam into solid floor.")
        print()
        print("Dazed and in pain, you barely focus your eyes in time to register the massive form racing towards you. You whirl onto your side to roll to safety, but soon find yourself in free fall again.")
        print()
        input()
        clear()
        print("The entirety of this collapsing world seems to unravel in front of you as its myriad fragments fill your vision. Some of them are familiar, but most are foreign to you: places never visited, people never encountered, things never touched.")
        print()
        print("Looking at it all, you're suddenly reminded of your own world.")
        input()
        clear()
        print("Your chest constricts at the thought and a surge of regret envelops your being. If you hadn't been so willy-nilly...")
        input()
        print("If you had been better, faster, more decisive...")
        input()
        print("If you hadn't even come here in the first place...")
        input()
        print('"What if?"')
        input()
        print("And then there was nothing.")
        playing = False #

