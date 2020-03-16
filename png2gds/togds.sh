### 
# @Author: Guojin Chen
 # @Date: 2019-11-19 12:51:07
 # @LastEditTime: 2020-03-13 15:09:24
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

$python paired2gds_nobbox.py \
--name via04dmo1024 \
--in_folder /home/glchen/datasets/dmo_results_splited \
--out_folder /home/glchen/datasets/dmo_results2gds \
--img_size 1024 \
--threshold 0.99 \
--split_id $sid
