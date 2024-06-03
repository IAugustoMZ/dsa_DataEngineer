# script to prepare the environment for the application

# download the Miniconda
wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    $$ /bin/bash ~/miniconda.sh -b -p $HOME/conda

# configure the miniconda in the PATH
echo -e '\nexport PATH=$HOME/conda/bin:$PATH' >> $HOME/.bashrc && source $HOME/.bashrc

# # install the required packages
# conda install -y boto3 pendulum numpy scikit-learn

# install the packages via pip
pip install --upgrade pip
pip install findspark
pip install pendulum
pip install boto3
pip install numpy
pip install python-dotenv
pip install scikit-learn

# create the folders
mkdir $HOME/pipeline
mkdir $HOME/logs