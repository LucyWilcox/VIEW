import numpy as np
import argparse
import cv2

"""
Colors are in boundraies should be in format: G, B, R

"""

class ImageProcessing:
	def __init__(self, image, split_val, color_gbrs, color_vals):
		# split is the number of pixels each slice will be, adapted from the split value
		self.image = image
		self.height = image.shape[0]
		self.width = image.shape[1]
		self.parts = round(self.width / float(split_val))
		self.split_val = split_val
		self.split = int(self.width / self.parts)
		self.color_gbrs = color_gbrs
		self.color_vals = color_vals

	def split_image(self):
		left = 0
		right = self.split
		while right <= self.width:
			split = self.image[: , left:right]
			left += self.split
			right += self.split
			# cv2.imshow("image", split)
			# cv2.waitKey(0)
			yield split

	def check_color(self, color_bounds):
		count = 0
		for s in self.split_image():
			lower = np.array(color_bounds[0], dtype='uint8')
			upper = np.array(color_bounds[1], dtype='uint8')

			mask = cv2.inRange(s, lower, upper)
			has_color = cv2.countNonZero(mask)
			if has_color > 50:
				count += 1

			#output = cv2.bitwise_and(s, s, mask=mask)
			# cv2.imshow("image", output)
			# cv2.waitKey(0)
		return count	

	def check_colors(self):
		color_score = 0
		for color, val in self.color_vals.iteritems():
			count = self.check_color(self.color_gbrs[color])
			color_score += count * val
		return color_score

	def get_score(self):
		ratio = self.width / (self.split_val * self.parts)
		return ratio * self.check_colors()


gbrs = {'TEAL':([75, 85, 25], [120, 150, 60])}
vals = {'TEAL': 1}

image1 = cv2.imread('image1.jpg')

i = ImageProcessing(image1, 500, gbrs, vals)
# i.check_colors()
print i.get_score()