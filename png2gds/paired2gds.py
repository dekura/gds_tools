"""
this file change
"""
import os
import nazca as nd
from PIL import Image
from tqdm import tqdm
import re


DESIGN_LAYER = 0
OPC_LAYER = 1
SRAF_LAYER = 4
CONTOUR_LAYER = 200
GAN_LAYER = 25

# gds size = img size * multi_size
MULTI_SIZE = 0.008


real_path = 'png/real_A'
real_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), real_path)

opc_path = 'png/opc_A'
opc_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), opc_path)

gray_path = 'gray'
gray_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), gray_path)

real_B_folder_path = 'png/real_B'
real_B_folder_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), real_B_folder_path)

with os.scandir(real_path) as entries:
    for entry in tqdm(entries):
        if entry.name.endswith('.png'):
            # print(entry.name)
            # pair_name = entry.name.replace('_mb_mb_lccout.oas.gds_opc_A.png','')
            # via1
            # pair_name = entry.name.replace('_mb_mb_lccout.oas.gds_real_A.png','')
            pair_id = re.findall(r"\d+", entry.name)[0]
            pair_name = 'via'+ pair_id
            # print(entry.path)
            gds_rel_path = 'gds/' + pair_name + '_rgb.gds'
            # gds_path = gds_rel_path.replace('.png','.gds')
            # print(gds_path)
            gds_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), gds_rel_path)
            # print(gds_path)

            # for design and sraf
            opc_A_name = pair_name + '_mb_mb_lccout.oas.gds_fake_B.png'
            opc_A_path = os.path.join(opc_path, opc_A_name)
            real_A_name = entry.name
            real_A_path = os.path.join(real_path, real_A_name)
            real_B_name = pair_name + '_mb_mb_lccout.oas.gds_real_B.png'
            real_B_path = os.path.join(real_B_folder_path, real_B_name)

            if not os.path.isfile(real_A_path) or not os.path.isfile(opc_A_path) or not os.path.isfile(real_B_path):
                print(real_A_path)
                print(opc_A_path)
                print(real_B_path)
                raise FileNotFoundError

            img_real_A = Image.open(real_A_path).convert('RGB').transpose(Image.FLIP_TOP_BOTTOM)
            img_opc_A = Image.open(opc_A_path).convert('RGB').transpose(Image.FLIP_TOP_BOTTOM)
            img_real_B = Image.open(real_B_path).convert('RGB').transpose(Image.FLIP_TOP_BOTTOM)

            design_img = img_real_A.getchannel('R')
            design_img_name = pair_name + '_design.png'
            design_path = os.path.join(gray_path, design_img_name)

            sraf_img = img_real_A.getchannel('B')
            sraf_img_name = pair_name + '_sraf.png'
            sraf_path = os.path.join(gray_path, sraf_img_name)

            mask_img = img_opc_A.getchannel('G')
            mask_img_name = pair_name + '_mask.png'
            mask_path = os.path.join(gray_path, mask_img_name)

            real_mask_img = img_real_B.getchannel('G')
            real_mask_img_name = pair_name + '_real_mask.png'
            real_mask_path = os.path.join(gray_path, real_mask_img_name)

            design_img.save(design_path)
            sraf_img.save(sraf_path)
            mask_img.save(mask_path)
            real_mask_img.save(real_mask_path)

            nd.image(design_path, pixelsize=MULTI_SIZE, invert=True, layer=0, box_layer=22, threshold=0.5, cellname='design').put(0)
            nd.image(mask_path, pixelsize=MULTI_SIZE, invert=True, layer=1, box_layer=22, threshold=0.5, cellname='mask').put(0)
            nd.image(sraf_path, pixelsize=MULTI_SIZE, invert=True, layer=4, box_layer=22, threshold=0.5, cellname='sraf').put(0)
            nd.image(real_mask_path, pixelsize=MULTI_SIZE, invert=True, layer=50, box_layer=22, threshold=0.5, cellname='real_mask').put(0)


            # nd.image(design_path, pixelsize=MULTI_SIZE, invert=True, layer=0, threshold=0.5, cellname='design').put(0)
            # nd.image(mask_path, pixelsize=MULTI_SIZE, invert=True, layer=1, threshold=0.5, cellname='mask').put(0)
            # nd.image(sraf_path, pixelsize=MULTI_SIZE, invert=True, layer=4, threshold=0.5, cellname='sraf').put(0)
            # nd.image(real_mask_path, pixelsize=MULTI_SIZE, invert=True, layer=50, threshold=0.5, cellname='real_mask').put(0)
            # nd.image(gray_path, invert=True, layer=1, box_layer=4,threshold=0.8).put()
            nd.export_gds(filename=gds_path)
            # print(nd.netlist.Cell('design'))
# image_path = './png/via1_mb_mb_lccout.oas.gds.png'

# nd.image(image_path, size=4000).put()

# nd.export_gds()
