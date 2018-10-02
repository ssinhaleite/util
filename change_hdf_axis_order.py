import h5py
import numpy as np


def axis_order_raw(project_path):

    print("reading dataset...")
    f = h5py.File(project_path, "r+")

    raw_ds = f["volumes/8nm"]
    raw = np.array(raw_ds, "uint8")

    print(raw.dtype)
    print(raw.shape)

    raw = np.transpose(raw)
    print(raw.shape)

    raw_ds = f.create_dataset("volumes/raw", raw.shape, "uint8", compression="gzip")
    raw_ds[:] = raw

    resolution = [50, 8, 8]
    raw_ds.attrs["resolution"] = resolution
    f.close()


def axis_order_lm(project_path):

    print("reading dataset...")
    f = h5py.File(project_path, "r+")

    raw_ds = f["volumes/104nm"]
    raw = np.array(raw_ds, "uint8")

    print(raw.dtype)
    print(raw.shape)

    raw = np.transpose(raw)
    print(raw.shape)

    raw_ds = f.create_dataset("volumes/lm", raw.shape, "uint8", compression="gzip")
    raw_ds[:] = raw

    resolution = [50, 8, 8]
    raw_ds.attrs["resolution"] = resolution
    f.close()


def axis_order_label(project_path, offset):

    print("reading dataset...")
    f = h5py.File(project_path, "r+")

    neuron_ids_ds = f["volumes/labels/canvas"]
    neuron_ids = np.array(neuron_ids_ds, "uint64")

    #    b = neuron_ids[:, :, 32:]

    #    print(b.dtype)
    #    print(b.shape)

    #    neuron_ids = np.transpose(b)
    neuron_ids = np.transpose(neuron_ids)
    print(neuron_ids.shape)

    neuron_ids_ds = f.create_dataset(
        "volumes/labels/neuron_ids", neuron_ids.shape, "uint64", compression="gzip"
    )
    neuron_ids_ds[:] = neuron_ids

    resolution = [50, 8, 8]
    neuron_ids_ds.attrs["resolution"] = resolution
    if offset != 0:
        neuron_ids_ds.attrs["offset"] = offset
    f.close()


if __name__ == "__main__":
    input_path = "/home/vleite/research/data/C1_LM_488_104nm.hdf"

    offset = 0  # [11200, 2048, 2048]
    axis_order_lm(input_path)
