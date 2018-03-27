from __future__ import division
import sys
import time
import argparse
from shuffler import getGameData, writeDataToFile

heroesStats = {2: {}, 3: {}, 4: {}, 5: {}}

def getHeroPicks(gameData, side='radiant'):
    heroPicks = map(lambda i: gameData[side]["{}HeroPick{}".format(side, i+1)], range(5))
    heroPicks.sort()
    return heroPicks

def createSuperset(picks):
    sets = [set([])]
    for heroId in picks:
        sets.extend([s | {heroId} for s in sets])
    return filter(lambda set: len(set) > 1, sets)

def addToHeroesStats(setOfHeroSets, didWin):
    for heroSet in setOfHeroSets:
        hs = list(heroSet)
        hs.sort()
        setAsStr = '_'.join(str(hId) for hId in hs)
        ph = heroesStats[len(heroSet)]
        # initialize if not in object
        if setAsStr not in ph.keys():
            ph[setAsStr] = { 'id': setAsStr, 'picked': 0, 'win': 0, 'lose': 0 }
            
        ph[setAsStr]['picked'] += 1
        if didWin:
            ph[setAsStr]['win'] += 1
        else:
            ph[setAsStr]['lose'] += 1

def getGameHeroData(game):
    start = time.time()

    radiantPicks = getHeroPicks(game)
    rSuperSet = createSuperset(radiantPicks)
    
    direPicks = getHeroPicks(game, 'dire')
    dSuperSet = createSuperset(direPicks)
    
    radiantWin = game['radiantWin'] == 1
    addToHeroesStats(rSuperSet, radiantWin)
    addToHeroesStats(dSuperSet, not radiantWin)

    end = time.time()
    print(end - start)

def heroDataFromGames(fileName='parsedGames.json'):
    games = getGameData(fileName)
    
    for game in games.values():
        getGameHeroData(game)
    
    writeDataToFile('heroStats.json', heroesStats, False)
    print('done wrting to file')

# gets an array of hero ids.
# returns an array of localized hero names.
def resolveHeroIdsToNames(heroIds):
    heroes = getGameData('heroes.json')
    return map(lambda heroId: heroes[heroId]['localized_name'], heroIds)

def getMost(games, what='picked', ofType='2', minGames = 0):
    heroStats = filter(lambda stat: stat['picked'] >= minGames ,games[ofType].values())
    sortedStats = []
    if what == 'w/l':
        sortedStats = sorted(heroStats, key=lambda stat: stat['win']/stat['picked'], reverse=True)
    else:
        sortedStats = sorted(heroStats, key=lambda stat: stat[what], reverse=True)

    return sortedStats

def prepareForPrint(heroesStats):
    heroIds = heroesStats['id'].split('_')
    heroNames = resolveHeroIdsToNames(heroIds)
    return [' & '.join(heroNames), str(heroesStats['picked']), str(heroesStats['win']), str(heroesStats['lose'])]

def countType(games, ofType='2', minGames=0):
    heroStats = filter(lambda stat: stat['picked'] > minGames ,games[ofType].values())
    return heroesStats.keys()

def main(args):
    games = getGameData('heroStats.json') 
    if args.most != None:
        most = getMost(games, what=args.most, ofType=args.ofType, minGames=args.minGames)
        totalOfType = len(most)
        statsToPrint = map(prepareForPrint, most[0:args.top])
        
        headers = ["Heroes", "Picked", "Win", "Lose"]
        print "\t".join(headers)
        for index, stats in enumerate(statsToPrint):
            print("{}. {}".format(str(index+1), " ".join(stats)))
        print("\nTotal: {} ".format(str(totalOfType)))


parser = argparse.ArgumentParser(description='Get some cool stats for hero combinations', add_help=False)
parser.add_argument('--most', dest='most', help='Choose from w/l, picked, win, lose')
parser.add_argument('-ofType', dest='ofType', help='Choose from 2,3,4,5', type=str, default='2')
parser.add_argument('-top', dest='top', help='how many rows to show', type=int, default=3)
parser.add_argument('-minGames', dest='minGames', help='minimum games to consider', type=int, default=0)