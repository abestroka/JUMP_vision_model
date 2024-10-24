from PIL import Image
import os

def is_tile_yellow(tile, threshold, percentage_required):
    tile = tile.convert('RGB')
    yellow_pixels = 0
    total_pixels = tile.width * tile.height

    yellow_rgb = (255, 255, 0)
    # yellow_rgb = (255, 255, 255)
    tolerance = 50 

    for y in range(tile.height):
        for x in range(tile.width):
            r, g, b = tile.getpixel((x, y))
            if abs(r - yellow_rgb[0]) < tolerance and abs(g - yellow_rgb[1]) < tolerance and abs(b - yellow_rgb[2]) < tolerance:
                yellow_pixels += 1


    yellow_percentage = (yellow_pixels / total_pixels) * 100
    print("YELLOW PERCENTAGE", yellow_percentage)
    return yellow_percentage >= percentage_required

def threshold_images(image_path, confluency):
    files = os.listdir(image_path)
    images = []
    for file in files:
        if '.txt' in file:
            curr_path = os.path.join(image_path, file)
            with open(curr_path, 'r') as f:
                val = f.read()
                print("VAL", val)
            if float(val) >= confluency:
                print("PASS")
                img = str(file[:12]) + '.png'
                print('IMG', img)
                images.append(img)
    
    return images

            

def segment_image(image_path, output_folder, rows, cols, yellow_threshold, yellow_percentage):

    # images = os.listdir(image_path)
    confluency = 0.2
    images = threshold_images(image_path, confluency)
    tile_num = 0
    for image in images:
        print("IMAGE", image)
        if '.png' in image:
            curr_path = os.path.join(image_path, image)

            img = Image.open(curr_path)
            img_width, img_height = img.size
            tile_width = img_width // cols
            tile_height = img_height // rows

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
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





# image_path = '/eagle/FoundEpidem/astroka/fib_and_htert/week_two/results/fib_rad/0.01/r08c09f02p01.png'  # Path to your image
# output_folder = f'/eagle/FoundEpidem/astroka/tiles/'  # Folder to save the tiles

# Set rows and cols for segmentation
rows, cols = 6, 6

yellow_threshold = 50         # Tolerance for yellow (e.g. ±50 from 255,255,0)
yellow_percentage = 1.0       # Minimum percentage of yellow pixels required to save the tile

# rads = ['0.001', '0.01', '0.1', '1.0', '2.0']
rads = ['untreated', 'Compound_1', 'Compound_2', 'Compound_3', 'Compound_4', 'Compound_5', 'Compound_6', 'Compound_7', 'Compound_8', 'Compound_9', 'Compound_10', 'Compound_11', 'Compound_12', 'Compound_13', 'Compound_14', 'Compound_15', 'Compound_16', 'Compound_17']
weeks = ['week_one', 'week_two', 'week_three']

for week in weeks:
    for rad in rads:
        # image_path = '/eagle/FoundEpidem/astroka/fib_and_htert/'+week+'/results/fib_rad/'+rad+'/'
        # output_folder = f'/eagle/FoundEpidem/astroka/fib_and_htert/cnn_data/'+week+'/fib_rad/'+rad+'/'
        image_path = '/eagle/FoundEpidem/astroka/fib_and_htert/'+week+'/results/fib_control/'+rad+'/'
        output_folder = f'/eagle/FoundEpidem/astroka/fib_and_htert/cnn_data/'+week+'/fib_control/'+rad+'/'
        # if os.path.isdir(output_folder) == False:
        #     os.mkdir(output_folder)
            
        segment_image(image_path, output_folder, rows, cols, yellow_threshold, yellow_percentage)

        

# Segment the image
# segment_image(image_path, output_folder, rows, cols, yellow_threshold, yellow_percentage)
