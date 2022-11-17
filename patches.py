import glob
import math
import os
from datetime import datetime
from tkinter import Image
import numpy as np
from matplotlib import pyplot as plt
from patchify import patchify
from PIL import Image as Im
from PIL import ImageOps as ImO

Im.MAX_IMAGE_PIXELS = None

def save_patch(patches: np.array):
    """
    Save all patches in order per row starting from a 
    patchfied image
    ----------------------
    Parameter: 
    patches: np.array containing all patches to be
    saved
    """
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            patch = patches[i, j, 0]
            patch = Im.fromarray(patch)
            num = i * patches.shape[1] + j
            patch.save(f"first_patch_{num+1}.jpg")

def reconstruct_image(patches_per_row: int,
                    n: int,
                    m: int)-> Image:
    """
    Reconstruct image starting from patches labelad with n° of
    col and row
    ----------------------
    Parameters: 
    patches_per_row: number of patches per each row and col
    m,n: index to move the starting point along the image 
    """
# all rows are stack together to recreate the original image with hyperbolic compression
    for j in range(1,patches_per_row+1):
        vector_row= []
        for i in range(1,patches_per_row+1):
            image = Im.open(f"patch_res_{j-n}_{i-m}.jpg")
            vector_row.append(image)
            merge = np.hstack(vector_row)
        merged = Im.fromarray(merge)
        merged.save(f"row_{j}.jpg")

# once all patches had hyperbolic compression, recreate rows
    vector_col= []
    for j in range(1,patches_per_row+1):
        image = Im.open(f"row_{j}.jpg")
        vector_col.append(image)
    merge = np.vstack(vector_col)
    hyperbolic_corner = Im.fromarray(merge)
    return hyperbolic_corner


def hyperbolic_patch(
    image: Image,
    image_name: str,
    angle: int,
    step: int,
    width: int,
    height: int) -> Image:
    """
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
    
    Parameters:
    ---------------
    image = input image whose want to perform an hyperbolic compression.
    image_name = str with the name of the input image
    angle = angle of rotation
    step = step of patches
    width = width of patches
    height = height of patches 
    """ 

    image = image.rotate(angle =angle, resample=0, expand=0)
    patches_per_col = image.width // step
    patches_per_row = image.height // step
   
    # the input for the patchify function must be an array 
    
    image = np.asarray(image)
    patches = patchify(image, (width, height, 3), step=step)
    
    for n in range(0, patches_per_row):
        for m in range(0, patches_per_col):
            save_patch(patches)
    # rename all patches per rows and columns in function of the indices values
            for j in range(0,patches_per_row): #n° row 
                for i in range(1,patches_per_col+1): #n° column
                    patch = Im.open(f"first_patch_{j*patches_per_col+ i}.jpg") 
                    patch.save(f"patch_{j+1-n}_{i-m}.jpg")

    # higher is the values of the indeces, higher is the distance from the starting patch. 
    # the starting patch has as indices j-n = i-m = 1
            for j in range(1,patches_per_row+1): 
                for i in range(1,patches_per_col+1):
                    image = Im.open(f"patch_{j-n}_{i-m}.jpg")
                    height= int(step/(2**abs((j-n-1))))
                    width = int(step/(2**abs((i-m-1))))
    # the h and w of the image must be >= 0 
                    if height & width >= 0: 
                        image_resized = image.resize((width,height), resample=0, reducing_gap=None)
                        image_resized.save(f"patch_res_{j-n}_{i-m}.jpg")
    # all rows are stack together to recreate the original image with hyperbolic compression
            hyperbolic_corner = reconstruct_image(patches_per_col, n, m)

    # the output image is labeled with the time, in order to not overwrite images
            now = datetime.now()
            now = now.strftime("%-I%-M%-S%f")
            image_name = "hyperbolic_corner"+str(now)+".jpg"
            hyperbolic_corner.save(image_name)



def rename(
    image_name: str,
    angle: int): 
    """
    This function renames all the outputs of the hyperbolic_patch
    function replacing the label of time with input image name and
    enumerating the images
    
    Parameters: 
    -------------------
    image_name = str with name of the input image
    angle = angle of rotation 
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
        
        Parameters
        -------------------
        step = original size of the region to be resized. Default 128.
        i = number of the i-th column/row
        """
        return step//(2**i)
        
def pad_per_row(row: int,
                n_rows: int
                )-> int:
    """
    This function returns values for padding at top and bottom in order
    to center the selected row.

    Parameters
    --------------------
    row = index of the selected row 
    n_rows = total number of rows 
    """
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
    
    return (bottom, top)

def pad_per_col(col: int,
                n_cols: int
                )-> int:
    """
    This function returns values for padding at right and left in order
    to center the selected column.

    Parameters
    --------------------
    col = index of the selected col
    n_cols = total number of columns
    """
    if col == 1: 
        left = 0 
        right= 0
    #i is the number of columns after the focused one
        for i in range(1, n_cols - col + 1): 
            left = left + pad(i)

    if 1< col <= n_cols//2 & col != 1: 
        right = 0
        sum_left = 0
        for i in range(1, n_cols - col + 1):  
            sum_left = sum_left + pad(i)
    # j is the number of columns before the focused one             
        for j in range(1, col): 
            sum_left = abs(sum_left - pad(j))
            left= sum_left
            
    if  n_cols//2 < col < n_cols:
        left = 0 
        sum_right=  0
        for i in range(1, n_cols - col + 1 ): 
            sum_right = sum_right + pad(i) 
        for j in range(1, col):
            right = sum_right - pad(j) 

    # if it's the last column there are not pixels after it            
    if col == n_cols: 
        left =  0 
        right = 0 
        for i in range(1, n_cols): 
            right = right + pad(i)
    return (right, left)
                  

def centering( 
    image: Image,
    image_name: str,
    angle: int,
    step: int): 
    """
    This function adds a black padding in order to center the zoomed part 
    of the hyperbolic patches.

    Parameters
    -----------------
    image = input image whose want to perform an hyperbolic compression.
    image_name = str with the name of the input image
    angle = angle of rotation
    step = size of the zoomed part in the hyperbolic patch 
    """
    n_cols = image.width // step # total number of columns and rows 
    n_rows= image.height// step

    num = 1 # initialize the enumeration the number of hyperbolic patch 
    
    # initialize the dimension of the padding borders
    right=0 
    bottom=0
    left=0
    top=0

    for row in range(1, n_rows+1):
        
        (bottom, top)= pad_per_row(row, n_rows)
        
    # same procedure also for colums, so adding padding at left and right 
        for col in range(1 ,n_cols+1):
            img=Im.open("images/hyperbolic_"+str(image_name)+"_"+str(angle)+ "_"+f"patch_n°{num}.jpg") 
            
            (right, left)= pad_per_col(col, n_cols)
            
            border = (left, top, right, bottom)
            new_img = ImO.expand(img, border=border, fill="black")
            new_img.save("images/hyperbolic_"+str(image_name)+"_"+str(angle)+ "_"+f"patch_n°{num}.jpg")
            num = num +1
 
def comparison(images
            )-> int:
    """
    This function plots all patches obtained by the previous 
    functions side by side in a grid

    Parameter:
    -----------------
    images: images you want to compare 
    """
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
    return (row, col)
