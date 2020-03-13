import gdspy
import sys
import os
from PIL import Image, ImageDraw
from progress.bar import Bar
import numpy as np
clipsize = 2000

DESIGN_LAYER = 0
OPC_LAYER = 1
SRAF_LAYER = 4
CONTOUR_LAYER = 200
GAN_LAYER = 25


R_OFFSET = 0.008
BOUNDARY_SIZE = 0.885
# def merge_p2r(bbox_lists):
#     points_clusters = []
#     for bbox in bbox_lists:
        # [[-885. -885.]
        #  [ 885.  885.]]
        # [[xld, yld]
        #  [xru, yru]]
        # pass

class RectPoints(object):
    def __init__(self, xld, yld, xru, yru):
        self.xld = float(xld)
        self.yld = float(yld)
        self.xru = float(xru)
        self.yru = float(yru)
        self.midx = (xld + xru)/2
        self.midy = (yld + yru)/2

# class FinalRect(object):
#     def __init__(self, RectPoints):
#         self.RectPoints = RectPoints

class GroupByXArr(object):
    def __init__(self, midx):
        self.midx = midx
        self.midxRPArr = []
        self.FinalRects = []

    def appendToMidX(self, RectPoints):
        self.midxRPArr.append(RectPoints)
        self.sortRPByY()

    def sortRPByY(self):
        self.midxRPArr.sort(key=takeMidY)

    def getFinalRects(self):
        final_rects = []
        midy_nums = len(self.midxRPArr)
        mdxa = self.midxRPArr
        start_index = 0
        for i in range(0, midy_nums - 1):
            if checkSuddenJump(mdxa[i].midy, mdxa[i+1].midy):
                self.mergeToFinalRect(start_index, i)
                start_index = i+1

        self.mergeToFinalRect(start_index, midy_nums - 1)

    def mergeToFinalRect(self, from_index, to_index):
        temRects = self.midxRPArr[from_index:to_index+1]
        # l  = len(temRects)
        orp = RectPoints(temRects[0].xld, temRects[0].yld, temRects[-1].xru, temRects[-1].yru)
        self.FinalRects.append(orp)


def checkSuddenJump(previous_y, new_y):
    if new_y - previous_y > R_OFFSET:
        return True
    else:
        return False


def takeMidX(elem):
    return elem.midx

def takeMidY(elem):
    return elem.midy

def getFinalRectsByCellName(gds_path, cell_name):
    gdsii   = gdspy.GdsLibrary(unit=1e-6)
    gdsii.read_gds(gds_path, units='convert')
    opc_cell = gdsii.cell_dict
    design = opc_cell[cell_name]
    design_polygons = design.polygons
    RectPointsArr = []
    for p in design_polygons:
        bbox = p.get_bounding_box()
        # print(bbox)
        if float(bbox[0][0]) == -BOUNDARY_SIZE and float(bbox[1][0]) == BOUNDARY_SIZE:
            print('REMOVE 855')
            continue
        rp = RectPoints(bbox[0][0],bbox[0][1],bbox[1][0], bbox[1][1])
        RectPointsArr.append(rp)

    RectPointsArr.sort(key=takeMidX)
    RectPointsMidXArr = list(set([x.midx for x in RectPointsArr]))

    GroupByXArrContainer = {}
    for rp_midx in RectPointsMidXArr:
        GroupByXArrContainer[str(rp_midx)] = GroupByXArr(rp_midx)
    for rp in RectPointsArr:
        GroupByXArrContainer[str(rp.midx)].appendToMidX(rp)
    for key, v in GroupByXArrContainer.items():
        v.getFinalRects()
    FinalRectArr = []
    for key, v in GroupByXArrContainer.items():
        for fr in v.FinalRects:
            FinalRectArr.append(fr)

    return FinalRectArr



def add_rect(FRs, cell, layerNum):
    for fr in FRs:
        pld = (fr.xld, fr.yld)
        pru = (fr.xru, fr.yru)
        ret = gdspy.Rectangle(pld, pru, layer=layerNum)
        cell.add(ret)

def draw_final_rects(in_gds_path, out_gds_path):
    # gdsii   = gdspy.GdsLibrary(unit=1e-6)
    gdspy.current_library = gdspy.GdsLibrary(unit=1e-6)
    cell = gdspy.Cell('TOP')
    design_FRs, mask_FRs, sraf_FRs = getAllFinalRects(in_gds_path)
    add_rect(design_FRs, cell, DESIGN_LAYER)
    add_rect(mask_FRs, cell, OPC_LAYER)
    add_rect(sraf_FRs, cell, SRAF_LAYER)
    gdspy.write_gds(out_gds_path)


def getAllFinalRects(in_gds_path):
    # gds_path = './gds/via1_rgb.gds'
    gds_path = in_gds_path
    design_FRs = getFinalRectsByCellName(gds_path, 'design')
    mask_FRs = getFinalRectsByCellName(gds_path, 'mask')
    sraf_FRs = getFinalRectsByCellName(gds_path, 'sraf')

    # for key in All_FRs:
        # print(len(key))
    return design_FRs, mask_FRs, sraf_FRs

# getAllFinalRects()
# draw_final_rects()


gds_folder_path = 'gds'
gds_folder_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), gds_folder_path)
out_folder_path = 'out'
out_folder_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), out_folder_path)


with os.scandir(gds_folder_path) as entries:
    for entry in entries:
        if entry.name.endswith('.gds'):
            print("now processing {}".format(entry.name))
            in_gds_path = os.path.join(gds_folder_path, entry.name)
            out_gds_path = os.path.join(out_folder_path, entry.name)
            draw_final_rects(in_gds_path, out_gds_path)
