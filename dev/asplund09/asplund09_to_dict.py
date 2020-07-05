"""
Parser to get Asplund+09 into iniabu dictionary format.

Data taken from NuPyCEE project, link:
https://github.com/NuGrid/NuPyCEE
"""

import json
import numpy as np
from collections import OrderedDict

isotopes = []
with open("asplund09_isotopes.txt", "r") as f:
    for line in f:
        isotopes.append(line.rstrip().split())

elements = []
with open("asplund09_elements.txt", "r") as f:
    for line in f:
        elements.append(line.rstrip().split())

# some transformations
for line in isotopes:
    # split isotope into tuple of (Symbol, A)
    iso_split = line[0].split("-")
    iso_new = (iso_split[0], int(iso_split[1]))
    line[0] = iso_new
    # turn abundance into float and divide by 100
    line[1] = float(line[1]) / 100.0

ele_keys = []
for line in elements:
    line[0] = int(line[0])
    ele_keys.append(line[1])
    line[2] = float(line[2])

# transform isotopic abundance such that it is linear, but arbitrary
for line in elements:
    abu_log = line[2]
    nh = 1e10  # this is temporary
    abu_lin = 10 ** (abu_log - 12) * nh
    if abu_log == -30:
        line[2] = np.nan
    else:
        line[2] = abu_lin

# normalize abundance such that si is 10^6
temp_dict = dict(zip(ele_keys, elements))
corr_factor = 1e6 / temp_dict["Si"][2]
for line in elements:
    line[2] *= corr_factor

ele_dict_entries = []
for it, ele in enumerate(ele_keys):
    tmp_append = []
    # append solar abundance
    solar_abu = elements[it][2]
    tmp_append.append(solar_abu)
    # prepare emtpy arrays for isotopes
    aa_tmp = []
    abu_tmp = []
    sol_abu_tmp = []
    # loop through isotopes
    for isodata in isotopes:
        if isodata[0][0] == ele:
            aa_tmp.append(isodata[0][1])
            abu_tmp.append(isodata[1])
            sol_abu_tmp.append(isodata[1] * solar_abu)
    # append to temp
    tmp_append.append(aa_tmp)
    tmp_append.append(abu_tmp)
    tmp_append.append(sol_abu_tmp)
    # append
    ele_dict_entries.append(tmp_append)

ele_dict = OrderedDict(zip(ele_keys, ele_dict_entries))

# MAKE ISOTOPE DICTIONARY #

iso_keys = []
iso_entries = []

for ele in ele_keys:
    for it, aa in enumerate(ele_dict[ele][1]):
        # iso key
        iso_keys.append("{}-{}".format(ele, aa))
        # entry
        tmp_entry = []
        # abundance
        tmp_entry.append(ele_dict[ele][2][it])
        # solar abundance
        tmp_entry.append(ele_dict[ele][3][it])
        # append
        iso_entries.append(tmp_entry)

iso_dict = OrderedDict(zip(iso_keys, iso_entries))


# write out
# header to write
py_header = r"""'''Asplund et al. (2009) data.

This file was automatically created using the `asplund09_to_dict.py` parser available
in the dev/asplund09 folder.

The abundance data in this file are taken from:
Asplund et al. (2009)
10.1146/annurev.astro.46.060407.145222

Solar abundances are number abundances normed such that N_Si = 1e6
'''"""

# save file
with open("asplund09.py", "w") as f:
    f.write(py_header)
    f.write("\n\n")
    f.write("import numpy as np\nNaN = np.nan\n\n")
    f.write("asplund09_elements = ")
    f.write(json.dumps(ele_dict, indent=4))
    f.write("\n\n")
    f.write("asplund09_isotopes = ")
    f.write(json.dumps(iso_dict, indent=4))
