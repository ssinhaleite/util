import mahotas as mh
import glob
import os

# rename files from 0 to number of files.

files = glob.glob("/path/*")
files.sort()

if not os.path.isdir("/path/renamed/"):
    os.mkdir("/path/renamed/")

for i in range(len(files)):
    print("Processing " + files[i])

    renamedFile = mh.imread(files[i])
    mh.imsave("/path/renamed/" + str(i).zfill(5) + ".tif", renamedFile)
