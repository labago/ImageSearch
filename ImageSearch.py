#!/usr/bin/python
from PIL import Image, ImageFilter, ImageChops
import sys
import os
import math
from datetime import datetime

# a class to represent the ImageSearch application
class ImageSearch:

	# constructor, takes the pattern image location string and source image location string
	# if either image/directory is not found, terminate program and alert user
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
				'''
				self.sourcePixelArray = []
				for x in range(0, self.sourceSize[0]):
					for y in range(0, self.sourceSize[1]):
						self.sourcePixelArray.append((self.sourcePixels[x,y], x, y))
				'''
				if (self.patSize[0]*self.patSize[1]) > 300:
					self.sift()
				else:
					self.is_match_brute_force()

		# print all matches
		for x in self.matches:
			# print the match in the spec's format
			# removed confidence level printing ---->  + " with confidence " + str(x[5]) + "%"
			print x[0] + " matches " + x[1] + " at "+ str(x[2][0]) + "x" + str(x[2][1]) + "+" + str(x[3]) + "+" + str(x[4])+ " (with "+ str(x[5]*100) + "% confidence)"

	# try to match images using the SIFT algorithm
	def sift(self):
	
		################################## PATTERN IMAGE ###################################

		# the current image, initilized to the patternImage
		PatternOctave = self.patternImage
		
		patternSize = PatternOctave.size
		
		###### Gaussian Blurs #########
		
		PatternOctaveOne = blur(PatternOctave)
		
	  #PatternOctave = PatternOctave.resize( (patternSize[0]/2, patternSize[1]/2) )
		
		#PatternOctaveTwo = blur(PatternOctave)
		
		#PatternOctave = PatternOctave.resize( (patternSize[0]/4, patternSize[1]/4) )
		
		#PatternOctaveThree = blur(PatternOctave)
		
		#PatternOctave = PatternOctave.resize( (patternSize[0]/8, patternSize[1]/8) )
		
		#PatternOctaveFour = blur(PatternOctave)
		
		####### Difference of Gaussians ########
		
		#PatternOctaveOne = diffGaus(PatternOctaveOne)
		
		# PatternOctaveTwo = diffGaus(PatternOctaveTwo)
	
		# PatternOctaveThree = diffGaus(PatternOctaveThree)
		
		#PatternOctaveFour = diffGaus(PatternOctaveFour)
		
		####### Locate Maxima/Minima ##########
		
		PatternKeypointsOne = filter_by_gradient(PatternOctaveOne[1:3], filter_out_low_contrast(PatternOctaveOne[1:3], maxMin(PatternOctaveOne)))
		# plot_keypoints(self.patternImage, PatternKeypointsOne[0], "patternTest.png")
		
		# PatternKeypointsTwo = filter_by_gradient(PatternOctaveTwo[1:3], filter_out_low_contrast(PatternOctaveTwo[1:3], maxMin(PatternOctaveTwo)))

		# PatternKeypointsThree = filter_by_gradient(PatternOctaveThree[1:3], filter_out_low_contrast(PatternOctaveThree[1:3], maxMin(PatternOctaveThree)))
		
		# PatternKeypointsFour = filter_by_gradient(PatternOctaveFour[1:3], filter_out_low_contrast(PatternOctaveFour[1:3], maxMin(PatternOctaveFour)))
		
		
		#################################### Source IMAGE ###################################
		
		#SourceOctave = self.sourceImage
		
		#sourceSize = SourceOctave.size
		
		###### Gaussian Blurs #########
		
		#SourceOctaveOne = blur(SourceOctave)
		
		# SourceOctave = SourceOctave.resize( (sourceSize[0]/2, sourceSize[1]/2) )
		
		# SourceOctaveTwo = blur(SourceOctave)
		
		# SourceOctave = SourceOctave.resize( (sourceSize[0]/4, sourceSize[1]/4) )
		
		# SourceOctaveThree = blur(SourceOctave)
		
		# SourceOctave = SourceOctave.resize( (sourceSize[0]/8, sourceSize[1]/8) )
		
		# SourceOctaveFour = blur(SourceOctave)
		
		####### Difference of Gaussians ########
		
		#SourceOctaveOne = diffGaus(SourceOctaveOne)
		
		# SourceOctaveTwo = diffGaus(SourceOctaveTwo)
	
		# SourceOctaveThree = diffGaus(SourceOctaveThree)
		
		# SourceOctaveFour = diffGaus(SourceOctaveFour)
		
		####### Locate Maxima/Minima ##########
		
		#SourceKeypointsOne = filter_by_gradient(SourceOctaveOne[1:3], filter_out_low_contrast(SourceOctaveOne[1:3], maxMin(SourceOctaveOne)))
		
		# SourceKeypointsTwo = filter_by_gradient(SourceOctaveTwo[1:3], filter_out_low_contrast(SourceOctaveTwo[1:3], maxMin(SourceOctaveTwo)))

		# SourceKeypointsThree = filter_by_gradient(SourceOctaveThree[1:3], filter_out_low_contrast(SourceOctaveThree[1:3], maxMin(SourceOctaveThree)))
		
		# SourceKeypointsFour = filter_by_gradient(SourceOctaveFour[1:3], filter_out_low_contrast(SourceOctaveFour[1:3], maxMin(SourceOctaveFour)))

		self.is_match(PatternKeypointsOne[0])

	def is_match(self, pattern_keypoints):
		maxMisses = len(pattern_keypoints)/4
		maxXoffset = (self.sourceImage.size[0]-self.patternImage.size[0])+1
		maxYoffset = (self.sourceImage.size[1]-self.patternImage.size[1])+1

		if len(pattern_keypoints) > 0:
			for x in range(0, maxXoffset):
				for y in range(0, maxYoffset):
					misses = 0
					for point in pattern_keypoints:
						if not misses > maxMisses:
							pattern_pixel = self.patternPixels[point[0], point[1]]
							source_pixel = self.sourcePixels[point[0]+x, point[1]+y]
							if not self.check_if_two_pixels_are_equivelant(pattern_pixel, source_pixel):
								misses += 1
					if misses <= maxMisses:
						self.new_or_better_match((self.patternName, self.sourceName, self.patSize, x, y, 1-(misses/len(pattern_keypoints))))
		return False

	def is_match_brute_force(self):
		maxMisses = len(self.patPixelArray)/8
		maxXoffset = (self.sourceImage.size[0]-self.patternImage.size[0])+1
		maxYoffset = (self.sourceImage.size[1]-self.patternImage.size[1])+1

		for x in range(0, maxXoffset):
			for y in range(0, maxYoffset):
				misses = 0
				for point in self.patPixelArray:
					if not misses > maxMisses:
						pattern_pixel = self.patternPixels[point[1], point[2]]
						source_pixel = self.sourcePixels[point[1]+x, point[2]+y]
						if not self.check_if_two_pixels_are_equivelant(pattern_pixel, source_pixel):
							misses += 1
				if misses <= maxMisses:
					self.new_or_better_match((self.patternName, self.sourceName, self.patSize, x, y, 1-(misses/len(self.patPixelArray))))
		return False

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
						return 0
				else:
					self.matches.append(image_info)
					return 0
		self.matches.append(image_info)
		return 0

	def check_if_two_pixels_are_equivelant(self, pixel1, pixel2):
		tolerableDiff = 5				
		# if both PNG, little room for error
		# if one is JPG, tolerable error = 60
		# if one is GIF, tolerable error = 150
		if self.patternFormat == "JPEG" or self.sourceFormat == "JPEG":
			tolerableDiff = 20
		if self.patternFormat == "GIF" or self.sourceFormat == "GIF":
			tolerableDiff = 55

		
		Rdiff = math.fabs(pixel1[0] - pixel2[0])
		Gdiff = math.fabs(pixel1[1] - pixel2[1])
		Bdiff = math.fabs(pixel1[2] - pixel2[2])
		
		totalDiff = Rdiff + Gdiff + Bdiff
		if (totalDiff < tolerableDiff):
			self.current_confidence += totalDiff/tolerableDiff
			return True
		else: 
			return False
##################### Functions #########################

# collects the average contrast of all pixels, and filters out the octave_keypoints
# that are greater than the average
def filter_out_low_contrast(octave, octave_keypoints):
	new_keypoints = []
	for blur in octave:
		pixels = blur.load()
		total_contrast = 0
		total_pixels = 0
		counter = 0
		for x in range(0, blur.size[0]):
			for y in range(0, blur.size[1]):
				pixel = pixels[x, y]
				total_contrast += pixel[0] + pixel[1] + pixel[2]
				total_pixels += 1
		avg_contrast = total_contrast/total_pixels
		new_pixels = []
		for x in octave_keypoints[counter]:
			pixel = pixels[x[0], x[1]]
			pixel_contrast = pixel[0] + pixel[1] + pixel[2]
			if pixel_contrast < (avg_contrast*.5):
				new_pixels.append(x)
		new_keypoints.append(new_pixels)
		counter += 1
	return new_keypoints


def filter_by_gradient(octave, octave_keypoints):
	new_keypoints = []
	for blur in octave:
		pixels = blur.load()
		counter = 0
		new_pixels = []
		for x in octave_keypoints[counter]:
			pixel = pixels[x[0], x[1]]
			neighbors = getNeighborsDict(pixels, x[0], x[1])
			if goodGradient(pixel, neighbors):
				new_pixels.append(x)
		new_keypoints.append(new_pixels)
		counter += 1
	return new_keypoints

def goodGradient(pixel, neighbors):
	pixel_value = pixel[0]+pixel[1]+pixel[2]

	left = []
	left.append(neighbors["topLeft"])
	left.append(neighbors["midLeft"])
	left.append(neighbors["botLeft"])
	left.append(neighbors["botMid"])

	right = []
	right.append(neighbors["topRight"])
	right.append(neighbors["midRight"])
	right.append(neighbors["botRight"])
	right.append(neighbors["topMid"])

	if checkMinimum(pixel_value, right) and checkMaximum(pixel_value, left):
		return True
	'''
	elif checkMinimum(pixel_value, left) and checkMaximum(pixel_value, right):
		return True
	'''
	return False
	
def plot_keypoints(image, keypoints, name):
	image = Image.new(image.mode, image.size)
	for y in keypoints:
		image.putpixel(y, (0, 255, 0))
	#image.save("tmp/"+name)
	image.save(name)

# creates 5 blur layers over an octave of an image
def blur(image):
	
	blurImages = []
	
	for i in range(0,5):
		
		blur = image.filter(ImageFilter.BLUR)
			
		blurImages.append(blur)	
		
		image = blur

	return blurImages


# creates the difference of gaussian for an octave of an image
def diffGaus(octave):

	save = octave[0]
	
	differences = []
	
	for i in range(1, len(octave)):
	
		curr = octave[i]
		
		diff = ImageChops.difference(save, curr)
		
		differences.append(diff)
		
		save = curr
		
	return differences
		
# locates maxima and minima in Difference of Gaussian Images
# returns a list of lists of keypoints
def maxMin(octave):

	# list of tuples of x,y coordinates of keypoints
	result = []

	for x in range(1, len(octave)-1):
	
		keypoints = []
	
		top = octave[x-1]
		middle = octave[x]
		bottom = octave[x+1]
		
		# all sizes in a octave are equal, so this variable represents 
		# the size of each entry in the octave
		size = top.size
		
		for x in range(1, size[0]-1):
			for y in range(1, size[1]-1):
				
				img = middle.load()
				
				center = img[x,y]
				center = center[0] + center[1] + center[2]
				
				neighbors = getNeighborsRGBValues(img, x, y)
				
				if checkMinimum(center, neighbors):
				
					imgTop = top.load()
					
					neighborsTop = getNeighborsRGBValues(imgTop, x, y)
					
					if checkMinimum(center, neighborsTop):
					
						imgBot = bottom.load()
						
						neighborsBot = getNeighborsRGBValues(imgBot, x, y)
						
						if checkMinimum(center, neighborsBot):
						
							keypoints.append((x,y))
				
				if checkMaximum(center, neighbors):
			
					imgTop = top.load()
					
					neighborsTop = getNeighborsRGBValues(imgTop, x, y)
					
					if checkMaximum(center, neighborsTop):
					
						imgBot = bottom.load()
						
						neighborsBot = getNeighborsRGBValues(imgBot, x, y)
						
						if checkMaximum(center, neighborsBot):
						
							keypoints.append((x,y))
							
		result.append(keypoints)
							

	return result
	
# gets the sum of the RGB values of the neighbors of a center pixel[x,y]
# returns values in an dictionary
def getNeighborsDict(data, x, y):
	
	neighbors = {}
	
	try:
	
		topLeft = data[x-1,y-1]
		topLeft = topLeft[0] + topLeft[1] + topLeft[2]
		neighbors["topLeft"] = topLeft
		
		topMid = data[x,y-1]
		topMid = topMid[0] + topMid[1] + topMid[2]
		neighbors["topMid"] = topMid
		
		topRight = data[x+1,y-1]
		topRight = topRight[0] + topRight[1] + topRight[2]
		neighbors["topRight"] = topRight
		
		midLeft = data[x-1,y]
		midLeft = midLeft[0] + midLeft[1] + midLeft[2]
		neighbors["midLeft"] = midLeft
		
		midRight = data[x+1,y]
		midRight = midRight[0] + midRight[1] + midRight[2]
		neighbors["midRight"] = midRight
		
		botLeft = data[x-1,y+1]
		botLeft = botLeft[0] + botLeft[1] + botLeft[2]
		neighbors["botLeft"] = botLeft
		
		botMid = data[x,y+1]
		botMid = botMid[0] + botMid[1] + botMid[2]
		neighbors["botMid"] = botMid
		
		botRight = data[x+1,y+1]
		botRight = botRight[0] + botRight[1] + botRight[2]
		neighbors["botRight"] = botRight
			
		return neighbors
		
	except(IndexError):
		
		print "x and y values provided are on the edge; Not enough neighbors."


# gets the sum of the RGB values of the neighbors of a center pixel[x,y]
# returns values in an array
def getNeighborsRGBValues(data, x, y):
	
	neighbors = []
	
	try:
	
		topLeft = data[x-1,y-1]
		topLeft = topLeft[0] + topLeft[1] + topLeft[2]
		neighbors.append(topLeft)
		
		topMid = data[x,y-1]
		topMid = topMid[0] + topMid[1] + topMid[2]
		neighbors.append(topMid)
		
		topRight = data[x+1,y-1]
		topRight = topRight[0] + topRight[1] + topRight[2]
		neighbors.append(topRight)
		
		midLeft = data[x-1,y]
		midLeft = midLeft[0] + midLeft[1] + midLeft[2]
		neighbors.append(midLeft)
		
		midRight = data[x+1,y]
		midRight = midRight[0] + midRight[1] + midRight[2]
		neighbors.append(midRight)
		
		botLeft = data[x-1,y+1]
		botLeft = botLeft[0] + botLeft[1] + botLeft[2]
		neighbors.append(botLeft)
		
		botMid = data[x,y+1]
		botMid = botMid[0] + botMid[1] + botMid[2]
		neighbors.append(topMid)
		
		botRight = data[x+1,y+1]
		botRight = botRight[0] + botRight[1] + botRight[2]
		neighbors.append(topRight)
			
		return neighbors
		
	except(IndexError):
		
		print "x and y values provided are on the edge; Not enough neighbors."
		
# checks neighboring cells to see if the center pixel in a matrix is the minimum
def checkMinimum(center, neighbors):

	for i in neighbors:
	
		if i < center:
			return False
	
	return True
	
# checks neighboring cells to see if the center pixel in a matrix is the maximum
def checkMaximum(center, neighbors):

	for i in neighbors:
	
		if i > center:
			return False
			
	return True

######### Input Checks ###############

# used to check if an image format is supported by the program
# Arguments: fileLoc is the file location and imgtype is the type of input (pattern, source, etc.)
def checkFormat(fileLoc, imgtype):
	try:
		frm = Image.open(fileLoc).format
	except (IndexError):
		print >>sys.stderr, 'Corrupted Image/File Found'
		sys.exit(1)
		
	if frm != 'JPG' and frm != 'JPEG' and frm != 'PNG' and frm != 'GIF':
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
			checkFormat(source_dir+"/"+f, 'source directory')

	if(str(sys.argv[x]) == '-pdir'):
		
		pattern_dir = str(sys.argv[x+1])

		# check if directory exists
		checkExistence(pattern_dir, 'pattern directory')
		
		# check for subdirectories and unsupported file formats
		try:
			for f in os.listdir(pattern_dir):
				checkSubDir(f, 'pattern directory', pattern_dir)
				checkFormat(pattern_dir+"/"+f, 'pattern directory')
		except (WindowsError):
			print >>sys.stderr, 'The directory name is invalid'
			sys.exit(1)

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