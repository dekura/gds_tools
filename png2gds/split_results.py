'''
@Author: Guojin Chen
@Date: 2019-11-14 12:29:14
@LastEditTime: 2019-11-25 09:43:15
@Contact: cgjhaha@qq.com
@Description: this file split the trained results to three png folder
    in order to get the gds file.
'''
import os
import re
import shutil
import argparse
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('--name', default='', type=str, help='experiment name')
parser.add_argument('--in_folder', default='', type=str, help='in folder')
parser.add_argument('--split_num', default=7, type=int, help='how many folder do you want to split')
parser.add_argument('--is_gan2gan', dest='is_gan2gan', default=False, action='store_true')
args = parser.parse_args()
print(args)
name = args.name

if name == '':
    print('please input experiment name')
    raise EnvironmentError


def mkdir_ifnotexists(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_convert_list():
    base_folder = '/Users/dekura/Desktop/opc/datasets/design_contour_paired/B/test'
    base_folder_list = os.listdir(base_folder)
    should_convert_list = []
    for file in base_folder_list:
        if file.endswith('.png'):
            file_id = re.findall(r"\d+", file)[0]
            should_convert_list.append(int(file_id))
    should_convert_list.sort()
    return should_convert_list


def split_results(in_folder, out_folder, test_convert_ids):
    if not os.path.exists(in_folder) or not os.path.exists(out_folder):
        print('in_floder: {}'.format(in_folder))
        print('out_folder: {}'.format(out_folder))
        raise NotADirectoryError
    if os.path.isfile(os.path.join(in_folder,'.DS_Store')):
        os.remove(os.path.join(in_folder,'.DS_Store'))
    # in_list = os.listdir(in_folder)
    for id in tqdm(test_convert_ids):
        # img_real_A = 'via{}_mb_mb_lccout.oas.gds_real_A.png'.format(id)

        img_opc_A = 'via{}_mb_mb_lccout.oas.gds_fake_B.png'.format(id)
        # img_real_B = 'via{}_mb_mb_lccout.oas.gds_real_B.png'.format(id)
        if args.is_gan2gan:
            img_opc_A = 'via{}_mb_mb_lccout.oas.gds_opc_A.png'.format(id)
        # copy file
        # img_real_A_path = os.path.join(in_folder, img_real_A)
        img_opc_A_path = os.path.join(in_folder, img_opc_A)

        if args.is_gan2gan:
            img_opc_A = img_opc_A.replace('_opc_A.png', '_fake_B.png')
        # img_real_B_path = os.path.join(in_folder, img_real_B)

        # if not os.path.isfile(img_real_A_path) or not os.path.isfile(img_opc_A_path) or not os.path.isfile(img_real_B_path):
        #     raise FileNotFoundError
        # if not os.path.isfile(img_opc_A_path) or not os.path.isfile(img_real_B_path):
        #     raise FileNotFoundError
        if not os.path.isfile(img_opc_A_path):
            raise FileNotFoundError
        # shutil.copyfile(img_real_A_path, os.path.join(out_folder, 'real_A', img_real_A))
        split_id = id%args.split_num
        out_opc_A_path = os.path.join(out_folder, 'opc_A')
        mkdir_ifnotexists(out_opc_A_path)
        out_split_path = os.path.join(out_opc_A_path, str(split_id))
        mkdir_ifnotexists(out_split_path)
        shutil.copyfile(img_opc_A_path, os.path.join(out_split_path, img_opc_A))
        # shutil.copyfile(img_real_B_path, os.path.join(out_folder, 'real_B', img_real_B))

# test_convert_ids = [
#     1, 7, 11, 1003, 1008, 1009, 3421, 3002, 3004, 3006, 519, 975
# ]



if __name__ == '__main__':
    # in_folder = '/Users/dekura/Downloads/aresults/dcupp_naive6_100epoch_c3_dr2mg_only/test_latest/images/'
    # out_folder = '/Users/dekura/chen/py/design_mask2gds_2048/png'
    # in_folder = '/Users/dekura/Downloads/aresults/dcupp_naive6_100epoch_dr2mg_2048/test_latest/images'
    # in_folder = '/Users/dekura/Downloads/aresults/epe_50epoch_2048_256/test_latest/images'
    # in_folder = '/Users/dekura/Downloads/aresults/ganopc_upp_base_50epoch/test_50/images/'
    in_folder = args.in_folder
    out_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'png')
    out_folder = os.path.join(out_folder, name)
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    test_convert_ids = get_convert_list()
    # test_convert_ids = [1,2,3,4,5,6,7,8,9,10]
    # print(test_convert_ids)
    split_results(in_folder, out_folder, test_convert_ids)
    # print(get_convert_list())