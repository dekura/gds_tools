import os
import sys
import gdspy
import pickle
import numpy as np


fp = './paths_b'



if __name__ == '__main__':
    with open(fp, 'rb') as f:
        paths = pickle.load(f)
    # print(polyset_np[0:10])
    for p in paths:
        # print(dir(p))
        # print(p.layers)
        if p.layers[0] == 30:
            # print(p.points)
            sx = p.points[0][0]
            sy = p.points[0][1]
            ex = p.points[1][0]
            ey = p.points[1][1]
            if sx == ex and sy == ey:
                print(p.points)
                print('del')
    # print(paths)


    # for poly in polyset_np:
        # print(len(poly))
        # if len(poly) < 4:

