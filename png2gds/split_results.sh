###
# @Author: Guojin Chen
 # @Date: 2019-11-19 20:45:42
 # @LastEditTime: 2020-03-22 12:59:59
 # @Contact: cgjhaha@qq.com
 # @Description:
 ###
python=/home/glchen/miniconda3/envs/py3/bin/python
$python split_results.py \
--name ovia2pixhd_e100_dr2mg \
--in_folder /home/glchen/datasets/dmo_results/ovia2pixhd_e100_dr2mg/test_latest/images \
--in_real_folder /home/glchen/datasets/dmo_results/ovia2pixhd_e100_dr2mg/testbg \
--out_folder /home/glchen/datasets/dmo_results_splited \
--split_num 8 \
--fake_B_postname _mbsraf.gds_lccout_CALI_synthesized_image.png \
--real_A_postname _mbsraf.gds_lccout_CALI.png



