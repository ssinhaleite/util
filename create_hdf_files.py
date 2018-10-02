import numpy as np
import PIL
from PIL import Image
import h5py
import glob
import os

# this script creates a HDF file that contains the information needed to use candidate_mc.
# each project contains one section volumes: groundtruth, intensities(raw), boundaries and affinities information.

# create a dataset in the given hdf project
def create_dataset(hdf_file, name, data):
    hdf_file.create_dataset(name, data=data, compression="gzip", dtype=data.dtype)


def get_dataset_information(file_path, dtype):
    print("reading {} images...".format(file_path))
    #    image = file_path
    image_files = glob.glob(file_path + "/*.tif")
    image_files.sort()

    print("Processing {} files".format(len(image_files)))

    #    dataset = np.array( [np.array(PIL.Image.open(image, 'r'))], data_type=type)
    dataset = np.array(
        [np.array(PIL.Image.open(image, "r")) for image in image_files], dtype
    )
    return dataset


def hdf_files_from_imgs(image_files):

    # creating new file: w = create file, fail if exists
    hdf_file = h5py.File(image_files_path + "/fully_annotated" + ".hdf", "w-")
    hdf_group = hdf_file.create_group("fragments")

    data = get_dataset_information(groundtruth_path, "uint32")
    create_dataset(hdf_group, "groundtruth", data)
    #
    #     for i in range(len(image_files)):
    #         print("Processing " + image_files[i])
    #         basename = os.path.basename(image_files[i]).strip(".tif")
    #         print (basename)
    #         # recovering groundtruth information
    #         data = get_dataset_information(groundtruth_path  + basename + ".tif", 'uint32')
    #         create_dataset(hdf_group, "groundtruth", data)

    #         # recovering intensities information
    #         data = get_dataset_information(intensities_path  + basename + ".tif", 'float32')
    #         create_dataset(hdf_group, "intensities", data)
    #
    #         # recovering boundaries information
    #         data = get_dataset_information(boundaries_path  + basename + ".tif", 'float32')
    #         create_dataset(hdf_group, "boundaries", data)
    #
    #         # recovering affinities information
    #         data = get_dataset_information(affinities_path + "X/"  + basename + ".tif", 'float32')
    #         create_dataset(hdf_group, "xAffinities", data)
    #         data = get_dataset_information(affinities_path + "Y/"  + basename + ".tif", 'float32')
    #         create_dataset(hdf_group, "yAffinities", data)
    #         data = get_dataset_information(affinities_path + "Z/"  + basename + ".tif", 'float32')
    #         create_dataset(hdf_group, "zAffinities", data)

    hdf_file.close()


# def hdf_files_from_hdf(hdf_input_file):
#     print("reading groundtruth...")
#     gt_file = h5py.File(path + "sample" + sample + "_all.hdf", 'r')
#     gt = gt_file['volumes/groundtruth']
#     dataset_array = np.array(gt, data_type='uint32')
#     print dataset_array.shape
#     print(dataset_array.dtype)
#
#     for z in range(dataset_array.shape[0]):
#         # creating new file: w = create file, fail if exists
#         hdf_file = h5py.File(path + "sections/" + sample + str(z).zfill(5) + ".hdf",'w-')
#         hdf_group = hdf_file.create_group('volumes/groundtruth')
#
#         #TODO: add other information to the hdf file

if __name__ == "__main__":

    image_files_path = (
        "/home/vleite/research/data/songbird/initial_fragments_fully_annotated"
    )
    from_imgs = True

    if from_imgs:
        groundtruth_path = image_files_path
        #         intensities_path = path + "raw_cropped/"
        #         boundaries_path = path + "affinitiesXY-mask-inv/"
        #         affinities_path = path + "affinities"

        image_files = glob.glob(groundtruth_path + "*.tif")
        image_files.sort()

        hdf_files_from_imgs(image_files)

#     else: # from hdf
#         input_file = path + "sample" + sample + "_all.hdf"
#         hdf_files_from_hdf( input_file )
