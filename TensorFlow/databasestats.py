import sys
import json

def main():
    inname = sys.argv[1]
    file = open(inname)
    data = json.load(file)
    radiant_map = dict()
    dire_map = dict()
    all_map = dict()

    for key in data.keys():
        gameData = data[key]
        rad_picks = []
        for i in range(1, 6):
            heroPickString = "radiantHeroPick{}".format(i)
            heroIdx = gameData["radiant"][heroPickString]
            rad_picks.append(heroIdx)
            rad_picks = sorted(rad_picks)
        hash_rad = (rad_picks[0], rad_picks[1], rad_picks[2], rad_picks[3], rad_picks[4])
        if hash_rad in radiant_map.keys():
            radiant_map[hash_rad] += 1
        else:
            radiant_map[hash_rad] = 1
    # other data
        # direpicks
        dire_picks = []
        for i in range(1, 6):
            heroPickString = "direHeroPick{}".format(i)
            heroIdx = gameData["dire"][heroPickString]
            dire_picks.append(heroIdx)
            dire_picks = sorted(dire_picks)
        hash_dire = (dire_picks[0], dire_picks[1], dire_picks[2], dire_picks[3], dire_picks[4])
        if hash_dire in dire_map.keys():
            dire_map[hash_dire] += 1
        else:
            dire_map[hash_dire] = 1

        hash_all = (hash_rad, hash_dire)
        if hash_all in all_map.keys():
            all_map[hash_all] += 1
        else:
            all_map[hash_all] = 1

    for key in all_map.keys():
        if all_map[key] > 1:
            print(key, all_map[key])



main()