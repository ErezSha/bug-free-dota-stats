from __future__ import division
from random import *
import argparse
from shuffler import getGameData, writeDataToFile

gamesChecked = 0
radiantWins = 0
def validateGame(winnerPick, loserPick, game):
    global gamesChecked, radiantWins
    
    radiantPicks = game['radiant'].values()
    direPicks = game['dire'].values()
    actualWinner = game['radiantWin']
    expectedWinner = -1
    if winnerPick in radiantPicks and loserPick in direPicks:
        expectedWinner = 1
    if winnerPick in direPicks and loserPick in radiantPicks:
        expectedWinner = 0

    if expectedWinner == -1:
        gamesChecked += 1
        radiantWins += actualWinner
        return None
    if expectedWinner != actualWinner:
        return 'should win {} but won {}'.format(expectedWinner, actualWinner)
    else:
        return 'all ok'


sumOfGames = 0
winnerPickWins = 0
radiantWin = 1

def getWinSide(winHeroSide = 1, desiredWinPer = 0.9):
    global sumOfGames, winnerPickWins
    
    sumOfGames += 1
    currWinPer = winnerPickWins / sumOfGames

    if currWinPer > desiredWinPer:
        winnerPickWins += 1
        return 1^winHeroSide
    else:
        return winHeroSide

def createGame(heroPool, winnerPick, loserPick, desiredWinPer = 0.9):
    global radiantWin
    
    radiantPicks = sample(heroPool, 5)
    direPicks = sample(set(heroPool)-set(radiantPicks), 5)

    _radiantWin = radiantWin
    flipWin = True
    if winnerPick in radiantPicks and loserPick in direPicks:
        _radiantWin = getWinSide(1)
        flipWin = False
    if winnerPick in direPicks and loserPick in radiantPicks:
        _radiantWin = getWinSide(0)
        flipWin = False
    
    game = { "radiantWin": _radiantWin, "radiant": {}, "dire": {} }
    for pickNum in range(1,6):
        p = str(pickNum)
        game["radiant"]["radiantHeroPick{}".format(p)] = radiantPicks[pickNum-1]
        game["dire"]["direHeroPick{}".format(p)] = direPicks[pickNum-1]
    
    if flipWin:
        radiantWin = 1^radiantWin
    
    return game

def createBogusData(poolSize=20, dataSize=100, desiredWinPer=0.9, writeTo="bogusData.json"):
    heroes = getGameData('heroes.json')
    heroIds = heroes.keys()

    # choose 20 heroes at random to use as picks
    heroPool = sample(heroIds, poolSize)
    
    # choose 2 heroes from those to serve as winner and loser
    winnerLoserPick = sample(heroPool, 2)
    winnerPick = winnerLoserPick[0]
    loserPick = winnerLoserPick[1]

    games = {}
    for matchId in range(0, dataSize):
        game = createGame(heroPool, winnerPick, loserPick, desiredWinPer)
        game["matchId"] = matchId
        games[str(matchId)] = game
    
    bogusData = { "winnerPick": winnerPick, "loserPick": loserPick, "games": games }
    writeDataToFile(writeTo, data=bogusData, mode='w')

def main(args):
    if args.create != None:
        createBogusData(poolSize=args.poolSize, dataSize=args.dataSize, 
                        desiredWinPer=args.desWinPer, writeTo=args.create)
    if args.countFile != None:
        countGamesInFile(args.countFile)

parser = argparse.ArgumentParser(description='Create bogus data games', add_help=False)
parser.add_argument('--create', dest='create', help='create new data to this file', type=str)
parser.add_argument('-dataSize', dest='dataSize', help='number of games to create', type=int, default=10000)
parser.add_argument('-heroPoolSize', dest='poolSize', help='number of hero ids to use as base hero pool', type=int, default=20)
parser.add_argument('-desWinPer', dest='desWinPer', help='desired win percentege of winning hero', type=float, default=0.9)
