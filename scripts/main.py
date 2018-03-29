import shuffler
import heroCounter
import bogusDataGen
import argparse

parser = argparse.ArgumentParser(description="beep boop",
    parents=[shuffler.parser, heroCounter.parser, bogusDataGen.parser])

args = parser.parse_args()

shuffler.main(args)
heroCounter.main(args)
bogusDataGen.main(args)