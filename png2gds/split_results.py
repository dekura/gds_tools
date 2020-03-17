'''
@Author: Guojin Chen
@Date: 2019-11-14 12:29:14
@LastEditTime: 2020-03-17 14:19:18
@Contact: cgjhaha@qq.com
@Description: this file split the trained results to 2 png folder
    in order to get the gds file.

    out_folder
        real_A (mostly 2048*2048)
        opc_A (mostly 1024*1024)
'''
import os
import re
import glob
import shutil
import argparse
from tqdm import tqdm


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--name', default='', type=str, help='experiment name')
parser.add_argument('--in_folder', default='', type=str, help='in folder, we take m')
parser.add_argument('--in_real_folder', default='', type=str, help='the folder store the 2048*2048 dms, we take ds')
parser.add_argument('--out_folder', default='./gds', type=str, help='out gds folder')
parser.add_argument('--split_num', default=7, type=int, help='how many folder do you want to split')
parser.add_argument('--fake_B_postname', default='_mbsraf.gds_lccout_CALI_fake_B.png', type=str,
    help='if fake b via1_mbsraf.gds_lccout_CALI_fake_B.png, so the post name'
)
parser.add_argument('--real_A_postname', default='_mbsraf.gds_lccout_CALI_real_A.png', type=str,
    help='if real A via1_mbsraf.gds_lccout_CALI_real_A.png, so the post name'
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

def get_convert_list():
    base_folder = args.in_folder
    restr = '*_fake_B.png'
    base_folder_list = glob.glob(os.path.join(base_folder, restr))
    should_convert_list = []
    for file in base_folder_list:
        filename = os.path.basename(file)
        file_id = re.findall(r"\d+", filename)[0]
        should_convert_list.append(int(file_id))
    should_convert_list.sort()
    return should_convert_list

def split_results(test_convert_ids, args):
    if not os.path.exists(args.in_folder) or not os.path.exists(args.in_real_folder):
        print('in_floder: {}'.format(args.in_folder))
        print('in_real_folder: {}'.format(args.in_real_folder))
        raise NotADirectoryError
    # in_list = os.listdir(in_folder)
    in_folder = args.in_folder
    out_folder = args.out_folder
    in_real_folder = args.in_real_folder
    fake_B_postname = args.fake_B_postname
    real_A_postname = args.real_A_postname
    out_opc_A_path = os.path.join(out_folder, 'opc_A')
    out_real_A_path = os.path.join(out_folder, 'real_A')
    mkdir_ifnotexists(out_opc_A_path)
    mkdir_ifnotexists(out_real_A_path)

    for id in tqdm(test_convert_ids):
        img_opc_A = 'via{}{}'.format(id, fake_B_postname)
        img_real_A = 'via{}{}'.format(id, real_A_postname)
        img_opc_A_path = os.path.join(in_folder, img_opc_A)
        img_real_A_path = os.path.join(in_real_folder, img_real_A)
        raiseErr_ifnotexists(img_opc_A_path, img_real_A_path)
        split_id = id%args.split_num
        out_split_path = os.path.join(out_opc_A_path, str(split_id))
        mkdir_ifnotexists(out_split_path)
        shutil.copyfile(img_opc_A_path, os.path.join(out_split_path, img_opc_A))
        shutil.copyfile(img_real_A_path, os.path.join(out_real_A_path, img_real_A))



if __name__ == '__main__':
    mkdir_ifnotexists(args.out_folder)
    out_folder = os.path.join(args.out_folder, name)
    mkdir_ifnotexists(out_folder)
    test_convert_ids = get_convert_list()
    split_results(test_convert_ids, args)