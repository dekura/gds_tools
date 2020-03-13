"""
this file change
"""
import re
import os
import glob
import argparse
import nazca as nd
from PIL import Image
from tqdm import tqdm

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--name', default='', type=str, help='experiment name')
parser.add_argument('--in_folder', default='./png', type=str, help='the splited input image folder')
parser.add_argument('--out_folder', default='./gds', type=str, help='the out gds folder')
parser.add_argument('--img_size', default=1024, type=int, help='the image size of your input, design + sraf')
parser.add_argument('--window_size', default=1024, type=int, help='the window image size of your mask')
parser.add_argument('--split_id', default=0, type=int, help='folder split 0|1|2|3|4|5|6|...')
parser.add_argument('--threshold', default=0.6, type=float, help='threshold to filter the noisy point')
parser.add_argument('--fake_B_postname', default='_mbsraf.gds_lccout_CALI_fake_B.png', type=str,
    help='if fake b via1_mbsraf.gds_lccout_CALI_fake_B.png, so the post name'
)
parser.add_argument('--real_A_postname', default='_mbsraf.gds_lccout_CALI_real_A.png', type=str,
    help='if real A via1_mbsraf.gds_lccout_CALI_real_A.png, so the post name'
)
args = parser.parse_args()
name = args.name

if name == '':
    print('please input experiment name')
    raise TypeError



def mkdir_ifnotexists(path):
    if not os.path.exists(path):
        os.mkdir(path)


DESIGN_LAYER = 0
OPC_LAYER = 1
SRAF_LAYER = 4
CONTOUR_LAYER = 200
GAN_LAYER = 25
# gds size = img size * multi_size
# GT_IMAGE_SIZE = 2048
GT_IMAGE_SIZE = args.img_size
GT_MULTI_SIZE = 0.001

IMAGE_SIZE = args.window_size
MULTI_SIZE = 0.001
THRESHOLD = args.threshold

root_path = os.path.join(args.in_folder, args.name)
real_path = os.path.join(root_path, 'real_A')
opc_path = os.path.join(root_path,'opc_A')
opc_split_path = os.path.join(opc_path, str(args.split_id))
if not os.path.exists(opc_split_path):
    print(opc_split_path)
    raise NotADirectoryError
gray_path = os.path.join(root_path, 'gray')
mkdir_ifnotexists(gray_path)
out_path = args.out_folder
mkdir_ifnotexists(out_path)
out_root_path = os.path.join(out_path, args.name)
mkdir_ifnotexists(out_root_path)
gds_folder = os.path.join(out_root_path, 'gds')
mkdir_ifnotexists(gds_folder)

opc_A_list = glob.glob(os.path.join(opc_split_path, '*.png'))
    # entries = [entry  for entry in entries if entry == 'via6_mb_mb_lccout.oas.gds_real_A.png']
for entry in tqdm(opc_A_list):
    # print(entry)
    # pair_name = entry.replace('_mb_mb_lccout.oas.gds_opc_A.png','')
    # via1
    # pair_name = entry.replace('_mb_mb_lccout.oas.gds_real_A.png','')
    entry_name = os.path.basename(entry)
    pair_id = re.findall(r"\d+", entry_name)[0]
    pair_name = 'via'+ pair_id
    # print(entry.path)
    # gds_rel_path = 'gds/' + pair_name + '_rgb.gds'
    gds_name = pair_name+'_rgb.gds'
    # gds_path = gds_rel_path.replace('.png','.gds')
    # print(gds_path)
    # gds_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), gds_rel_path)
    gds_path = os.path.join(gds_folder, gds_name)
    # print(gds_path)
    # for design and sraf
    opc_A_name = pair_name + args.fake_B_postname
    opc_A_path = os.path.join(opc_split_path, opc_A_name)
    real_A_name = pair_name + args.real_A_postname
    real_A_path = os.path.join(real_path, real_A_name)
    # real_B_name = pair_name + '_mb_mb_lccout.oas.gds_real_B.png'
    # real_B_path = os.path.join(real_B_folder_path, real_B_name)
    if not os.path.isfile(real_A_path) or not os.path.isfile(opc_A_path):
        print(real_A_path)
        print(opc_A_path)
        # print(real_B_path)
        raise FileNotFoundError
    print('split id is : {}'.format(args.split_id))
    print('window img size is : {}'.format(args.window_size))
    print('multi size is : {}'.format(MULTI_SIZE))
    print(real_A_path)
    print(opc_A_path)
    print(gds_path)
    # img_size
    img_real_A = Image.open(real_A_path).convert('RGB').transpose(Image.FLIP_TOP_BOTTOM)
    # window_size
    img_opc_A = Image.open(opc_A_path).convert('RGB').transpose(Image.FLIP_TOP_BOTTOM)

    design_img = img_real_A.getchannel('R')
    design_img_name = pair_name + '_design.png'
    design_path = os.path.join(gray_path, design_img_name)

    sraf_img = img_real_A.getchannel('B')
    sraf_img_name = pair_name + '_sraf.png'
    sraf_path = os.path.join(gray_path, sraf_img_name)

    mask_img = img_opc_A.getchannel('G')
    mask_img_name = pair_name + '_mask.png'
    mask_path = os.path.join(gray_path, mask_img_name)
    # 256
    # real_mask_img = img_real_B.getchannel('G')
    # real_mask_img_name = pair_name + '_real_mask.png'
    # real_mask_path = os.path.join(gray_path, real_mask_img_name)
    # 2048
    # gt_mask_img = img_real_A.getchannel('G')
    # gt_mask_img_name = pair_name + '_gt_mask.png'
    # gt_mask_path = os.path.join(gray_path, gt_mask_img_name)
    design_img.save(design_path)
    sraf_img.save(sraf_path)
    mask_img.save(mask_path)
    # real_mask_img.save(real_mask_path)
    # gt_mask_img.save(gt_mask_path)

    nd.image(design_path, size=GT_IMAGE_SIZE, pixelsize=GT_MULTI_SIZE, invert=True, layer=DESIGN_LAYER, threshold=THRESHOLD, cellname='design').put(0)
    nd.image(mask_path, size=IMAGE_SIZE, pixelsize=MULTI_SIZE, invert=True, layer=OPC_LAYER, threshold=THRESHOLD, cellname='mask').put(0)
    nd.image(sraf_path, size=GT_IMAGE_SIZE, pixelsize=GT_MULTI_SIZE, invert=True, layer=SRAF_LAYER, threshold=THRESHOLD, cellname='sraf').put(0)
    # nd.image(real_mask_path, size=IMAGE_SIZE, pixelsize=MULTI_SIZE, invert=True, layer=50, threshold=THRESHOLD, cellname='real_mask').put(0)
    # nd.image(gt_mask_path, size=GT_IMAGE_SIZE, pixelsize=GT_MULTI_SIZE, invert=True, layer=75, threshold=THRESHOLD, cellname='gt_mask').put(0)
    nd.export_gds(filename=gds_path)

