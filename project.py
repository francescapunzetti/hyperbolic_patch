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


# Importing the input image
# It must be a squared image
image_name = "histo"
image = Im.open("images/" + str(image_name)+".jpg") 

# To perform hyperbolic patches at different rotations
angle = float(0) # choose angle of rotation 
image= image.rotate(angle, resample=0, expand=0)

# Saving the original dimensions for the following functions
original_width = image.width

def hyperbolic_patch(
    image: Image,
    step: int,
    width: int,
    height: int) -> Image:
    """
    Parameter:
    ---------------
    image = input image whose want to perform an hyperbolic compression.
    
    This patchify the input image in a number of patches variable, equal to 
    image_dim // step.
    Then for each of them is performed and hyperbolic compression 
    of the (w,h) of a factor 1/(2**(n-1)). n depends on the distance 
    from the first patch which has index == 1 and mantains 
    the same dimensions. 
    The first patch changes and the index == 1 moves along the image.

    n can be separated in i for the columns and j for the row. 
    After the resized all the patches are stacked back together. 
    The output is an RGB image with an hyperbolic compression.
    """ 

    patches_per_row = image.width // step
   
    # the input for the patchify function must be an array 
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

    # rename all patches per rows and columns in function of the indices values
            for j in range(0,patches_per_row): #n° row 
                for i in range(1,patches_per_row+1): #n° column
                    patch = Im.open(f"patch_{j*patches_per_row+ i}.jpg") 
                    patch.save(f"patch_{j+1-n}_{i-m}.jpg")

    # higher is the values of the indeces, higher is the distance from the starting patch. 
    # the starting patch has as indices j-n = i-m = 1
            for j in range(1,patches_per_row+1): 
                for i in range(1,patches_per_row+1):
                    image = Im.open(f"patch_{j-n}_{i-m}.jpg")
                    height= int(step/(2**abs((j-n-1))))
                    width = int(step/(2**abs((i-m-1))))
    # the h and w of the image must be >= 0 
                    if height & width >= 0: 
                        image_resized = image.resize((width,height), resample=0, reducing_gap=None)
                        image_resized.save(f"patch_res_{j-n}_{i-m}.jpg")

    # once all patches had hyperbolic compression, recreate rows
            for j in range(1,patches_per_row+1):
                vector_row= []
                for i in range(1,patches_per_row+1):
                    image = Im.open(f"patch_res_{j-n}_{i-m}.jpg")
                    vector_row.append(image)
                    merge = np.hstack(vector_row)
                merged = Im.fromarray(merge)
                merged.save(f"row_{j}.jpg")

    # all rows are stack together to recreate the original image with hyperbolic compression
            vector_col= []
            for j in range(1,patches_per_row+1):
                image = Im.open(f"row_{j}.jpg")
                vector_col.append(image)
            merge = np.vstack(vector_col)
            hyperbolic_corner = Im.fromarray(merge)

    # the output image is labeled with the time, in order to not overwrite images
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

    # sorting the image make us sure we are opening the images in order by row
    images = sorted(images)
    i = 0

    for image in images: 
        with open(image, 'rb') as file:
            old_name = image
            new_name = "images/hyperbolic_"+str(image_name)+"_"+str(angle)+ "_"+"patch_n°"+str(i+1) +".jpg"  
            os.rename(old_name, new_name)
            i = i+1


def pad(i: int,
        step=128) -> int: 
        """
        This funtion returns the dimension in pixels of the columns or rows
        after the hyperbolic compression. 
        
        Parameter
        -------------------
        step = original size of the region to be resized. Default 128.
        i = number of the i-th column/row
        """
        return step//(2**i)
        
def centering(step: int): 
    """
    This function adds a black padding in order to center the zoomed part 
    of the hyperbolic patches.

    Paramenter
    -----------------
    step = size of the zoomed part in the hyperbolic patch 
    """
    n_rows = original_width // step # total number of columns and rows 
    
    num = 1 # initialize the enumeration the number of hyperbolic patch 
    
    # initialize the dimension of the padding borders
    right=0 
    bottom=0
    left=0
    top=0

    for row in range(1, n_rows+1):
    
    # adding the padding in the direction of the zoomed patch. In this way we can 
    # balance the image in order to center it 

        if row == 1: 
    #first row has no rows above, so need to be balanced with all the remaining rows        
            top= 0 
            bottom = 0 
            for i in range(1, n_rows - row + 1):
    # just adding the number of pixels of the image in y direction excluding the current row
                top = top + pad(i)  
                

        if 1 < row <= n_rows//2 & row != 1: 
            bottom = 0 
            sum_top =  0
    # adding a number of pixels equal to the difference between the n° of pixels
    # before and after the current row
            for i in range(1, n_rows - row + 1):
                sum_top = sum_top + pad(i)
            for j in range(1, row):
                top = sum_top - pad(j)


        if n_rows//2 < row < n_rows: 
            top = 0 
            sum_bottom = 0
            for i in range(1, n_rows - row + 1):
                sum_bottom = sum_bottom + pad(i)  
            for j in range(1, row):
                bottom = sum_bottom - pad(j)
        
        if row == n_rows: 
            bottom= 0 
            top= 0 
            for i in range(1, n_rows):
                bottom = bottom + pad(i)
        
    # same procedure also for colums, so adding padding at left and right 
        for col in range(1 ,n_rows+1):
            img=Im.open("images/hyperbolic_"+str(image_name)+"_"+str(angle)+ "_"+f"patch_n°{num}.jpg") 
            
            if col == 1: 
                left = 0 
                right= 0
    #i is the number of columns after the focused one
                for i in range(1, n_rows - col + 1): 
                    left = left + pad(i)

            if 1< col <= n_rows//2 & col != 1: 
                right = 0
                sum_left = 0
                for i in range(1, n_rows - col + 1):  
                    sum_left = sum_left + pad(i)
    # j is the number of columns before the focused one             
                for j in range(1, col): 
                    sum_left = abs(sum_left - pad(j))
                    left= sum_left
            
            if  n_rows//2 < col < n_rows:
                left = 0 
                sum_right=  0
                for i in range(1, n_rows - col + 1 ): 
                    sum_right = sum_right + pad(i) 
                for j in range(1, col):
                    right = sum_right - pad(j) 

    # if it's the last column there are not pixels after it            
            if col == n_rows: 
                left =  0 
                right = 0 
                for i in range(1, n_rows): 
                    right = right + pad(i)
                  
            border = (left, top, right, bottom)
            new_img = ImO.expand(img, border=border, fill="black")
            new_img.save("images/hyperbolic_"+str(image_name)+"_"+str(angle)+ "_"+f"patch_n°{num}.jpg")
            num = num +1
 
def comparison():
   
    """
    This function plots all patches obtained by the previous 
    functions side by side in a grid
    """
    images = glob.glob("images/hyperbolic_"+str(image_name)+"_"+str(angle)+ "_"+"patch_n°*")
    
    # creating a squarred grid with equal number of column and rows where showing the output
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
centering(step=128)
comparison()
