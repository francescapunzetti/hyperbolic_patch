import numpy as np
from PIL import Image, ImageOps
from patchify import patchify
from matplotlib import pyplot as plt
from datetime import datetime
import glob
from natsort import natsorted
import sys


#importing the initial image
image = Image.open("images/labrador.jpg")
angle = sys.argv[1]
angle = float(angle)
image= image.rotate(angle, resample=0, expand=0, center=None, translate=None, fillcolor=None)
original_width = image.width
channels = 3
image = np.asarray(image)

#stack together the resized patches in both directions
def concatenate_hor(im1, im2):
    row = Image.new('RGB', (im1.width + im2.width, im1.height))
    row.paste(im1, (0, 0))
    row.paste(im2, (im1.width, 0))
    return row

def concatenate_vert(im1, im2):
    col = Image.new('RGB', (im1.width, im1.height + im2.height))
    col.paste(im1, (0, 0))
    col.paste(im2, (0, im1.height))
    return col

#create the four angles 
def create_corners(image):
    step= (original_width //2)
    width= (original_width //2)
    height = (original_width //2)
    patches = patchify(image, (width, height, 3), step=step)
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            patch = patches[i, j, 0]
            patch = Image.fromarray(patch)
            num = i * patches.shape[1] + j
            patch.save(f"corner_{num+1}.jpg")
    for i in range(1, 5):
        patch = Image.open(f"corner_{i}.jpg")
        if i == 1: 
            corner = ImageOps.mirror(patch)
            corner = ImageOps.flip(corner)
            corner.save("images/upper_left.jpg")
        if i==2: 
            corner = ImageOps.flip(patch)
            corner.save("images/upper_right.jpg")
        if i==3:
            corner = ImageOps.mirror(patch)
            corner.save("images/bottom_left.jpg")  


#create the hyperbolic patch
def hyperbolic_patch(image):
    step=image.width//4
    width= image.width//4
    height = image.width//4
    patches_per_row = 4
    image = np.asarray(image)
    patches = patchify(image, (width, height, 3), step=step)
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            patch = patches[i, j, 0]
            patch = Image.fromarray(patch)
            num = i * patches.shape[1] + j
            patch.save(f"patch_{num+1}.jpg")

## rename all patches per row
    for i in range(1,patches_per_row+1):
        patch = Image.open(f"patch_{i}.jpg")   
        patch.save(f"patch_1_{i}.jpg")
    for i in range(1,patches_per_row+1):
        patch = Image.open(f"patch_{4+i}.jpg")
        patch.save(f"patch_2_{i}.jpg")
    for i in range(1,patches_per_row+1):
        patch = Image.open(f"patch_{8+i}.jpg")
        patch.save(f"patch_3_{i}.jpg")
    for i in range(1,patches_per_row+1):
        patch = Image.open(f"patch_{12+i}.jpg")
        patch.save(f"patch_4_{i}.jpg")

    for j in range(1,patches_per_row+1):
        for i in range(1,patches_per_row+1):
            image = Image.open(f"patch_{j}_{i}.jpg")
            height= int(step/(2**(j-1)))
            width = int(step/(2**(i-1)))
            image_resized = image.resize((width,height), resample=0, box=None, reducing_gap=None)
            image_resized.save(f"patch_res_{j}_{i}.jpg")

    for j in range(1,patches_per_row+1):
        for i in range(1,patches_per_row+1):
            image = Image.open(f"patch_res_{j}_{i}.jpg")
            if i == 1:
                im1= image
            if i == 2:
                im2= image
                row1= concatenate_hor(im1 , im2)
            if i == 3:
                im3= image
                row2 = concatenate_hor(row1 , im3)
            if i == 4:
                im4= image
                row3= concatenate_hor(row2 , im4)
                row3.save(f"row_{j}.jpg")

    row1 = Image.open("row_1.jpg")
    row2 = Image.open("row_2.jpg")
    row3 = Image.open("row_3.jpg")
    row4 = Image.open("row_4.jpg")
    row12=concatenate_vert(row1,row2)
    row123 = concatenate_vert(row12, row3)
    final = concatenate_vert(row123, row4)
    now = datetime.now()
    now = now.strftime("%-I%-M%-S%f")
    image_name = "final"+str(now)+".jpg"
    final.save(image_name)
    return final

#showing the differences between the original image and the generated
def comparison(reference, final):
    fig = plt.figure(figsize=(10, 7))
    fig.add_subplot(2, 2, 1) #in first position 
    plt.imshow(reference)
    plt.title("Reference")
    fig.add_subplot(1, 2, 2) #in second position 
    plt.imshow(final)
    plt.title("Hyperbolic patch 15°")
    plt.show()

create_corners(image)

u_left = Image.open("images/upper_left.jpg")
u_right = Image.open("images/upper_right.jpg")
b_left = Image.open("images/bottom_left.jpg")
b_right = Image.open("corner_4.jpg")
hyperbolic_patch(u_left)
hyperbolic_patch(u_right)
hyperbolic_patch(b_left)
hyperbolic_patch(b_right)


images = glob.glob("final*")
images = natsorted(images)
i = 0
for image in images: 
    with open(image, 'rb') as file:
        img = Image.open(file)
        corner = img.copy()
        corner.save("corner_res_"+str(i+1)+".jpg")
        i = i +1 



u_left = Image.open("corner_res_1.jpg")
u_left = ImageOps.mirror(u_left)
u_left = ImageOps.flip(u_left)
u_left.save("corner_res_1.jpg")
u_left = Image.open("corner_res_1.jpg")
###ok
u_right = Image.open("corner_res_2.jpg")
u_right = ImageOps.flip(u_right)
u_right.save("corner_res_2.jpg")
u_right= Image.open("corner_res_2.jpg")
##
b_left = Image.open("corner_res_3.jpg")
b_left = ImageOps.mirror(b_left)
b_left.save("corner_res_3.jpg")
b_left = Image.open("corner_res_3.jpg")
##ok
b_right = Image.open("corner_res_4.jpg")
up =concatenate_hor(u_left,u_right)
bottom = concatenate_hor(b_left, b_right)
final_image = concatenate_vert(up, bottom)
final_image.save("images/final_image.jpg")
final = Image.open("images/final_image.jpg")

image = Image.open("images/labrador.jpg")
comparison(image, final)
