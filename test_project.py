from project import hyperbolic_patch, rename, comparison, pad, pad_per_row, pad_per_col, centering, save_patch, reconstruct_image
import numpy as np
from PIL import Image as Im 
import glob
from PIL import ImageOps as ImO
import math
from patchify import patchify

image_name = "histo" #test image
image = Im.open("images/" + str(image_name)+".jpg") 
original_width = image.width
angle= 0.0
#step must have the same value as in project.py
step = 128 
n_rows = original_width//step

def test_save_patch():
    """
    GIVEN: an np array of different patches
    WHEN: applied the function save_patch
    THEN: the test passes when all patches are saved 
    with a given name 
    """
    image = Im.open("images/" + str(image_name)+".jpg") 
    image = np.asarray(image)
    patches = patchify(image, (128, 128, 3), step=128)
    save_patch(patches)
    images = glob.glob("first_patch*")
    assert len(images) == 4

def test_reconstruct_image(): 
    """
    GIVEN: patches of images
    WHEN: apply the reconstruct_image function
    THEN: test passes when all patches are reconstructed
    per group 
    """
    patches_per_row = 2
    for n in range(0, patches_per_row):
        for m in range(0, patches_per_row):
            reconstruct_image(patches_per_row, n, m)

    rows = glob.glob("row*")
    assert len(rows) == patches_per_row


def test_hyperbolic_patch():
    """
    GIVEN: an image
    WHEN: apply the hyperbolic_patch function to it 
    THEN: test passes when the output are patches of the 
    original image that scale with the factor 1/(2**(n-1)) 
    """
    hyperbolic_patch(image,  step=128, width= 128, height = 128)
    hyperbolic = glob.glob("hyperbolic*")
    for hyper in hyperbolic: 
        hyper = Im.open(hyper)
        hyper.height == hyper.width == 128+64 #dimension from 256x256 image with 128 step

def test_rename():
    """
    GIVEN: the outputs of hyperbolic_patch function
    WHEN: apply the rename function to them
    THEN: the tests passes when the number of previous images 
    it's equal to the renamed ones, so all have been renamed
    """
    old_name = len(glob.glob("hyperbolic_corner*"))
    rename()
    new_name = glob.glob("images/hyperbolic_*")
    assert old_name == len(new_name)


def test_pad():
    """
    GIVEN: step
    WHEN: applying pad(i) function, where i is and integer
    THEN: the test passes when 0 is the neutral element and 
    step scales by two for all the other numbers from 1 to 
    the total number of rows.
    """
    assert pad(0) == step
    for i in range(n_rows):
        assert pad(i) % 2 == 0

def test_pad_per_row():
    """
    GIVEN: an image
    WHEN: applied the function pad_per_row
    THEN: the test passes when the padding in fuction of 
    the row makes the zoomed part of the image beeing in the
    center of the y dimension.
    """
    image = Im.open("images/test_pad_1.jpg") 

    row=1
    (bottom, top) = pad_per_row(row, n_rows=4)
    assert image.height //2  == top + step//2
    assert bottom == 0 
    
    image = Im.open("images/test_pad_2.jpg") 
    
    row=2
    (bottom, top) = pad_per_row(row, n_rows=4)
    assert image.height //2  == top + 2*pad(1)

    image = Im.open("images/test_pad_3.jpg") 

    row=3
    (bottom, top) = pad_per_row(row, n_rows=4)
    assert image.height //2  == bottom + 2*pad(1)

def test_pad_per_col():
    """
    GIVEN: an image
    WHEN: applied the function pad_per_col
    THEN: the test passes when the padding in fuction of 
    the column makes the zoomed part of the image beeing in the
    center of the x dimension.
    """
    image = Im.open("images/test_pad_1.jpg") 
    col=1
    (right, left) = pad_per_col(col, n_rows=4)
    assert image.width //2  == left + step//2
    assert right == 0 

    image = Im.open("images/test_pad_2.jpg") 
    
    col=2
    (right, left) = pad_per_col(col, n_rows=4)
    assert image.width //2  == left + 2*pad(1)

    image = Im.open("images/test_pad_3.jpg") 

    col=3
    (right, left) = pad_per_col(col, n_rows=4)
    assert image.width //2  == right + 2*pad(1)

    image = Im.open("images/test_pad_4.jpg") 

    col=4
    (right, left) = pad_per_col(col, n_rows=4)
    assert image.width //2  == right + pad(1)

def test_centering():
    """
    GIVEN: hyperbolic patches
    WHEN: applying centering function
    THEN: the test passes when the output image has dimensions 
    given by the padding corresponding to the dim of the 
    test centered images.
    """
    centering(step=128) 
    images_centering = glob.glob("images/hyperbolic_"+str(image_name)+"_"+str(angle)+ "_"+"patch_n°*")
    i = 1
    for image in images_centering:
        img = Im.open(image) 
        test = Im.open(f"images/test{i}.jpg")
        i = i +1 
        assert img.width == test.width
        assert img.height == test.height
    
def test_comparison():
    """
    GIVEN: hyperbolic patches
    WHEN: opening all images to plot them 
    THEN: the tests passes when rows and col of the plot are integer numbers
    and their product gives the total number of patches. It means they all are 
    shown into a squared grid. 
    """
    images = glob.glob("images/test*") #there are 8 images
    (row, col) = comparison(images)
    assert row * col == 8