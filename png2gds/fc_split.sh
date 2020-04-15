###
# @Author: Guojin Chen
 # @Date: 2019-11-19 20:45:42
 # @LastEditTime: 2020-03-24 13:27:00
 # @Contact: cgjhaha@qq.com
 # @Description:
###

# you only need to change this
# -------
testname=ovia1_e70_dr2mg_fc
# -------
python=/home/glchen/miniconda3/envs/py3/bin/python
$python split_results.py \
--name $testname \
--in_folder /home/glchen/datasets/dmo_results/$testname/test_latest/images \
--in_real_folder /home/glchen/datasets/dmo_results/$testname/testbg \
--out_folder /home/glchen/datasets/dmo_results_splited \
--split_num 16 \
--fake_B_postname _fake_B.png \
--real_A_postname .png
