###
 # @Author: Guojin Chen
 # @Date: 2020-05-07 14:11:22
 # @LastEditTime: 2020-05-07 14:14:32
 # @Contact: cgjhaha@qq.com
 # @Description: split for ganopc
###


# you only need to change this
# -------
testname=
# -------
python=/home/glchen/miniconda3/envs/py3/bin/python
$python split_results.py \
--name $testname \
--in_folder /home/glchen/datasets/dmo_results/$testname/images \
--in_real_folder home/glchen/datasets/dmo_results/$testname/images \
--out_folder /home/glchen/datasets/dmo_results_splited \
--split_num 8 \
--fake_B_postname _mbsraf.gds_lccout_CALI_fake_B.png \
--real_A_postname _mbsraf.gds_lccout_CALI_real_A.png

