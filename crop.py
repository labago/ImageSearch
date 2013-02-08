from PIL import Image
import sys

the_image = Image.open(sys.argv[1])

w,h = the_image.size
the_image.crop((20, 20, 200, 400)).save('croppedImage.png')