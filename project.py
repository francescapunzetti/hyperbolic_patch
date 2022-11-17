import glob
from PIL import Image as Im
from main import main
from patches import hyperbolic_patch, rename, centering, comparison

Im.MAX_IMAGE_PIXELS = None

# setting input parameters
(image_name, image, angle) = main()

hyperbolic_patch(image, image_name, angle, step=128, width= 128, height = 128) 
rename(image_name, angle)
centering(image, image_name, angle, step=128)

images = glob.glob("images/hyperbolic_"+str(image_name)+"_"+str(angle)+ "_"+"patch_n°*")
comparison(images)
