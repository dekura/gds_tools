'''
@Author: Guojin Chen
@Date: 2020-04-09 13:00:44
@LastEditTime: 2020-04-09 13:07:02
@Contact: cgjhaha@qq.com
@Description: cut gds
'''
###########################
import gdspy
import numpy as np
import sys
import os
from tqdm import tqdm
from progress.bar import Bar
clipsize = 2048

SCALE_LAYER = 40
VIA_LAYER = 2
NO_SRAF_LAYER = 21
BBOX_LAYER = 22
ALLOW_SRAF_LAYER = 23
PRECISION = 1000

'''
1. 500
'''

def scale_rect_by_poly(poly):
    xl = poly[0][0]  # 25
    xr = poly[1][0]  # 75
    yd = poly[0][1]  # 25
    yu = poly[2][1]  # 75
    point1 = np.array([xl-10/PRECISION, yd-10/PRECISION])
    point2 = np.array([xr+10/PRECISION, yu+10/PRECISION])
    return (point1, point2)

def sraf_area_by_poly(poly):
    xl = poly[0][0]  # 25
    xr = poly[1][0]  # 75
    yd = poly[0][1]  # 25
    yu = poly[2][1]  # 75
    point1 = np.array([xl-110/PRECISION, yd-110/PRECISION])
    point2 = np.array([xr+110/PRECISION, yu+110/PRECISION])
    return (point1, point2)

def center_by_poly(poly):
    xl = poly[0][0]  # 25
    xr = poly[1][0]  # 75
    yd = poly[0][1]  # 25
    yu = poly[2][1]  # 75
    x = (xl + xr)/2
    y = (yd + yu)/2
    center = np.array([x, y])
    return center

def scale_gds(Infolder, Infile, ImgOut):
    GdsIn = os.path.join(Infolder, Infile)
    gdsii   = gdspy.GdsLibrary()
    lib_out = gdspy.GdsLibrary()

    gdsii.read_gds(GdsIn,units='convert')
    cell    = gdsii.top_level()[0]
    cell_out = lib_out.new_cell('TOP')
    bbox    = cell.get_bounding_box()
    # bbox:  [[     0.      0.]
    #        [148400. 146000.]]
    # print('width: ', width)
    # print('height: ', height)
    bbox_out = gdspy.Rectangle(bbox[0],bbox[1], layer=BBOX_LAYER)
    cell_out.add(bbox_out)
    sellayer = [SCALE_LAYER] #Layer Number
    dtype = 0  #Layout Data Type
    token = 1
    for i in tqdm(range(len(sellayer))):
        try:
            polyset = cell.get_polygons(by_spec=True)[(sellayer[i],dtype)]
        except:
            token=0
            print("Layer not found, skipping...")
            break
        centers = np.zeros((len(polyset), 2))
        for poly in range(0, len(polyset)):
            # polyset[poly]
            # [[121925.  56675.]
            # [121975.  56675.]
            # [121975.  56725.]
            # [121925.  56725.]]
            # print(polyset[poly][0])
            rect_points = scale_rect_by_poly(polyset[poly])
            sraf_points = sraf_area_by_poly(polyset[poly])
            # print(rect_points[0])
            rect = gdspy.Rectangle(rect_points[0], rect_points[1], layer=VIA_LAYER)
            sraf_rect = gdspy.Rectangle(sraf_points[0], sraf_points[1], layer=NO_SRAF_LAYER)
            center = center_by_poly(polyset[poly])
            cell_out.add(rect)
            cell_out.add(sraf_rect)
            centers[poly] = center
    if token == 1:
        filename = Infile.replace('.gds', '_scaled.gds')
        outpath  = os.path.join(ImgOut,filename)
        lib_out.write_gds(outpath)
        # txtname = Infile.replace('.gds', '_centers.txt')
        # outtxtpath  = os.path.join(ImgOut,txtname)
        # lib_out.write_gds(outpath)
        # np.savetxt(outtxtpath, centers, fmt='%.5f', delimiter=' ')



# Infolder = sys.argv[1]
# Outfolder= sys.argv[2]
dir = os.path.abspath(os.path.dirname(__file__))
Infolder = os.path.join(dir,'input_gds')
# Infolder = '/Users/dekura/Desktop/opc/design-april'
Outfolder = os.path.join(dir,'output_gds')

for dirname, dirnames, filenames in os.walk(Infolder):
    bar=Bar("Scaling GDSII", max=len(filenames))
    for f in range(0, len(filenames)):
        scale_gds(Infolder, filenames[f], Outfolder)
        # try:
        #     scale_gds(Infolder, filenames[f], Outfolder)
        # except:
        #     bar.next()
        #     continue
        bar.next()
bar.finish()
print('all rect scaled')