from project import concatenate_hor, concatenate_vert, create_corners, hyperbolic_patch, comparison
import numpy as np
from PIL import Image, ImageOps
from patchify import patchify
from matplotlib import pyplot as plt
from datetime import datetime
import glob
from natsort import natsorted
import sys

image = Image.open("images/labrador.jpg")

def test_concatenate_hor(): 
    img= concatenate_hor(image, image)
    assert (img.width == 2* image.width)
    assert img.height == image.height

def test_concatenate_vert(): 
    img= concatenate_vert(image, image)
    assert (img.width == image.width)
    assert img.height == 2*image.height



