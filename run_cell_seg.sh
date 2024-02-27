#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=24:00:00
#PBS -q debug 
#PBS -A APSDataAnalysis
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
python ~/workspace/JUMP_vision_model/pull_image.py -s 10