import argparse
import importlib
import numpy as np
import math
import random

from helpers import str2bool
from datamanager import DataManager
from comprescoretest import CompreScoreTest

def compress(seqs, encoder):
    scores = []
    for i in range(100):
        subseqs = list(random.sample(seqs, k=50))
        scores.append( encoder.score(subseqs) )
    return np.average(scores)

parser = argparse.ArgumentParser()
parser.add_argument("--iter", help="How many times you want to run the model. Default: 200.", type=int, default=10)
parser.add_argument("--compressor", help="Which compressor to use with the model. Default: gzip", type=str, default="gzip")
parser.add_argument("--blosum", type=str2bool, nargs='?', const=True, default=False, help="Use BLOSUM replacement with the model.")
parser.add_argument("--input", help="File to use as input. Format: QUANTITY SEQUENCE", type=str, default="example_file.txt")
args = parser.parse_args()

if args.compressor not in ["gzip","zlib","bz2","lzma"]:
    raise Exception("Compressor not valid.")

if args.input is None:
    raise Exception("Input can't be empty.")

method = str(args.compressor).upper()
if args.blosum:
    method = method + "_Blosum"

module = importlib.import_module('models.{}'.format(method))
toUseMethod = getattr(module, method)()

f = open(args.input, "r")
seqs = []
for line in f.readlines():
    quant, seq = line.strip().split()
    for i in range(int(quant)):
        seqs.append(seq)

f.close()

print("Calculating score for input using  " + str(args.compressor).upper() + " as compressor. Using Blosum? " + str(args.blosum))

score = []
for i in range(args.iter):
    subsample = list(random.sample(seqs, k=int(len(seqs)/3)))
    subseqs = list(set(subsample))
    score.append(compress(subseqs, toUseMethod))


print("Score: " + str(np.average(score)))