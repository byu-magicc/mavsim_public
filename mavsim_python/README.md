# Setting Up Your Python Environment

## Install Core Dependencies

```bash
pip3 install --upgrade pip
pip3 install numpy scipy matplotlib pyqtgraph pyqt6 pyopengl pynput numpy-stl
```

> **Note for ROS users:** If you have ROS installed and encounter issues with the data viewer, run the following and then reinstall PyQt6:
> ```bash
> sudo apt autoremove pyqt6*
> ```
> If problems persist, consider cleaning your Python environment or using a virtual environment ([see below](#creating-a-python-virtual-environment)).

## Video Writer Dependencies

```bash
pip3 install opencv-python Pillow
```

---

## Creating a Python Virtual Environment

### 1. Install virtualenvwrapper

```bash
pip3 install virtualenvwrapper
```

### 2. Configure your shell

Add the following to your `~/.bashrc` file:

```bash
export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'
source /home/username/.local/bin/virtualenvwrapper.sh
```

### 3. Create and use an environment

```bash
# Create a new environment
mkvirtualenv name_of_env

# Activate the environment
workon name_of_env

# Deactivate when done
deactivate
```
