import streamlit as st				#Streamlit allows you to write an app the same way you write a python code.

import cv2					#A library of Python bindings designed to solve computer vision problems.

from PIL import Image				#PIL is the Python Imaging Library which provides the python interpreter with image editing capabilities.
from io import BytesIO				#Binary I/O (also called buffered I/O) expects bytes-like objects and produces bytes objects. 

import pybase64 as base64			#To get the fastest decoding, it is recommended to use the pybase64.
import os					#The Os module in Python provide functions for interacting with the operating system.
import numpy					#NumPy is the fundamental package for scientific computing in Python.

from skimage import exposure			#Performs Gamma Correction on the input image.
from skimage.transform import rotate		#Rotate image by a certain angle around its center.
from skimage import util			#Return an image showing the differences between two images.#Return intensity limits, i.e. (min, max) tuple, of the image's dtype.etc
st.balloons()					#in-built python
def load_image(image_file):			#helps in loading images.
    img = Image.open(image_file)
    return img

def convert_to_sketch(image_file):		#function to convert the selected image into sketch.
    pil_img = Image.open(image_file)		#PIL is the Python Imaging Library which provides the python interpreter with image editing capabilities. 						 							
    img = numpy.array(pil_img)		#
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)	#converting image to grayfrom(bgr=blue,green,red)
    invert = cv2.bitwise_not(grey_img)		#We are using the bitwise_not function which is used to make brighter regions lighter and vice versa so that we can find the edges to create a 								#pencil sketch.
    blur = cv2.GaussianBlur(invert, (21, 21), 0)	#we are specifically converting to gussian blur, although there are various types of blur in photoshop like motion blur,lens blur,radial blur etc.
    							#in this we are also defining that for how much level we want to blur like for me it is (21,21),0)
    invertedblur = cv2.bitwise_not(blur)		#a new variable having properties of both blur and invert.
    sketch = cv2.divide(grey_img, invertedblur, scale=255.0)		#final variable that is finally converting to sketch and here we have to provide a scale for sketch likewise I have provided 256.
    return sketch

def adjust_brightness(image_file):		#function to adjust the brightness of selected or uploaded image.
    pil_img = Image.open(image_file)		#PIL is the Python Imaging Library which provides the python intrepreter with image editing capabilities. The image module provides a class with the same 						#name which is used to represent a PIL image. The module also provides a number of factory functions, including functions to load images from files, and 
    						#to create new images. 
    img = numpy.array(pil_img)
    max_gamma = 50				#setting max value of gamma to 50. We can set it to according to our need.
    gamma_value = st.slider("Select brightness", 0, max_gamma, 5, 1)		#here I have created or set the starting the value of brightness means the lowest, i.e, 0 and max to 50 and the increament 										#or decreament of 1.
    image_final = exposure.adjust_gamma(img, gamma=gamma_value/10, gain=1)	
    return image_final

def adjust_rotation(image_file):		#function to rotate the selected or uploaded image.
    pil_img = Image.open(image_file)		#PIL is the Python Imaging Library which provides the python intrepreter with image editing capabilities. The image module provides a class with the same 						#name which is used to represent a PIL image. The module also provides a number of factory functions, including functions to load images from files, and 
    						#to create new images.
    img = numpy.array(pil_img)
    max_angle = 360				#setting max value of angle to 360 degrees ,ie. we can full rotate our image.
    angle = st.slider("Select image rotation angle", 0, max_angle, 70, 5)	#here I have created or set the starting value of rotation means default to 70 and increament or decreament of 5.
    image_rotated = rotate(img, angle=angle, resize=True)
    image_array_rotated_bytes = util.img_as_ubyte(image_rotated)
    return image_array_rotated_bytes

def get_image_download_link(image, conversion_mode):		#a function for download link, i.e, to download the converted image or the image in which we have made changes.
    pil_image = Image.fromarray(numpy.uint8(image), mode=conversion_mode)	#PIL is the Python Imaging Library which provides the python intrepreter with image editing capabilities. The image module 										#provides a class with the same name which is used to represent a PIL image. The module also provides a number of factory 											#functions, including functions to load images from files. mode=conversion_mode means the converted image to download.
    path_prefix = os.path.dirname(os.path.abspath(__file__)) + "/"		#providing the path of file
    byte_io = BytesIO()
    pil_image.save(byte_io, format="PNG")
    png_buffer = byte_io.getvalue()
    b64_download_data = base64.b64encode(png_buffer).decode()
    filename = path_prefix + "converted_image"
    href = f'<a href="data:file/txt;base64,{b64_download_data}" download="{filename}">Download converted image</a>'
    return href

def process_image_download(image, conversion_mode):
    href = get_image_download_link(image, conversion_mode)
    st.markdown("Your image is ready for download. Please click this " + href + " to download the image.", unsafe_allow_html=True)

def process_image(image_file, operation):
    if image_file is None:
        return

    st.subheader("Preview")			#it is a subheader, i.e, I ahve written preview. we can write anything we want. That is the preview of uploaded image.
    st.image(load_image(image_file), width = 350)

    result_image = None
    conversion_mode = "RGB"

    st.subheader("Output")			#it is a subheader, i.e, I ahve written preview. we can write anything we want. That is it showing the output.
    if operation == "convert2sketch":		#condition dependent on user.
        result_image = convert_to_sketch(image_file) 
        conversion_mode = "L"
    elif operation == "rotate":		#condition dependent on user.
        result_image = adjust_rotation(image_file)
    elif operation == "brightness":		#condition dependent on user.
        result_image = adjust_brightness(image_file)

    st.image(result_image, width=350)
    st.button("Get Download Link", on_click=process_image_download, args=(result_image, conversion_mode, ))	#download link button.
