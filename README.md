
# ctgan
This ctgan package provides a simple way to deploy
[CTGAN](github.com/sdv-dev/CTGAN), a GAN-based data synthesizer onto a remote server.
The package allows you to create synthetic samples of tabular data i.e confidential or
proprietary datasets for sharing. For more details and use cases, see 
[References](#references).
The package contains the following additional features:
 - simple username/password feature to separate multiple models/synthetic datasets for multiple users on server
 - As soon as original data has been uploaded and stored in memory for fitting, the original file is deleted from server
 - pytorch models are stored in compressed serialized .gzip for efficient storage
 - synthetic csv files are stored in compressed .gzip on the server
 
 ### warning! The username/password feature is not secure as the username/passwords are stored in an unencrpyted dictionary. This feature exists for proof of concept and as a simple method to separate models/data between TRUSTED users on the same server.

## Installation

You can install the development version from
[GitHub](https://github.com/) by:
* copying the **ctgan_host** folder onto your local machine
* copying the **ctgan_server** folder onto your server
* updating the **ctgan_host/config.sh** to point towards your server 

You will also need to install the required packages onto the server. From the **ctgan_server** folder:

``` r
pip3 install -r requirements.txt
```

## Requirements

* CTGAN has been developed and tested on Python 3.5, 3.6 and 3.7
* ctgan_server package tested on Python 3.6.9, Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-66-generic x86_64)


## Example

A quick example:


``` r
bash fit.sh
#>=========================================================
#>                  ___ _____ ___   _   _  _
#>                 / __|_   _/ __| /_\ | \| |
#>                | (__  | || (_ |/ _ \| .` |
#>                 \___| |_| \___/_/ \_\_|\_|
#>
#>               Deep Learning Synthetic Data.
#>                  github.com/sdv-dev/CTGAN
#>
#>=========================================================
#>
#>Original data files:
#>--------------------------------------------------------
#>original_data_demo.csv
#>--------------------------------------------------------
#>
#>Please enter original data filename: original_data_demo.csv
#>
#>original_data_demo.csv                                      100% 3722KB   3.6MB/s   00:01                                                                                                                                                     
#>Fit Module
#>
#>A CLI implemention of CTGAN
#>
#>
#>Please enter your username.
#>user1
#>Please enter your password.
#>password1
#>***** Login successful *****
#>
#>
#>Please re-confirm the file name you wish to fit: original_data_demo.csv
#>Data Integrity check PASSED
#>Please choose number of epochs for fitting: 5
#>Fitting Data. This may take a while...
#>
#>Epoch 1, Loss G: 1.9984, Loss D: -0.3420
#>Epoch 2, Loss G: 1.2560, Loss D: 0.0264
#>Epoch 3, Loss G: 0.3803, Loss D: 0.0651
#>Epoch 4, Loss G: -0.2293, Loss D: 0.0992
#>Epoch 5, Loss G: -0.4099, Loss D: 0.0719
#>Fitting Complete
#>/root/ctgan_server/model_database/user1/ Successfully found existing database for current user
#>
#>Model successfully added to database. Exiting...

```

This generated synthetic model is now stored on the server in a compressed serialized
file format. We can sample from the model using the sampler.sh script:

``` r
bash sampler.sh

#>
#>=========================================================
#>                  ___ _____ ___   _   _  _
#>                 / __|_   _/ __| /_\ | \| |
#>                | (__  | || (_ |/ _ \| .` |
#>                 \___| |_| \___/_/ \_\_|\_|
#>
#>               Deep Learning Synthetic Data.
#>                  github.com/sdv-dev/CTGAN
#>
#>=========================================================
#>
#>Sample Module
#>
#>A CLI implemention of CTGAN
#>
#>
#>Please enter your username.
#>user1
#>Please enter your password.
#>password1
#>
#>***** Login successful *****
#>
#>user1 database models:
#>========================================================
#>
#>original_data_demo_20200301t181421_model.gz
#>
#>========================================================
#>
#>Please enter model to load:
#>original_data_demo_20200301t181421_model.gz
#>original_data_demo_20200301t181421_model.gz selected
#>Processing model...
#>Model loaded successfully
#>
#>Please enter sampling size: 100000
#>Sampling Data...
#>created synthetic csv folder for user
#>Download Synthetic data from server...
#>original_data_demo_20200301t181928_100000_synthetic.csv     100%   11MB   4.1MB/s   00:02
#>Download complete
```
The sampled data is now saved within the local folder **synthetic_output**


In the case that a user does not want to re-sample data from a model, but instead wants an exact carbon copy of a previously generated synthetic dataset, they can use the downloader.sh script:


``` r
bash downloader.sh
#>
#>=========================================================
#>                  ___ _____ ___   _   _  _
#>                 / __|_   _/ __| /_\ | \| |
#>                | (__  | || (_ |/ _ \| .` |
#>                 \___| |_| \___/_/ \_\_|\_|
#>
#>               Deep Learning Synthetic Data.
#>                  github.com/sdv-dev/CTGAN
#>
#>=========================================================
#>
#>Download module
#>
#>A CLI implemention of CTGAN
#>
#>
#>Please enter your username.
#>user1
#>Please enter your password.
#>password1
#>
#>*****Login successful*****
#>
#>user1 database models:
#>========================================================
#>
#>original_data_demo_20200301t181928_100000_synthetic.csv.gz
#>
#>========================================================
#>
#>Please enter synthetic data to download: original_data_demo_20200301t181928_100000_synthetic.csv.gz
#>
#>original_data_demo_20200301t181928_100000_synthetic.csv.gz selected
#>Processing data...
#>Download Synthetic data from server...
#>original_data_demo_20200301t181928_100000_synthetic.csv      100% 4480KB   4.4MB/s   00:01 ETA                                                                                                                     
#>Download complete
```




## References

If you use ctgan, please cite the original work,

  - *Lei Xu, Maria Skoularidou, Alfredo Cuesta-Infante, Kalyan
    Veeramachaneni.* **Modeling Tabular data using Conditional GAN**.
    NeurIPS, 2019. [arXiv:1907.00503](https://arxiv.org/abs/1907.00503)
    
   - github.com/sdv-dev/CTGAN

for an R package implementation of ctgan, see the following work,
  
  - *Kevin Kuo.* **Generative Synthesis of Insurance Datasets**.
    2019. [arXiv:1912.02423](https://arxiv.org/abs/1912.02423)
    
  - github.com/kasaai/ctgan

<!-- end list -->

``` latex
@inproceedings{xu2019modeling,
  title={Modeling Tabular data using Conditional GAN},
  author={Xu, Lei and Skoularidou, Maria and Cuesta-Infante, Alfredo and Veeramachaneni, Kalyan},
  booktitle={Advances in Neural Information Processing Systems},
  year={2019}
}

@misc{kuo2019generative,
    title={Generative Synthesis of Insurance Datasets},
    author={Kevin Kuo},
    year={2019},
    eprint={1912.02423},
    archivePrefix={arXiv},
    primaryClass={stat.AP}
}
```
