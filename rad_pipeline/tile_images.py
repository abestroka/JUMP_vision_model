from PIL import Image
import os

def segment_image(image_path, output_folder, rows, cols):

    img = Image.open(image_path)
    img_width, img_height = img.size
    tile_width = img_width // cols
    tile_height = img_height // rows

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    tile_num = 0
    for row in range(rows):
        for col in range(cols):
            
            #get bounding box
            left = col * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height
            tile = img.crop((left, upper, right, lower))
            
            # export tile
            tile.save(os.path.join(output_folder, f'tile_{tile_num}.png'))
            tile_num += 1

    print(f"Segmented the image into {rows*cols} tiles.")



image_path = '/eagle/FoundEpidem/astroka/fib_and_htert/week_two/results/fib_rad/0.1/r01c07f01p01.png'  # Path to your image
output_folder = f'/eagle/FoundEpidem/astroka/tiles/'  # Folder to save the tiles

# Set rows and cols for segmentation
rows, cols = 10, 10

# Segment the image
segment_image(image_path, output_folder, rows, cols)
