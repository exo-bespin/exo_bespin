export PATH=/home/ec2-user/miniconda3/bin:$PATH
conda init bash
source ~/.bashrc
conda activate exo-bespin
"$@"