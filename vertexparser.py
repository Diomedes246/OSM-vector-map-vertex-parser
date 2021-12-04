import csv
import numpy as np
import matplotlib.pyplot as plt
import math
import json
from PIL import Image
import scipy.signal

'''CSV Parser'''

data = []
buildings = []

''' building data csv import'''

with open('nelson vertices xy.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	next(csvfile)
	for i, row in enumerate(reader):
		row = row[0].split(",")
		row = row[:4]
		data.append(row)

	building = []

	for i  in range(len(data)):
		if data[i][3] != data[i-1][3] and i != 0:
			#print(data[i][0])
			buildings.append(building)
			building = []
			building.append(data[i])
		else:
			building.append(data[i])

	buildings_x = []
	buildings_y = []
	x = []
	y = []
	for i, building in enumerate(data):
		#print(data[i][3])
		try:
			if i != 0 and (data[i][2] != data[i-1][2] or data[i][3] != data[i-1][3]):
				buildings_x.append(x)
				buildings_y.append(y)
				x = []
				y = []
				x.append(float(building[0]))
				y.append(float(building[1]))
			else:
				x.append(float(building[0]))
				y.append(float(building[1]))
		except IndentationError:
			pass

''' road data csv import '''

roads = []

with open('nelson_line_vertices.csv', newline='') as csvfile:
	reader = csv.reader(csvfile)
	next(csvfile)
	data = []
	for i, row in enumerate(reader):
		data.append([row[0]] + row[-2:])

	road = []

	for i  in range(len(data)):
		if data[i][0] != data[i-1][0] and i != 0:
			#print(data[i][0])
			roads.append(road)
			road = []
			road.append(data[i][-2:])
		else:
			road.append(data[i][-2:])

print(roads)

roads_x = []
roads_y = []

for road in roads:
	x_list = []
	y_list = []
	for x, y in road:
		x_list.append(float(x))
		y_list.append(float(y))
	roads_x.append(x_list)
	roads_y.append(y_list)

for i in range(len(roads_x)):
	plt.plot(roads_x[i], roads_y[i])

#for i in range(len(buildings_x)):
# 	plt.plot(buildings_x[i], buildings_y[i])

#plt.show()

	#plt.plot(float(road[1]), float(road[2]))
#plt.show()



# 	#for i in range(len(buildings_x)):
# 		#plt.plot(buildings_x[i], buildings_y[i])

# 	#plt.show()

# '''Json format data'''

building_data = [{"name":"building"+str(i),"x":str(buildings_x[i]), "y":str(buildings_y[i])} for i in range(len(buildings_x))]
road_data = [{"name":"road"+str(i), "x":str(roads_x[i]), "y":str(roads_y[i])} for i in range(len(roads_x))]

road_json = json.dumps(road_data, indent = 4)
  
# # Writing to sample.json
with open("road_generation_data.json", "w") as outfile:
    outfile.write(road_json)

print(road_data)


# '''map generation'''


# final_x = []
# final_y = []
# x_grid = []

# for i, key in enumerate(building_data):
# 	x = key['x'][1:-1].split(",")
# 	y = key['y'][1:-1].split(",")
# 	x = np.array([float(x_) for x_ in x])
# 	y = np.array([float(y_) for y_ in y])
# 	final_x.append(x)
# 	final_y.append(y)


# x_min = min([min(r) for r in final_x])
# x_max = max([max(r) for r in final_x])
# y_min = min([min(r) for r in final_y])
# y_max = max([max(r) for r in final_y])


# resolution = 1000

# #print(x_min-x_max)
# x_grid_range = np.linspace(x_min, x_max, resolution)
# y_grid_range = np.linspace(y_min, y_max, resolution)

# grid = np.zeros((resolution,resolution))

# def find_nearest(array, value):
#     array = np.asarray(array)
#     idx = (np.abs(array - value)).argmin()
#     return idx


# for i in range(len(final_x)):
# 		for x in range(len(final_x[i])):
# 			for y in range(len(final_y[i])):
# 				if x == 0 or y == 0:
# 					grid[find_nearest(x_grid_range, final_x[i][x])][find_nearest(y_grid_range, final_y[i][y])] = 1
# 				else:
# 					prev_x_i = find_nearest(x_grid_range, final_x[i][x-1])
# 					prev_y_i = find_nearest(y_grid_range, final_y[i][y-1])
# 					current_x_i = find_nearest(x_grid_range, final_x[i][x])
# 					current_y_i = find_nearest(y_grid_range, final_y[i][y])
# 					line_x = list(range(prev_x_i, current_x_i + 1))
# 					line_y = list(range(prev_y_i, current_y_i + 1))
# 					for n in line_x:
# 						for m in line_y:
# 							grid[n][m] = 1
# 					grid[current_x_i][current_y_i] = 1

# img = np.rot90(grid,1)
# img = np.array(img)

# chunks = np.hsplit(img, 4)
# for i in range(len(chunks)):
# 	chunks[i] = np.vsplit(chunks[i], 4)






# '''tile definition generation'''



# ne_corner = [0,0,0,0,1,1,0,1,1]
# nw_corner = [0,0,0,1,1,0,1,1,0]
# se_corner = [0,1,1,0,1,1,0,0,0]
# sw_corner = [1,1,0,1,1,0,0,0,0]

# ne_int_corner = [1,1,0,1,1,1,1,1,1]
# nw_int_corner = [0,1,1,1,1,1,1,1,1]
# sw_int_corner = [1,1,1,1,1,1,0,1,1]
# se_int_corner = [1,1,1,1,1,1,1,1,0]

# n_wall = [0,0,0,1,1,1,1,1,1]
# e_wall = [1,1,0,1,1,0,1,1,0]
# s_wall = [1,1,1,1,1,1,0,0,0]
# w_wall = [0,1,1,0,1,1,0,1,1]


# floor = [1,1,1,1,1,1,1,1,1]

# corners = {"ne_corner": ne_corner, "nw_corner": nw_corner,"se_corner": se_corner,"sw_corner": sw_corner}
# int_corners = {"ne_int_corner": ne_int_corner, "nw_int_corner": nw_int_corner,"se_int_corner": se_int_corner,"sw_int_corner": sw_int_corner}
# walls = {"n_wall":n_wall, "e_wall":e_wall, 's_wall':s_wall, "w_wall":w_wall}

# cornerlocations = []
# walllocations = []
# floorlocations = []
# intcornerlocations = []


# for i in range(len(img)):
# 	for j in range(len(img[0])):
# 		try:
# 			neigbourhood = [img[i-1][j-1], img[i][j-1], img[i+1][j-1], img[i-1][j], img[i][j], img[i+1][j],img[i-1][j+1], img[i][j+1], img[i+1][j+1]]
# 		except IndexError:
# 			pass
# 		for key, value in corners.items():
# 			if neigbourhood == value:
# 				cornerlocations.append((i,j,key))
# 		for key, value in walls.items():
# 			if neigbourhood == value:
# 				walllocations.append((i,j,key))
# 		for key, value in int_corners.items():
# 			if neigbourhood == value:
# 				intcornerlocations.append((i,j,key))
# 		if neigbourhood == floor:
# 			floorlocations.append((i,j,"floor"))

# #print(cornerlocations)
# #print(walllocations)
# #print(floorlocations)	
	
# generation_data = [{"name":i[2]+str(idx), "type": i[2], "x":str(i[0]), "y":str(i[1])} for idx, i in enumerate(cornerlocations)]
# generation_data = generation_data + [{"name":i[2]+str(idx), "type": i[2], "x":str(i[0]), "y":str(i[1])} for idx, i in enumerate(walllocations)]
# generation_data = generation_data + [{"name":i[2]+str(idx), "type": i[2], "x":str(i[0]), "y":str(i[1])} for idx, i in enumerate(floorlocations)]
# generation_data = generation_data + [{"name":i[2]+str(idx), "type": i[2], "x":str(i[0]), "y":str(i[1])} for idx, i in enumerate(intcornerlocations)]

# building_json = json.dumps(generation_data, indent = 4)
  
# # Writing to sample.json
# with open("generation_data.json", "w") as outfile:
#     outfile.write(building_json)
		
		
		



# imgplot = plt.imshow(img)
# plt.show()


