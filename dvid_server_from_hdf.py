import numpy as np
import h5py
import signal
from diced import DicedStore, ArrayDtype

hdf_path = "/home/vleite/Downloads/sample_A_20160501.hdf"

store = DicedStore("~/repo.diced")  # location of diced repo
print("store " + str(store))

repoName = "22"
store.create_repo(repoName, "no dataset")
uuid = store.get_repouuid(repoName)
print(uuid)

repo = store.open_repo(repoName, uuid)
print("repo " + str(repo))

arr_raw = repo.create_array("raw", ArrayDtype.uint8)  # default 3D array

hdf_file = h5py.File(hdf_path, "r")
lm_ds = hdf_file["volumes/raw"]
print(lm_ds.size)
arr_raw[0:125, 0:1250, 0:1250] = np.array(lm_ds, "uint8")

arr_label = repo.create_array("label", ArrayDtype.uint64)  # default 3D array
lm_ds = hdf_file["volumes/labels/neuron_ids"]
arr_label[0:125, 0:1250, 0:1250] = np.array(lm_ds, "uint64")

# print(arr_raw.get_numdims())
# print(arr_raw.get_extents())
# print(arr_label.get_extents())
print("Done!")

signal.pause()
