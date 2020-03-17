### 
# @Author: Guojin Chen
 # @Date: 2019-11-19 20:45:42
 # @LastEditTime: 2020-03-17 14:11:03
 # @Contact: cgjhaha@qq.com
 # @Description:
 ###
python=/home/glchen/miniconda3/envs/py3/bin/python
$python split_results.py \
--name layouts05frac48via12 \
--in_folder /home/glchen/datasets/dmo_results/layouts05frac48via12_e100_dr2mg_1024_1024/test_latest/images \
--in_real_folder /home/glchen/datasets/dmo_results/layouts05frac48via12_e100_dr2mg_1024_1024/testbg \
--out_folder /home/glchen/datasets/dmo_results_splited \
--split_num 8 \
--real_A_postname mbsraf.gds_lccout_CALI.png



