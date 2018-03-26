from random import *
import sys
import json
import argparse

def getGameData(fileName):
    getDataFrom = './data/'+fileName
    return json.load(open(getDataFrom))

def writeDataToFile(fileName, data, pretty=False):
    writeTo = './data/'+fileName
    with open(writeTo, 'w+') as outfile:
        if pretty:
            data = json.dumps(data, sort_keys=True, indent=4)
        json.dump(data, outfile)

def getDataFromGames(games, ids):
    data = {}
    for gameId in ids:
        data[gameId] = games[gameId]
    return data

def shuffle(dataFile, testTo, validationTo, valSize):
    games = getGameData(dataFile)
    gameIds = games.keys()
    
    validationIds = sample(gameIds, valSize)
    testIds = set(gameIds) - set(validationIds)
    
    validationData = getDataFromGames(games, validationIds)
    testData = getDataFromGames(games, testIds)

    writeDataToFile(testTo, testData, False)
    writeDataToFile(validationTo, validationData, False)

def countGames(fileName):
    games = getGameData(fileName)
    print len(games)

#countGames('validationGames.json')
#shuffle()

parser = argparse.ArgumentParser(description='Shuffle test and validation games')
parser.add_argument('--count', dest='count', help='Count games in a file')
parser.add_argument('--shuffle', dest='shuffle', help='Shuffle games to test and validation files', type=str)
parser.add_argument('-valSize', dest='valSize', help='Sets number of games used for validation', type=int, default=700)
parser.add_argument('-testTo', dest='testTo', help='write test data to this file', type=str, default='testGames.json')
parser.add_argument('-validationTo', dest='validationTo', help='write validation data to this file', type=str, default='validationGames.json')

args = parser.parse_args()
if args.count != None:
    countGames(args.count)

if args.shuffle != None:
    valSize = args.valSize
    gameDataFile = args.shuffle
    testTo = args.testTo
    validationTo = args.validationTo
    shuffle(gameDataFile, testTo, validationTo, valSize)