from tkinter import Image
import numpy as np
from PIL import Image as Im
from PIL import ImageOps as ImO
from patchify import patchify
from matplotlib import pyplot as plt
from datetime import datetime
import glob
import os
import math


#SETTING PARAMETERS: 

#Importing the input image.
#It must be a squared image.
image_name = "labrador"
image = Im.open("images/" + str(image_name)+".jpg") 

#To perform hyperbolic patches at different rotations
angle = float(10) #choose angle of rotation 
image= image.rotate(angle, resample=0, expand=0)

#Saving the original dimensions for the following functions
original_width = image.width

def hyperbolic_patch(
    image: Image,
    step: int,
    width: int,
    height: int) -> Image:
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
    patches_per_row = image.width // step
    image = np.asarray(image)
    patches = patchify(image, (width, height, 3), step=step)
    for n in range(0, patches_per_row):
        for m in range(0, patches_per_row):
            for i in range(patches.shape[0]):
                for j in range(patches.shape[1]):
                    patch = patches[i, j, 0]
                    patch = Im.fromarray(patch)
                    num = i * patches.shape[1] + j
                    patch.save(f"patch_{num+1}.jpg")

#rename all patches per rows and columns to work on indices
            for j in range(0,patches_per_row): #n° row 
                for i in range(1,patches_per_row+1): #n° column
                    patch = Im.open(f"patch_{j*patches_per_row+ i}.jpg")   #works
                    patch.save(f"patch_{j+1-n}_{i-m}.jpg")

#higher is the values of the indeces, higher is the distance from the starting patch. The starting patch has 
#value 2**(args) = 1
            for j in range(1,patches_per_row+1): 
                for i in range(1,patches_per_row+1):
                    image = Im.open(f"patch_{j-n}_{i-m}.jpg")
                    height= int(step/(2**abs((j-n-1))))
                    width = int(step/(2**abs((i-m-1))))
                    image_resized = image.resize((width,height), resample=0, reducing_gap=None)
                    image_resized.save(f"patch_res_{j-n}_{i-m}.jpg")

#once all patches had hyperbolic compression, recreate rows
            for j in range(1,patches_per_row+1):
                vector_row= []
                for i in range(1,patches_per_row+1):
                    image = Im.open(f"patch_res_{j-n}_{i-m}.jpg")
                    vector_row.append(image)
                    merge = np.hstack(vector_row)
                merged = Im.fromarray(merge)
                merged.save(f"row_{j}.jpg")

#all rows are stack together to recreate the original image with hyperbolic compression
            vector_col= []
            for j in range(1,patches_per_row+1):
                image = Im.open(f"row_{j}.jpg")
                vector_col.append(image)
            merge = np.vstack(vector_col)
            hyperbolic_corner = Im.fromarray(merge)

#the output image is labeled with the time, in order to not overwrite images
            now = datetime.now()
            now = now.strftime("%-I%-M%-S%f")
            image_name = "hyperbolic_corner"+str(now)+".jpg"
            hyperbolic_corner.save(image_name)
    return hyperbolic_corner

def rename(): 
    """
    This function renames all the outputs of the hyperbolic_patch
    function replacing the label of time with input image name and
    enumerating the images
    """
    images = glob.glob("hyperbolic_corner*")
    images = sorted(images)
    i = 0
    for image in images: 
        with open(image, 'rb') as file:
            old_name = image
            new_name = "images/hyperbolic_"+str(image_name)+"patch_n°"+str(i+1) +".jpg"  
            os.rename(old_name, new_name)
            i = i+1


def comparison():
   
    """
    This function plots all patches obtained side by side
    """
    images = glob.glob("images/hyperbolic_"+str(image_name)+ "patch_n*") #opening patches
    n_patch = len(images)
    row= int(math.sqrt(n_patch))
    col = n_patch // row
    i=0
    for image in images: 
        img=Im.open(str(image))
        plt.subplot(row, col , i+1) 
        plt.suptitle('Patches')
        plt.imshow(img)      
        i = i+1
    plt.show()


hyperbolic_patch(image,  step=128, width= 128, height = 128) 
rename()
comparison()
