from project import concatenate_hor, concatenate_vert, create_corners, hyperbolic_patch, result_image, comparison
import numpy as np
from PIL import Image, ImageOps
from patchify import patchify
from matplotlib import pyplot as plt
from datetime import datetime
from natsort import natsorted
from mock import patch
import sys
from unittest.mock import patch

image = Image.open("images/labrador.jpg")
angle= 0.0

def test_concatenate_hor(): 

    """
    GIVEN: two image with the same height
    WHEN: apply to the concatenate_hor function
    THEN: pass when the output is an image with dimensions (w1+w2,h)
    """

    img= concatenate_hor(image, image)
    assert (img.width == 2* image.width)
    assert img.height == image.height

def test_concatenate_vert(): 
    """
    GIVEN: two image with the same width
    WHEN: apply to the concatenate_vert function
    THEN: pass when the output is an image with dimensions (w, h1+h2)
    """

    img= concatenate_vert(image, image)
    assert (img.width == image.width)
    assert img.height == 2*image.height

def test_create_corners():
    """
    GIVEN: a squared image into array form
    WHEN: apply the create_corner function to it 
    THEN: pass when the output is the input image split in 4 images with same dimensions
    """
    img = Image.open("images/labrador.jpg")
    img = np.asarray(img)
    create_corners(img)
    for i in range(1, 5):
        patch = Image.open(f"corner_{i}.jpg")
        assert patch.width == image.width // 2
        assert patch.height == image.height // 2

patches_per_row = 4

def test_hyperbolic_patch():
    """
    GIVEN: an image
    WHEN: apply the hyperbolic_patch function to it 
    THEN: pass when the output are patches of the original image that scale with the factor 1/(2**(n-1)) 
    """
    hyperbolic_patch(image)
    for j in range(1,patches_per_row+1):
        for i in range(1,patches_per_row+1):
            img = Image.open(f"patch_res_{j}_{i}.jpg")
            assert img.height == image.height // (4* int(2**(j-1)))
            assert img.width == image.width // (4* int(2**(i-1)))



def test_result_image():
    #result_image()
    """
    GIVEN: the output of the 
    WHEN: apply the creat_corner function to it 
    THEN: pass when the output is the input image split in 4 images with same dimensions
    """
    img = Image.open("images/final_image" +str(angle)+ ".jpg")
    assert img.width < image.width
    assert img.height < image.height