from project import hyperbolic_patch, rename, pad
import numpy as np
from PIL import Image as Im 
import glob
from PIL import ImageOps as ImO
import math

image_name = "histo"
image = Im.open("images/" + str(image_name)+".jpg") 
original_width = image.width
angle= 0.0
step = 128
n_rows = original_width//step

def test_hyperbolic_patch():
    """
    GIVEN: an image
    WHEN: apply the hyperbolic_patch function to it 
    THEN: test passes when the output are patches of the original image that scale with the factor 1/(2**(n-1)) 
    """
    hyperbolic_patch(image,  step=128, width= 128, height = 128)
    patches_per_row = image.width // step
    for n in range(0, patches_per_row):
        for m in range(0, patches_per_row):
            for j in range(1,patches_per_row+1): 
                for i in range(1,patches_per_row+1):
                    img = Im.open(f"patch_res_{j-n}_{i-m}.jpg")
                    assert img.height == image.height//(patches_per_row*2**abs((j-n-1)))
                    assert img.width == image.width // (patches_per_row*2**abs((i-m-1)))

def test_rename():
    """
    GIVEN: the outputs of hyperbolic_patch function
    WHEN: apply the rename function to them
    THEN: the tests passes when the number of previous images it's equal to the 
    renamed ones, so all have been renamed
    """
    old_name = len(glob.glob("hyperbolic_corner*"))
    rename()
    new_name = glob.glob("images/hyperbolic_*")
    assert old_name == len(new_name)

def test_comparison():
    """
    GIVEN: hyperbolic patches
    WHEN: opening all images to plot them 
    THEN: the tests passes when rows and col of the plot are integer numbers
    and their product gives the total number of patches. It means they all are 
    shown into a squared grid. 
    """
    images = glob.glob("images/hyperbolic_"+str(image_name)+ "patch_n*") #opening patches
    n_patch = len(images)
    row= int(math.sqrt(n_patch))
    col = n_patch // row
    assert type(row)  == int
    assert type(col) == int
    assert row * col == n_patch 

def test_pad():
    assert pad(0) == step
    for i in range(n_rows):
        assert pad(i) % 2 == 0

def test_centering():
    # rewriting centering_function 

    n_rows = original_width // step  
    
    num = 1 
    right=0 
    bottom=0
    left=0
    top=0

    for row in range(1, n_rows+1):
        if row == 1: 
            top= 0 
            bottom = 0 
            for i in range(1, n_rows - row + 1):
                top = top + pad(i)  
                

        if 1 < row <= n_rows//2 & row != 1: 
            bottom = 0 
            sum_top =  0
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
        
        for col in range(1 ,n_rows+1):
            img=Im.open("images/hyperbolic_"+str(image_name)+ f"patch_n°{num}.jpg") 
            
            if col == 1: 
                left = 0 
                right= 0
                for i in range(1, n_rows - col + 1): 
                    left = left + pad(i)

            if 1< col <= n_rows//2 & col != 1: 
                right = 0
                sum_left = 0
                for i in range(1, n_rows - col + 1):
                    sum_left = sum_left + pad(i)
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
            
            if col == n_rows: 
                left =  0 
                right = 0 
                for i in range(1, n_rows):
                    right = right + pad(i)
                  
            border = (left, top, right, bottom)
            new_img = ImO.expand(img, border=border, fill="black")
        
            if row == 1: 
                assert new_img.height //2  == top + step//2 
            if 1 < row <= n_rows//2: 
                half = 0 
                for j in range(1, row):
                    half = half + pad(j)
                assert new_img.height //2  == top + step//2 + half

            num = num +1