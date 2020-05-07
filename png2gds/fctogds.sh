### 
# @Author: Guojin Chen
 # @Date: 2019-11-19 12:51:07
 # @LastEditTime: 2020-03-24 13:29:46
 # @Contact: cgjhaha@qq.com
 # @Description:
 ###

sid=$1

if [ ! -n "$1" ] ;then
    echo "you have not input a sid!"
    exit 2
else
    echo "the word you input is $1"
fi

name=orect2pixhd_e50_1024_good_dr2mg_D2d1_fc5
python=/home/glchen/miniconda3/envs/py3/bin/python

# python=/usr/local/miniconda3/envs/pytorch/bin/python
$python paired2gds_nobbox.py \
--name $name \
--in_folder /home/glchen/datasets/dmo_results_splited \
--out_folder /home/glchen/datasets/dmo_results2gds \
--img_size 2048 \
--threshold 0.9 \
--split_id $sid \
--fake_B_postname _synthesized_image.png \
--real_A_postname .png
