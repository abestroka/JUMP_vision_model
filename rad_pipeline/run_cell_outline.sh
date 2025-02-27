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



plate="rpe"
# week='week_one'
images="/eagle/FoundEpidem/astroka/rpe/week_two/20241105_Week2_RPE-1/20241105_OSU_HTSC_MW_ANL_CellPainting_RPE-1_W2C1__2024-11-06T07_43_59-Measurement1/Images"
# treatment_file="/home/astroka/workspace/JUMP_vision_model/rad_pipeline/week_five_rpe_layout.xlsx"
treatment_file="/home/astroka/workspace/JUMP_vision_model/rad_pipeline/week_two_rpe_layout.xlsx"

python ~/workspace/JUMP_vision_model/rad_pipeline/cropped_cells.py -i $images -p $plate -t $treatment_file -o /eagle/projects/FoundEpidem/astroka/rpe/week_two/rpe_control_seg --tmp_dir /dev/shm --num_workers 32

# python ~/workspace/JUMP_vision_model/rad_pipeline/cell_outlines.py -i $images -p $plate -t $treatment_file -o /eagle/projects/FoundEpidem/astroka/rpe/week_seven/rpe_control --tmp_dir /dev/shm --num_workers 32
# python ~/workspace/JUMP_vision_model/rad_pipeline/cropped_cells.py -i $images -p $plate -t $treatment_file -o /eagle/projects/FoundEpidem/astroka/rpe/week_three/rpe_rad_seg --tmp_dir /dev/shm --num_workers 32
