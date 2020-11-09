#! /bin/bash

HOME_DIR=$HOME
cd $HOME_DIR

echo ''
echo '~~~~~ INSTALLING DEV TOOLS ~~~~~'
echo ''
if [ $HOME_DIR = "/home/ec2-user" ]; then
    sudo yum -y install bzip2
    sudo yum -y groupinstall "Development Tools"
fi

if [ $HOME_DIR = "/home/ubuntu" ]; then
    sudo apt update
    sudo apt -y install build-essential
fi

echo ''
echo '~~~~~ INSTALLING ANACONDA ~~~~~'
echo ''
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 700 ./Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh -b -p $HOME_DIR/miniconda3

echo ''
echo '~~~~~ SETTING ENVIRONMENT VARIABLES ~~~~~'
echo ''
export PATH=$HOME_DIR/miniconda3/bin:$PATH

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
chmod -R 777 $HOME_DIR/miniconda3/envs/exo-bespin/
cp /var/log/cloud-init-output.log $HOME_DIR