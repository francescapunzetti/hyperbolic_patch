from tkinter import Image
import numpy as np
from PIL import Image as Im
from PIL import ImageOps as ImO
from patchify import patchify
from matplotlib import pyplot as plt
from datetime import datetime
import glob
from natsort import natsorted
import sys


#SETTING PARAMETERS: 

#Importing the input image.
#It must be a squared image.
image_name = "histo"
image = Im.open("images/" + str(image_name)+".jpg") 

#To perform hyperbolic patches at different rotations
angle = float(45) #choose angle of rotation 
image= image.rotate(angle, resample=0, expand=0)

#Saving the original dimensions for the following functions
original_width = image.width


def create_corners(
    image: Image,
    original_width: int):
    """
    Arguments: 
    image = input image which suold be diveded in quarters;
    original_width = dimension of the image (it must be squared). 

    This function divides a squared image into quartes, alias 
    splitting the image into 4 identical part. 

    All of them are flipped in order to have the center of 
    the image in the upper- left corner.
    """

    step= (original_width //2) #step must be the same value of the w and h to avoid overlap
    width= (original_width //2)
    height = (original_width //2)
    image = np.asarray(image) #change in array type to separate in multiple array
    patches = patchify(image, (width, height, 3), step=step) 
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            patch = patches[i, j, 0]
            patch = Im.fromarray(patch)
            num = i * patches.shape[1] + j
            patch.save(f"corner_{num+1}.jpg")
    for i in range(1, 5):
        patch = Im.open(f"corner_{i}.jpg")
        if i == 1: 
            corner = ImO.mirror(patch)
            corner = ImO.flip(corner)
            corner.save("upper_left.jpg")
        if i==2: 
            corner = ImO.flip(patch)
            corner.save("upper_right.jpg")
        if i==3:
            corner = ImO.mirror(patch)
            corner.save("bottom_left.jpg")  

#To stack together all the resized patches: 
def concatenate_hor(
    im1: Image, 
    im2: Image) -> Image:
    """
    Arguments:
    im1, im2 = images to be stack together in the horizontal direction.
    
    The two images can have whatever dimensions.
    The function return an image with dimension (w1+w2, h1).
    The images will be stack in the writing order.
    """
    row = Im.new('RGB', (im1.width + im2.width, im1.height))
    row.paste(im1, (0, 0))
    row.paste(im2, (im1.width, 0))
    return row

def concatenate_vert(
    im1: Image, 
    im2: Image) -> Image:
    """
    Arguments:
    im1, im2 = images to be stack together in the vertical direction.

    The two images can have whatever dimensions. 
    The function return an image with dimension (w1, h1+h2).
    The images will be stack in the writing order.
    """
    col = Im.new('RGB', (im1.width, im1.height + im2.height))
    col.paste(im1, (0, 0))
    col.paste(im2, (0, im1.height))
    return col


def hyperbolic_patch(
    image: Image) -> Image:
    """
    Argument:
    image = input image whose want to make an hyperbolic compression.
    
    This patchify the input image in 16 patches. Then for each of them 
    is performed and hyperbolic compression of the (w,h) of a factor
    1/(2**(n-1)). n depends on the distance from the first patch
    in the upper-left corner, which mantain the same dimensions. 
    n can be separated in i for the columns and j for the row. 
    After the resized all the patches are stacked back together. 
    The output is an RGB image with an hyperbolic compression.
    """
    step=image.width//4 
    width= image.width//4
    height = image.width//4
    patches_per_row = 4
    image = np.asarray(image)
    patches = patchify(image, (width, height, 3), step=step)
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            patch = patches[i, j, 0]
            patch = Im.fromarray(patch)
            num = i * patches.shape[1] + j
            patch.save(f"patch_{num+1}.jpg")

#rename all patches per rows and columns to work on indices
    for i in range(1,patches_per_row+1):
        patch = Im.open(f"patch_{i}.jpg")   
        patch.save(f"patch_1_{i}.jpg")
    for i in range(1,patches_per_row+1):
        patch = Im.open(f"patch_{4+i}.jpg")
        patch.save(f"patch_2_{i}.jpg")
    for i in range(1,patches_per_row+1):
        patch = Im.open(f"patch_{8+i}.jpg")
        patch.save(f"patch_3_{i}.jpg")
    for i in range(1,patches_per_row+1):
        patch = Im.open(f"patch_{12+i}.jpg")
        patch.save(f"patch_4_{i}.jpg")

#higher is the values of the indeces, higher is the distance from the starting patch (upper left)
    for j in range(1,patches_per_row+1): 
        for i in range(1,patches_per_row+1):
            image = Im.open(f"patch_{j}_{i}.jpg")
            height= int(step/(2**(j-1)))
            width = int(step/(2**(i-1)))
            image_resized = image.resize((width,height), resample=0, reducing_gap=None)
            image_resized.save(f"patch_res_{j}_{i}.jpg")

#once all patches had hyperbolic compression, recreate rows
    for j in range(1,patches_per_row+1):
        for i in range(1,patches_per_row+1):
            image = Im.open(f"patch_res_{j}_{i}.jpg")
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

#all rows are stack together to recreate the original image with hyperbolic compression
    row1 = Im.open("row_1.jpg")
    row2 = Im.open("row_2.jpg")
    row3 = Im.open("row_3.jpg")
    row4 = Im.open("row_4.jpg")
    row12=concatenate_vert(row1,row2)
    row123 = concatenate_vert(row12, row3)
    hyperbolic_corner = concatenate_vert(row123, row4)

#the output image is labeled with the time, in order to not overwrite images
    now = datetime.now()
    now = now.strftime("%-I%-M%-S%f")
    image_name = "hyperbolic_corner"+str(now)+".jpg"
    hyperbolic_corner.save(image_name)
    return hyperbolic_corner

def result_image():
    """
    This function recompose the compressed quarters of the input 
    image and the output is the original image with an hyperbolic 
    compression. 

    It sorts the outputs from the function hyperbolic_patch 
    and rename them in function of the position of the corners. 
    Then it flips them as in origin and stack together to obtain
    the final image
    """
#images are labeld with time, so need to sort them in ascending order
#to fix the order of the corners and reconstruct the image
    images = glob.glob("hyperbolic_corner*")
    images = natsorted(images)
    i = 0
    for image in images: 
        with open(image, 'rb') as file:
            img = Im.open(file)
            corner = img.copy()
            corner.save("corner_res_"+str(i+1)+".jpg") #rename corners to simplify recognition 
            i = i +1 
#flipping the quarters as in origin
    u_left = Im.open("corner_res_1.jpg")
    u_left = ImO.mirror(u_left)
    u_left = ImO.flip(u_left)
    u_left.save("corner_res_1.jpg")
    u_left = Im.open("corner_res_1.jpg")

    u_right = Im.open("corner_res_2.jpg")
    u_right = ImO.flip(u_right)
    u_right.save("corner_res_2.jpg")
    u_right= Im.open("corner_res_2.jpg")

    b_left = Im.open("corner_res_3.jpg")
    b_left = ImO.mirror(b_left)
    b_left.save("corner_res_3.jpg")
    b_left = Im.open("corner_res_3.jpg")

    b_right = Im.open("corner_res_4.jpg")
#reconstruct the total image with all the quarters
    up =concatenate_hor(u_left,u_right)
    bottom = concatenate_hor(b_left, b_right)
    final_image = concatenate_vert(up, bottom)
    final_image.save("images/final_image_" +str(image_name)+str(angle)+".jpg")

def comparison(
    reference: Image,
    final: Image) -> Image: 
    """
    Arguments: 
    reference: input image
    final: output image
    This function plots the two images side by side
    """
    #no test needed because it's a visualization function 
    fig = plt.figure(figsize=(10, 10))
    fig.add_subplot(2, 2, 1) #in first position 
    plt.imshow(reference)
    plt.title("Reference")
    fig.add_subplot(2, 2, 2) #in second position 
    plt.imshow(final)
    plt.title("Hyperbolic patch"+ str(angle))
    plt.show()


create_corners(image, original_width)

u_left = Im.open("upper_left.jpg")   #u = upper
u_right = Im.open("upper_right.jpg") 
b_left = Im.open("bottom_left.jpg") #b = bottom 
b_right = Im.open("corner_4.jpg")

#repeat this operation for all quarters of the input image
hyperbolic_patch(u_left)
hyperbolic_patch(u_right)
hyperbolic_patch(b_left)
hyperbolic_patch(b_right)
result_image()
final = Im.open("images/final_image_" +str(image_name) +str(angle)+".jpg")
comparison(image, final)
