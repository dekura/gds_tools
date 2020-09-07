import os
import sys
import gdspy
import pickle
import numpy as np

PATH_LAYER = 30


def checkpath(gds_path):
    gds_in  = gds_path
    gdsii = gdspy.GdsLibrary()
    gdsii.read_gds(gds_in, units='convert')
    cell = gdsii.top_level()[0]
    paths = cell.get_paths()
    with open('./paths_b', 'wb') as f:
        pickle.dump(paths, f)


    dtype = 0
    polyset = cell.get_polygons(by_spec=True)[(PATH_LAYER, dtype)]

    print(polyset[0])
    polyset_np = np.array(polyset)
    with open('./polyset_b', 'wb') as f:
        pickle.dump(polyset_np, f)

    print(polyset_np[0:10])


if __name__ == '__main__':
    gds_path = '/Users/dekura/Downloads/Sha3AccelwBB.gds'
    checkpath(gds_path)