import numpy as np
from PIL import Image
import h5py

if __name__ == "__main__":

    lm_path = "/media/vleite/a5c2cdb0-d068-41ea-a7a1-b28a29d082f3/ThomasDataset/Wafer1/C1_EM_2sections.hdf"

    hdf_file = h5py.File(lm_path, "r")
    imgs = hdf_file["volumes/raw"]
    img_array = np.asarray(imgs).astype("uint8")
    print(img_array.shape)
    print(img_array.dtype)

    for i in range(imgs.shape[0]):
        print("Saving image {}".format(i))
        im = Image.fromarray(img_array[i, :])
        im.save("/home/vleite/testes" + "/" + str(i).zfill(5) + ".tif")
        exit()
