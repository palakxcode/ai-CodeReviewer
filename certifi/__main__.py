import argparse

from certifi import contents, where

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--contents", action="store_true")
args = parser.parse_args()

if args.contents:
    print("Printing certificate contents:")
    print(contents())
else:
    print("Certificate path:")
    print(where())

