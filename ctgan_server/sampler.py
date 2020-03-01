import time
import datetime
import torch
import re
from ctgan import CTGANSynthesizer
import os
import json
import fnmatch
import gzip
import sys
sys.tracebacklimit = 0 #comment out this line for debugging or development


from credentials import username_password


print("Sample Module\n")
print("A CLI implemention of CTGAN\n")
print()



u_name= False

while not u_name: 
    login_username = input("Please enter your username.\n")
    login_password = input("Please enter your password.\n")
    print()


    if username_password.get(login_username) == login_password:
        # Correct username and password match
        print("***** Login successful *****\n")
        u_name = True
    else:
        # Incorrect username/password match
        print("***** Incorrect username/password combination *****\n")

cwd = os.path.dirname(os.path.realpath(__file__))

# Check if user model directory exists, if not, end program.
model_dir = str(cwd+'/model_database/')
MYDIR = (model_dir + login_username + '/')
CHECK_FOLDER = os.path.isdir(MYDIR)

# check user model folder exists
if not CHECK_FOLDER:
    sys.exit("No model database exists for : ", login_username)

else:
    print(login_username + ' database models:')
    
    model_lst = fnmatch.filter(os.listdir(MYDIR), '*.gz')
    model_lst = list(model_lst)
    print("========================================================\n")
    for i in model_lst:
        print(i)

print()
print("========================================================\n")
while u_name:
    model_select = input("Please enter model to load: \n")

    if model_select in model_lst:
        #user selects model which is in database
        print(model_select + " selected")
        u_name = False
    else:
        #user selection not in database
        print("***** Model selection not found in database for: ", login_username, " *****")



torch_path = (MYDIR + model_select)

# decompress a gzip file
new_torch_path = torch_path.replace('.gz', '.pt')
input_ = gzip.GzipFile(torch_path, 'rb')
s = input_.read()
input_.close()

output = open(new_torch_path, 'wb')
output.write(s)
output.close()
print("Processing model...")


load_model = torch.load(new_torch_path)
print("Model loaded successfully\n")


size_numeric = True
while size_numeric:
        sample_size = input("Please enter sampling size: ")
        if sample_size.isdigit() == True:
            size_numeric = False
        else:
            print("***** Invalid input. Please enter an integer *****")


sample_size = int(sample_size)
print("Sampling Data...")
samples = load_model.sample(sample_size)

#restore dtypes of original
json_path = torch_path.replace('.gz', '.json')
with open(json_path, 'r') as f:
    data_types = json.load(f)

samples = samples.astype(dtype= data_types)



# Check if user csv output directory exists, if not, create it.
output_dir = str(cwd+'/synthetic_csv_database/')
MYDIR = (output_dir + login_username + '/')
CHECK_FOLDER = os.path.isdir(MYDIR)

# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs(MYDIR)
    print("created synthetic csv folder for user")

else:
    print(MYDIR, "user synthetic csv folder already exists.")


#define timestamp for output of sampled data
timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
timestamp = timestamp.replace(':','')
timestamp = timestamp.replace('-','')

synthetic_name = (model_select[:-25] + '_' + timestamp + '_' + str(sample_size) + '_synthetic' + '.csv').lower()
synthetic_name_dir = str(MYDIR+synthetic_name)

#save a copy of the data to the scp folder
scp_name_dir = str(model_dir + synthetic_name)


samples.to_csv(synthetic_name_dir.replace('.csv','.csv.gz'),compression='gzip', encoding='utf-8', index=False)

samples.to_csv(scp_name_dir.replace('model_database','scp_folder'),encoding='utf-8', index=False)
os.remove(new_torch_path)


time.sleep(3)





