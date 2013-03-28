#!/usr/bin/python
from PIL import Image, ImageFilter, ImageChops
import sys
import os
import math
import scipy
import numpy
from datetime import datetime

# a class to represent the ImageSearch application
class ImageSearch:

	# constructor, takes the pattern image location string and source image location string
	# if either image is not found, termiinate program and alert user
	def __init__(self, pattern_array, source_array):
		self.pattern_array = pattern_array
		self.source_array = source_array
		self.current_confidence = 0
		self.matches = []
		self.output_image_name = ""

	# function for matching two directories of images
	def match_images(self):
		for pattern in self.pattern_array:
			for source in self.source_array:
				try:
					self.patternImage = Image.open(pattern)
					self.patternName = pattern.split('\\')[-1]
				except (IOError, IndexError):
					print >>sys.stderr, 'Pattern image not found or not of the correct image format.'
					sys.exit(1)

				try:
					self.sourceImage = Image.open(source)
					self.sourceName = source.split('\\')[-1]
				except (IOError, IndexError):
					print >>sys.stderr, 'Source image not found or not of the correct image format.'
					sys.exit(1)
				
				self.patternFormat = self.patternImage.format
				self.sourceFormat = self.sourceImage.format

				if self.patternImage.mode != "RGB":
					self.patternImage = self.patternImage.convert("RGB")

				if self.sourceImage.mode != "RGB":
					self.sourceImage = self.sourceImage.convert("RGB")
				# try to match the images

				self.patternPixels = self.patternImage.load()
				self.patSize = self.patternImage.size
				self.patPixelArray = []
				for x in range(0, self.patSize[0]):
					for y in range(0, self.patSize[1]):
						self.patPixelArray.append((self.patternPixels[x,y], x, y))

				self.sourcePixels = self.sourceImage.load()
				self.sourceSize = self.sourceImage.size
				self.sourcePixelArray = []
				for x in range(0, self.sourceSize[0]):
					for y in range(0, self.sourceSize[1]):
						self.sourcePixelArray.append((self.sourcePixels[x,y], x, y))

				self.sift()
				#self.SAD()

		# print all matches
		for x in self.matches:
			# print the match in the professor's format
			# removed confidence level printing ---->  + " with confidence " + str(x[5]) + "%"
			print x[0] + " matches " + x[1] + " at "+ str(x[2][0]) + "x" + str(x[2][1]) + "+" + str(x[3]) + "+" + str(x[4])

	#########################################################
	### SAD ALGORITHM, ONLY USE ON SMALL IMAGES VERY SLOW ###
	#########################################################
	def SAD(self):
		xOffset = 0
		yOffset = 0

		for x in range(0, self.sourceSize[0]):
			if x+self.patSize[0] <= self.sourceSize[0]:
				for y in range(0, self.sourceSize[1]):
					if y+self.patSize[1] <= self.sourceSize[1]:
						diff = self.get_SAD_diff(x, y)
						if diff == 0:
							self.matches.append((self.patternName, self.sourceName, self.patSize, x, y, 100))

	def get_SAD_diff(self, xoffset, yoffset):
		total_diff = 0

		for x in range(0, self.patSize[0]):
			for y in range(0, self.patSize[1]):
				sourcePixel = self.sourcePixels[x+xoffset, y+yoffset]
				patternPixel = self.patternPixels[x, y]
				total_diff += (abs(sourcePixel[0]-patternPixel[0])+abs(sourcePixel[1]-patternPixel[1])+abs(sourcePixel[2]-patternPixel[2]))		

		return total_diff

	#########################
	### END SAD ALGORITHM ###
	#########################

	############
	### SIFT ###
	############

	# try to match images using the SIFT algorithm
	def sift(self):

		patternPixels = self.patternImage.load()
		patSize = self.patternImage.size

		patPixelArray = []			# holds the "RGB" pixel data for the pattern image

		# adds the "RGB" pixel data to the list
		for x in range(0,patSize[0]):
			for y in range(0, patSize[1]):
				patPixelArray.append((patternPixels[x,y], x, y))

		patPixelArray.sort(key=lambda x: x[0])		# sorts the list of pattern "RGB" pixel data

		self.pattern_octaves = self.generate_gaussian_octavtes(self.patternImage, "pattern_"+self.patternName)
		self.source_octaves = self.generate_gaussian_octavtes(self.sourceImage, "source_"+self.sourceName)

		self.output_image_name = "Pattern"
		self.find_octave_key_points(self.pattern_octaves)
		self.output_image_name = "Source"
		self.find_octave_key_points(self.source_octaves)

	def generate_gaussian_octavtes(self, img, name):
		results = []

		size = img.size
		original_pic = img
		# for each octave
		for x in range(0, 4):
			if(x != 0):
					size = (size[0]/2, size[1]/2)
					original_pic = original_pic.resize(size)
					img = img.resize(size)
			blurred = []
			# for each progressive blur
			for y in range(0, 5):
				img = img.filter(ImageFilter.BLUR)

				diff = ImageChops.difference(original_pic, img)

				loc = "tmp/"+str(x)+"_"+str(y)+name

				temp = []
				temp.append(img)

				blurred.append(temp)
				#diff.save(loc)
			results.append(blurred)
		return results

	def find_octave_key_points(self, octaves):
			for octave in range(0, len(octaves)):
				for blurred in range(1, len(octaves[octave])-1):
					keypoints = []
					#print "Octave "+str(octave), "Blurred "+str(blurred)
					imgPixels = octaves[octave][blurred][0].load()
					imgPixels1 = octaves[octave][blurred-1][0].load()
					imgPixels2 = octaves[octave][blurred+1][0].load()
					imgSize = octaves[octave][blurred][0].size
					for x in range(0,imgSize[0]):
						for y in range(0, imgSize[1]):
							if self.check_keypoint(imgPixels[x,y], self.sourounding_pixels(x, y, imgPixels, imgPixels1, imgPixels2)):
								keypoints.append((x, y))
					octaves[octave][blurred] = (octaves[octave][blurred][0], keypoints)
			self.plot_keypoints(octaves[0])

		# for octave in range(0, len(self.source_octaves)):
		# 	for blurred in range(1, len(self.source_octaves[octave])-1):
		# 		source_keypoints = []
		# 		sourcePixels = self.source_octaves[octave][blurred].load()
		# 		sourcePixels1 = self.source_octaves[octave][blurred-1][0].load()
		# 		sourcePixels2 = self.source_octaves[octave][blurred+1][0].load()
		# 		sourceSize = self.source_octaves[octave][blurred].size
		# 		for x in range(0,sourceSize[0]):
		# 			for y in range(0, sourceSize[1]):
		# 				if self.check_keypoint(sourcePixels[x,y], self.sourounding_pixels(x, y, sourcePixels, sourcePixels1, sourcePixels2)):
		# 					source_keypoints.append((x, y))
		# 		self.source_octaves[octave][blurred] = (self.source_octaves[octave][blurred], source_keypoints)

	def plot_keypoints(self, octave):
		for x in range(1, len(octave)-1):
			image = octave[x][0]
			keypoints = octave[x][1]
			size = image.size
			new = image.copy()
			for y in keypoints:
				new.putpixel(y, (0, 255, 0))
				new.putpixel((y[0]+1, y[1]+1), (0, 255, 0))
				new.putpixel((y[0]-1, y[1]+1), (0, 255, 0))
				new.putpixel((y[0]+1, y[1]-1), (0, 255, 0))
				new.putpixel((y[0]-1, y[1]-1), (0, 255, 0))
			new.save("tmp/plotted"+self.output_image_name+str(x)+".jpg")


	def check_keypoint(self, pixel, sourounding):
		greater = False
		less = False

		pixel_value = pixel[0]+pixel[1]+pixel[2]

		for x in sourounding:
			if not less or not greater:
				temp_value = x[0]+x[1]+x[2]			
				if pixel_value < temp_value:
					less = True
				elif pixel_value > temp_value:
					greater = True
				else:
					return False
			else:
				return False
		return True

	def sourounding_pixels(self, x, y, pixels, pixels1, pixels2):
		results = []

		results.append(pixels1[x, y])
		results.append(pixels2[x, y])

		try:
			temp = pixels[x+1, y]
			results.append(temp)
			results.append(pixels1[x+1, y])
			results.append(pixels2[x+1, y])
		except IndexError:
			pass

		try:
			temp = pixels[x-1, y]
			results.append(temp)
			results.append(pixels1[x-1, y])
			results.append(pixels2[x-1, y])
		except IndexError:
			pass

		try:
			temp = pixels[x, y+1]
			results.append(temp)
			results.append(pixels1[x, y+1])
			results.append(pixels2[x, y+1])
		except IndexError:
			pass

		try:
			temp = pixels[x, y-1]
			results.append(temp)
			results.append(pixels1[x, y-1])
			results.append(pixels2[x, y-1])
		except IndexError:
			pass

		try:
			temp = pixels[x+1, y+1]
			results.append(temp)
			results.append(pixels1[x+1, y+1])
			results.append(pixels2[x+1, y+1])
		except IndexError:
			pass

		try:
			temp = pixels[x+1, y-1]
			results.append(temp)
			results.append(pixels1[x+1, y-1])
			results.append(pixels2[x+1, y-1])
		except IndexError:
			pass

		try:
			temp = pixels[x-1, y+1]
			results.append(temp)
			results.append(pixels1[x-1, y+1])
			results.append(pixels2[x-1, y+1])
		except IndexError:
			pass

		try:
			temp = pixels[x-1, y-1]
			results.append(temp)
			results.append(pixels1[x-1, y-1])
			results.append(pixels2[x-1, y-1])
		except IndexError:
			pass

		return results




	def get_image_format(self, format):
		if format == "JPEG":
			return ".jpg"
		if format == "GIF":
			return ".gif"
		if format == "PNG":
			return ".png"


#########

# used to check if an image format is supported by the program
# Arguments: fileLoc is the file location and imgtype is the type of input (pattern, source, etc.)
def checkFormat(fileLoc, imgtype):
	
	frm = fileLoc.split('.')[1]
	
	if frm != 'jpg' and frm != 'jpeg' and frm != 'png' and frm != 'gif':
		print >>sys.stderr, 'Unsupported file format: ' + '.' + frm + " in " + imgtype
		sys.exit(1)
		
# used to check if a directory has any subdirectories. Exits with exit code 1 if true
# Arguments: fileLoc is the file location and direc is the type of directory: pattern or source
def checkSubDir(fileLoc, direc, p):

	path = p.split(fileLoc)[0] + '/'   # gets the path that leads to 'fileLoc'

	if os.path.isdir(os.path.join(path, fileLoc)):
		print >>sys.stderr, 'Subdirectory found in ' + direc
		sys.exit(1)
		
# used to check if a file exists. Exits with exit code 1 if false
def checkExistence(fileLoc, filetype):

	if not os.path.exists(fileLoc):
		print >>sys.stderr, filetype + ' <' + fileLoc  + '>  does not exist'
		sys.exit(1)

#**************************************************#
#**********# BEGIN EXECUTION OF PROGRAM #**********#
#**************************************************#

startTime = datetime.now()

# parse command line arguments as the assignment requires
pattern = "NONE"
source = "NONE"
pattern_dir = "NONE"
source_dir = "NONE"

for x in range(0, len(sys.argv)):

	if(str(sys.argv[x]) == '-p'):
		
		pattern = str(sys.argv[x+1])

		# check if file exists
		checkExistence(pattern, 'pattern image')
		
		#check for unsupported file formats
		checkFormat(pattern, 'pattern image')

	if(str(sys.argv[x]) == '-s'):

		source = str(sys.argv[x+1])

		# check if file exists
		checkExistence(source, 'source image')

		# check for unsupported file formats
		checkFormat(source, 'source image')

	if(str(sys.argv[x]) == '-sdir'):

		source_dir = str(sys.argv[x+1])

		# check if directory exists
		checkExistence(source_dir, 'source directory')

		# check for subdirectories and unsupported file formats
		for f in os.listdir(source_dir):
			checkSubDir(f, 'source directory', source_dir)
			checkFormat(f, 'source directory')

	if(str(sys.argv[x]) == '-pdir'):
		
		pattern_dir = str(sys.argv[x+1])

		# check if directory exists
		checkExistence(pattern_dir, 'pattern directory')
		
		# check for subdirectories and unsupported file formats
		for f in os.listdir(pattern_dir):
			checkSubDir(f, 'pattern directory', pattern_dir)
			checkFormat(f, 'pattern directory')

# if the command line arguments were set then run the program, otherwise alert the user they did something wrong
if (pattern != "NONE" or pattern_dir != "NONE") and (source != "NONE" or source_dir != "NONE"):

	# get pattern images into an array
	if pattern != "NONE":
		pattern_array = [pattern]
	else:
		pattern_array = []
		for root, subFolders, files in os.walk(pattern_dir):
			# add all image paths to the array
			for file in files:
				pattern_array.append(os.path.join(root,file))

	# get source images into an array
	if source != "NONE":
		source_array = [source]
	else:
		source_array = []
		for root, subFolders, files in os.walk(source_dir):
			# add all image paths to the array
			for file in files:
				source_array.append(os.path.join(root,file))


	imageSearch = ImageSearch(pattern_array, source_array)
	imageSearch.match_images()
else:
	print >>sys.stderr, 'There was a problem parsing the command line arguments'
	sys.exit(1)

# uncomment to see benchmark
# print(datetime.now()-startTime)
sys.exit(0)

	
