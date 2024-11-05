#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=1:00:00
#PBS -q debug
#PBS -A FoundEpidem
#PBS -l filesystems=home:eagle

# module load singularity
module use /soft/spack/gcc/0.6.1/install/modulefiles/Core
module load apptainer

module use /soft/modulefiles 
module load conda
# conda activate cellprofiler
conda activate cellseg
cd ~/workspace

# MPI example w/ 4 MPI ranks per node w/ threads spread evenly across cores (1 thread per core)
NNODES=`wc -l < $PBS_NODEFILE`
NRANKS_PER_NODE=4
NDEPTH=8
NTHREADS=1

NTOTRANKS=$(( NNODES * NRANKS_PER_NODE ))

# proxy settings
export HTTP_PROXY="http://proxy.alcf.anl.gov:3128"
export HTTPS_PROXY="http://proxy.alcf.anl.gov:3128"
export http_proxy="http://proxy.alcf.anl.gov:3128"
export https_proxy="http://proxy.alcf.anl.gov:3128"
export ftp_proxy="http://proxy.alcf.anl.gov:3128"
export no_proxy="admin,polaris-adminvm-01,localhost,*.cm.polaris.alcf.anl.gov,polaris-*,*.polaris.alcf.anl.gov,*.alcf.anl.gov"


echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE} THREADS_PER_RANK= ${NTHREADS}"
SECONDS=0

# python ~/workspace/JUMP_vision_model/rad_pipeline/tile_images.py
# python ~/workspace/JUMP_vision_model/rad_pipeline/CNN.py

python ~/workspace/JUMP_vision_model_rad_pipeline/pull_pngs.py

# python ~/workspace/JUMP_vision_model/rad_pipeline/CNN.py --color '1' --tiles '10' --percent '20' --batch '4'
# for c in {1..2} # color white or yellow
# do
#     for t in {2..10} # num of tiles 1-10
#     do
#         for p in {1..10} # percentage of color 0.1-1%
#         do

#             python ~/workspace/JUMP_vision_model/rad_pipeline/tile_images.py --color $c --tiles $t --percent $p

#             for b in {1..6} # batch size for cnn
#             do
#                 python ~/workspace/JUMP_vision_model/rad_pipeline/CNN.py --color $c --tiles $t --percent $p --batch $b

#             done




#         done


#     done
# done