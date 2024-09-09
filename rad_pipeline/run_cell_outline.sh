#!/bin/bash -l
#PBS -l select=1:system=polaris
#PBS -l place=scatter
#PBS -l walltime=24:00:00
#PBS -q preemptable
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


#TODO: Change
week='week_one'

# concatenate all images into a single excel file, and get length, then iterate through
images="/eagle/FoundEpidem/astroka/ten_week/week_one/20240718_Week1/20240717_OSU_HTSC_MW_ANL_CellPainting_P3_8stacks_1__2024-07-17T17_38_31-Measurement1/Images"

treatment_file="/home/astroka/workspace/JUMP_vision_model/rad_pipeline/week_one_cells_layout.xlsx"

# plate="HUVEC_Control"
# plate="Fibroblast_Control"
# plate="Plate8"
plate="Plate3"

seg_image_temp="huvec_rad_seg_temp"
# seg_image_temp="fib_rad_seg_temp"
# seg_image_temp="huvec_control_seg_temp"
# seg_image_temp="fib_control_seg_temp"

image_temp="huvec_rad_temp"
# image_temp="huvec_control_temp"
# image_temp="fib_rad_temp"
# image_temp="fib_control_temp"

# results="fib_control"
# results="huvec_control"
# results="fib_rad"
results="huvec_rad"



python ~/workspace/JUMP_vision_model/rad_pipeline/concat_images.py --image_path $images --plate $plate --treatment $treatment_file

#TODO: CHANGE
# num=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/Fibroblast_Control_num_images.txt')
# num=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/HUVEC_Control_num_images.txt')
# num=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/Plate8_num_images.txt')
num=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/Plate3_num_images.txt')


echo $num
#TODO: extra function for extracting desired samples ie 1 of each well
# for i in {1..$num}
for i in $( eval echo {0..$num} )
do
    # echo "get next image set, and id target name from excel file"
    python ~/workspace/JUMP_vision_model/rad_pipeline/pull_images.py --index $i --path $images --temp $image_temp --seg $seg_image_temp --res $results

    #TODO: CHANGE
    # target=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/fib_control_target_name.txt')
    # name=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/fib_control_image_name.txt')

    # target=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/huvec_control_target_name.txt')
    # name=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/huvec_control_image_name.txt')

    # target=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/fib_rad_target_name.txt')
    # name=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/fib_rad_image_name.txt')

    target=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/huvec_rad_target_name.txt')
    name=$(head -n 1 '/home/astroka/workspace/JUMP_vision_model/rad_pipeline/huvec_rad_image_name.txt')


    # cellprofiler into target directory
    singularity run cellprofiler_4.2.6.sif -c -r -p ~/workspace/JUMP_vision_model/rad_pipeline/outlines_and_sheet.cppipe -i ~/workspace/JUMP_vision_model/rad_pipeline/"$image_temp" -o ~/workspace/JUMP_vision_model/rad_pipeline/"$seg_image_temp"/"$target"/

    # iterate through target directory and change names of cells
    # check if target directory exists on eagle, if not create one, and transfer contents
    # delete local directory

    python ~/workspace/JUMP_vision_model/rad_pipeline/change_names.py --target "$target" --name "$name" --src "$seg_image_temp" --dst "$results"

    echo "image set $i segmented in $SECONDS seconds"


done

# model

# echo "time before running model: $SECONDS seconds"

# echo "running vision transformer"
# python ~/workspace/JUMP_vision_model/ViT.py
# echo "model finished at $SECONDS seconds"