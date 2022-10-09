
# Hyperbolic Patch

## Project

The aim of this project is to create an hyperbolic patch starting from a given image.

This method is mainly used for histological images for neural networks; indeed this images could have high dimensions and in general pictures with dimensions larger than 512x512 pixels require a lot of time to be elaborated by a neural network, when it's possible.

  

The solution consists into divid the original image in subsection; the center of the image mantain the same dimensions, the peripherical sections instead are scaled in both the direction by $\frac{1}{2^{n-1}}$ where *n* is and integer number, equal to 1 for the centered senctions and increases in function of the distance from the center.

This scaling takes into account both direction:

$$\begin{cases}
height' = \frac{height}{2^{j-1}}\\
\\ width' = \frac{width}{2^{i-1}}
\end{cases}$$
  

The result image is compressed, but the center of the image, hypotetically where there are insterresting informations, has still a good resolution, while as you go far from the core the spatial resolution decrease as a power of 2.

Here's some examples with a general image at different angles of rotation:

<div  align='center'>

<img  src="https://i.ibb.co/KKdQBTw/Hyperbolic-patches.png"  alt="mid"  border="0">

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

At the end `requirements.txt` contains packages that must be installed for the the project.

  

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

    angle = float(10) #inster 0 if you don't want rotation 

Then all parameters are set and you can compile the script. 
All images to obtain the patches will be saved in the main folder, and will be overwrite if you decide to perform the program multiple times. 

The only exception are the output, which are labeled with the original name and the angle of rotation, and the set of image `hyperbolic_corner*` which are labeled with the time; the latters shoul be **rename or removed** if you want to perform again the program, because it is set to pick 4 image in ascedent order, **so this would false your results**. 

The output is a comparison between the original image and the hyperbolic compressed image, which is also saved as jpg. 
Here's some results: 

<table cellspacing="0" cellpadding="0" border="0" align="center">
<tbody>
<tr>
<th> <img src="https://i.ibb.co/m9yPqsw/final-image-histo0-0.jpg" width="200px" alt="No rotation" align=”center” border="0"><br> <a> No rotation
</a></th>
<th valign="top" ><img src="https://i.ibb.co/FXpc6tZ/final-image-histo15-0.jpg" width="200px" alt="15 degree rotation" align=”center” border="0"><br> <a> 15 degree rotation 
</a></th>
</tr>
<tr>
<th valign="top" ><img src="https://i.ibb.co/HCpHYVQ/final-image-histo30-0.jpg" width="200px" alt="30 degree rotation" align=”center” border="0"><br> <a> 30 degree rotation
</a></th>
<th valign="top" ><img src="https://i.ibb.co/8P3xWmR/final-image-histo45-0.jpg" width="200px" alt="45 degree rotation" align=”center” border="0"><br> <a> 45 degree rotation
</a></th>
</tr>
</tbody>
</table>

Enjoy!
