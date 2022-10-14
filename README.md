

# Hyperbolic Patch

## Project

The aim of this project is to create hyperbolic patches starting from a given image.

This method is mainly used for histological images for neural networks; indeed this images could have high dimensions and in general pictures with dimensions larger than 512x512 pixels require a lot of time to be elaborated by a neural network.

The solution consists into divide the original image into a grid with squares of a fixed dimension (e.g. 128 x 128 pixels)
Fixing one of this square as the seed section, the peripherical ones are scaled in both the direction by $\frac{1}{2^{n-1}}$ where *n* is and integer number, equal to 1 for the centered sections and increases in function of the distance from the center.
This scaling takes into account both direction:

$$\begin{cases}
height' = \frac{height}{2^{j-1}}\\
\\ width' = \frac{width}{2^{i-1}}
\end{cases}$$

The result is called hyperbolic patch; it's an image with smaller dimensions compared to the original. 
The seed square maintain the same dimension, while the rest of the image is compressed. 
This operation is repeated using as seed section each square of the grid.

The result is a series of images with reduced dimensions that focus on different features of the original image, as shown below: 

<div  align='center'>
<img  src="https://i.ibb.co/NmqgC9b/lab.png"  alt="mid" border="0">
</div>


It's also possible to perform a rotation of the input image, here's some example:

<div  align='center'>
<img  src="https://i.ibb.co/KKdQBTw/Hyperbolic-patches.png"  alt="mid" border="0">
</div>


## Table of contents

  

-  `images`

-  `.gitignore`

-  `project.py`

-  `test_project.py`

-  `requirements.txt`

  

The folder `images` contains the images used as input and some output examples

Into `.gitignore` are contained all files we don't want to track.

`project.py` is the main script for the project.

`test_project.py` is the script used for the testing.

At the end `requirements.txt` contains packages that must be installed for the project.

  

## Installation

To install the packages usefull for the project clone the repository and use pip:

```

git clone https://github.com/francescapunzetti/hyperbolic_patch.git

cd hyperbolic_patch

pip install -r requirements.txt

```

In this way the whole repository in cloned.

## How to run 
Once installed the requirements, it's possible to proceed with the project. 
First of all, should decide the input image; if it isn't present yet into the folder `images`, you can add it: 

    mv path_your_file/file  images/

The only restriction is that the input should be a squared image. 

Then at the beginning of the script you can set the input:

    image_name = "your_image"
    image = Im.open("images/" + str(image_name)+".jpg") #change also the
    #type of image if it's not .jpg

And if you want to perform a rotation of the input image: 

    angle = float(number) #insert 0 if you don't want rotation 

Then all parameters are set and you can compile the script. 

All images to obtain the intermediate patches will be saved in the main folder, and will be overwrite if you decide to perform the program multiple times. 
Instead, the output hyperbolic patches will be saved in the folder `images` and labeled with the name of the initial image and enumerated.

At the end the code will plot all the hyperbolic patches obtained: 

<div  align='center'>

<img  src="https://i.ibb.co/FK2xP0y/Input-512pixel.png"  alt="mid"  border="0">

</div>

**Attention:** take into account that the grid would be compressed, so the squares cannot be too small: some rows or columns could be compressed at dimensions < 1 and that's not possible! For this reason the dimension of the squares are fixed to 128x128 pixels.