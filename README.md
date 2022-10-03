# Hyperbolic Patch 
## Project
The aim of this project is to create an hyperbolic patch starting from a given image. 
This method is mainly used for histological images for neural networks; indeed this images could have higher dimension and in general picture with dimensions larger of 512x512 pixels require a lot of time to be elaborated by a neural network, when it's possible. 

The solution consists into dived the original image in subsection; the center of the image mantain the same dimensions, the peripherical sections instead are scaled in both the direction by $\frac{1}{2^{n-1}}$ where *n* is and integer number, equal to 1 for the centered senctions and increases in function of the distance from the center. 
This scaling takes into account both direction: 

$$\begin{cases}
height' = \frac{height}{2^{j-1}}\\
\\ width' = \frac{width}{2^{i-1}}
\end{cases}$$

The result image is compressed, but the center of the image, hypotetically where there are insterresting informations, has still a good resolution, while as you go far from the core the spatial resolution decrease as a power of 2. 
Here's some examples with a general image at different angles of rotation:
<div align='center'>
<img src="https://i.ibb.co/KKdQBTw/Hyperbolic-patches.png" alt="mid" border="0">
</div>

## Table of contents

 - `images`
 - `.gitignore`
 - `project.py`
 - `test_project.py`
 - `requirements.txt`

The folder `images`  contains the images used as input and some output examples

Into `.gitignore` contains all files we don't want to track. 

`project.py` is the main script for the project.

`test_project.py` is the script used for the testing. 

At the end `requirements.txt` contains packages that must be installed for the the project.

## Installation 
 To install the packages usefull for the project clone the repository and use pip: 
 ```
git clone https://github.com/francescapunzetti/project.git
cd project
pip install -r requirements.txt
```
In this way the whole repository in cloned.
