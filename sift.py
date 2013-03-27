from PIL import Image, ImageFilter
import os
from numpy import *
from pylab import *

def gen_blurred_images(img):
    img = img.filter(ImageFilter.BLUR)
    outputFile = 'tmp/test1.png'
    img.save(outputFile)

    img = Image.open(outputFile)
    img = img.filter(ImageFilter.BLUR)
    outputFile = 'tmp/test2.png'
    img.save(outputFile)

    img = Image.open(outputFile)
    img = img.filter(ImageFilter.BLUR)
    outputFile = 'tmp/test3.png'
    img.save(outputFile)

    img = Image.open(outputFile)
    img = img.filter(ImageFilter.BLUR)
    outputFile = 'tmp/test4.png'
    img.save(outputFile)

    img = Image.open(outputFile)
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)
    img = img.filter(ImageFilter.BLUR)
    outputFile = 'tmp/test5.png'
    img.save(outputFile)

test_image = Image.open("TestImages/ab0010.jpg")

gen_blurred_images(test_image)
