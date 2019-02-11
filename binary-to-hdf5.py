import json
import glob
import re
import h5py
import os
import numpy as np
from scipy.ndimage import interpolation

data_path = "/media/vleite/a5c2cdb0-d068-41ea-a7a1-b28a29d082f3/ThomasDataset/Wafer1/precomputed"
data_name = "C1_EM"
json_file = data_path + "/" + data_name + "/" + "info"

skipped_blocks = 0
json_data = open(json_file)
data = json.load(json_data)
data_type = data["data_type"]

i = 0
data_size = data["scales"][i]["size"]
chunk_size = data["scales"][i]["chunk_sizes"][0]
key_blocks = data["scales"][i]["key"]

limitDataset = False
"""
In case limitDataset is true, the values of minX, maxX, minY, maxY, minZ and maxZ will be used.
"""

minX = 18176
maxX = 19648

minY = 11072
maxY = 12352

minZ = 320
maxZ = 384

specific_path = data_path + "/" + data_name + "/" + data["scales"][i]["key"]
print(specific_path)
# creating new file: w = create file, fail if exists
if limitDataset:

    hdf_file = h5py.File(
        data_path
        + "/"
        + data_name
        + "_"
        + key_blocks
        + "_"
        + str(minX)
        + "-"
        + str(maxX)
        + "_"
        + str(minY)
        + "-"
        + str(maxY)
        + "_"
        + str(minZ)
        + "-"
        + str(maxZ)
        + ".hdf",
        "w-",
    )
else:
    hdf_file = h5py.File(data_path + "/" + data_name + "_" + key_blocks + ".hdf", "w-")

hdf_group = hdf_file.create_group("volumes")

specific_path = data_path + "/" + data_name + "/" + key_blocks
blockFiles = glob.glob(specific_path + "/*")

if limitDataset:
    dset = hdf_group.create_dataset(
        key_blocks,
        (maxZ - minZ, maxY - minY, maxX - minX),
        chunks=(64, 64, 64),
        dtype=data_type,
        compression="gzip",
    )
    print(
        "data size: "
        + str(maxZ - minZ)
        + " "
        + str(maxY - minY)
        + " "
        + str(maxX - minX)
    )
else:
    dset = hdf_group.create_dataset(
        key_blocks,
        (data_size[2], data_size[1], data_size[0]),
        chunks=(chunk_size[2], chunk_size[1], chunk_size[0]),
        dtype=data_type,
        compression="gzip",
    )
    print(
        "data size: "
        + str(data_size[2])
        + " "
        + str(data_size[1])
        + " "
        + str(data_size[0])
    )

resolution = [50, 8, 8]
dset.attrs["resolution"] = resolution

for infile in sorted(blockFiles):
    # remove the complete path from the file name
    position = infile.rfind("/")
    infile = infile[position + 1 :]
    #     print( "Processing " + infile)

    splits = infile.split("_", 3)

    x_begin = int(splits[0].split("-", 1)[0])
    y_begin = int(splits[1].split("-", 1)[0])
    z_begin = int(splits[2].split("-", 1)[0])

    x_end = int(splits[0].split("-", 1)[1])
    y_end = int(splits[1].split("-", 1)[1])
    z_end = int(splits[2].split("-", 1)[1])

    if x_begin >= data_size[0] or y_begin >= data_size[1] or z_begin >= data_size[2]:
        print("warning: skipping block outside the range!")
        print(
            "wrong -> "
            + str(x_begin)
            + "-"
            + str(x_end)
            + "_"
            + str(y_begin)
            + "-"
            + str(y_end)
            + "_"
            + str(z_begin)
            + "-"
            + str(z_end)
        )
        skipped_blocks += 1
        continue

    if limitDataset:
        if z_begin < minZ or z_begin >= maxZ:
            continue

        if x_begin < minX or x_begin >= maxX:
            continue

        if y_begin < minY or y_begin >= maxY:
            continue

    print(
        "copying data from "
        + str(x_begin)
        + "-"
        + str(x_end)
        + "_"
        + str(y_begin)
        + "-"
        + str(y_end)
        + "_"
        + str(z_begin)
        + "-"
        + str(z_end)
    )

    if limitDataset:
        print(
            "indices data from "
            + str(x_begin - minX)
            + "-"
            + str(x_end - minX)
            + "_"
            + str(y_begin - minY)
            + "-"
            + str(y_end - minY)
            + "_"
            + str(z_begin - minZ)
            + "-"
            + str(z_end - minZ)
        )

    block = np.fromfile(specific_path + "/" + infile, data_type)
    block3d = block.reshape(
        (z_end - z_begin, y_end - y_begin, x_end - x_begin), order="C"
    )

    if limitDataset:
        dset[
            z_begin - minZ : z_end - minZ,
            y_begin - minY : y_end - minY,
            x_begin - minX : x_end - minX,
        ] = block3d
    else:
        dset[z_begin:z_end, y_begin:y_end, x_begin:x_end] = block3d

print(str(skipped_blocks) + " were skipped")

# downscale the EM raw to the LM size
print("Downscaling EM dataset...")
downscaling_factor = [1, 0.0769, 0.0769]
data_downscaled = interpolation.zoom(block3d, downscaling_factor, order=0)
print("raw downscaled shape: {}".format(data_downscaled.shape))

dset = hdf_group.create_dataset(
    key_blocks + "downscaled",
    (data_size[2] / 13, data_size[1] / 13, data_size[0] / 13),
    chunks=(chunk_size[2], chunk_size[1], chunk_size[0]),
    dtype=data_type,
    compression="gzip",
)
resolution = [50, 8, 8]
dset.attrs["resolution"] = resolution

dset[
    0 : data_size[2] / 13, 0 : data_size[1] / 13, 0 : data_size[0] / 13
] = data_downscaled


print("done!")
