from PIL import Image
import sys

class ImageSearch:

	def __init__(self, pattern, source):
		self.pattern_image = Image.open(pattern)
		self.source_image = Image.open(source)

	# function for matching two directories of images
	def match_images(self, patterns, specimens):
		return 0

	def exact_match_image(self, pattern, source):
		patternPixels = pattern.load()
		sourcePixels = source.load()
		patSize = pattern.size
		sourceSize = source.size

		patPixelArray = []
		sourcePixelArray = []

		# make pattern pixel array
		for x in range(0,patSize[0]):
			for y in range(0, patSize[1]):
				patPixelArray.append(patternPixels[x,y])

		# make source pixel array
		for x in range(0,sourceSize[0]):
			for y in range(0, sourceSize[1]):
				sourcePixelArray.append(sourcePixels[x,y])

		return patPixelArray == sourcePixelArray

	def key_point_match(self, pattern, source):
		patternPixels = pattern.load()
		sourcePixels = source.load()

		patWidth = pattern.size[0] - 1
		patHeight = pattern.size[1] - 1
		Xinterval = int((patWidth/100) - 1)
		Yinterval = int((patHeight/100) - 1)

		sourceWidth = source.size[0] - 1
		sourceHeight = source.size[1] - 1

		patPixelArray = []
		sourcePixelArray = []


		# Pattern Image
		# get very top row of pattern image 
		for x in range(0,patWidth, Xinterval):
			patPixelArray.append(patternPixels[x,0])

		# get very bottom pattern image 
		for x in range(0,patWidth, Xinterval):
			patPixelArray.append(patternPixels[x,patHeight])

		# get very left column of pattern image
		for y in range(0,patHeight, Yinterval):
			patPixelArray.append(patternPixels[0,y])

		# get very right column of pattern image
		for y in range(0,patHeight, Yinterval):
			patPixelArray.append(patternPixels[patWidth,y])


		# Source Image
		# get very top row of source image 
		for x in range(0,sourceWidth, Xinterval):
			sourcePixelArray.append(sourcePixels[x,0])

		# get very bottom source image 
		for x in range(0,sourceWidth, Xinterval):
			sourcePixelArray.append(sourcePixels[x,sourceHeight])

		# get very left column of source image
		for y in range(0,sourceHeight, Yinterval):
			sourcePixelArray.append(sourcePixels[0,y])

		# get very right column of source image
		for y in range(0,sourceHeight, Yinterval):
			sourcePixelArray.append(patternPixels[patWidth,y])

		return patPixelArray == sourcePixelArray

imageSearch = ImageSearch(str(sys.argv[1]), str(sys.argv[2]))

# print 'Pattern Image Info: ', patSize[0]
# print 'Source Image Info: ', sourceSize[0]

if(imageSearch.key_point_match(imageSearch.pattern_image, imageSearch.source_image)):
	print "MATCHES"
else:
	print "Does Not Match"

