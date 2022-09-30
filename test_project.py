from project import concatenate_hor, concatenate_vert, create_corners, hyperbolic_patch, result_image, comparison
import numpy as np
from PIL import Image, ImageOps
from patchify import patchify
from matplotlib import pyplot as plt
from datetime import datetime
import glob
from natsort import natsorted
import sys

image = Image.open("images/labrador.jpg")
angle = 0

def test_concatenate_hor(): 
    img= concatenate_hor(image, image)
    assert (img.width == 2* image.width)
    assert img.height == image.height

def test_concatenate_vert(): 
    img= concatenate_vert(image, image)
    assert (img.width == image.width)
    assert img.height == 2*image.height

def test_create_corners():
    create_corners(image)
    for i in range(1, 5):
        patch = Image.open(f"corner_{i}.jpg")
        assert patch.width == image.width // 4
        assert patch.height == image.height // 4

patches_per_row = 4
def test_hyperbolic_patch():
    hyperbolic_patch(image)
    for j in range(1,patches_per_row+1):
        for i in range(1,patches_per_row+1):
            img = Image.open(f"patch_res_{j}_{i}.jpg")
            assert img.height == image.height // int(2**(j-1))
            assert img.width == image.width // int(2**(i-1))
#testing the scaling by the 1/2**(n-1) factor 

def test_result_image():
    img = Image.open("images/final_image" +str(angle)+".jpg")
    assert img.width < image.width
    assert img.height < image.height