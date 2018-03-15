from random import *
import sys
import json

gameDataFile = 'parsedGames.json'
validationSize = 700
testDataOutputFile = 'testGames.json'
validateDataOutputFile = 'validationGames.json'

def getGameData(fileName):
    getDataFrom = './data/'+fileName
    return json.load(open(getDataFrom))

def writeDataToFile(fileName, data, pretty):
    writeTo = './data/'+fileName
    with open(writeTo, 'w+') as outfile:
        json.dump(data, outfile)

def getDataFromGames(games, ids):
    data = {}
    for gameId in ids:
        data[gameId] = games[gameId]
    return data

def shuffle():
    games = getGameData(gameDataFile)
    gameIds = games.keys()
    
    validationIds = sample(gameIds, validationSize)
    testIds = set(gameIds) - set(validationIds)
    
    validationData = getDataFromGames(games, validationIds)
    testData = getDataFromGames(games, testIds)

    writeDataToFile(testDataOutputFile, testData, True)
    writeDataToFile(validateDataOutputFile, validationData, True)

def countGames(fileName):
    games = getGameData(fileName)
    print len(games)

countGames('validationGames.json')
#shuffle()