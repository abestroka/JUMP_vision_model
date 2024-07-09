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


# concatenate all images into a single excel file, and get length, then iterate through
images="/eagle/FoundEpidem/astroka/pilot_imgs/Test1/20240517_OSU_HTSC_MW_ANL_CellPainting_P3_2__2024-05-17T15_59_05-Measurement1/Images"
image_dir_path="/eagle/projects/FoundEpidem/astroka/pilot_imgs/Test1/20240517_OSU_HTSC_MW_ANL_CellPainting_P3_2__2024-05-17T15_59_05-Measurement1/all_images.xlsx"
# plate="Plate3"
# python ~/workspace/JUMP_vision_model/rad_pipeline/concat_images.py --image_path $images --plate $plate
# num=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad/pipeline/num_images.txt')
#TODO: extra function for extracting desired samples ie 1 of each well
for i in {1..2}
do
    # echo "get next image set, and id target name from excel file"
    python ~/workspace/JUMP_vision_model/rad_pipeline/pull_images.py --index $i --path image_dir_path

    # target=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/target_name.txt')

    # cellprofiler into target directory
    # singularity run cellprofiler_4.2.6.sif -c -r -p ~/workspace/JUMP_vision_model/my_project_421.cppipe -i ~/workspace/JUMP_vision_model/image_temp -o ~/workspace/results/segmented_image_temp/"$target"/

    #iterate through target directory and change names of cells
    # check if target directory exists on eagle, if not create one, and transfer contents
    # delete local directory
    # python ~/workspace/JUMP_vision_model/change_names.py --target "$target"

    echo "image set $i segmented in $SECONDS seconds"


done

# model

# echo "time before running model: $SECONDS seconds"

# echo "running vision transformer"
# python ~/workspace/JUMP_vision_model/ViT.py
# echo "model finished at $SECONDS seconds"