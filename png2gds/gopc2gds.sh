###
 # @Author: Guojin Chen
 # @Date: 2020-05-07 14:24:14
 # @LastEditTime: 2020-05-07 14:27:10
 # @Contact: cgjhaha@qq.com
 # @Description: ganopc to gds
###


sid=$1

if [ ! -n "$1" ] ;then
    echo "you have not input a sid!"
    exit 2
else
    echo "the word you input is $1"
fi

name=ganopc_upp_base_50epoch_rect1_50
python=/home/glchen/miniconda3/envs/py3/bin/python

# python=/usr/local/miniconda3/envs/pytorch/bin/python
$python paired2gds_nobbox.py \
--name $name \
--in_folder /home/glchen/datasets/dmo_results_splited \
--out_folder /home/glchen/datasets/dmo_results2gds \
--img_size 256 \
--window_size 256 \
--threshold 0.9 \
--split_id $sid \
--fake_B_postname _mbsraf.gds_lccout_CALI_fake_B.png \
--real_A_postname _mbsraf.gds_lccout_CALI_real_A.png
