#WARNING: currently only compatible with non-indexed png files.  
#If your folder contains indexed png files (you'll know because the program will crash),
#use the included deindex.py to convert them.  It requires the third-party 
#program ImageMagick.

#to-do: add native indexed png compatibility

#to-do: add HSV compatibility

#to-do: The far upper-left corner of any sprite is almost certain to be 
#background, so I could just tell the program to ignore that exact color.

from PIL import Image
import numpy as np
from os import listdir
import pdb
import math

def distance(a,b):
	return(math.sqrt( (int(a[0])-int(b[0]))**2 + (int(a[1])-int(b[1]))**2 + (int(a[2])-int(b[2]))**2))

def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.array( img, dtype="uint8" )
    return data

def nearest_color(coords1, coords_list):
	nearest_distance=float("inf")
	print("new pixel")
	for coords2 in coords_list:
		if coords2[3]!=0:
			color_dist = distance(coords1[0:3], coords2[0:3])
			if color_dist<nearest_distance:
				nearest_distance=color_dist
				nearest_color=coords2
			if 16 in coords1:
					print("/n")
					print("source pixel color: ",coords1)
					print("test color replacement: ",coords2)
					print("color distance: ",color_dist)
					print("nearest distance: ",nearest_distance)
					print("nearest color: ",nearest_color)
	return nearest_color

def palette_swap(source_pokemon_filename,palette_pokemon_filename, color_format="RGB"):

	source_pokemon_file=load_image(source_pokemon_filename)
	palette_pokemon_file=load_image(palette_pokemon_filename)

	#flatten into a list of 4-value "pixels"
	palette_pixels=palette_pokemon_file.reshape(-1, palette_pokemon_file.shape[-1])

	#get the unique values
	palette_colors=(np.unique(palette_pixels,axis=0))

	if color_format=="HSV":
		#to-do: convert palette colors to HSV
		pass
	
	for i,row in enumerate(source_pokemon_file):
		for j,pixel in enumerate(row):
			if pixel.tolist()!=[0,0,0,255] and pixel[3]!=[0]:
				if color_format=="RGB":
					source_pokemon_file[i][j]=nearest_color(pixel,palette_colors)
				elif color_format=="HSV":
					#to-do:
					#convert source_pokemon colors to HSV
					#determine the closest colors
					#convert back to RGB
					pass
	return source_pokemon_file

files=[]

for filename in listdir():
	if ".png" in filename:
		files.append(filename)

for pokemon1 in files:
	for pokemon2 in files:
		Image.fromarray(palette_swap(pokemon1, pokemon2),mode="RGBA").save("./output5/{}-{}.png".format(pokemon1.split(".")[0],pokemon2.split(".")[0]))

'''
#testing code
pokemon1="BW-104.png"
pokemon2="BW-575.png"
Image.fromarray(palette_swap(pokemon1, pokemon2),mode="RGBA").resize((400,400)).show()
'''