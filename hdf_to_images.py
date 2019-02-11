import numpy as np
import h5py
import sys
import os

from PIL import Image

# generates images from an hdf5 file.
# input path to the hdf file, dataset_path, path to save the images
# The images are generated considering that the hdf has 3-dimensions (z, y, x). Will be generated z images of (y,x).


def generate_images(data_path, dataset, output_path):
    hdf_file = h5py.File(data_path, "r")
    imgs = hdf_file[dataset]
    img_array = np.asarray(imgs).astype("uint8")

    print(img_array.shape)
    print(img_array.dtype)

    for i in range(imgs.shape[0]):
        print("Saving image {}".format(i))
        im = Image.fromarray(img_array[i, :])
        im.save(output_path + str(i).zfill(5) + ".tif")


if __name__ == "__main__":

    basic_dir = (
        "/media/vleite/a5c2cdb0-d068-41ea-a7a1-b28a29d082f3/unet-songbird/01_data/soma/"
    )
    data_path = (
        basic_dir
        + "affinities/segmentation_soma_26368-29056_21248-23936_0-256_120000_0.19.hdf"
    )
    dataset = "volumes/raw"
    output_path = basic_dir + "imgs/26368-29056_21248-23936_0-256/"

    # first argv is the script name
    if len(sys.argv) == 4:
        data_path = sys.argv[1]
        dataset = sys.argv[2]
        output_path = sys.argv[3]

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    generate_images(data_path, dataset, output_path)
