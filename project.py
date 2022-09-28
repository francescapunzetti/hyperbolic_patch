from math import log2
import numpy as np
from PIL import Image, ImageOps
from patchify import patchify
from matplotlib import pyplot as plt
import math

#importing the initial image
image = Image.open("images/image1.jpg")
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

def final_image():
    quarter_right = Image.open("final.jpg")
    quarter_left = ImageOps.flip(quarter_right)
    quarter_left.save("quarter_left.jpg")
    image = concatenate_vert(quarter_left, quarter_right)
    image.save("half.jpg")

    half_right = Image.open("half.jpg")
    half_left = ImageOps.mirror(half_right)
    half_left.save("half_left.jpg")
    image = concatenate_hor(half_left, half_right)
    image.save("geometric_projection.jpg")

####################
#create the hyperbolic patch
def hyperbolic_patch(image):
    step=64
    width= 64
    height = 64
    patches_per_row = 4
    patches = patchify(image, (width, height, 3), step=step)
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            patch = patches[i, j, 0]
            patch = Image.fromarray(patch)
            num = i * patches.shape[1] + j
            patch.save(f"patch_{num+1}.jpg")

## rename all patches per row
    for i in range(1,patches_per_row):
        patch = Image.open(f"patch_{i}.jpg")   
        patch.save(f"patch_1_{i}.jpg")
    for i in range(1,patches_per_row):
        patch = Image.open(f"patch_{4+i}.jpg")
        patch.save(f"patch_2_{i}.jpg")
    for i in range(1,patches_per_row):
        patch = Image.open(f"patch_{8+i}.jpg")
        patch.save(f"patch_3_{i}.jpg")
    for i in range(1,patches_per_row):
        patch = Image.open(f"patch_{12+i}.jpg")
        patch.save(f"patch_4_{i}.jpg")

    for j in range(1,patches_per_row):
        for i in range(1,patches_per_row):
            image = Image.open(f"patch_{j}_{i}.jpg")
            height= int(step/(2**(j-1)))
            width = int(step/(2**(i-1)))
            image_resized = image.resize((width,height), resample=0, box=None, reducing_gap=None)
            image_resized.save(f"patch_res_{j}_{i}.jpg")

    for j in range(1,patches_per_row):
        for i in range(1,patches_per_row):
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
    final.save("final.jpg")
    return final

#showing the differences between the original image and the generated
def comparison(reference, final):
    fig = plt.figure(figsize=(10, 7))
    fig.add_subplot(1, 2, 1) #in first position 
    plt.imshow(reference)
    plt.title("Reference")
    fig.add_subplot(1, 2, 2) #in second position 
    plt.imshow(final)
    plt.title("Hyperbolic patch")
    plt.show()

hyperbolic_patch(image)
final = Image.open("final.jpg")
comparison(image, final)
