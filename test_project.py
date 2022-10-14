from project import hyperbolic_patch, comparison
import numpy as np
from PIL import Image, ImageOps
from patchify import patchify
from matplotlib import pyplot as plt
from datetime import datetime
from natsort import natsorted
from mock import patch
import sys
from unittest.mock import patch

image = Image.open("images/margherita.jpg")
original_width = image.width
angle= 0.0
step = 128
def test_hyperbolic_patch():
    """
    GIVEN: an image
    WHEN: apply the hyperbolic_patch function to it 
    THEN: pass when the output are patches of the original image that scale with the factor 1/(2**(n-1)) 
    """
    hyperbolic_patch(image)
    patches_per_row = image.width // step
    for n in range(0, patches_per_row):
        for m in range(0, patches_per_row):
            for j in range(1,patches_per_row+1): 
                for i in range(1,patches_per_row+1):
                    img = Image.open(f"patch_res_{j-n}_{i-m}.jpg")
                    assert img.height == image.height//(patches_per_row*2**abs((j-n-1)))
                    assert img.width == image.width // (patches_per_row*2**abs((i-m-1)))

