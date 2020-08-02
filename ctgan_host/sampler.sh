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
mkdir synthetic_output

cd "$(dirname "$0")"
ssh $server_address "python3 -u $server_sample_script"
cwd=$(pwd)
echo Download Synthetic data from server...
scp -r $server_address:$server_scp_folder* $cwd/synthetic_output
ssh $server_address "cd $server_scp_folder ; rm *" 
echo Download Complete
