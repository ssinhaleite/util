import numpy as np
import h5py

# define all values where id is true as 1, other ids will be 0
def generate_neuron_mask(file_path, neuron_id):

    print("reading segmentation...")
    f = h5py.File(file_path, "r+")

    ds = f["volumes/labels/merged_ids"]
    segmentation = np.array(ds, "uint64")
    offset = f["volumes/labels/merged_ids"].attrs["offset"]
    resolution = f["volumes/labels/merged_ids"].attrs["resolution"]

    print("loaded everything")
    f.close()

    f = h5py.File(file_path, "a")
    print("creating dataset...")

    neuron_mask = np.zeros(segmentation.shape)
    neuron_mask[np.where(segmentation == neuron_id)] = 1

    ds = f.create_dataset(
        "volumes/labels/neuron_ids_mask",
        data=neuron_mask,
        compression="gzip",
        dtype=np.uint64,
    )
    ds.attrs["offset"] = offset
    ds.attrs["resolution"] = resolution

    f.close()

    print("Done!")


if __name__ == "__main__":

    file_path = "/media/vleite/a5c2cdb0-d068-41ea-a7a1-b28a29d082f3/unet-songbird/01_data/soma/affinities/segmentation_soma_22784-24576_10112-11712_192-514_120000_0.19.hdf"
    neuron_id = 674753

    generate_neuron_mask(file_path, neuron_id)
