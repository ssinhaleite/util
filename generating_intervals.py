import json
import glob
import re
import h5py
import os
import numpy as np


f = open("/home/vleite/Desktop/range.txt", "w")

f.write("x range:\n")
for x in range(0, 55296, 64):
    f.write(str(x) + "-" + str(x + 64) + "\n")

f.write("y range:\n")
for x in range(0, 46080, 64):
    f.write(str(x) + "-" + str(x + 64) + "\n")

f.write("z range:\n")
for x in range(0, 514, 64):
    f.write(str(x) + "-" + str(x + 64) + "\n")

print("done!")
