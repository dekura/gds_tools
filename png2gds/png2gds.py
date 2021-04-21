'''
Author: Guojin Chen @ CUHK-CSE
Homepage: https://dekura.github.io/
Date: 2021-04-21 10:15:09
LastEditTime: 2021-04-21 10:36:46
Contact: cgjhaha@qq.com
Description: the simple png2gds script
'''

import re
import os
import glob
import argparse
import nazca as nd
from PIL import Image
from tqdm import tqdm
from pathlib import Path


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# parser.add_argument('--name', default='', type=str, help='experiment name')
# parser.add_argument('--in_folder', default='./png', type=str, help='the splited input image folder')
# parser.add_argument('--out_folder', default='./gds', type=str, help='the out gds folder')
parser.add_argument('--img_size', default=2048, type=int, help='the image size of your input, only sraf, a simple strategy')
parser.add_argument('--gt_mt_size', default=0.001, type=float, help='2048 * 0.001 = 2um')
parser.add_argument('--window_size', default=1024, type=int, help='the window image size of your design + mask')
parser.add_argument('--win_mt_size', default=0.001, type=float, help='1024 * 0.001 = 1um')
parser.add_argument('--split_id', default=0, type=int, help='folder split 0|1|2|3|4|5|6|...')
parser.add_argument('--threshold', default=0.6, type=float, help='threshold to filter the noisy point')

args = parser.parse_args()
# name = args.name

GT_IMAGE_SIZE = args.img_size
GT_MULTI_SIZE = args.gt_mt_size
THRESHOLD = args.threshold

MASK_LAYER = 1

mask_path = '/Users/dekura/chen/bei/projects/neurallevelsetOPC/develset_opc/analysis/test_data/Mask24_s900.png'
gds_path = '/Users/dekura/chen/bei/projects/neurallevelsetOPC/develset_opc/analysis/test_data/Mask24_s900.gds'

# img_mask = Image.open(mask_path).convert('L').transpose(Image.FLIP_TOP_BOTTOM)
nd.image(mask_path, size=GT_IMAGE_SIZE, pixelsize=GT_MULTI_SIZE, invert=True, layer=MASK_LAYER, threshold=THRESHOLD, cellname='mask').put(0)
nd.export_gds(filename=gds_path)