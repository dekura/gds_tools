###
# @Author: Guojin Chen
 # @Date: 2019-11-19 20:45:42
 # @LastEditTime: 2020-04-15 14:47:12
 # @Contact: cgjhaha@qq.com
 # @Description:
###

# you only need to change this
# -------
testname=ovia2pixhd_e100_1024_local_dr2mg_fc
testname=$1
# -------
python=/home/glchen/miniconda3/envs/py3/bin/python
$python split_results.py \
--name $testname \
--in_folder /home/glchen/datasets/dmo_results/$testname/test_latest/images \
--in_real_folder /home/glchen/datasets/dmo_results/$testname/testbg \
--out_folder /home/glchen/datasets/dmo_results_splited \
--split_num 2 \
--fake_B_postname _synthesized_image.png \
--real_A_postname .png \
--is_fc
