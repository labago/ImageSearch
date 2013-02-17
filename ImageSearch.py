#!/usr/bin/python
from PIL import Image
import sys
import os
import math

# a class to represent the ImageSearcg application
class ImageSearch:

	# constructor, takes the pattern image location string and source image location string
	# if either image is not found, termiinate program and alert user
	def __init__(self, pattern, source):
		
		try:
			self.pattern_image = Image.open(pattern)
		except (IOError):
			print "Pattern image not found."
			sys.exit()

		try:
			self.source_image = Image.open(source)
		except (IOError):
			print "Source image not found."
			sys.exit()
		
		self.patternFormat = self.pattern_image.format
		self.sourceFormat = self.source_image.format

		# convert image into the correct format and into the correct RGB mode
		# simplified
		if self.pattern_image.format != "PNG":
			self.pattern_image.save("Temp/temp_pattern_image.png")
			self.pattern_image = Image.open("Temp/temp_pattern_image.png")
		if self.pattern_image.mode != "RGB":
			self.pattern_image = self.pattern_image.convert("RGB")

		if self.source_image.format != "PNG":
			self.source_image.save("Temp/temp_source_image.png")
			self.source_image = Image.open("Temp/temp_source_image.png")
		if self.source_image.mode != "RGB":
			self.source_image = self.source_image.convert("RGB")
		# # changes the source image format to match the pattern image format if the pattern format is not "GIF"
		# if self.source_image.format != self.pattern_image.format:
			
		# 	if self.pattern_image.format == "GIF":
			
		# 		# convert pattern image to "RGB" and change format to "PNG"
		# 		self.pattern_image = self.pattern_image.convert("RGB")
		# 		self.pattern_image.save("Temp/temp_pattern_image.png")
		# 		self.pattern_image = Image.open("Temp/temp_pattern_image.png")

		# 		if self.source_image.format != "PNG":
		# 			# change source image format to "PNG"
		# 			self.source_image.save("Temp/temp_source_image.png")
		# 			self.source_image = Image.open("Temp/temp_source_image.png")

		# 	elif self.source_image.format == "GIF":
			
		# 		# convert source image to "RGB" and change format to match pattern format
		# 		self.source_image = self.source_image.convert("RGB")
		# 		pattern_format = pattern.split('.')[1]
		# 		location = "Temp/temp_source_image." + pattern_format
		# 		self.source_image.save(location)
		# 		self.source_image = Image.open(location)
				
		# 	else:
				
		# 		# change source image format to match pattern format
		# 		pattern_format = pattern.split('.')[1]
		# 		location = "Temp/temp_source_image." + pattern_format
		# 		self.source_image.save(location)
		# 		self.source_image = Image.open(location)

		# # if both images are format "GIF", change both to "PNG"
		# if self.source_image.format == "GIF" == self.pattern_image.format:
		
		# 	# convert pattern image to "RGB" and change format to "PNG"
		# 	self.pattern_image = self.pattern_image.convert("RGB")
		# 	self.pattern_image.save("Temp/temp_pattern_image.png")
		# 	self.pattern_image = Image.open("Temp/temp_pattern_image.png")
				
		# 	# convert source image to "RGB" and change format to "PNG"
		# 	self.source_image = self.source_image.convert("RGB")
		# 	location = "Temp/temp_source_image.png"
		# 	self.source_image.save(location)
		# 	self.source_image = Image.open(location)
			
		# # changes the pattern image format to "PNG"
		# if self.pattern_image.format != "PNG":
		# 	self.pattern_image.save("Temp/temp_pattern_image.png")
		# 	self.pattern_image = Image.open("Temp/temp_pattern_image.png")
			
		# # changes the source image format to "PNG"
		# if self.source_image.format != "PNG":
		# 	self.source_image.save("Temp/temp_source_image.png")
		# 	self.source_image = Image.open("Temp/temp_source_image.png")

	# function for matching two directories of images
	def match_images(self, patterns, specimens):
		return 0

	# try to match these two images based on important pixels
	def key_point_match(self):

		patternPixels = imageSearch.pattern_image.load()
		patSize = imageSearch.pattern_image.size

		patPixelArray = []			# holds the "RGB" pixel data for the pattern image

		# adds the "RGB" pixel data to the list
		for x in range(0,patSize[0]):
			for y in range(0, patSize[1]):
				patPixelArray.append((patternPixels[x,y], x, y))

		patPixelArray.sort(key=lambda x: x[0])		# sorts the list of pattern "RGB" pixel data


		uniques = imageSearch.find_unique_pixels(patPixelArray)# list of the unique pixels in the pattern image

		patternPixels = self.pattern_image.load()	# holds the pattern pixel information
		sourcePixels = self.source_image.load()		# holds the source pixel information 

		sourceWidth = self.source_image.size[0]		# width of the source image
		sourceHeight = self.source_image.size[1]	# height of the source image

		sourcePixelArray = []						# a list to hold the "RGB" pixel data for the source image

		# adds the "RGB" pixel data to the list
		for x in range(0,sourceWidth):
			for y in range(0, sourceHeight):
				sourcePixelArray.append((sourcePixels[x,y], x, y))

		found_index = -1

		# checks to see any unique pixels are in the source image
		for x in range(0, len(uniques)):
			if self.is_pixel_in_source(uniques[x], sourcePixelArray):
				found_index = x
				break

		if found_index != -1:
			# if a unique pixel is in the source image, finds the pixel in the source 
			# and calculates the percentage of the match. If the percentage is above 50%, 
			# prints out the match message
			source_coordinates = self.find_pixels_in_source(uniques[found_index], sourcePixelArray)
			for i in range(0, len(source_coordinates)):
				pattern_xc = uniques[found_index][1]
				pattern_yc = uniques[found_index][2]

				source_xc = source_coordinates[i][0]
				source_yc = source_coordinates[i][1]

				x_offset = source_xc - pattern_xc
				y_offset = source_yc - pattern_yc
				if x_offset >= 0 and y_offset >= 0:

					percentage = self.percentage_of_unique_matches(uniques, x_offset, y_offset)

					if(percentage >= .3):
						isMatch = self.checkExactMatch(x_offset, y_offset)				

						if isMatch == True:

							#print the match in the professor's format
							pat = pattern.split('/')[-1]
							src = source.split('/')[-1]
							return pat + " matches " + src + " at "+ str(patSize[0]) + "x" + str(patSize[1]) + "+" + str(x_offset) + "+" + str(y_offset)
				
		#No match found
		return ""

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

	# determines if the pixel is in the picture
	def is_pixel_in_source(self, pixel, array):
		for x in range(0, len(array)):
			if self.checkIfTwoPixelsAreEquivalent(array[x][0][0:3], pixel[0][0:3]):
				return True
		return False

	# returns the coordinates to the pixel in the picture
	def find_pixels_in_source(self, pixel, array):
		matches = []
		for x in range(0, len(array)):
			if self.checkIfTwoPixelsAreEquivalent(array[x][0][0:3], pixel[0][0:3]):
				matches.append((array[x][1], array[x][2]))
		return matches

	# returns the percentage of pixel to pixel matches in the unique pixel array and the source picture
	def percentage_of_unique_matches(self, uniques, x_offset, y_offset):
		matches = 0.00								# initial value for the match percentage
		source_pixels = self.source_image.load()	
		source_size = self.source_image.size		

		# 
		for x in range(0, len(uniques), 10):
			pattern_xc = uniques[x][1]+x_offset
			pattern_yc = uniques[x][2]+y_offset

			if(pattern_xc >= 0 and pattern_yc >= 0 and pattern_xc <= (source_size[0]-1) and pattern_yc <= (source_size[1]-1)):
				source_pixel = source_pixels[pattern_xc, pattern_yc]

				if self.checkIfTwoPixelsAreEquivalent(source_pixel[0:3], uniques[x][0][0:3]):
					matches += 1.00

		return matches/((len(uniques)/10.0)+0.00)

	def checkExactMatch(self, x_offset, y_offset):
		source_pixels = self.source_image.load()
		pattern_pixels = self.pattern_image.load()
		pattern_width = self.pattern_image.size[0]
		pattern_height = self.pattern_image.size[1]
		source_width = self.source_image.size[0]
		source_height = self.source_image.size[1]
		
		for y in range(0, pattern_height):
			for x in range(0, pattern_width):
				if x + x_offset < source_width and y + y_offset < source_height:
					patPixel = pattern_pixels[x, y]
					sourcePixel = source_pixels[x + x_offset, y + y_offset]
					
					if self.checkIfTwoPixelsAreEquivalent(patPixel, sourcePixel) == False:
						return False
				else:
					return False
		return True

	#it seems that pixels are getting changed slightly in the process of this program
	#I saw some images failing matching because some pixels had tiny differences in RGB vals
	#not sure why the pixels are getting altered, but this is a workaround
	def checkIfTwoPixelsAreEquivalent(self, pixel1, pixel2):
		tolerableDiff = 5				
		#if both PNG, little room for error
		#if one is JPG, tolerable error = 60
		#if one is GIF, tolerable error = 150
		if self.patternFormat == "JPEG" or self.sourceFormat == "JPEG":
			tolerableDiff = 60
		if self.patternFormat == "GIF" or self.sourceFormat == "GIF":
			tolerableDiff = 150

		Rdiff = math.fabs(pixel1[0] - pixel2[0])
		Gdiff = math.fabs(pixel1[1] - pixel2[1])
		Bdiff = math.fabs(pixel1[2] - pixel2[2])
		
		if (Rdiff + Gdiff + Bdiff < tolerableDiff):
			return True
		else: 
			return False


#**************************************************#
#**********# BEGIN EXECUTION OF PROGRAM #**********#
#**************************************************#

# parse command line arguments as the assignment requires
pattern = "NONE"
source = "NONE"

for x in range(0, len(sys.argv)):
	if(str(sys.argv[x]) == '-p'):
		pattern = str(sys.argv[x+1])
	if(str(sys.argv[x]) == '-s'):
		source = str(sys.argv[x+1])

# if the command line arguments were set then run the program, otherwise alert the user they did something wrong
if(pattern != "NONE" and source != "NONE"):
	imageSearch = ImageSearch(pattern, source)
	output = imageSearch.key_point_match()
	if(len(output) > 0):
		print output
else:
	print "There was a problem parsing the command line arguments"

# delete all files in the temp directory
for theFile in os.listdir('Temp'):
	file_path = os.path.join('Temp', theFile)
	if os.path.isfile(file_path):
		os.unlink(file_path)
