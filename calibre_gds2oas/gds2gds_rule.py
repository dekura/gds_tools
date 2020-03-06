'''
@Author: Guojin Chen
@Date: 2019-11-13 02:53:10
@LastEditTime: 2020-03-02 17:31:28
@Contact: cgjhaha@qq.com
@Description: convert gds to gds, why? using calibre to merge some areas.
'''
### SRAF post processing rule
def make_gds2gds_rule(gds_path, oas_path):
    drc_code = """
LAYOUT PATH    '%s'
""" % (gds_path)
    drc_code += """
LAYOUT PRIMARY '*'
"""
    drc_code += """
DRC RESULTS DATABASE '%s' GDSII
""" % (oas_path)
    drc_code += """
PRECISION 1000
LAYOUT SYSTEM GDSII
DRC MAXIMUM RESULTS ALL
DRC MAXIMUM VERTEX 4000

LAYER MAP 2   datatype 0 1000 LAYER target     1000
LAYER MAP 21   datatype 0 1001 LAYER lay_nosraf    1001
LAYER MAP 22   datatype 0 1002 LAYER lay_bbox   1002
// LAYER MAP 50  datatype 0 1003 LAYER lay_gangt  1003

// #01: output results
OUT_target     {COPY target     } DRC CHECK MAP OUT_target    2     0
OUT_nosraf     {COPY lay_nosraf } DRC CHECK MAP OUT_nosraf    21    0
OUT_bbox       {COPY lay_bbox   } DRC CHECK MAP OUT_bbox      22    0
OUT_sraf       {not lay_nosraf lay_bbox  } DRC CHECK MAP OUT_sraf  23    0
"""
    return drc_code


def make_gds2oas_3layer_rule(gds_path, oas_path):
    drc_code = """
LAYOUT PATH    '%s'
""" % (gds_path)
    drc_code += """
LAYOUT PRIMARY '*'
"""
    drc_code += """
DRC RESULTS DATABASE '%s' OASIS
""" % (oas_path)
    drc_code += """
PRECISION 1000
LAYOUT SYSTEM GDSII
DRC MAXIMUM RESULTS ALL
DRC MAXIMUM VERTEX 4000

LAYER MAP 0   datatype 0 1000 LAYER target     1000
LAYER MAP 1   datatype 0 1001 LAYER lay_opc    1001
LAYER MAP 4   datatype 0 1002 LAYER lay_sraf   1002
// LAYER MAP 50  datatype 0 1003 LAYER lay_gangt  1003

// #01: output results
OUT_target     {COPY target     } DRC CHECK MAP OUT_target    0     0
OUT_opc        {COPY lay_opc    } DRC CHECK MAP OUT_opc       1     0
OUT_sraf       {COPY lay_sraf   } DRC CHECK MAP OUT_sraf      4     0
// OUT_gangt      {COPY lay_gangt  } DRC CHECK MAP OUT_gangt     50    0
"""
    return drc_code