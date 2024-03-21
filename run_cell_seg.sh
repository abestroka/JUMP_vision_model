#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=1:00:00
#PBS -q debug
#PBS -A FoundEpidem
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

# proxy settings
export HTTP_PROXY="http://proxy.alcf.anl.gov:3128"
export HTTPS_PROXY="http://proxy.alcf.anl.gov:3128"
export http_proxy="http://proxy.alcf.anl.gov:3128"
export https_proxy="http://proxy.alcf.anl.gov:3128"
export ftp_proxy="http://proxy.alcf.anl.gov:3128"
export no_proxy="admin,polaris-adminvm-01,localhost,*.cm.polaris.alcf.anl.gov,polaris-*,*.polaris.alcf.anl.gov,*.alcf.anl.gov"


echo "NUM_OF_NODES= ${NNODES} TOTAL_NUM_RANKS= ${NTOTRANKS} RANKS_PER_NODE= ${NRANKS_PER_NODE} THREADS_PER_RANK= ${NTHREADS}"
SECONDS=0
echo "pulling metadata"
# pull metadata, save to csv (TODO pare down into just filenames and targets, then export as lists)
python ~/workspace/JUMP_vision_model/pull_meta.py
echo "metadata pulled at $SECONDS seconds"
# image_set=1
# echo "pulling images from aws"
# for i in {1001..2000}
# do
#     # echo "image set"
#     # echo "$i"
#     python ~/workspace/JUMP_vision_model/pull_images.py --index $i
#     target=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/target_name.txt')

#     # cellprofiler into target directory
#     # singularity run cellprofiler_4.2.6.sif -c -r -p ~/workspace/JUMP_vision_model/my_project_421.cppipe -i /eagle/projects/FoundEpidem/astroka/image_temp -o /eagle/projects/APSDataAnalysis/LUCID/segmented_images/"$i"/
#     singularity run cellprofiler_4.2.6.sif -c -r -p ~/workspace/JUMP_vision_model/my_project_421.cppipe -i ~/workspace/JUMP_vision_model/image_temp -o ~/workspace/results/segmented_image_temp/"$target"/

#     #iterate through target directory and change names of cells
#     # check if target directory exists on eagle, if not create one, and transfer contents
#     # delete local directory
#     python ~/workspace/JUMP_vision_model/change_names.py --target "$target"

#     echo "image set $i segmented in $SECONDS seconds"


# done

# model

# echo "time before running model: $SECONDS seconds"

# echo "running vision transformer"
# python ~/workspace/JUMP_vision_model/ViT.py
# echo "model finished at $SECONDS seconds"