import gzip
import datetime
import time
import numpy as np
import re
import pandas as pd
from ctgan import CTGANSynthesizer
import os
import torch
import json
from credentials import username_password
import sys
sys.tracebacklimit = 0 #comment out this line for debugging or development
print("Fit Module\n")
print("A CLI implemention of CTGAN\n")
print()




u_name= True

while u_name: 
    login_username = input("Please enter your username.\n")
    login_password = input("Please enter your password.\n")



    if username_password.get(login_username) == login_password:
        # Correct username and password match
        print("***** Login successful *****")
        u_name = False
    else:
        # Incorrect username/password match
        print("***** Incorrect username/password combination *****")

#current folder directory
cwd = os.path.dirname(os.path.realpath(__file__))

#folder directory that will contain the original data
original_dir = str(cwd+'/original_data/')

#original data folder should only contain 1 file at a time, we define the file location here
fname1 =os.listdir(original_dir)[0]
fname2 =str(original_dir+fname1)


#read original data file into pandas memory then remove the file
data = pd.read_csv(fname2)
os.remove(fname2)


discrete_columns = list(data.select_dtypes(include=['object']).columns)

print()
print()



ctgan = CTGANSynthesizer()

security_check= True

'''
In the rare case that multiple users upload files at the same time, there is a chance that since we grab
the first file in fname1, we might accidently grab another user's file. By asking a simple security question
we can verify that the file we selected in fname1 is the same file that the user intended to use
'''
while security_check:
    security = input('Please re-confirm the file name you wish to fit: ')



    if security == fname1:
        # match is found between fileuploaded and the file pulled from the 'original_data' folder
        print("Data Integrity check PASSED")
        security_check = False
    else:
        # fileuploaded and file pulled are not matching
        print("Data Integrity check FAILED")
        #remove all files in the original data folder
        filelist = [ f for f in os.listdir(original_dir) if f.endswith(".csv") ]
        print("System purge initiated")
        for f in filelist:
                os.remove(os.path.join(original_dir, f))



epochs_numeric = True
while epochs_numeric:
        user_epoch = input('Please choose number of epochs for fitting: ')
        if user_epoch.isdigit() == True:
            print("Fitting Data. This may take a while...\n")
            epochs_numeric = False
        else:
            print("*** Invalid input. Please enter an integer ***")


ctgan.fit(data, discrete_columns,epochs=int(user_epoch))

print("Fitting Complete")



model_dir = str(cwd+'/model_database/')
usr_model_dir = (model_dir + login_username + '/')
check_usr_modeldir = os.path.isdir(usr_model_dir)

# If usr_model_dir doesn't exist, then create it.
if not check_usr_modeldir:
    os.makedirs(usr_model_dir)
    print("*** No existing database has been detected for current user. A new database will be created ***\n")

else:
    print(usr_model_dir, "Successfully found existing database for current user\n")
#timestamp creation and formatting
timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
timestamp = timestamp.replace(':','')
timestamp = timestamp.replace('-','')

#format the output name
synthetic_name =str(fname1.replace('.csv',' ') + timestamp + ' model') 
#remove special characters and spaces
synthetic_name_mod = re.sub('[^A-z0-9 -]', '', synthetic_name).lower().replace(" ", "_")
synthetic_name_mod = synthetic_name_mod + '.pt'
synthetic_name_mod = str(usr_model_dir + synthetic_name_mod)


torch.save(ctgan, synthetic_name_mod)

# compress the model into gzip

input = open(synthetic_name_mod, 'rb')
s = input.read()
input.close()
output = gzip.GzipFile(synthetic_name_mod.replace('.pt','.gz'), 'wb')
output.write(s)
output.close()
os.remove(synthetic_name_mod)


#save the dtypes as a json file
# first create dictionary
d = data.dtypes.apply(lambda x: x.name).to_dict()

with open(synthetic_name_mod.replace('.pt','.json'), 'w') as f:
    json.dump(d, f)


print("Model successfully added to database. Exiting...\n")
time.sleep(5)
