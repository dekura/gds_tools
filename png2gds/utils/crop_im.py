'''
@Author: Guojin Chen
@Date: 2020-03-17 10:47:52
@LastEditTime: 2020-03-17 10:54:58
@Contact: cgjhaha@qq.com
@Description: crop 2048 to 1024 image
'''

import os
import glob
import argparse
import numpy as np
from tqdm import tqdm
from PIL import Image

infolder = '/Users/dekura/Downloads/testnewpng2gds/opc_A/1/'

restr = os.path.join(infolder, '*.png')

imglist = glob.glob(restr)

for img in tqdm(imglist):
    img_name = os.path.basename(img)
    left = 512
    top = left
    right = left + 1024
    down = top + 1024
    im = Image.open(img).convert('RGB')
    im_crop = im.crop((left, top, right, down))
    im_crop_name = img_name.replace('.png', '_fake_B.png')
    im_crop_path = os.path.join(infolder, im_crop_name)
    print(im_crop_path)
    im_crop.save(im_crop_path)
