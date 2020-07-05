"""
This is a helper script to transform the `nist_iso_ratios.txt` data file into
some appropriate python dictionary structures. One for elements, one for
isotopes.
"""


import numpy as np
import re
import json
from collections import OrderedDict


# some global patterns
re_uncertainty = re.compile(r"\((.+?)\)")
re_reference = re.compile(r"\[(.+?)\]")


data_in = []
with open("nist_iso_ratios.txt", "r") as f:
    for line in f:
        data_in.append(line.rstrip())


def unc_stripper(s):
    """
    Strips the uncertainty in parentheses from the number. Also strips square brackets.

    :param <str> s: String input

    :return: Value of the string
    :rtype: float
    """

    # replace the uncertainty and references
    s = re_uncertainty.sub("", s)
    s = re_reference.sub("0.0", s)

    try:
        s = float(s)
    except ValueError:
        s = ""
    return s


def save_data(data):
    """
    Helper function to save a test.txt file with the data in it.
    """
    with open("tmp_out.txt", "w") as f:
        f.writelines("Z\tName\tA\tRel_Mass\tAbundance\n")
        for line in data:
            for item in line:
                f.writelines("{}\t".format(item))
            f.writelines("\n")


# remove the header
data_in = data_in[2 : len(data_in)]

# now go through the input data and parse out the lines, put it into a real list
data = []
# read in fixed width
fixed_width = ((0, 4), (4, 8), (8, 13), (13, 32), (32, 46))
for line in data_in:
    if line[0] != "_":
        tmp_append = []
        for tpl in fixed_width:
            value = line[tpl[0] : tpl[1]].replace(" ", "")
            tmp_append.append(value)
        # append to list
        data.append(tmp_append)


# now go through the array and transform data to ints and floats when required
for line in data:
    if line[0] != "":
        line[0] = int(line[0])
    line[2] = int(line[2])
    line[3] = unc_stripper(line[3])
    try:
        line[4] = unc_stripper(line[4])
    except IndexError:
        pass

# DICTIONARIES FOR ABUNDANCES #

# ELEMENT DICTIONARY #

# Element / isotope dictionary, keys: Element names
ele_keys = []
ele_entries = []

# for later:
ele_zz = []  # for later - NIST special
ele_iso_masses = []

tmp_list = None  # helper array, to be initialized in loop
tmp_isomass = None
for dat in data:
    if dat[0] != "":  # we have a new element!
        # write over tmp_append -> append it and re-init
        if tmp_list is not None:
            tmp_list[0] = np.nan
            # add list
            ele_entries.append(tmp_list)
            ele_iso_masses.append(tmp_isomass)
        # z, mass, [a1, a2,...], [abu1, abu2,...], [mass1, mass2,...]
        tmp_list = [np.nan, [], [], []]
        # save these data for later
        ele_keys.append(dat[1])
        ele_zz.append(dat[0])
        tmp_isomass = []

    tmp_list[1].append(dat[2])
    if dat[4] == "":
        tmp_list[2].append(0.0)
    else:
        tmp_list[2].append(dat[4])
    # solar abundance, does not exist
    tmp_list[3].append(np.nan)
    # isomass - for later
    tmp_isomass.append(dat[3])

# The final append
tmp_list[0] = np.nan
# add list
ele_entries.append(tmp_list)
ele_iso_masses.append(tmp_isomass)

ele_dict = OrderedDict(zip(ele_keys, ele_entries))

# ISOTOPE DICTIONARY #

iso_keys = []
iso_entries = []

# loop through element
for element in ele_keys:
    # loop through A list
    for it, aa in enumerate(ele_dict[element][1]):
        # create the isotope name
        iso_keys.append("{}-{}".format(element, aa))
        # stitch information together
        tmp_list = []
        tmp_list.append(ele_dict[element][2][it])
        tmp_list.append(np.nan)
        iso_entries.append(tmp_list)

iso_dict = OrderedDict(zip(iso_keys, iso_entries))

# MAKE GENERAL DICTIONARIES FROM EXISTING DATA #
masses = []
for it, element in enumerate(ele_keys):
    abus = np.array(ele_dict[element][2])
    mass = np.array(ele_iso_masses[it])
    sum_abu = np.sum(abus)
    if sum_abu > 0:
        masses.append(np.sum(abus * mass) / sum_abu)
    else:
        masses.append(np.nan)

ele_mass_dict = OrderedDict(zip(ele_keys, masses))

ele_zz_dict = OrderedDict(zip(ele_keys, ele_zz))

iso_mass_entry = []
# loop through element
for it in range(len(ele_iso_masses)):
    for jt in range(len(ele_iso_masses[it])):
        iso_mass_entry.append(ele_iso_masses[it][jt])

iso_mass_dict = OrderedDict(zip(iso_keys, iso_mass_entry))

# header to write
py_header = r"""'''NIST isotope data, retrieved in 2020.

This file was automatically created using the `nist_data.py` parser available in the
dev/nist_data folder.

The atomic weights are available for elements 1 through 118 and isotopic compositions
or abundances are given when appropriate. The atomic weights data were published by
J. Meija et al in Atomic Weights of the Elements 2013, and the isotopic compositions
data were published by M. Berglund and M.E. Wieser in Isotopic Compositions of the
Elements 2009. The relative atomic masses of the isotopes data were published by
M. Wang, G. Audi, A.H. Wapstra, F.G. Kondev, M. MacCormick, X. Xu1, and B. Pfeiffer in
The AME2012 Atomic Mass Evaluation.

The NIST data were exported on July 1, 2020 from the NIST database:
https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses

The text file with the NIST data can be seen in dev/nist_data as well.
'''"""

# save file
with open("nist15.py", "w") as f:
    f.write(py_header)
    f.write("\n\n")
    f.write("import numpy as np\nNaN = np.nan\n\n")
    f.write("elements_mass = ")
    f.write(json.dumps(ele_mass_dict, indent=4))
    f.write("\n\n")
    f.write("elements_z = ")
    f.write(json.dumps(ele_zz_dict, indent=4))
    f.write("\n\n")
    f.write("isotopes_mass = ")
    f.write(json.dumps(iso_mass_dict, indent=4))
    f.write("\n\n")
    f.write("nist15_elements = ")
    f.write(json.dumps(ele_dict, indent=4))
    f.write("\n\n")
    f.write("nist15_isotopes = ")
    f.write(json.dumps(iso_dict, indent=4))
