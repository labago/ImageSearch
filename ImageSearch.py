from SearchImage import *
from PIL import Image
import sys


class ImageSearch:

	def __init__(self, pattern, source):
		self.pattern_image = Image.open(pattern)
		self.source_image = Image.open(source)

	# function for matching two directories of images
	def match_images(self, patterns, specimens):
		return 0

	def match_image(self, pattern, source):
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

imageSearch = ImageSearch(str(sys.argv[1]), str(sys.argv[2]))

# print 'Pattern Image Info: ', patSize[0]
# print 'Source Image Info: ', sourceSize[0]

if(imageSearch.match_image(imageSearch.pattern_image, imageSearch.source_image)):
	print "MATCHES"
else:
	print "Does Not Match"

