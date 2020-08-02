#!/bin/bash

cat << "EOF"
=========================================================
                  ___ _____ ___   _   _  _ 
                 / __|_   _/ __| /_\ | \| |
                | (__  | || (_ |/ _ \| .` |
                 \___| |_| \___/_/ \_\_|\_|
                            
               Deep Learning Synthetic Data.
                  github.com/sdv-dev/CTGAN
                                                                    
=========================================================

EOF


source "$(dirname "$0")/config.sh"




cd "$(dirname "$0")/original_data"
echo Original data files:
echo -------------------------------------------------------- 
ls | egrep '\.csv$'
echo --------------------------------------------------------
echo
read -p "Please enter original data filename: " VARR
echo
ssh $server_address "mkdir $server_original_data"
scp $VARR $server_address:$server_original_data
ssh $server_address "python3 -u $server_fit_script"


