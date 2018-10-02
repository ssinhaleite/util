# util
Set of many scripts that can be useful (or not) for random necessities.

## Scripts:

- apt-remove-duplicate-source-entries.py: detects and interactively deactivates duplicate apt source entries in `/etc/sources.list' and `/etc/sources.list.d/*.list'.
Source code from https://github.com/davidfoerster/apt-remove-duplicate-source-entries

- binary_to_hdf5.py: converts binary blocks of uint8 into a HDF5 project. The name of each block must be in the representation `x1-x2_y1-y2_z1-z2`. Where `[x,y,z]1` represents the initial position of the block and `[x,y,z]2` represents the final position of the block. This is useful for generate the hdf5 of a [chunk representation of volume data used by neuroglancer](https://github.com/google/neuroglancer/tree/master/src/neuroglancer/datasource/precomputed).

- change_hdf_axis_order.py:

- create_hdf_files.py:

- dvid_server_from_hdf.py: creates a local dvid server with data from an hdf5 file. Can be useful to see data in neuroglancer.

- extract_hdf_project.py

- generating_intervals.py:

- hdf_to_images.py: generates images from an hdf5 file. The images are generated considering that the first dimension is the z-direction.

- random_location_xyz.py: generates random x,y,z position given an interval.

- rename_files.py:

- u_net_input_output_relation.py: generates valid values for input and output in the u-net architecture.

