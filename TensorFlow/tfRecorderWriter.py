import tensorflow as tf
import numpy as np
import sys
import os
import json

def _bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

nHeroes = 120
nFeatures = nHeroes

class Examle:
    def __init__(self, GameData):

        self.picks = np.zeros([1, nFeatures*2], dtype=np.float32)
        self.label = np.ndarray([1,1], dtype=np.float32)
        #radiant picks
        for i in range(1,6):
            heroPickString = "radiantHeroPick{}".format(i)
            heroIdx = GameData["radiant"][heroPickString]
            self.picks[0,heroIdx] = 1.0
        #other data
        #direpicks
        for i in range(1,6):
            heroPickString = "direHeroPick{}".format(i)
            heroIdx = GameData["dire"][heroPickString]
            self.picks[0,heroIdx + nFeatures] = 1.0
        self.label[0,0] = GameData["radiantWin"]









def test():
    file = open("../data/sampleGame.json")
    data = json.load(file)

    for key in data.keys():
        hero1 = data[key]["radiant"]["radiantHeroPick1"]
    return

def main():

    #filename = sys.argv[1]
    #outname = sys.argv[2]
    outname = "ico.tfrecord"
    #file = open(filename, "r")
    file = open("../data/sampleGame.json")
    data = json.load(file)
    examples = []
    for key in data.keys():
        gameData = data[key]
        example = Examle(gameData)
        examples.append(example)

    writer = tf.python_io.TFRecordWriter(outname)
    for exmp in examples:
        picks = exmp.picks
        picks_raw = picks.tostring('C')
        label = exmp.label
        label_raw = label.tostring('C')
        features = {
            'x': _bytes_feature(picks_raw),
            'y': _bytes_feature(label_raw),
        }
        example = tf.train.Example(features=tf.train.Features(feature=features))
        writer.write(example.SerializeToString())
    writer.close()

main()