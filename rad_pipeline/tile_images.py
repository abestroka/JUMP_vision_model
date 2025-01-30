from PIL import Image
import os
import argparse
import shutil

def is_tile_yellow(tile, threshold, percentage_required, curr_color):
    tile = tile.convert('RGB')
    yellow_pixels = 0
    total_pixels = tile.width * tile.height
    # print("CURR COLOR", curr_color)
    if curr_color == "yellow":
        yellow_rgb = (255, 255, 0)
    elif curr_color == "green":
        # yellow_rgb = (0, 255, 0)
        yellow_rgb = (0, 150, 0)
    elif curr_color == "white":
        yellow_rgb = (255, 255, 255)
    tolerance = threshold

    print()

    for y in range(tile.height):
        for x in range(tile.width):
            r, g, b = tile.getpixel((x, y))
            if abs(r - yellow_rgb[0]) < tolerance and abs(g - yellow_rgb[1]) < tolerance and abs(b - yellow_rgb[2]) < tolerance:
                yellow_pixels += 1


    yellow_percentage = (yellow_pixels / total_pixels) * 100
    print("YELLOW PERCENTAGE", yellow_percentage)
    print("PERCENTAGE REQUIRED", percentage_required)
    return yellow_percentage >= percentage_required

def threshold_images(image_path, confluency):
    files = os.listdir(image_path)
    images = []
    for file in files:
        if '.txt' in file:
            curr_path = os.path.join(image_path, file)
            with open(curr_path, 'r') as f:
                val = f.read()
                # print("VAL", val)
            if float(val) >= confluency and float(val):
                # print("PASS")
                img = str(file[:12]) + '.png'
                # print('IMG', img)
                images.append(img)
    
    return images

            

def segment_image(image_path, output_folder, rows, cols, yellow_threshold, yellow_percentage, curr_color):

    # images = os.listdir(image_path)
    #threshold for 10% confluency
    confluency = 0.1
    images = threshold_images(image_path, confluency)
    #images = images that pass confluency thresholding
    tile_num = 0
    for image in images:
        # print("IMAGE", image)
        #TODO only one stack? ie 'p03.png'
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
                    if is_tile_yellow(tile, yellow_threshold, yellow_percentage, curr_color):
                        tile.save(os.path.join(output_folder, f'tile_{tile_num}.png'))
                        tile_num += 1

            # print(f"Segmented the image into {rows*cols} tiles.")





# image_path = '/eagle/FoundEpidem/astroka/fib_and_htert/week_two/results/fib_rad/0.01/r08c09f02p01.png'  # Path to your image
# output_folder = f'/eagle/FoundEpidem/astroka/tiles/'  # Folder to save the tiles

# Set rows and cols for segmentation
def main(args):
    print("MAIN START")
    tiles = vars(args)["tiles"]
    color = vars(args)["color"]
    percent = vars(args)["percent"]
    # rows, cols = 10, 10
    rows, cols = int(tiles), int(tiles)


    yellow_threshold = 50         # Tolerance for yellow (e.g. ±50 from 255,255,0)
    # yellow_percentage = 1.0       # Minimum percentage of yellow pixels required to save the tile
    yellow_percentage = 0.1 * float(percent)
    print("THRESHOLD SET")
    # print("COLOR", color)
    if color == "1":
        curr_color = "white"
    elif color == "3":
        curr_color = "green"
    else:
        curr_color = "yellow"
    rads = ['0.001', '0.01', '0.1', '1.0', '2.0']
    # rads = ['untreated', 'Compound_1', 'Compound_2', 'Compound_3', 'Compound_4', 'Compound_5', 'Compound_6', 'Compound_7', 'Compound_8', 'Compound_9', 'Compound_10', 'Compound_11', 'Compound_12', 'Compound_13', 'Compound_14', 'Compound_15', 'Compound_16', 'Compound_17']
    # weeks = ['week_one', 'week_two', 'week_three', 'week_four']
    weeks = ['week_nine']

    # remove contents of directory
    # dir_path = f'/eagle/FoundEpidem/astroka/fib_and_htert/cnn_data/'+week+'/fib_control/'
    # if os.path.isdir(dir_path):
    #     for item in os.listdir(dir_path):
    #         item_path = os.path.join(dir_path, item)
    #         if os.path.isdir(item_path):
    #             shutil.rmtree(item_path)
    print("START OF LOOP")
    for week in weeks:
        for rad in rads:
            print(week, rad)
            # image_path = '/eagle/FoundEpidem/astroka/fib_and_htert/'+week+'/results/fib_rad/'+rad+'/'
            # output_folder = f'/eagle/FoundEpidem/astroka/fib_and_htert/cnn_data/'+week+'/fib_rad/'+rad+'/'
            image_path = f'/eagle/FoundEpidem/astroka/rpe/'+week+'/results/rpe_rad/'+rad+'/'
            output_folder = f'/eagle/FoundEpidem/astroka/yolo/rpe_rad_tiles_9/images/'+rad+'/'
            if os.path.isdir(output_folder) == False:
                print("output folder made")
                os.mkdir(output_folder)
            
            print("IMAGE_PATH", image_path)
            print("OUTPUT PATH", output_folder)

            # remove contents of directory
            # dir_path = f'/eagle/FoundEpidem/astroka/fib_and_htert/cnn_data/'+week+'/fib_control/'
            # if os.path.isdir(dir_path):
            #     for item in os.listdir(dir_path):
            #         item_path = os.path.join(dir_path, item)
            #         if os.path.isdir(item_path):
            #             shutil.rmtree(item_path)

                
            segment_image(image_path, output_folder, rows, cols, yellow_threshold, yellow_percentage, curr_color)

            #if contents of output folder are empty, delete output folder

            if os.path.isdir(output_folder) and not os.listdir(output_folder):
                os.rmdir(output_folder)  

# Segment the image
# segment_image(image_path, output_folder, rows, cols, yellow_threshold, yellow_percentage)

if __name__ == "__main__":
    print('START')
    parser = argparse.ArgumentParser()

    parser.add_argument(
    "-c",
    "--color",
    help="source folder name",
    type=str,
    required=True,
    )

    parser.add_argument(
    "-t",
    "--tiles",
    help="source folder name",
    type=str,
    required=True,
    )

    parser.add_argument(
    "-p",
    "--percent",
    help="source folder name",
    type=str,
    required=True,
    )


    args = parser.parse_args()
    main(args)