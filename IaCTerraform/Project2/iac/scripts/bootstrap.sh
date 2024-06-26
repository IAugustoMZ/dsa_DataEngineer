# script to prepare the environment for the application
# download the Miniconda
# download and install Miniconda
sudo wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    sudo /bin/bash ~/miniconda.sh -b -p $HOME/conda

# configure Miniconda in the PATH
sudo echo -e '\nexport PATH=$HOME/conda/bin:$PATH' >> $HOME/.bashrc && sudo source $HOME/.bashrc

# # install the required packages
# sudo conda install -y boto3 pendulum numpy scikit-learn

# install the packages via pip
sudo pip install --upgrade pip
sudo pip install findspark
sudo pip install pendulum
sudo pip install boto3
sudo pip install numpy
sudo pip install python-dotenv
sudo pip install scikit-learn

# create the folders
sudo mkdir $HOME/pipeline
sudo mkdir $HOME/logs