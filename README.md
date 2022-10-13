

# Hyperbolic Patch

## Project

The aim of this project is to create hyperbolic patches starting from a given image.

This method is mainly used for histological images for neural networks; indeed this images could have high dimensions and in general pictures with dimensions larger than 512x512 pixels require a lot of time to be elaborated by a neural network.

The solution consists into divide the original image in subsection; then starting from a chosen section in the image, that will maintain the same dimensions, the peripherical sections are scaled in both the direction by $\frac{1}{2^{n-1}}$ where *n* is and integer number, equal to 1 for the centered sections and increases in function of the distance from the center.

This scaling takes into account both direction:

$$\begin{cases}
height' = \frac{height}{2^{j-1}}\\
\\ width' = \frac{width}{2^{i-1}}
\end{cases}$$
  
 The result image has an hyperbolic compression but the seed section keeps the initial resolution. 
Here's some examples with a general image; the first one focus the compression into the center of the input images with different angle of rotation: 

<div  align='center'>
<img  src="https://i.ibb.co/KKdQBTw/Hyperbolic-patches.png"  alt="mid" border="0">
</div>
The second one has an angle of rotation fixed to 0 and moves the focus along the image:
<div  align='center'>
<img  src="https://i.ibb.co/NmqgC9b/lab.png"  alt="mid" border="0">
</div>

The latter is the direct output of the script. 
As we can see, it's possible to focus on different details of the orginal images even if the final dimensions of the patches are smaller.
  

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

    angle = float(10) #insert 0 if you don't want rotation 

Then all parameters are set and you can compile the script. 

All images to obtain the intermediate patches will be saved in the main folder, and will be overwrite if you decide to perform the program multiple times. 
Instead, the output images will be saved in the folder `images` and labeled with the name of the initial image and the angle of rotation.

The output is a plot with the input image and all the patches generated, which are also saved as jpg. 
Here's some results, with angle of rotation equal to 0: 

<div  align='center'>

<img  src="https://i.ibb.co/W6H9vH5/Patches.png"  alt="mid"  border="0">

</div>

Enjoy!
