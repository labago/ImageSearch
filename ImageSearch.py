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

		percentage = self.array_match_percentage(patPixelArray, sourcePixelArray)

		if(percentage > .5):
			return "MATCHES", percentage*100, "percent."
		else:
			print "Does Not Match", percentage*100, "percent"

	def key_point_match(self, pattern, source):
		patternPixels = pattern.load()
		sourcePixels = source.load()

		patWidth = pattern.size[0]
		patHeight = pattern.size[1]

		Xinterval = int((patWidth/10))-1
		Yinterval = int((patHeight/10))-1

		sourceWidth = source.size[0]
		sourceHeight = source.size[1]

		patPixelArray = []
		
		# Pattern Image
		# get very top row of pattern image 
		for x in range(0,patWidth, Xinterval):
			patPixelArray.append(patternPixels[x,0])

		# get very bottom pattern image 
		for x in range(0,patWidth, Xinterval):
			patPixelArray.append(patternPixels[x,patHeight-1])

		# get very left column of pattern image
		for y in range(0,patHeight, Yinterval):
			patPixelArray.append(patternPixels[0,y])

		# get very right column of pattern image
		for y in range(0,patHeight, Yinterval):
			patPixelArray.append(patternPixels[patWidth-1,y])

		# make source pixel array as many times as needed until a match is found or
		# until we run out of places to try the pattern image against it. 
		# it starts at x=0 and y=0, moving down in the y direction as far as it can before
		# moving over the next x pixel and starting over. Not very optimized but its something.
		column = 0
		row = 0
		for x in range(0,sourceWidth-patWidth, Xinterval):
			column += 1
			print "Column:", column
			for y in range(0, sourceHeight-patHeight, Yinterval):
				row += 1
				print "Row:", row
				# Source Image
				sourcePixelArray = []
				# get very top row of source image 
				for xx in range(x, patWidth, Xinterval):
					sourcePixelArray.append(sourcePixels[xx,x])

				# get very bottom pattern image 
				for xx in range(x, patWidth, Xinterval):
					sourcePixelArray.append(sourcePixels[xx,patHeight-1])

				# get very left column of pattern image
				for yy in range(y, patHeight, Yinterval):
					sourcePixelArray.append(sourcePixels[y,yy])

				# get very right column of pattern image
				for yy in range(y, patHeight, Yinterval):
					sourcePixelArray.append(sourcePixels[patWidth-1,yy])

				percentage = self.array_match_percentage(patPixelArray, sourcePixelArray)

				if(percentage > .5):
					return "MATCHES", percentage*100, "percent."
				else:
					print "Does Not Match", percentage*100, "percent"

		return "NO MATCH FOUND"

	def array_match_percentage(self, pattern, source):
		matches = 0.00
		print "Size of pattern array", len(pattern)
		print "Size of pattern array", len(source)
		for x in range(0, len(pattern)):
			if x < (len(source)-1):
				if pattern[x] == source[x]:
					matches += 1.00

		return matches/(len(pattern)+0.00)



imageSearch = ImageSearch(str(sys.argv[1]), str(sys.argv[2]))

# print 'Pattern Image Info: ', patSize[0]
# print 'Source Image Info: ', sourceSize[0]

#print imageSearch.key_point_match(imageSearch.pattern_image, imageSearch.source_image)
print imageSearch.key_point_match(imageSearch.pattern_image, imageSearch.source_image)

