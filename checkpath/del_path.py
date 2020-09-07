import os
import sys
import gdspy
import pickle
import numpy as np

PATH_LAYER = 30


def del_path(gds_path):
    gds_in  = gds_path
    gdsii = gdspy.GdsLibrary()
    gdsii.read_gds(gds_in, units='convert')
    cell = gdsii.top_level()[0]
    # paths = cell.get_paths()
    cell.remove_paths(lambda p: p.layers[0] == 30 and p.points[0][0] == p.points[1][0] and p.points[0][1] == p.points[1][1])
    # gdspy.write_gds()
    # cell.to_gds('./removed.gds', 1)
    gdsii.write_gds('./asap7_removed.gds',)



if __name__ == '__main__':
    gds_path = '/Users/dekura/Downloads/Sha3AccelwBB.gds'
    del_path(gds_path)