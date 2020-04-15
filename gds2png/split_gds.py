'''
@Author: Guojin Chen
@Date: 2020-03-22 14:45:14
@LastEditTime: 2020-03-22 15:01:48
@Contact: cgjhaha@qq.com
@Description: split gds folder for sraf insertation
'''

import os
import re
import glob
import shutil
import argparse
from tqdm import tqdm
from random import sample


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--name', default='', type=str, help='experiment name')
parser.add_argument('--in_folder', default='', type=str, help='in folder, we take m')
parser.add_argument('--out_folder', default='./gds', type=str, help='out gds folder')
parser.add_argument('--split_num', default=4, type=int, help='how many folder do you want to split')
parser.add_argument('--max_datanum', default=2100, type=int, help='max data num')
parser.add_argument('--gds_postname', default='.gds', type=str,
    help='if via1.gds, so the post name'
)
args = parser.parse_args()
print(args)
name = args.name

if name == '':
    print('please input experiment name')
    raise ValueError


def mkdir_ifnotexists(path):
    if not os.path.exists(path):
        os.mkdir(path)
def raiseErr_ifnotexists(*paths):
    for path in paths:
        if not os.path.exists(path):
            print('Not found path :{}'.format(path))
            raise FileExistsError

def get_convert_list(args):
    base_folder = args.in_folder
    restr = '*{}'.format(args.gds_postname)
    base_folder_list = glob.glob(os.path.join(base_folder, restr))
    should_convert_list = []
    for file in base_folder_list:
        filename = os.path.basename(file)
        file_id = re.findall(r"\d+", filename)[0]
        should_convert_list.append(int(file_id))
    should_convert_list.sort()
    should_convert_list = sample(should_convert_list, args.max_datanum)
    print('total data : {}'.format(len(should_convert_list)))
    return should_convert_list

def split_results(test_convert_ids, args):
    if not os.path.exists(args.in_folder):
        print('in_floder: {}'.format(args.in_folder))
        raise NotADirectoryError
    # in_list = os.listdir(in_folder)
    in_folder = args.in_folder
    mkdir_ifnotexists(args.out_folder)
    out_folder = os.path.join(args.out_folder, name)
    mkdir_ifnotexists(out_folder)
    out_gds_path = os.path.join(out_folder, 'gds')
    mkdir_ifnotexists(out_gds_path)

    for id in tqdm(test_convert_ids):
        img_opc_A = 'via{}{}'.format(id, args.gds_postname)
        img_opc_A_path = os.path.join(in_folder, img_opc_A)
        raiseErr_ifnotexists(img_opc_A_path)
        split_id = id%args.split_num
        out_split_path = os.path.join(out_gds_path, str(split_id))
        mkdir_ifnotexists(out_split_path)
        shutil.copyfile(img_opc_A_path, os.path.join(out_split_path, img_opc_A))



if __name__ == '__main__':
    test_convert_ids = get_convert_list(args)
    split_results(test_convert_ids, args)
