'''
@Author: Guojin Chen
@Date: 2019-11-11 21:41:03
@LastEditTime: 2019-11-14 21:46:51
@Contact: cgjhaha@qq.com
@Description: input one gds, output one 2048*2048 rgb image
'''
# gds to png by guojin, this trans design to red channel
###########################
import gdspy
import sys
import os
from PIL import Image, ImageDraw
from progress.bar import Bar
clipsize = 2048

DESIGN_LAYER = 0
OPC_LAYER = 1
SRAF_LAYER = 2
CONTOUR_LAYER = 200


def gds2img(Infolder, Infile, ImgOut):
    GdsIn = os.path.join(Infolder, Infile)
    gdsii   = gdspy.GdsLibrary(unit=1e-9)
    gdsii.read_gds(GdsIn,units='convert')
    cell    = gdsii.top_level()[0]
    bbox    = cell.get_bounding_box()
    opt_space=40 #Leave space at border in case of edge correction

    width = int((bbox[1,0]-bbox[0,0]))
    height= int((bbox[1,1]-bbox[0,1]))
    w_offset = int(bbox[0,0] - (clipsize-width)/2)
    h_offset = int(bbox[0,1] - (clipsize-height)/2)


    sellayer = [DESIGN_LAYER, OPC_LAYER, SRAF_LAYER] #Layer Number
    dtype = 0  #Layout Data Type
    polygon  = []
    im = Image.new("RGB", (clipsize, clipsize))
    im_r = im.getchannel('R')
    im_g = im.getchannel('G')
    im_b = im.getchannel('B')
    draw_r = ImageDraw.Draw(im_r)
    draw_g = ImageDraw.Draw(im_g)
    draw_b = ImageDraw.Draw(im_b)
    token = 1
    for i in range(len(sellayer)):
        try:
            polyset = cell.get_polygons(by_spec=True)[(sellayer[i],dtype)]
        except:
            token=0
            # print("Layer not found, skipping...")
            break
        for poly in range(0, len(polyset)):
            for points in range(0, len(polyset[poly])):
                polyset[poly][points][0]=int(polyset[poly][points][0]-w_offset)
                polyset[poly][points][1]=int(polyset[poly][points][1]-h_offset)
        for j in range(0, len(polyset)):
            tmp = tuple(map(tuple, polyset[j]))
            if sellayer[i] == DESIGN_LAYER:
                draw_r.polygon(tmp, fill=255)
            if sellayer[i] == OPC_LAYER:
                draw_g.polygon(tmp, fill=255)
            if sellayer[i] == SRAF_LAYER:
                draw_b.polygon(tmp, fill=255)
    if token == 1:
        filename = Infile+".png"
        outpath  = os.path.join(ImgOut,filename)
        im = Image.merge('RGB', [im_r, im_g, im_b])
        im.save(outpath)



# Infolder = sys.argv[1]
# Outfolder= sys.argv[2]

# Infolder = os.path.join(os.path.abspath(os.path.dirname(__file__)),'test_sample')
# Infolder = '/Users/dekura/Desktop/opc/design-april'
# Outfolder = os.path.join(os.path.abspath(os.path.dirname(__file__)),'test_sample_output/mask_sraf')
Infolder = '/Users/dekura/Desktop/opc/datasets/myresults/gds/'
Outfolder = '/Users/dekura/Desktop/opc/datasets/myresults/maskg_designr_srafb_png_2048'

if not os.path.isdir(Outfolder):
    os.mkdir(Outfolder)

for dirname, dirnames, filenames in os.walk(Infolder):
    bar=Bar("Converting GDSII to Image", max=len(filenames))
    for f in range(0, len(filenames)):
        try:
            gds2img(Infolder, filenames[f], Outfolder)
        except:
            bar.next()
            continue
        bar.next()
bar.finish()