import h5py
import numpy as np

# copy dataset from one project to another
def copy_dataset(
    project_read, old_dataset_name, dataset_type, project_write, new_dataset_name
):

    print("reading dataset...")
    f = h5py.File(project_read, "r+")

    ds = f[old_dataset_name]
    print("loaded everything")
    #     ds = ds[:21, :, :]
    #     print("got slices")
    ds_array = np.array(ds, "float")

    print(ds_array.dtype)
    print(ds_array.shape)
    f.close()

    f = h5py.File(project_write, "a")
    print("creating dataset...")
    new_ds = f.create_dataset(
        new_dataset_name, ds_array.shape, dataset_type, compression="gzip"
    )
    new_ds[:] = ds_array * 255
    resolution = [50, 8, 8]
    new_ds.attrs["resolution"] = resolution
    offset = [0, 0, 0]
    new_ds.attrs["offset"] = offset

    f.close()
    print("done!")


if __name__ == "__main__":
    input_path = "/media/vleite/a5c2cdb0-d068-41ea-a7a1-b28a29d082f3/unet-songbird/01_data/soma/affinities/predictions_songbird8_23040-29184_7936-10496_0-514_120000.hdf"
    output_path = "/media/vleite/a5c2cdb0-d068-41ea-a7a1-b28a29d082f3/unet-songbird/01_data/soma/affinities/segmentation_soma_23040-29184_7936-10496_0-514_120000_0.00.hdf"

    # information about the dataset being copied
    old_dataset_name = "volumes/raw"
    dataset_type = "uint8"
    new_dataset_name = "volumes/raw"

    copy_dataset(
        input_path, old_dataset_name, dataset_type, output_path, new_dataset_name
    )
