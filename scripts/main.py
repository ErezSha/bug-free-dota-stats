import shuffler
import heroCounter
import argparse

parser = argparse.ArgumentParser(description="beep boop",
    parents=[shuffler.parser, heroCounter.parser])

args = parser.parse_args()

shuffler.main(args)
heroCounter.main(args)