from project import hyperbolic_patch, rename, comparison 
import numpy as np
from PIL import Image as Im 
from patchify import patchify
import glob
import math

image_name = "labrador"
image = Im.open("images/" + str(image_name)+".jpg") 
original_width = image.width
angle= 0.0
step = 128
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
