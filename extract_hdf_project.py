import numpy as np
import h5py
from infos import affinities_path, gt_path, sample

# given a hdf file project with a groundtruth information (neuron ids) and mask, 
# creates a new hdf file only with the relevant information

def get_gt_bounding_box(gt):

    # no-label ids are <0, i.e. the highest numbers in uint64
    fg_indices = np.where(gt <= np.uint64(-10))
    return tuple(
        slice(np.min(fg_indices[d]),np.max(fg_indices[d])+1)
        for d in range(3)
    )

def crop(a, bb):

    cur_shape = list(a.shape[-3:])
    print("Cropping from " + str(cur_shape) + " to " + str(bb))
    if len(a.shape) == 3:
        a = a[bb]
    elif len(a.shape) == 4:
        a = a[(slice(0,4),)+bb]
    else:
        raise RuntimeError("encountered array of dimension " + str(len(a.shape)))

    return a

def create_dataset(hdf_file, name, data, data_type):
    hdf_file.create_dataset(name, data=data, compression='gzip', data_type=data_type)

if __name__ == "__main__":

    gt_group = "volumes/labels/neuron_ids"

    lm_path = "/home/vleite/research/data/20170330_no2/01_data_preparation/sample" + sample + "/"
    
    # creating new file: w = create file, fail if exists
    hdf_file = h5py.File(lm_path + "sample" + sample + "_all.hdf",'w-')
    hdf_group = hdf_file.create_group("volumes")

    ####  Groundtruth
    print "Reading gt..."
    gt_file = h5py.File(gt_path, 'r')
    gt = gt_file['volumes/labels/neuron_ids']
    print gt.shape
    print gt.dtype

    print "Getting ground-truth bounding box..."
    bb = get_gt_bounding_box(gt)

    print "Cropping gt"
    gt = crop(gt, bb)
    print gt.shape
    print gt.dtype

    print "Getting no gt positions..."
    no_dataset = gt>=np.uint64(-10)
    print no_dataset

    print "Copying gt to memory..."
    dataset_array = np.array(gt)
    gt[no_dataset] = 0

    print "Saving gt in the output hdf project..."
    create_dataset(hdf_group, "groundtruth", dataset_array, 'uint64')

    ####  Raw intensities
    print "Reading intensities..."
    raw_file = h5py.File(gt_path, 'r')
    intensities = raw_file['volumes/raw']
    print intensities.shape
    print intensities.dtype

    print "Cropping intensities to ground-truth bounding box..."
    intensities = crop(intensities, bb)
    print intensities.shape
    print intensities.dtype

    print "Copying intensities to memory..."
    intensities = np.array(intensities)
    print intensities.dtype

    print "Saving intensities in the output hdf project..."
    create_dataset(hdf_group, "intensities", intensities, 'uint8')

    ####  Affinities
    print "Reading affinities..."
    aff_file = h5py.File(affinities_path, 'r')
    affs = aff_file['main']

    print "Cropping affinities to ground-truth bounding box..."
    affs = crop(affs, bb)
    print affs.shape
    print affs.dtype

    print "Copying affs to memory..."
    affs = np.array(affs)

    print "Masking affinities outside ground-truth..."
    for d in range(3):
        affs[d][no_dataset] = 0
    print affs.dtype

    print "Saving x affinities in the output hdf project..."
    create_dataset(hdf_group, "xAffinities", affs[2], 'float32')
    print "Saving y affinities in the output hdf project..."
    create_dataset(hdf_group, "yAffinities", affs[1], 'float32')
    print "Saving z affinities in the output hdf project..."
    create_dataset(hdf_group, "zAffinities", affs[0], 'float32')

    ####  Boundaries
    print "Calculating boundaries as average of x-, and y-affinities..."
    boundaries = (affs[2] + affs[1])/2
    print boundaries.dtype

    print "Saving boundaries in the output hdf project..."
    create_dataset(hdf_group, "boundaries", boundaries, 'float32')

    aff_file.close()
    raw_file.close()
    gt_file.close()
    hdf_file.close()


