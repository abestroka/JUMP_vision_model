#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=1:00:00
#PBS -q debug
#PBS -A FoundEpidem
#PBS -l filesystems=home:eagle

# module load singularity
# module use /soft/spack/gcc/0.6.1/install/modulefiles/Core
# module load apptainer

module use /soft/modulefiles 
module load conda
# conda activate cellprofiler
# conda activate cellseg
conda activate yolo
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


python ~/workspace/JUMP_vision_model/rad_pipeline/yolo_test.py
# python ~/workspace/JUMP_vision_model/rad_pipeline/yolo_compare.py
# python ~/workspace/JUMP_vision_model/rad_pipeline/yolo_ablate.py


# path1="/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_1/images"
# path2="/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_2/images"
# path3="/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_3/images"
# path4="/eagle/FoundEpidem/astroka/yolo/rpe_rad_seg_4/images"

# python ~/workspace/JUMP_vision_model/rad_pipeline/remove_dups.py --path $path1
# python ~/workspace/JUMP_vision_model/rad_pipeline/remove_dups.py --path $path2
# python ~/workspace/JUMP_vision_model/rad_pipeline/remove_dups.py --path $path3
# python ~/workspace/JUMP_vision_model/rad_pipeline/remove_dups.py --path $path4




