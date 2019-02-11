import numpy as np
import h5py
import sys
import os
import glob

from PIL import Image

# generates a hdf5 project from a folder with tif images.
# input path to the images folder, path of the new hdf file and the dataset_path (inside the hdf file)
# It will generate an hdf file with 3-dimensions (z, y, x), where z is the number of images. The images will be stacked considering the order of the filenames.


def generate_hdf(folder_path, hdf_path, dataset):

    image_files = glob.glob(folder_path + "/*.tif")
    image_files.sort()
    print("reading {} images...".format(len(image_files)))
    image_data = np.array(
        [np.array(Image.open(image, "r")) for image in image_files], dtype="uint8"
    )

    print(image_data.dtype)
    print(image_data.shape)

    # creating new file: w = create file, fail if exists
    hdf_file = h5py.File(hdf_path, "w-")
    hdf_group = hdf_file.create_group("volumes")

    print("Saving images in the hdf project...")
    hdf_group.create_dataset(
        dataset, data=image_data, compression="gzip", dtype=image_data.dtype
    )


if __name__ == "__main__":

    basic_name = "24000-26112_16128-17088_0-514"
    basic_dir = (
        "/media/vleite/a5c2cdb0-d068-41ea-a7a1-b28a29d082f3/unet-songbird/01_data/soma/"
    )
    folder_path = basic_dir + "imgs/" + basic_name + "/"
    dataset = "raw_masked"
    hdf_path = basic_dir + basic_name + "_120000_0.19-raw-masked.hdf"

    # first argv is the script name
    if len(sys.argv) == 4:
        folder_path = sys.argv[1]
        hdf_path = sys.argv[2]
        dataset = sys.argv[3]

    generate_hdf(folder_path, hdf_path, dataset, True)

    print("Done!")
