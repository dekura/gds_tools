# gds2img.py by Guojin.
###########################
import os
import gdspy
import sys
from pathlib import Path
from PIL import Image, ImageDraw
from tqdm import tqdm

clipsize = 2048
DESIGN_LAYER = 0
OPC_LAYER = 1
SRAF_LAYER = 2
CONTOUR_LAYER = 200


def gds2img(in_folder, in_file, out_folder):
    gds_in = in_folder / in_file
    gdsii = gdspy.GdsLibrary(unit=1e-9)
    gdsii.read_gds(gds_in, units='convert')
    cell = gdsii.top_level()[0]
    bbox = cell.get_bounding_box()
    opt_space = 40  # Leave space at border in case of edge correction

    width = int((bbox[1, 0] - bbox[0, 0]))
    height = int((bbox[1, 1] - bbox[0, 1]))
    w_offset = int(bbox[0, 0] - (clipsize - width) / 2)
    h_offset = int(bbox[0, 1] - (clipsize - height) / 2)

    sellayer = [1]  # Layer Number
    dtype = 0  # Layout Data Type
    polygon = []
    im = Image.new('1', (clipsize, clipsize))
    draw = ImageDraw.Draw(im)
    token = 1
    for i in range(len(sellayer)):
        try:
            polyset = cell.get_polygons(by_spec=True)[(sellayer[i], dtype)]
        except:
            token = 0
            print("Layer not found, skipping...")
            break
        for poly in range(len(polyset)):
            for points in range(len(polyset[poly])):
                polyset[poly][points][0] = int(polyset[poly][points][0] - w_offset)
                polyset[poly][points][1] = int(polyset[poly][points][1] - h_offset)
        for j in range(len(polyset)):
            tmp = tuple(map(tuple, polyset[j]))
            draw.polygon(tmp, fill=255)
    if token == 1:
        im = im.rotate(180, expand=True)
        # Apply flip (horizontal)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        filename = in_file + ".png"
        outpath = out_folder / filename
        im.save(outpath)


def main(in_folder, out_folder):
    in_folder = Path(in_folder).resolve()
    out_folder = Path(out_folder).resolve()
    out_folder.mkdir(parents=True, exist_ok=True)

    for dirname, dirnames, filenames in os.walk(in_folder):
        filenames = [f for f in filenames if f.endswith('.gds')]
        with tqdm(total=len(filenames), desc="Converting GDSII to Image") as pbar:
            for f in filenames:
                try:
                    gds2img(Path(dirname), f, out_folder)
                except Exception as e:
                    print(f"Error processing file {f}: {e}")
                pbar.update()


if __name__ == "__main__":
    # Infolder = sys.argv[1]
    # Outfolder = sys.argv[2]


    infolder = '/Users/guojinc/Downloads/datasets/nvdla-samples/cliptest'
    outfolder = '/Users/guojinc/Downloads/datasets/nvdla-samples-png/cliptest'

    for i in range(0, 32):
        infolder = f'/Users/guojinc/Downloads/datasets/nvdla-samples/clip{i}'
        outfolder = f'/Users/guojinc/Downloads/datasets/nvdla-samples-png/clip{i}'
        main(infolder, outfolder)
