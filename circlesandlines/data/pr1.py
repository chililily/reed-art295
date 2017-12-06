import random
import math
import pr1testing
random.seed()


def roll(): #function that rolls 1 6-sided die, returning an integer between 0 and 5
    return random.randint(0,5)

def play():
    player1 = input("Name of Player 1?")
    player2 = input("Name of Player 2?")
    score1 = 0
    score2 = 0
    last = False
    while True:
        print()
        print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2))
        print('It is', player1 + "'s turn.")
        numDice = int(input("How many dice do you want to roll?"))
        diceTotal = 0
        diceString = ""
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            diceString = diceString + " "  + str(d)
            i = i-1
        print("Dice rolled: ", diceString)
        print("Total for this turn: ", str(diceTotal))
        score1 += diceTotal
        if score1 > 100 or last:
            break
        if numDice == 0:
            last = True
        print()
        print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2))
        print('It is', player2 + "'s turn.")
        numDice = int(input("How many dice do you want to roll?"))
        diceTotal = 0
        diceString = ""
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            diceString = diceString + " "  + str(d)
            i = i-1
        print("Dice rolled: ", diceString)
        print("Total for this turn: ", str(diceTotal))
        score2 += diceTotal
        if score2 > 100 or last:
            break
        if numDice == 0:
            last = True
    print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2))
    if score1 > 100:
        print(player2 + " wins.")
        return 2
    elif score2 > 100:
        print(player1 + " wins.")
        return 1
    elif score1 > score2:
        print(player1 + " wins.")
        return 1
    elif score2 > score1:
        print(player2 + " wins.")
        return 2
    else:
        print("Tie.")
        return 3

def autoplayLoud(strat1, strat2):
    player1 = "Player 1"
    player2 = "Player 2"
    score1 = 0
    score2 = 0
    last = False
    while True:
        print()
        print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2))
        print('It is', player1 + "'s turn.")
        numDice = strat1(score1, score2, last)
        diceTotal = 0
        diceString = ""
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            diceString = diceString + " "  + str(d)
            i = i-1
        print(numDice, "dice chosen.")
        print("Dice rolled: ", diceString)
        print("Total for this turn: ", str(diceTotal))
        score1 += diceTotal
        if score1 > 100 or last:
            break
        if numDice == 0:
            last = True
        print()
        print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2))
        print('It is', player2 + "'s turn.")
        numDice = strat2(score2, score1, last)
        diceTotal = 0
        diceString = ""
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            diceString = diceString + " "  + str(d)
            i = i-1
        print(numDice, "dice chosen.")
        print("Dice rolled: ", diceString)
        print("Total for this turn: ", str(diceTotal))
        score2 += diceTotal
        if score2 > 100 or last:
            break
        if numDice == 0:
            last = True
    print(player1 + ": " + str(score1) + "   " + player2 + ": " + str(score2))
    if score1 > 100:
        print(player2 + " wins.")
        return 2
    elif score2 > 100:
        print(player1 + " wins.")
        return 1
    elif score1 > score2:
        print(player1 + " wins.")
        return 1
    elif score2 > score1:
        print(player2 + " wins.")
        return 2
    else:
        print("Tie.")
        return 3

def autoplay(strat1, strat2):
    score1 = 0
    score2 = 0
    last = False
    while True:
        numDice = strat1(score1, score2, last)
        diceTotal = 0
        diceString = ""
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            diceString = diceString + " "  + str(d)
            i = i-1
        score1 += diceTotal
        if score1 > 100 or last:
            break
        if numDice == 0:
            last = True
        numDice = strat2(score2, score1, last)
        diceTotal = 0
        diceString = ""
        i = numDice
        while i > 0:
            d = roll()
            diceTotal += d
            diceString = diceString + " "  + str(d)
            i = i-1
        score2 += diceTotal
        if score2 > 100 or last:
            break
        if numDice == 0:
            last = True
    if score1 > 100:
        return 2
    elif score2 > 100:
        return 1
    elif score1 > score2:
        return 1
    elif score2 > score1:
        return 2
    else:
        return 3

def manyGames(strat1, strat2, n):
    i = 0
    player1Wins, player2Wins, ties = 0, 0, 0
    while i < n//2:
        i = i + 1
        result = autoplay(strat1, strat2)
        if result == 1:
            player1Wins = player1Wins + 1
        elif result == 2:
            player2Wins = player2Wins + 1
        else:
            ties = ties + 1
    while i >= n//2 and i < n:
        i = i + 1
        result = autoplay(strat2, strat1)
        if result == 1:
            player2Wins = player2Wins + 1
        elif result == 2:
            player1Wins = player1Wins + 1
        else:
            ties = ties + 1
    print("Player 1 wins:", player1Wins)
    print("Player 2 wins:", player2Wins)
    print("Ties:", ties)

def sample1(myscore, theirscore, last):
    if myscore > theirscore:
        return 0
    else:
        return 12

def sample2(myscore, theirscore, last):
    if myscore <= 50:
        return 30
    elif myscore > 50 and myscore <= 80:
        return 10
    else:
        return 0

def improve(strat1):
    def imp_strat1(myscore, theirscore, last):
        if myscore == 100:
            return 0
        else:
            return strat1(myscore, theirscore, last)
    return imp_strat1

def myStrategy(myscore, theirscore, last):
    if myscore == 0:
        if theirscore > 50:
            return int(theirscore / 2.5)
        else:
            return 33
    elif myscore >= 97:
        return 0
    elif last and myscore > theirscore:
        return 0
    elif myscore < 70:
        return (100 - myscore) // 3.2
    else:
        return int((100 - myscore) / 3.5)
