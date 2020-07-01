"""
This is a helper script to transform the `nist_iso_ratios.txt` data file into
some appropriate python dictionary structures. One for elements, one for
isotopes.
"""


import numpy as np
import re
import json


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
for line in data_in:
    if line[0] != "_":
        tmp = line.split()
        if len(tmp) > 4:  # element, but with isotope abundance
            data.append(tmp[0:5])
        elif len(tmp) == 4:  # element
            try:
                float(tmp[0])
                data.append(tmp)
            except ValueError:  # take care of deuterium
                tmp.insert(0, "")
                data.append(tmp)
        else:
            if tmp[0] == "T":  # exception for tritium
                tmp.insert(0, "")
            else:
                tmp.insert(0, "")
                tmp.insert(0, "")
            data.append(tmp)

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

# Element / isotope dictionary, keys: Element names
ele_isos_header = ("A", "Mass", "Abundance")
ele_isos_keys = []
ele_z = []
ele_isos_tmp = []

tmp_list = None
for line in data:
    if line[0] != "":
        ele_isos_keys.append(line[1])
        ele_z.append(line[0])
        if tmp_list is not None:
            ele_isos_tmp.append(tmp_list)
        tmp_list = [[], [], []]

    tmp_list[0].append(line[2])
    tmp_list[1].append(line[3])
    try:
        tmp_list[2].append(line[4])
    except IndexError:
        tmp_list[2].append(0.0)

ele_isos_tmp.append(tmp_list)

ele_isos_dict = dict(zip(ele_isos_keys, ele_isos_tmp))


# Element dictionary, keys: Element names
ele_header = ("Z", "Mass")
ele_tmp = []
for it, line in enumerate(ele_isos_tmp):
    denominator = np.array(line[2], dtype=np.float).sum()
    if denominator > 0:
        mass_tmp = (
            np.sum(
                np.array(line[1], dtype=np.float)
                * np.array(line[2], dtype=np.float)
            )
            / denominator
        )
    else:
        mass_tmp = 0.0
    ele_tmp.append([ele_z[it], mass_tmp])

ele_dict = dict(zip(ele_isos_keys, ele_tmp))

# Isotope dictionary, keys: "Name-A"
iso_dict_keys = []
iso_dict_header = ("Mass", "Abundance")
iso_dict_tmp = []

for ele in ele_isos_keys:
    for jt, a in enumerate(ele_isos_dict[ele][0]):
        mass = ele_isos_dict[ele][1][jt]
        abu = ele_isos_dict[ele][2][jt]
        iso_dict_keys.append("{}-{}".format(ele, a))
        iso_dict_tmp.append([mass, abu])

iso_dict = dict(zip(iso_dict_keys, iso_dict_tmp))
print(iso_dict)

# make an elementary dictionary: {"Name": average_mass}
with open("nist_data.py", "w") as f:
    f.write("elements = ")
    f.write(json.dumps(ele_dict, indent=4))
    f.write("\n\n")
    f.write("elements_isotopes = ")
    f.write(json.dumps(ele_isos_dict, indent=4))
    f.write("\n\n")
    f.write("isotopes = ")
    f.write(json.dumps(iso_dict, indent=4))
