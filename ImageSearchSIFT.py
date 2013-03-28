#!/usr/bin/python
from PIL import Image, ImageFilter, ImageChops
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
				except (IOError, IndexError):
					print >>sys.stderr, 'Pattern image not found or not of the correct image format.'
					sys.exit(1)

				try:
					self.sourceImage = Image.open(source)
					self.sourceName = source.split('/')[-1]
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
				self.sift()

		# print all matches
		for x in self.matches:
			# print the match in the professor's format
			# removed confidence level printing ---->  + " with confidence " + str(x[5]) + "%"
			print x[0] + " matches " + x[1] + " at "+ str(x[2][0]) + "x" + str(x[2][1]) + "+" + str(x[3]) + "+" + str(x[4])

	# try to match images using the SIFT algorithm
	def sift(self):
	
		################################## PATTERN IMAGE ###################################

		# the current image, initilized to the patternImage
		octave = self.patternImage
		
		size = octave.size
		
		### Gaussian Blurs ########
		
		firstOctave = blur(octave)
		
		octave = octave.resize( (size[0]/2, size[1]/2) )
		
		secondOctave = blur(octave)
		
		octave = octave.resize( (size[0]/2, size[1]/2) )
		
		thirdOctave = blur(octave)
		
		octave = octave.resize( (size[0]/2, size[1]/2) )
		
		fourthOctave = blur(octave)

		####### Difference of Gaussians ########
		
		firstOctave = diffGaus(firstOctave)
		
		secondOctave = diffGaus(secondOctave)
	
		thirdOctave = diffGaus(thirdOctave)
		
		fourthOctave = diffGaus(fourthOctave)
		
		####### Locate Maxima/Minima ##########
		
		firstKeypoints = maxMin(firstOctave)
		
		secondKeypoints = maxMin(secondOctave)
		
		thirdKeypoints = maxMin(thirdOctave)
		
		fourthKeypoints = maxMin(fourthOctave)
		
		
		#################################### SOURCE IMAGE ###################################
		
		octave_S = self.sourceImage
		
		size_S = octave_S.size
		
		###### Gaussian Blurs #########
		
		octaveOne = blur(octave_S)
		
		octave_S = octave_S.resize( (size_S[0]/2, size_S[1]/2) )
		
		octaveTwo = blur(octave_S)
		
		octave_S = octave_S.resize( (size_S[0]/2, size_S[1]/2) )
		
		octaveThree = blur(octave_S)
		
		octave_S = octave_S.resize( (size_S[0]/2, size_S[1]/2) )
		
		octaveFour = blur(octave_S)
		
		####### Difference of Gaussians ########
		
		octaveOne = diffGaus(octaveOne)
		
		octaveTwo = diffGaus(octaveTwo)
	
		octaveThree = diffGaus(octaveThree)
		
		octaveFour = diffGaus(octaveFour)
		
		####### Locate Maxima/Minima ##########
		
		keypointsOne = maxMin(octaveOne)
		
		keypointsTwo = maxMin(octaveTwo)
		
		keypointsThree = maxMin(octaveThree)
		
		keypointsFour = maxMin(octaveFour)
		
		
		
##################### Functions #########################
		
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
				
				neighbors = getNeighbors(img, x, y)
				
				if checkMinimum(center, neighbors):
				
					imgTop = top.load()
					
					neighborsTop = getNeighbors(imgTop, x, y)
					
					if checkMinimum(center, neighborsTop):
					
						imgBot = bottom.load()
						
						neighborsBot = getNeighbors(imgBot, x, y)
						
						if checkMinimum(center, neighborsBot):
						
							keypoints.append((x,y))
				
				if checkMaximum(center, neighbors):
			
					imgTop = top.load()
					
					neighborsTop = getNeighbors(imgTop, x, y)
					
					if checkMaximum(center, neighborsTop):
					
						imgBot = bottom.load()
						
						neighborsBot = getNeighbors(imgBot, x, y)
						
						if checkMaximum(center, neighborsBot):
						
							keypoints.append((x,y))
							
		result.append(keypoints)
							

	return result
		
# gets the sum of the RGB values of the neighbors of a center pixel[x,y]
# returns values in an array
def getNeighbors(data, x, y):
	
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
	
	
# gets the sum of the RGB values of the neighbors 
# of an image neighboring the image of a center pixel[x,y]
# returns values in an array
def getNeighborsImage(data, x, y):
	
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
		
		midMid = data[x,y]
		midMid = midMid[0] + midMid[1] + midMid[2]
		neighbors.append(midMid)
		
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




######### Input Checks ###############

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

	
