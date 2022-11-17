from PIL import Image as Im
from PIL import ImageSequence

def main():
    """
    This function sets the input parameters for the functions
    contained in patches.py
    """
    # 'y' is the input is an OME tiff and need to separate different
    # layers, 'n' otherwise
    OME_tiff = "n"
    if OME_tiff == "y":
        pyramidal = Im.open("images/CMU.tiff")
        for i, page in enumerate(ImageSequence.Iterator(pyramidal)):
            page.save("images/Page%d.jpg" % i)

    # insert the layer or the image to be used as input for the 
    # hyperbolic patches
    image_name = "histo"
    image = Im.open("images/" + str(image_name)+".jpg") 

    # insert the area of the image where you want to perform hyperbolic 
    # patches. If you want to peform in all the image, insert the image 
    #dimensions
    area = (0, 0, 256, 256)
    image = image.crop(area)

    angle = 0.0
    image= image.rotate(angle, resample=0, expand=0, fillcolor=(255,255,255))
    return (image_name, image, angle)    
    
    
    