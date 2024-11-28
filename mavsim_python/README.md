# Setup your python environment

pip3 install --upgrade pip

pip3 install numpy

pip3 install scipy

pip3 install matplotlib

pip3 install pyqtgraph

pip3 install pyqt6

pip3 install pyopengl

pip3 install pynput

#sometimes there are issues with that data_viewer if you have ROS installed on your system, in this case. If you are having problems
#with the data viewer try running the following in the commandline and then reinstalling pqt6. 

sudo apt autoremove pyqt6*

#If you still have problems try cleaning your python environment or using a virtual environment.

#To run the video writer install the following

pip3 install opencv-python
pip3 install Pillow



# Creating a python virtual environment

#First install virtualenvwrapper

pip3 install virtualenvwrapper

#Export and source the appropriate files in bashrc file

export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3' 

source /home/username/.local/bin/virtualenvwrapper.sh 

#create and environment

mkvirtualenv name_of_env 

#start using environment

workon name_of_env

#close environemnt

deactivate

# Create a `conda` environment

Alternatively, if you prefer to use [`anaconda`](https://www.anaconda.com/download) or [`miniconda`](https://docs.conda.io/projects/miniconda/en/latest/) for managing your python environment, you can use the `environment.yml` file in this folder:

```shell
conda env create -f environment.yml
conda activate uavbook
```
