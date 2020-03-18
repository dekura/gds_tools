###
# @Author: Guojin Chen
 # @Date: 2019-11-19 20:45:42
 # @LastEditTime: 2020-03-18 10:32:37
 # @Contact: cgjhaha@qq.com
 # @Description:
 ###
python=/home/glchen/miniconda3/envs/py3/bin/python
$python split_results.py \
--name ovia1_e70_dr2mg \
--in_folder /home/glchen/datasets/dmo_results/ovia1_e70_dr2mg/test_latest/images \
--in_real_folder /home/glchen/datasets/dmo_results/ovia1_e70_dr2mg/testbg \
--out_folder /home/glchen/datasets/dmo_results_splited \
--split_num 8 \
--real_A_postname _mbsraf.gds_lccout_CALI.png



