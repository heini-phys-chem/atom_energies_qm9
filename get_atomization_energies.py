#!/usr/bin/env python3

import os
import numpy as np

# dictionary containing elements and their correspinding energies from: https://doi.org/10.1038/sdata.2014.22
U0   = {"H": -0.500273, "C":-37.846772, "N":-54.583861, "O":-75.064579, "F":-99.718730}
U298 = {"H": -0.498857, "C":-37.845355, "N":-54.582445, "O":-75.063163, "F":-99.717314}
H    = {"H": -0.497912, "C":-37.844411, "N":-54.581501, "O":-75.062219, "F":-99.716370}
G298 = {"H": -0.510927, "C":-37.861317, "N":-54.598897, "O":-75.079532, "F":-99.733544}

def get_data(f):
    '''
    read in the file
    first line: # of atoms
    lines 3 to numAtoms+2: labels (first column)
    energies in line 2: column 12, 13, 14, 15
    '''
    lines = open(f, 'r').readlines()

    numAtoms = int(lines[0])
    labels   = []

    for i in range(2, numAtoms+2):
        labels.append(lines[i].split()[0])

    energies = np.array([ float(lines[1].split()[12]), float(lines[1].split()[13]), float(lines[1].split()[14]), float(lines[1].split()[15]) ])

    return labels, energies

def get_atomization_energies(labels, energies):
    '''
    loop trhough the labels and substract the atomization energy from the total energy using the dictionary and numpys -= operator
    '''
    for label in labels:
        energies[0] -= U0[label]
        energies[1] -= U298[label]
        energies[2] -= H[label]
        energies[3] -= G298[label]

    return energies[0], energies[1], energies[2], energies[3]

def main():
    directory = "xyz/"

    # define output file
    fout = open("atomization_energies.txt", 'w')

    # get all files in the directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # check if it is a file
        if os.path.isfile(f):
            # get atom labels and energies
            labels, energies  = get_data(f)
            # get the atomization energies
            u0, u298, h, g298 = get_atomization_energies(labels, energies)

            # write to file
            fout.write("{} {} {} {} {}\n".format(filename, u0, u298, h, g298))

    fout.close()


if __name__ == '__main__':
    main()

