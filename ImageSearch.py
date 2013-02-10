from PIL import Image
import sys

class ImageSearch:

	def __init__(self, pattern, source):
		self.pattern_image = Image.open(pattern)
		self.source_image = Image.open(source)

	# function for matching two directories of images
	def match_images(self, patterns, specimens):
		return 0

	# try to match these two images based on important pixels
	def key_point_match(self, pattern, source, uniques):
		patternPixels = pattern.load()
		sourcePixels = source.load()

		sourceWidth = source.size[0]
		sourceHeight = source.size[1]

		sourcePixelArray = []

		print "Getting source pixel array..."
		for x in range(0,sourceWidth):
			for y in range(0, sourceHeight):
				sourcePixelArray.append((sourcePixels[x,y], x, y))

		print "Trying to match unique pixels with source image..."
		for x in range(0, len(uniques)):
			if self.is_pixel_in_source(uniques[x], sourcePixelArray):
				source_coordinates = self.find_pixel_in_source(uniques[x], sourcePixelArray)
				pattern_xc = uniques[x][1]
				pattern_yc = uniques[x][2]

				source_xc = source_coordinates[0]
				source_yc = source_coordinates[1]

				x_offset = source_xc - pattern_xc
				y_offset = source_yc - pattern_yc

				print "X Offset:", x_offset
				print "Y Offset:", y_offset

				percentage = self.percentage_of_unique_matches(uniques, sourcePixelArray, x_offset, y_offset)

				if(percentage > .5):
					return "MATCHES!!! "+str(percentage*100)+" percent."

		return "Does Not Match!"

	# finds the unique pixels inside of the pattern picture
	def find_unique_pixels(self, pattern):
		print "Getting unique pixel array..."

		patternPixels = pattern.load()
		patSize = pattern.size

		patPixelArray = []
		uniques = []

		for x in range(0,patSize[0]):
			for y in range(0, patSize[1]):
				patPixelArray.append((patternPixels[x,y], x, y))

		print "Original # of pattern pic pixels:", len(patPixelArray)

		for x in range(0, len(patPixelArray)):
			if self.is_unique_pixel(patPixelArray[x], patPixelArray):
				uniques.append(patPixelArray[x])

		print len(uniques), "unique pixels found"
		return uniques

	# determines if this pixel only appears once in the picture
	def is_unique_pixel(self, pixel, array):
		for x in range(0, len(array)):
			if array[x][0] == pixel[0] and array[x][1] != pixel[1] and array[x][2] != pixel[2]:
				return False
		return True

	# determines if the pixel is in the picture
	def is_pixel_in_source(self, pixel, array):
		for x in range(0, len(array)):
			if array[x][0] == pixel[0]:
				return True
		return False

	# returns the coordinates to the pixel in the picture
	def find_pixel_in_source(self, pixel, array):
		for x in range(0, len(array)):
			if array[x][0] == pixel[0]:
				return (array[x][1], array[x][2])
		return False

	# returns the percentage of pixel to pixel matches in the unique pixel array and the source picture
	def percentage_of_unique_matches(self, uniques, source, x_offset, y_offset):
		matches = 0.00

		for x in range(0, len(uniques)):
			if self.is_pixel_in_source(uniques[x], source):
				source_coordinates = self.find_pixel_in_source(uniques[x], source)
				pattern_xc = uniques[x][1]+x_offset
				pattern_yc = uniques[x][2]+y_offset

				source_xc = source_coordinates[0]
				source_yc = source_coordinates[1]

				if pattern_xc == source_xc and pattern_yc == source_yc:
					matches += 1.00

		return matches/(len(uniques)+0.00)


imageSearch = ImageSearch(str(sys.argv[1]), str(sys.argv[2]))

print imageSearch.key_point_match(imageSearch.pattern_image, imageSearch.source_image, imageSearch.find_unique_pixels(imageSearch.pattern_image))