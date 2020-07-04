"""
Helper routine to make an element and isotope dictionary out of the Lodders+09
data file.
"""

import numpy as np
import json
from collections import OrderedDict


# read in data file
data_in = []
with open("lodders09.dat", "r") as f:
    for line in f:
        data_in.append(line.rstrip().split())

# kick header
data = data_in[1 : len(data_in)]

# make numbers and integers
for dat in data:
    dat[0] = int(dat[0])
    dat[2] = int(dat[2])
    dat[3] = float(dat[3]) / 100.0  # abundance needs to be normed to 1
    dat[4] = float(dat[4])

# ISOTOPE DICTIONARY #

iso_keys = []
iso_entries = []

for dat in data:
    iso_keys.append("{}-{}".format(dat[1], dat[2]))
    iso_entries.append([dat[3], dat[4]])

iso_dict = OrderedDict(zip(iso_keys, iso_entries))

# ELEMENT DICTIONARY #
ele_keys = []
ele_entries = []

last_ele = None
tmp_append = None

for dat in data:
    ele = dat[1]
    if ele != last_ele:
        # average solar abundance calculation and appending
        if tmp_append is not None:
            ssabu = np.array(tmp_append[3]).sum()
            tmp_append[0] = ssabu
            # append
            ele_entries.append(tmp_append)
        # write the element
        ele_keys.append(ele)
        last_ele = ele
        # initialize the array
        tmp_append = [0, [], [], []]

    # append to the array
    tmp_append[1].append(dat[2])
    tmp_append[2].append(dat[3])
    tmp_append[3].append(dat[4])

# last append
ssabu = (
    np.sum(np.array(tmp_append[2]) * np.array(tmp_append[3]))
    / np.array(tmp_append[2]).sum()
)
tmp_append[0] = ssabu
# append
ele_entries.append(tmp_append)

ele_dict = OrderedDict(zip(ele_keys, ele_entries))

# write out
# header to write
py_header = r"""'''
This file was automatically created using the `lodders09_to_dict.py` parser available
in the dev/lodders09 folder.

The abundance data in this file are taken from:
Lodders, Palme, and Gail (2009)
doi: 10.1007/978-3-540-88055-4_34
'''"""

# save file
with open("lodders09.py", "w") as f:
    f.write(py_header)
    f.write("\n\n")
    f.write("lodders09_elements = ")
    f.write(json.dumps(ele_dict, indent=4))
    f.write("\n\n")
    f.write("lodders09_isotopes = ")
    f.write(json.dumps(iso_dict, indent=4))
