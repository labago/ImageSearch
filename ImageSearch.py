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
				source_coordinates = self.find_pixels_in_source(uniques[x], sourcePixelArray)
				for i in range(0, len(source_coordinates)):
					pattern_xc = uniques[x][1]
					pattern_yc = uniques[x][2]

					source_xc = source_coordinates[i][0]
					source_yc = source_coordinates[i][1]

					x_offset = source_xc - pattern_xc
					y_offset = source_yc - pattern_yc

					print "X Offset:", x_offset
					print "Y Offset:", y_offset

					percentage = self.percentage_of_unique_matches(uniques, source, x_offset, y_offset)

					if(percentage > .5):
						return "MATCHES!!! "+str(percentage*100)+" percent."
					else:
						print "Not a match "+str(percentage*100)+" percent."

		return "Does Not Match!"

	# first sorts the list of pattern pixels by pixel, meaning the pixel with least RGB value will
	# be first and the one with the largest will be last. It then takes the 100 least value RGB pixels and 
	# 100 of the largest ones. If the pattern picture has less than 200 pixels total, the whole picture will 
	# be returned and compared
	def find_unique_pixels(self, pattern):
		patternPixels = pattern.load()
		patSize = pattern.size

		patPixelArray = []
		uniques = []
		
		for x in range(0,patSize[0]):
			for y in range(0, patSize[1]):
				patPixelArray.append((patternPixels[x,y], x, y))

		patPixelArray.sort(key=lambda x: x[0])

		length = len(patPixelArray)
		seperator = length/100

		if(length > 201):
			for x in range(0, 100):
				uniques.append(patPixelArray[x])

			for x in range((length-101), length-1):
				uniques.append(patPixelArray[x])
		else:
			for x in patPixelArray:
				uniques.append(x)

		print uniques

		return uniques

	# determines if the pixel is in the picture
	def is_pixel_in_source(self, pixel, array):
		for x in range(0, len(array)):
			if array[x][0][0:3] == pixel[0][0:3]:
				return True
		return False

	# returns the coordinates to the pixel in the picture
	def find_pixels_in_source(self, pixel, array):
		matches = []
		for x in range(0, len(array)):
			if array[x][0][0:3] == pixel[0][0:3]:
				matches.append((array[x][1], array[x][2]))
		return matches

	# returns the percentage of pixel to pixel matches in the unique pixel array and the source picture
	def percentage_of_unique_matches(self, uniques, source, x_offset, y_offset):
		matches = 0.00
		source_pixels = source.load()

		for x in range(0, len(uniques), 100):
			pattern_xc = uniques[x][1]+x_offset
			pattern_yc = uniques[x][2]+y_offset

			source_pixel = source_pixels[pattern_xc, pattern_yc]

			if source_pixel == uniques[x][0][0:3]:
				matches += 1.00

		return matches/((len(uniques)/100.0)+0.00)


imageSearch = ImageSearch(str(sys.argv[1]), str(sys.argv[2]))

print imageSearch.key_point_match(imageSearch.pattern_image, imageSearch.source_image, imageSearch.find_unique_pixels(imageSearch.pattern_image))