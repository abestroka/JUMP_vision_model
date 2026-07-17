#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=1:00:00
#PBS -q debug
#PBS -A FRAME-IDP
#PBS -l filesystems=home:grand

# module load singularity
module use /soft/spack/gcc/0.6.1/install/modulefiles/Core
module load apptainer

module use /soft/modulefiles 
module load conda
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



plate="Plate3"
images="/grand/FRAME-IDP/astroka/exp_05_26/week_four/20260716_ANL_Week4/20260617_20x_ANL_CellPainting_RPE-1_Plate3_1__2026-06-16T18_41_35-Measurement1/Images"
treatment_file="/home/astroka/workspace/JUMP_vision_model/rad_pipeline/rpe1_ko_wt.xlsx"
python ~/workspace/JUMP_vision_model/rad_pipeline/cell_outlines.py -i $images -p $plate -t $treatment_file -o /grand/projects/FRAME-IDP/astroka/exp_05_26/week_four/results/Plate3/ --tmp_dir /dev/shm --num_workers 16

