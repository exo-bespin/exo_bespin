#! /bin/bash

cd /home/ec2-user/

echo ''
echo '~~~~~ INSTALLING DEV TOOLS ~~~~~'
echo ''
sudo apt update
sudo apt -y install bzip2
sudo apt -y groupinstall "Development Tools"
sudo apt -y install screen

echo '~~~~~ STARTING SCREEN ~~~~~'
screen -S exobespin # start a screen session named 'exobespin'

echo ''
echo '~~~~~ INSTALLING ANACONDA ~~~~~'
echo ''
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 700 ./Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh -b -p /home/ec2-user/miniconda3

echo ''
echo '~~~~~ SETTING ENVIRONMENT VARIABLES ~~~~~'
echo ''
export PATH=/home/ec2-user/miniconda3/bin:$PATH

echo ''
echo '~~~~~ CREATING INITIAL CONDA ENVIRONMENT ~~~~~'
echo ''
conda create --yes -n exo-bespin python=3.7
conda init bash
source ~/.bashrc
conda activate exo-bespin

echo ''
echo '~~~~~ INSTALLING exo-bespin ENVIRONMENT ~~~~~'
echo ''
git clone https://github.com/exo-bespin/exo_bespin.git
cd exo_bespin/
git checkout -b screen_testing origin/screen_testing
conda env update -f environment.yml
conda init bash
source ~/.bashrc
conda activate exo-bespin
python setup.py develop
cd ../

echo ''
echo '~~~~~ THE ENVIRONMENT BEING USED ~~~~~'
echo ''
conda env export

echo ''
echo '~~~~~ SETTING PERMISSIONS AND COPYING INIT OUTPUT ~~~~~'
echo ''
chmod -R 777 /home/ec2-user/miniconda3/envs/exo-bespin/
cp /var/log/cloud-init-output.log /home/ec2-user/