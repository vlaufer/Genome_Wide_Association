#!/bin/bash

#qlogin -l h_rt=48:00:00,vf=6G -m b -M $USER@uab.edu

MY_DIR="/home/dosun/5M_data"

## for prototyping
## tail -n+11  $MY_DIR/Bridges_5M_FinalReport.lgen | head -100 | awk '{print 0,$2,$1,$3,$4}' 

## transform lgen file from HA into true lgen file for input into plink
tail -n+11 $MY_DIR/Bridges_5M_FinalReport.lgen | awk '{print 0, $2, $1, $3, $4}' | awk '{ if ($4=="-" && $5=="-") print $1, $2, $3, 0, 0; else if ($4=="-" && $5!="-") print $1, $2, $3, 0, $5; else if ($4!="-" && $5=="-") print $1, $2, $3, $4, 0; else print $0}' > $MY_DIR/Bridges_5M_FinalReport_1.lgen

## load module 
module load plink/plink-1.07
##transform lgen to plink
plink --lfile $MY_DIR/Bridges_5M_FinalReport_1 --recode --out $MY_DIR/Bridges_5M_FinalReport_2


## former sed syntax not used keep for reference. has untoward effects.
###sed 's/\t-/\t0/g' testfile.txt
