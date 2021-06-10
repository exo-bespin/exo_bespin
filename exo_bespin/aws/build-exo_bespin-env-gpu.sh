echo ''
echo '~~~~~ INSTALLING NVIDIA GPU DRIVER ~~~~~'
echo ''
sudo yum -y update
sudo yum -y install wget nano elfutils-libelf-devel
sudo yum -y groupinstall "Development Tools"
sudo sed -i 's/crashkernel=auto"/crashkernel=auto nouveau.modeset=0"/g' /etc/default/grub
sudo grub2-mkconfig -o /boot/grub2/grub.cfg
sudo touch /etc/modprobe.d/blacklist.conf
sudo chmod 777 /etc/modprobe.d/blacklist.conf
sudo echo 'blacklist nouveau' > /etc/modprobe.d/blacklist.conf
sudo mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r)-nouveau.img
sudo dracut /boot/initramfs-$(uname -r).img $(uname -r)
sudo reboot
sudo systemctl isolate multi-user.target
wget http://us.download.nvidia.com/XFree86/Linux-x86_64/430.40/NVIDIA-Linux-x86_64-430.40.run
sudo sh NVIDIA-Linux-x86_64-430.40.run  # Select "No" when prompted to install 32-bit materials
sudo reboot

echo ''
echo '~~~~~ INSTALLING CUDA TOOLKIT ~~~~~'
echo ''
wget http://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.243_418.87.00_linux.run
sudo sh cuda_10.1.243_418.87.00_linux.run  # Enter "accept" and then choose "install", keeping everything selected
export PATH=$PATH:/usr/local/cuda-10.1/bin
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64

echo ''
echo '~~~~~ INSTALLING ANACONDA ~~~~~'
echo ''
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 700 ./Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3

echo ''
echo '~~~~~ SETTING ENVIRONMENT VARIABLES ~~~~~'
echo ''
export PATH=/home/ec2-user/miniconda3/bin:$PATH

echo ''
echo '~~~~~ CREATING base CONDA ENVIRONMENT ~~~~~'
echo ''
conda create --yes -n exo-bespin python=3.7 git numpy flask pytest
conda init bash
source ~/.bashrc
conda activate exo-bespin

echo ''
echo '~~~~~ INSTALLING exo_bespin ~~~~~'
echo ''
git clone https://github.com/exo-bespin/exo_bespin.git
cd exo_bespin/
git checkout -b develop origin/develop
conda env update -f environment.yml
conda init bash
source ~/.bashrc
conda activate exo-bespin
python setup.py develop
cd ../

echo ''
echo '~~~~~ INSTALLING ADDITIONAL LIBRARIES ~~~~~'
echo ''
pip install bibtexparser==1.1.0
pip install corner==2.0.1
pip install lmfit==0.9.13
pip install platon==3.1

echo ''
echo '~~~~~ INSTALLING cudamat ~~~~~'
echo ''
git clone https://github.com/cudamat/cudamat.git
sudo sed -i "s/-O',/-O3',/g" /home/ec2-user/cudamat/setup.py
cd cudamat
python setup.py develop
cd ../

echo ''
echo '~~~~~ INSTALLING gnumpy ~~~~~'
echo ''
git clone https://github.com/ExoCTK/gnumpy3.git
cd gnumpy3
python setup.py develop
cd ../

echo ''
echo '~~~~~ THE ENVIRONMENT BEING USED ~~~~~'
echo ''
conda env export

wget https://developer.download.nvidia.com/hpc-sdk/21.2/nvhpc_2021_212_Linux_x86_64_cuda_11.2.tar.gz
tar xpzf nvhpc_2021_212_Linux_x86_64_cuda_11.2.tar.gz
sudo nvhpc_2021_212_Linux_x86_64_cuda_11.2/install  # Select option 2 (Network installation), keep default paths
export PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/21.2/compilers/bin:$PATH

git clone https://github.com/lkreidberg/batman.git
cd batman
LDSHARED="pgcc" LDFLAGS="-noswitcherror -O3 -shared -L/opt/nvidia/hpc_sdk/Linux_x86_64/21.2/compilers/lib -laccapimp -laccgmp -laccnmp -laccg2mp -ldl -lcudadevice -lpgmp -lnuma -lpthread -lnspgc -lpgc" CC=pgcc CFLAGS="-noswitcherror -O3 -acc -ta=nvidia:nordc -Minfo=accel -mp" python setup.py install

