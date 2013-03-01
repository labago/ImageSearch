#!/usr/bin/python
from PIL import Image
import sys
import os
import math
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

	# function for matching two directories of images
	def match_images(self):
		for pattern in self.pattern_array:
			for source in self.source_array:
				try:
					self.patternImage = Image.open(pattern)
					self.patternName = pattern.split('/')[-1]
				except (IOError):
					print >>sys.stderr, 'Pattern image not found or not of the correct image format.'
					sys.exit(1)

				try:
					self.sourceImage = Image.open(source)
					self.sourceName = source.split('/')[-1]
				except (IOError):
					print >>sys.stderr, 'Source image not found or not of the correct image format.'
					sys.exit(1)
				
				self.patternFormat = self.patternImage.format
				self.sourceFormat = self.sourceImage.format

				if self.patternImage.mode != "RGB":
					self.patternImage = self.patternImage.convert("RGB")

				if self.sourceImage.mode != "RGB":
					self.sourceImage = self.sourceImage.convert("RGB")
				# try to match the images
				self.key_point_match()

		# print all matches
		for x in self.matches:
			# print the match in the professor's format
			# removed confidence level printing ---->  + " with confidence " + str(x[5]) + "%"
			print x[0] + " matches " + x[1] + " at "+ str(x[2][0]) + "x" + str(x[2][1]) + "+" + str(x[3]) + "+" + str(x[4])

	# try to match these two images based on important pixels
	def key_point_match(self):

		patternPixels = imageSearch.patternImage.load()
		patSize = imageSearch.patternImage.size

		patPixelArray = []			# holds the "RGB" pixel data for the pattern image

		# adds the "RGB" pixel data to the list
		for x in range(0,patSize[0]):
			for y in range(0, patSize[1]):
				patPixelArray.append((patternPixels[x,y], x, y))

		patPixelArray.sort(key=lambda x: x[0])		# sorts the list of pattern "RGB" pixel data


		uniques = imageSearch.find_unique_pixels(patPixelArray) # list of the unique pixels in the pattern image

		patternPixels = self.patternImage.load()	# holds the pattern pixel information
		sourcePixels = self.sourceImage.load()		# holds the source pixel information 

		sourceWidth = self.sourceImage.size[0]		# width of the source image
		sourceHeight = self.sourceImage.size[1]	# height of the source image

		sourcePixelArray = []						# a list to hold the "RGB" pixel data for the source image

		# adds the "RGB" pixel data to the list
		for x in range(0,sourceWidth):
			for y in range(0, sourceHeight):
				sourcePixelArray.append((sourcePixels[x,y], x, y))

		foundIndex = -1

		# checks to see any unique pixels are in the source image
		for x in range(0, len(uniques)):
			if self.is_pixel_in_source(uniques[x], sourcePixelArray):
				foundIndex = x
				break

		if foundIndex != -1:
			# if a unique pixel is in the source image, finds the pixel in the source 
			# and calculates the percentage of the match. If the percentage is above 50%, 
			# prints out the match message
			source_coordinates = self.find_pixels_in_source(uniques[foundIndex], sourcePixelArray)
			for i in range(0, len(source_coordinates)):
				patternXC = uniques[foundIndex][1]
				patternYC = uniques[foundIndex][2]

				sourceXC = source_coordinates[i][0]
				sourceYC = source_coordinates[i][1]

				xOffset = sourceXC - patternXC
				yOffset = sourceYC - patternYC
				if xOffset >= 0 and yOffset >= 0:
					self.current_confidence = 0;
					percentage = self.percentage_of_unique_matches(uniques, xOffset, yOffset)
				
					if(percentage >= .3):
						
						# this also sets the confidence level self.current_confidence
						isMatch = self.check_exact_match(xOffset, yOffset)				

						if isMatch == True:

							# inverse the confidence to get the real value, then change to percent, trim decimals
							self.current_confidence = 1 - self.current_confidence
							self.current_confidence = self.current_confidence * 100
							confd = int(self.current_confidence)

							# decide whether to add the match to the total array of matches, replace a match, or do not add
							self.new_or_better_match((self.patternName, self.sourceName, patSize, xOffset, yOffset, confd))

	# first sorts the list of pattern pixels by pixel, meaning the pixel with least RGB value will
	# be first and the one with the largest will be last. It then takes the 100 least value RGB pixels and 
	# 100 of the largest ones. If the pattern picture has less than 200 pixels total, the whole picture will 
	# be returned and compared
	def find_unique_pixels(self, patPixelArray):
		uniques = []				# holds the found unique values in the pattern image	
		
		length = len(patPixelArray)
		seperator = length/100						# a value to control what pixels are considered "unique"

		if(length > 101):
			for x in range(0, 50):
				uniques.append(patPixelArray[x])

			for x in range((length-51), length-1):
				uniques.append(patPixelArray[x])
		else:
			for x in patPixelArray:
				uniques.append(x)		

		return uniques

	# checks if this is a duplicate match/over-lapping match
	def new_or_better_match(self, image_info):
		for i in range(0, len(self.matches)):
			# if the pattern and source names are the same we should check if the
			# if the matched area are over lapping too much (50 percent)
			if self.matches[i][0] == image_info[0] and self.matches[i][1] == image_info[1]:
				xOffsetDiff = abs(self.matches[i][3] - image_info[3])
				yOffsetDiff = abs(self.matches[i][4] - image_info[4])
				xC = self.matches[i][2][0] - xOffsetDiff
				yC = self.matches[i][2][1] - yOffsetDiff
				overlap_area = (xC*yC)+0.0
				image_area = (self.matches[i][2][0]*self.matches[i][2][1])+0.0
				percentage_overlap = overlap_area/image_area
				if(percentage_overlap >= .5):
					if not self.matches[i][5] > image_info[5]:
						self.matches[i] = image_info
						return 0
				else:
					self.matches.append(image_info)
					return 0
		self.matches.append(image_info)
		return 0

	# determines if the pixel is in the picture
	def is_pixel_in_source(self, pixel, array):
		for x in range(0, len(array)):
			if self.check_if_two_pixels_are_equivelant(array[x][0][0:3], pixel[0][0:3]):
				return True
		return False

	# returns the coordinates to the pixel in the picture
	def find_pixels_in_source(self, pixel, array):
		matches = []
		for x in range(0, len(array)):
			if self.check_if_two_pixels_are_equivelant(array[x][0][0:3], pixel[0][0:3]):
				matches.append((array[x][1], array[x][2]))
		return matches

	# returns the percentage of pixel to pixel matches in the unique pixel array and the source picture
	def percentage_of_unique_matches(self, uniques, xOffset, yOffset):
		matches = 0.00								# initial value for the match percentage
		sourcePixels = self.sourceImage.load()	
		sourceSize = self.sourceImage.size		

		for x in range(0, len(uniques), 10):
			patternXC = uniques[x][1]+xOffset
			patternYC = uniques[x][2]+yOffset

			if(patternXC >= 0 and patternYC >= 0 and patternXC <= (sourceSize[0]-1) and patternYC <= (sourceSize[1]-1)):
				source_pixel = sourcePixels[patternXC, patternYC]

				if self.check_if_two_pixels_are_equivelant(source_pixel[0:3], uniques[x][0][0:3]):
					matches += 1.00

		return matches/((len(uniques)/10.0)+0.00)

	# checks if the current pattern and source image exactly match in the
	# partial match area. This also sets the confidence level of the match
	def check_exact_match(self, xOffset, yOffset):
		sourcePixels = self.sourceImage.load()
		patternPixels = self.patternImage.load()
		patternWidth = self.patternImage.size[0]
		patternHeigth = self.patternImage.size[1]
		sourceWidth = self.sourceImage.size[0]
		sourceHeight = self.sourceImage.size[1]

		counter = 0
		for y in range(0, patternHeigth):
			for x in range(0, patternWidth):
				if x + xOffset < sourceWidth and y + yOffset < sourceHeight:
					patPixel = patternPixels[x, y]
					sourcePixel = sourcePixels[x + xOffset, y + yOffset]
					
					counter += 1
					if self.check_if_two_pixels_are_equivelant(patPixel, sourcePixel) == False:
						return False
				else:
					return False
		self.current_confidence = self.current_confidence/counter
		return True

	# checks pixel equivalency rather than equality, since changing image format will alter pixels
	def check_if_two_pixels_are_equivelant(self, pixel1, pixel2):
		tolerableDiff = 5				
		# if both PNG, little room for error
		# if one is JPG, tolerable error = 60
		# if one is GIF, tolerable error = 150
		if self.patternFormat == "JPEG" or self.sourceFormat == "JPEG":
			tolerableDiff = 60
		if self.patternFormat == "GIF" or self.sourceFormat == "GIF":
			tolerableDiff = 150

		
		Rdiff = math.fabs(pixel1[0] - pixel2[0])
		Gdiff = math.fabs(pixel1[1] - pixel2[1])
		Bdiff = math.fabs(pixel1[2] - pixel2[2])
		
		totalDiff = Rdiff + Gdiff + Bdiff
		if (totalDiff < tolerableDiff):
			self.current_confidence += totalDiff/tolerableDiff
			return True
		else: 
			return False

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