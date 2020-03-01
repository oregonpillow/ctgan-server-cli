import time
import fnmatch
import os
import shutil
import gzip
from credentials import username_password
import sys
sys.tracebacklimit = 0 #comment out this line for debugging or development
print("Download module\n")
print("A CLI implemention of CTGAN\n")
print()



u_name= False

while not u_name: 
    login_username = input("Please enter your username.\n")
    login_password = input("Please enter your password.\n")
    print()


    if username_password.get(login_username) == login_password:
        # Correct username and password match
        print("*****Login successful*****\n")
        u_name = True
    else:
        # Incorrect username/password match
        print("***** Incorrect username/password combination *****\n")

cwd = os.path.dirname(os.path.realpath(__file__))

# Check if user model directory exists, if not, end program.
model_dir = str(cwd+'/synthetic_csv_database/')
MYDIR = (model_dir + login_username + '/')
CHECK_FOLDER = os.path.isdir(MYDIR)

# check user model folder exists
if not CHECK_FOLDER:
    sys.exit("No synthetic database exists for : ", login_username)

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
    model_select = input("Please enter synthetic data to download: ")
    print()
    if model_select in model_lst:
        #user selects model which is in database
        print(model_select + " selected")
        u_name = False
    else:
        #user selection not in database
        print("Data selection not found in database for: ", login_username)



torch_path = (MYDIR + model_select)

# decompress a gzip file
new_torch_path = torch_path.replace('.gz', '')

print("Processing data...")


input_ = gzip.GzipFile(torch_path, 'rb')
s = input_.read()
input_.close()


output = open(new_torch_path, 'wb')
output.write(s)
output.close()

download_dir = str(cwd+'/download_folder/')
newpath = shutil.copy(new_torch_path, download_dir)

os.remove(new_torch_path)


time.sleep(5)