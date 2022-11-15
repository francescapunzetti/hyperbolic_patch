# Hyperbolic Patch

## Project

The aim of this project is to create hyperbolic patches starting from a given image.

This method is mainly used for histological images for neural networks; indeed these images could have high dimensions and in general pictures large dimensions require a lot of time to be elaborated by any neural network.

To overcome this problem, a solution could consist into dividing the original image into a grid with squares of a fixed dimension.

Fixing one of this square as the seed section, the peripherical ones are scaled in both the direction by $\frac{1}{2^{n-1}}$ where *n* is and integer number, equal to 1 for the centered sections and increases in function of the distance from the center.
This scaling takes into account both direction:

$$\begin{cases}
height' = \frac{height}{2^{j-1}}\\
\\ width' = \frac{width}{2^{i-1}}
\end{cases}$$

The output is an hyperbolic compressed patch; indeed, it's an image with smaller dimensions compared to the original. 
In particular, the seed square maintain the same dimension, while the rest of the image is compressed. 
This operation is repeated using as seed section each square of the grid.

The result is a series of images with reduced dimensions that focus on different features of the original image, as shown below: 

<div align='center'>
<table cellspacing="2" cellpadding="2" width="600" border="0">
<tbody>
<tr>
<td valign="top" height="400" width="400"><img src="https://i.ibb.co/tmkjVqm/Schermata-2022-11-08-alle-15-53-22.png" alt="original" align=”center” title="Original" border="0"></a></td>
<td valign="top" width="500"><img src="https://i.ibb.co/P1gtPcX/lab-1.png" alt="lab 0" align=”center” border="0"></a></td>
</tr>
</tbody>
</table>
</div>

It's also possible to perform a rotation of the input image, here's an example with a rotation angle of 45 degrees:

<div  align='center'>
<img  src="https://i.ibb.co/rbzpZMH/lab-45.png"  alt="mid" border="0">
</div>


## Table of contents

  

-  `images`

-  `.gitignore`

-  `project.py`

-  `test_project.py`

-  `requirements.txt`

  

The folder `images` contains the images used as input and some output examples. This folder includes also test images, used to test functions.

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
    
The input parameters are optimize to use as input also OME tiff type; in particular this images are pyramidal tiff containing different layers of the picture with a decreasing resolution. 

So once compiled the script, you can choose to use as input a pyramidal tiff and separate the different "pages" or use another format. 

If you select the first one, the program creates a number of .jpg equal to the number of layer in the folder `images`; if you select the latter, you skip directly to insert the name of the page or image you want to use:
```
image_name = input("Name of layer or image to be considered:")
```

After this, in case of particularly large image, you can crop just a part as input by entering the (xmin, ymin, xmax, ymax) value of the area:
```
area = input("Select area in the image (x0, y0, y0, y1). \nIf you don't want to crop the image insert original dims: ") 
area = tuple(map(int, area.split(', ')))
```

Then, it's possible to insert an angle of rotation of the input image.

After this, it is necessary to set the dimensions of the grid of the image and consequently the number of patches for which perform the hyperbolic compression. 

    hyberbolic_patches(image, step, width, height) 

In order to obtain best results, the values of `step`, `width` and `height` should be the same; in this way you can avoid the oversampling (patches overlap) and the undersampling (you lose some pixels between a patch and the next one).

Then it's necessary to add borders to the obtained images in order to center the "zoomed" part of the image, where we have the focus; this would be very helpfull when using these images as input for any neural network. 

That's done using the function `centering()`. In this function the default value of the step is 128, so if it is set differently in the function `hyperbolic_patches()`, you have also to change in the first one, so that you can have the correct centering of the patches. 

After you compile the script, all intermediate patches will be saved in the main folder, and will be overwrite if you decide to compile the script multiple times. 

Instead, the final hyperbolic patches will be saved in the folder `images`, enumerated and labeled with the name of the input image and the angle of rotation.

At the end the code will plot all the hyperbolic patches obtained: 

<div  align='center'>

<img  src="https://i.ibb.co/cyNmRK7/Patches1.png"  alt="mid"  border="0">

</div>
