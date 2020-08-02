#quick script to setup on linux server using bash. 

sudo apt -y update
#sudo apt -y upgrade
sudo apt -y install python3-pip
sudo apt -y install git
git clone https://github.com/oregonpillow/ctgan-server-cli.git

pip3 install ctgan --no-cache-dir
