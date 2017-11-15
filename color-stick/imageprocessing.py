import numpy as np
import cv2
from collections import OrderedDict
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
			cv2.waitKey(0)
			yield split

	def check_color(self, color_bounds, image):
		lower = np.array(color_bounds[0], dtype='uint8')
		upper = np.array(color_bounds[1], dtype='uint8')

		mask = cv2.inRange(image, lower, upper) 
		has_color = cv2.countNonZero(mask)
		if has_color > 50: # 50 is subject to change
			output = cv2.bitwise_and(image, image, mask=mask)
			cv2.imshow("image", output) 
			cv2.waitKey(0)
			return True
		return False	

	def check_colors(self):
		color_score = 0
		for image in self.split_image():
			for color, val in self.color_vals.iteritems():
				if self.check_color(self.color_gbrs[color], image):
					color_score += val
					break
		return color_score

	def get_score(self):
		# pure score, not out of 100 or anything
		ratio = self.width / (self.split_val * self.parts)
		return ratio * self.check_colors()


# gbrs = {'TEAL':([75, 85, 25], [120, 150, 60])}
# vals = {'TEAL': 1}
 
# inside_gbrs = {'RED': ([30, 20, 150], [40, 30, 190]), 
# 	'BLUE': ([130, 180, 55], [150, 210, 75]),
# 	'PINK': ([110, 165, 230], [135, 180, 250]),
# 	'YELLOW': ([220, 115, 215], [235, 130, 235]),
# 	'ORANGE': ([180, 110, 240], [200, 135, 265]),
# 	'GREEN': ([210, 135, 170], [235, 155, 195])
# 	}

cloudy_gbrs = {'RED': ([25, 20, 120], [50, 50, 195]), #these aren't perfect yet
	'BLUE': ([95, 145, 0], [175, 220, 30]),
	'PINK': ([85, 95, 230], [195, 240, 255]),
	'YELLOW': ([215, 105, 185], [250, 225, 250]),
	'ORANGE': ([155, 80, 240], [195, 125, 255]),
	'GREEN': ([195, 85, 80], [240, 200, 190])
	}


vals = OrderedDict([('RED', 6), ('BLUE', 5), ('PINK', 4), ('YELLOW', 3), ('ORANGE', 2), ('GREEN', 1)]) 

image1 = cv2.imread('image2.jpg')

i = ImageProcessing(image1, 500, cloudy_gbrs, vals)
print i.get_score()