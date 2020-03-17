### 
# @Author: Guojin Chen
 # @Date: 2019-11-19 12:51:07
 # @LastEditTime: 2020-03-17 14:27:18
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

python=/home/glchen/miniconda3/envs/py3/bin/python
# python=/usr/local/miniconda3/envs/pytorch/bin/python
$python paired2gds_nobbox.py \
--name layouts05frac48via12 \
--in_folder /home/glchen/datasets/dmo_results_splited \
--out_folder /home/glchen/datasets/dmo_results2gds \
--img_size 2048 \
--threshold 0.6 \
--split_id $sid \
--fake_B_postname _mbsraf.gds_lccout_CALI_fake_B.png \
--real_A_postname _mbsraf.gds_lccout_CALI.png

# $python paired2gds_nobbox.py \
# --name via04dmo1024 \
# --in_folder /Users/dekura/Downloads/testnewpng2gds/ \
# --out_folder /Users/dekura/Downloads/testnewpng2gdsout/ \
# --img_size 2048 \
# --threshold 0.6 \
# --split_id $sid \
# --fake_B_postname _mbsraf_mb_mb_lccout.oas_fake_B.png \
# --real_A_postname _mbsraf_mb_mb_lccout.oas.png
