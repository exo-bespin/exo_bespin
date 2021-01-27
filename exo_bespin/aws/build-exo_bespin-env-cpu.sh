#! /bin/bash

export HOME_DIR=/home/ec2-user/
cd $HOME_DIR  # Ensure that this script operates relative to the $HOME_DIR directory

# This is not working since there doesn't appear to be a default $HOME directory
# # Additional libraries are needed, especially for C compilers
# echo ''
# echo '~~~~~ INSTALLING DEV TOOLS ~~~~~'
# echo ''
# if [ $HOME = "/home/ec2-user" ]; then
#     sudo yum -y install bzip2
#     sudo yum -y groupinstall "Development Tools"
# fi
# if [ $HOME = "/home/ubuntu" ]; then
#     sudo apt update
#     sudo apt -y install build-essential
# fi

sudo yum -y install bzip2
sudo yum -y groupinstall "Development Tools"

echo ''
echo '~~~~~ INSTALLING ANACONDA ~~~~~'
echo ''
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  # Download latest version of miniconda
chmod 700 ./Miniconda3-latest-Linux-x86_64.sh  # Ensure the shell script is executable
bash ./Miniconda3-latest-Linux-x86_64.sh -b -p $HOME_DIR/miniconda3  # Install miniconda into the $HOME_DIR directory

echo ''
echo '~~~~~ SETTING ENVIRONMENT VARIABLES ~~~~~'
echo ''
export PATH=$HOME_DIR/miniconda3/bin:$PATH  # Add miniconda install path to $PATH

echo ''
echo '~~~~~ CREATING INITIAL CONDA ENVIRONMENT ~~~~~'
echo ''
conda create --yes -n exo-bespin python=3.7  #  Create base conda environment
conda init bash  # Initialize bash
source ~/.bashrc  # Initialize bash
conda activate exo-bespin  # Activate new conda environment

echo ''
echo '~~~~~ INSTALLING exo-bespin ENVIRONMENT ~~~~~'
echo ''
git clone https://github.com/exo-bespin/exo_bespin.git  # Clone the exo_bespin repository
cd exo_bespin/
conda env update -f environment.yml  # Install exo-bespin conda environment
conda init bash  # Re-initialize bash
source ~/.bashrc  # Re-initialize bash
conda activate exo-bespin  # Activate conda environment
python setup.py develop  #  Install exo_bespin package into conda environment
cd ../

echo ''
echo '~~~~~ THE ENVIRONMENT BEING USED ~~~~~'
echo ''
conda env export  #  Display full environment for logging purposes

echo ''
echo '~~~~~ SETTING PERMISSIONS AND COPYING INIT OUTPUT ~~~~~'
echo ''
chmod -R 777 $HOME_DIR/miniconda3/envs/exo-bespin/  # Open up permissions so other users can use exo-bespin environment
cp /var/log/cloud-init-output.log $HOME_DIR   # Copy log file to home directory for easier access and to signify installation completion