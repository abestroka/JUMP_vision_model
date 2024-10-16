from PIL import Image
import os

def is_tile_yellow(tile, threshold, percentage_required):
    # Convert the tile to RGB if it's not already
    tile = tile.convert('RGB')
    
    # Count how many pixels are close to yellow
    yellow_pixels = 0
    total_pixels = tile.width * tile.height

    # Define the yellow color range
    yellow_rgb = (255, 255, 0)
    tolerance = 50  # Adjust the tolerance for color matching

    # Go through each pixel and check if it's close to yellow
    for y in range(tile.height):
        for x in range(tile.width):
            r, g, b = tile.getpixel((x, y))
            if abs(r - yellow_rgb[0]) < tolerance and abs(g - yellow_rgb[1]) < tolerance and abs(b - yellow_rgb[2]) < tolerance:
                yellow_pixels += 1

    # Check if the percentage of yellow pixels meets the threshold
    yellow_percentage = (yellow_pixels / total_pixels) * 100
    return yellow_percentage >= percentage_required

def segment_image(image_path, output_folder, rows, cols, yellow_threshold, yellow_percentage):

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
            # tile.save(os.path.join(output_folder, f'tile_{tile_num}.png'))
            # tile_num += 1
            if is_tile_yellow(tile, yellow_threshold, yellow_percentage):
                tile.save(os.path.join(output_folder, f'tile_{tile_num}.png'))
                tile_num += 1

    print(f"Segmented the image into {rows*cols} tiles.")



image_path = '/eagle/FoundEpidem/astroka/fib_and_htert/week_two/results/fib_rad/0.01/r08c09f02p01.png'  # Path to your image
output_folder = f'/eagle/FoundEpidem/astroka/tiles/'  # Folder to save the tiles

# Set rows and cols for segmentation
rows, cols = 6, 6

yellow_threshold = 50         # Tolerance for yellow (e.g. ±50 from 255,255,0)
yellow_percentage = 10.0        # Minimum percentage of yellow pixels required to save the tile

# Segment the image
segment_image(image_path, output_folder, rows, cols, yellow_threshold, yellow_percentage)
