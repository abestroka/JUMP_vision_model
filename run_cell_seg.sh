#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=1:00:00
#PBS -q debug 
#PBS -A RL-fold
#PBS -l filesystems=home:eagle

module load singularity
module load conda
conda activate cellprofiler
cd ~/workspace

# MPI example w/ 4 MPI ranks per node w/ threads spread evenly across cores (1 thread per core)
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=4
NDEPTH=8
NTHREADS=1

NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))
echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE} THREADS_PER_RANK= ${NTHREADS}"

echo "pulling metadata"
# pull metadata, save to csv (TODO pare down into just filenames and targets, then export as lists)
# python ~/workspace/JUMP_vision_model/pull_meta.py -s 10
# image_set=1
# while [$image_set -le 10]
# do
#     python ~/workspace/JUMP_vision_model/pull_images.py -i image_set


#     ((image_set++))
# done

aws s3 cp \--no-sign-request \s3://cellpainting-gallery/cpg0016-jump/source_11/images/Batch3/images/EC000133__2021-09-24T18_01_09-Measurement1/Images/r01c01f01p01-ch1sk1fk1fl1.tiff /workspace/results/image_temp

