import sys
import time
from shuffler import getGameData, writeDataToFile

getDataFrom = 'parsedGames.json'
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
            ph[setAsStr] = { 'picked': 0, 'win': 0, 'lose': 0 }
            
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

def main():
    games = getGameData(getDataFrom)
    
    for game in games.values():
        getGameHeroData(game)
    
    writeDataToFile('heroStats.json', heroesStats, False)

main()