echo ''
echo '~~~~~ INSTALLING ANACONDA ~~~~~'
echo ''
sudo yum -y install bzip2
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 700 ./Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3

echo ''
echo '~~~~~ SETTING ENVIRONMENT VARIABLES ~~~~~'
echo ''
export PATH=/home/ec2-user/miniconda3/bin:$PATH
echo 'Set $PATH'

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
conda env update -f env/environment.yml
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
echo '~~~~~ THE ENVIRONMENT BEING USED ~~~~~'
echo ''
conda env export