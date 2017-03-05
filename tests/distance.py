   
import math

width = 1400
height = 1000
init_x = 200
init_y = 500

class distance():
	def __init__(self):
		pass

	def get_BLE_distance(self,xR,yR,xC,yC):
		# Used to count the distance.
		i = 0
		# calculate distance between 2 points
		i = math.sqrt((xR-xC)*(xR-xC)+(yR-yC)*(yR-yC))
		# Return the distance for the arm.
		return i

	def make_BLE_sensors(self,x,y):
		distance = 15   #sensors dis
		BLE_points = []
		BLE_points.append((x-15,y+15))
		BLE_points.append((x+25,y))
		BLE_points.append((x-15,y-15))
		return BLE_points

	def get_rotated_BLE(self, x_1, y_1, x_2, y_2, radians):
		# Rotate x_2, y_2 around x_1, y_1 by angle.
		x_change = (x_2 - x_1) * math.cos(radians) + \
			(y_2 - y_1) * math.sin(radians)
		y_change = (y_2 - y_1) * math.cos(radians) + \
			(x_2 - x_1) * math.sin(radians)
		new_x = x_change + x_1
		new_y = (y_change + y_1)
		return int(new_x), int(new_y)

	def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
		# Rotate x_2, y_2 around x_1, y_1 by angle.
		x_change = (x_2 - x_1) * math.cos(radians) + \
			(y_2 - y_1) * math.sin(radians)
		y_change = (y_1 - y_2) * math.cos(radians) - \
			(x_1 - x_2) * math.sin(radians)
		new_x = x_change + x_1
		new_y = height - (y_change + y_1)
		return int(new_x), int(new_y)

	def get_BLE_readings(self,xR,yR,xC,yC,angle):
		d = []
		e = []
		sensors = self.make_BLE_sensors(xR,yR)
		for point in sensors:
				rotated_p = self.get_rotated_BLE(xR, yR, point[0], point[1], angle)
				d.append(self.get_BLE_distance(rotated_p[0],rotated_p[1],xC,yC))
				e.append(rotated_p)
		return d, e


if __name__ == '__main__':
	dist = distance()
	getdist,rot = dist.get_BLE_readings(0,0,100,100,0.75)
	print(getdist)
	print(rot)
	print(math.sqrt(20000))