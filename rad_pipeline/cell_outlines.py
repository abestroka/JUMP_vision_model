from __future__ import annotations

import argparse
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

import pandas as pd


@dataclass
class ImageSet:
    """Dataclass to hold image set information."""

    dna: str
    rna: str
    agp: str
    er: str
    mito: str
    brightfield: str
    treatment: str

    @property
    def image_id(self) -> str:
        """Get the unique id for the image set, e.g., r06c04f09p14."""
        return Path(self.dna).stem.split('-')[0]

    def copy(self, dst: Path) -> None:
        """Copy the images to the specified directory."""
        # Move the images to the temporary directory
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy(self.dna, dst / 'dna.tiff')
        shutil.copy(self.rna, dst / 'rna.tiff')
        shutil.copy(self.agp, dst / 'agp.tiff')
        shutil.copy(self.er, dst / 'er.tiff')
        shutil.copy(self.mito, dst / 'mito.tiff')


def collect_image_sets(
    image_path: Path,
    plate: str,
    treatment_path: Path,
) -> list[ImageSet]:
    treatments = pd.read_excel(treatment_path, sheet_name=plate)

    image_sets = []

    for index, row in treatments.iterrows():
        location = row['Location']
        treatment = row['Treatment']
        # pull the every image set at this location
        well_images = list(map(str, image_path.glob(f'{location}*')))

        # iterate through, first by field, then by stack

        # r06c04f09p14
        # Location is r06c04 (row 6, column 4)
        # Field is f09 (field 9)
        # Stack is p14 (stack 14)

        # iterate through fields
        for field in range(1, 10):
            for stack in range(1, 6):
                curr_images = [
                    file
                    for file in well_images
                    if f'f0{field}' in file and f'p0{stack}' in file
                ]
                # iterate through images of this set
                # dna = 'NA'
                # rna = 'NA'
                # agp = 'NA'
                # er = 'NA'
                # brightfield = 'NA'
                # mito = 'NA'
                for img in curr_images:
                    if 'ch2' in img:
                        dna = img
                    elif 'ch4' in img:
                        rna = img
                    elif 'ch3' in img:
                        agp = img
                    elif 'ch6' in img:
                        er = img
                    elif 'ch7' in img:
                        brightfield = img
                    elif 'ch8' in img:
                        mito = img

                image_sets.append(
                    ImageSet(dna, rna, agp, er, mito, brightfield, treatment),
                )

    return image_sets


def run_cellprofiler(
    image_set: ImageSet,
    output_dir: Path,
    tmp_dir: Path,
    cellprofiler: str,
    cellprofiler_pipeline: Path,
) -> None:
    """Execute a cell profiler command with the specified parameters.

    Parameters
    ----------
    image_set : ImageSet
        The image set to process.
    output_dir : Path
        The directory to write the output files to.
    tmp_dir : Path
        The temporary directory to use for processing.
    cellprofiler : str
        The path to the cell profiler singularity image.
    cellprofiler_pipeline : Path
        The cell profiler pipeline to use.

    Returns
    -------
        None
    """
    # Create the temporary image directory
    image_set.copy(tmp_dir)

    # Create an output directory for the segmented images
    tmp_output_dir = tmp_dir / str(uuid4())
    tmp_output_dir.mkdir(exist_ok=True, parents=True)

    # Create the command
    command = (
        f'singularity run --bind {tmp_dir}:{tmp_dir} '
        f'{cellprofiler} -c -r '
        f'-p {cellprofiler_pipeline} '
        f'-i {tmp_dir} '
        f'-o {tmp_output_dir}'
    )

    # Run the command and check for errors
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'An error occurred: {e}')
        return
    except Exception as e:
        print(f'Unexpected error: {e}')
        return

    # Now we need to process and move the output files

    # TODO: See if we just rename files in the tmp directory,
    # then do bulk mv operation

    # Create the output directory
    output_dir = output_dir / image_set.treatment
    output_dir.mkdir(exist_ok=True, parents=True)

    # Handle the cells CSV file
    cells_csv = next(tmp_output_dir.glob('*Cells.csv'))
    shutil.copy(cells_csv, output_dir / f'{image_set.image_id}_cells.csv')

    # Handle the image CSV file
    image_csv = next(tmp_output_dir.glob('*Image.csv'))
    shutil.copy(image_csv, output_dir / f'{image_set.image_id}_image.csv')

    # Calculate the confluency and write it to a file
    df = pd.read_csv(image_csv)
    totalarea = df['AreaOccupied_TotalArea_Cells'][0]
    cellarea = df['AreaOccupied_AreaOccupied_Cells'][0]
    confluency = float(cellarea / totalarea)
    with open(output_dir / f'{image_set.image_id}_confluency.txt', 'w') as f:
        f.write(str(confluency))

    # Gather the segmented images and move them to the appropriate directory
    src_images = list(tmp_output_dir.glob('*.png'))

    # If there are more than one image, we need to assign unique names
    if len(src_images) > 1:
        for image in src_images:
            new_name = f'{image_set.image_id}_{uuid4()}.png'
            shutil.copy(image, output_dir / new_name)
    else:
        shutil.copy(src_images[0], output_dir / f'{image_set.image_id}.png')

    # Clean up the temporary directory
    shutil.rmtree(tmp_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run cell profiler on a set of images.',
    )
    parser.add_argument(
        '-i',
        '--image_dir',
        help='Directory path to the cell image files (.tiff)',
        type=Path,
    )
    parser.add_argument(
        '-p',
        '--plate',
        help='The plate number used to read the treament file',
        type=str,
    )
    parser.add_argument(
        '-t',
        '--treatment_file',
        help='The treatment file path',
        type=Path,
    )
    parser.add_argument(
        '-o',
        '--output_dir',
        help='The output directory for the segmented images',
        type=Path,
    )
    parser.add_argument(
        '--tmp_dir',
        help='The working directory for temporary files',
        type=Path,
    )
    parser.add_argument(
        '--cellprofiler',
        help='The path to the cell profiler singularity image',
        default='cellprofiler_4.2.6.sif',
        type=Path,
    )
    parser.add_argument(
        '--cellprofiler_pipeline',
        help='The cell profiler pipeline to use',
        default=Path(
            '~/workspace/JUMP_vision_model/rad_pipeline/no_outlines.cppipe',
        ),
        type=Path,
    )
    args = parser.parse_args()

    # First collect the image sets
    image_sets = collect_image_sets(
        image_path=args.image_dir,
        plate=args.plate,
        treatment_path=args.treatment_path,
    )

    # Run the cell profiler on each image set
    for image_set in image_sets:
        run_cellprofiler(
            image_set=image_set,
            output_dir=args.output_dir,
            tmp_dir=args.tmp_dir,
            cellprofiler=args.cellprofiler,
            cellprofiler_pipeline=args.cellprofiler_pipeline,
        )