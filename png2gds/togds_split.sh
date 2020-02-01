### 
# @Author: Guojin Chen
 # @Date: 2019-11-19 12:51:07
 # @LastEditTime: 2019-11-25 09:46:23
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

# $python paired2gds_nobbox.py --name dcupp_naive6_weighted_100epoch_dr2mg_2048_2048_uppscale4 --img_size 2048 --split_id $sid
# $python paired2gds_nobbox.py --name newdcupp_naive6_100epoch_dr2mg_2048_1024_50epoch --img_size 1024 --split_id $sid
# $python paired2gds_nobbox.py --name gan2gan_100epoch_2048_1024_gl_sl1_fixed_50epoch --img_size 1024 --split_id $sid
# $python paired2gds_nobbox.py --threshold 0.99 --name gan2gan_100epoch_2048_1024_gl_sl1_fixed_100epoch --img_size 1024 --split_id $sid
# $python paired2gds_nobbox.py --threshold 0.99 --name via1_10_100epoch --img_size 1024 --split_id $sid
$python paired2gds_nobbox.py --threshold 0.99 --name via1-10-100-convert-order --img_size 1024 --split_id $sid


