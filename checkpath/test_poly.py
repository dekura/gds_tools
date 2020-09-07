import os
import sys
import gdspy
import pickle
import numpy as np


fp = './polyset_b'



if __name__ == '__main__':
    with open(fp, 'rb') as f:
        polyset_np = pickle.load(f)
    # print(polyset_np[0:10])

    for poly in polyset_np:
        print(len(poly))
        # if len(poly) < 4:

