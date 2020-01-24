import argparse
import importlib
import numpy as np
import math

from helpers import str2bool
from datamanager import DataManager
from comprescoretest import CompreScoreTest

parser = argparse.ArgumentParser()
parser.add_argument("--iter", help="How many times you want to run the model. Default: 200.", type=int, default=10)
parser.add_argument("--compressor", help="Which compressor to use with the model. Default: gzip", type=str, default="gzip")
parser.add_argument("--blosum", type=str2bool, nargs='?', const=True, default=False, help="Use BLOSUM replacement with the model.")
args = parser.parse_args()

if args.compressor not in ["gzip","zlib","bz2","lzma"]:
	raise Exception("Compressor not valid.")

dm = DataManager()

method = str(args.compressor).upper()
if args.blosum:
	method = method + "_Blosum"

module = importlib.import_module('models.{}'.format(method))
toUseClass = getattr(module, method)
gc = CompreScoreTest(dm, toUseClass)
avg = []

print("Calculating MSE for method " + str(args.compressor).upper() + ". Using Blosum? " + str(args.blosum))

for j in range(1,args.iter):
	gc.train()
	evaluation = gc.model_evaluation()
	avg.append(math.sqrt(evaluation['mse']))
	

print("Mean squared error: " + str(np.average(avg)))