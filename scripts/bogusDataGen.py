from __future__ import division
from random import *
from shuffler import getGameData, writeDataToFile

currentWinPer = 0
radiantWin = 1

def createGame(heroPool, winnerPick, loserPick, desiredWinPer = 0.9):
    global radiantWin
    
    radiantPicks = sample(heroPool, 5)
    direPicks = sample(set(heroPool)-set(radiantPicks), 5)

    _radiantWin = radiantWin
    flipWin = True
    if winnerPick in radiantPicks and loserPick in direPicks:
        _radiantWin = 1
        flipWin = False
    if winnerPick in direPicks and loserPick in radiantPicks:
        _radiantWin = 0
        flipWin = False
    
    game = { "radiantWin": _radiantWin, "radiant": {}, "dire": {} }
    for pickNum in range(1,6):
        p = str(pickNum)
        game["radiant"]["radiantHeroPick{}".format(p)] = radiantPicks[pickNum-1]
        game["dire"]["direHeroPick{}".format(p)] = direPicks[pickNum-1]
    
    if flipWin:
        radiantWin = 1^radiantWin
    
    return game

def main():
    heroes = getGameData('heroes.json')
    heroIds = heroes.keys()

    # choose 20 heroes at random to use as picks
    heroPool = sample(heroIds, 20)
    
    # choose 2 heroes from those to serve as winner and loser
    winnerLoserPick = sample(heroPool, 2)
    winnerPick = winnerLoserPick[0]
    loserPick = winnerLoserPick[1]

    games = {}
    for matchId in range(0, 1):
        game = createGame(heroPool, winnerPick, loserPick)
        game["matchId"] = matchId
        games[str(matchId)] = game
    
    bogusData = { "winnerPick": winnerPick, "loserPick": loserPick, "games": games }
    print bogusData

main()