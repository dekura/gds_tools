### 
# @Author: Guojin Chen
 # @Date: 2019-11-19 20:45:42
 # @LastEditTime: 2020-03-13 15:09:43
 # @Contact: cgjhaha@qq.com
 # @Description: 
 ###
# python=/usr/local/miniconda3/envs/pytorch/bin/python
python=/home/glchen/miniconda3/envs/py3/bin/python
# $python split_results.py --name ganopc_upp_base_25epoch --in_folder /Users/dekura/Downloads/aresults/ganopc_upp_base_50epoch/test_25/images/

# $python split_results.py --split_num 10 --name dcupp_naive6_weighted_100epoch_dr2mg_2048_2048_uppscale4 --in_folder /Users/dekura/Downloads/aresults/dcupp_naive6_weighted_100epoch_dr2mg_2048_2048_uppscale4/test_latest/images/
# $python split_results.py --split_num 8 --name newdcupp_naive6_100epoch_dr2mg_2048_1024_50epoch --in_folder /Users/dekura/Downloads/aresults/newdcupp_naive6_100epoch_dr2mg_2048_1024_50epoch/test_50/images/
# $python split_results.py --split_num 8 --is_gan2gan --name gan2gan_100epoch_2048_1024_gl_sl1_fixed_50epoch --in_folder /Users/dekura/Downloads/aresults/gan2gan_100epoch_2048_1024_gl_sl1_fixed_50epoch/test_50/images/
# $python split_results.py --split_num 8 --is_gan2gan --name gan2gan_100epoch_2048_1024_gl_sl1_fixed_100epoch --in_folder /Users/dekura/Downloads/aresults/gan2gan_100epoch_2048_1024_gl_sl1_fixed_50epoch/test_latest/images/
# $python split_results.py --split_num 4 --is_gan2gan --name via1-10-100-convert-order --in_folder /Users/dekura/Desktop/figures/via1-10-100-convert-order
$python split_results.py \
--name via04dmo1024 \
--in_folder /Users/dekura/Downloads/via0.4_100epoch_dr2mg_1024_1024_g4/test_latest/images/ \
--out_folder /Users/dekura/Downloads/datasets/ \
--split_num 8 \
--fake_B_postname _mbsraf.gds_lccout_CALI_fake_B.png



