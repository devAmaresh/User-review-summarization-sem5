#!/bin/bash
#PBS -u naveen
#PBS -N check
#PBS -q gpu
#PBS -l select=1:ncpus=20:ngpus=1

#PBS -o out.log
#PBS -e error.log
#PBS -V

# Change to the working directory
cd /home/naveen/project

# Load required modules
module load codes/pgi/qe/qe-gpu
module load compilers/gcc-8.4.0
module load compilers/intel/parallel_studio_xe_2018_update3_cluster_edition
# module load compilers/cuda/11.0

# Update library paths
export LD_LIBRARY_PATH=/apps/compilers/gcc/6.5.0/lib64:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_VISIBLE_DEVICES=0,1

# Ensure Conda is available
source /home/naveen/miniconda3/etc/profile.d/conda.sh

# Activate the Conda environment
ENV_NAME="minor_proj"
conda activate $ENV_NAME

# Verify CUDA installation
which nvcc
nvcc --version
nvidia-smi

# # Upgrade pip and install required packages
# pip install --upgrade pip

# # Install specific PyTorch version with CUDA 11.0 support
# pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 \
#     -f https://download.pytorch.org/whl/torch_stable.html

# Run the Python script
# python3 final.py
python3 eval.py

# Exit the script
exit
