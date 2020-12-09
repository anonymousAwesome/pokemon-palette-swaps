#to-do: The far upper-left corner of any sprite is almost certain to be background, so I could just tell the program to ignore that exact color.

#to-do: add HSV compatibility

from PIL import Image
import numpy as np
from os import listdir
from scipy.spatial import distance
import colorsys


def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.array( img, dtype="uint8" )
    return data

def nearest_color(coords1, coords_list):
	nearest_distance=float("inf")
	for coords2 in coords_list:
		if coords2[3]!=0:
			color_dist = distance.euclidean(coords1[0:2], coords2[0:2])
			if color_dist<nearest_distance:
				nearest_distance=color_dist
				nearest_color=coords2
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


#for each color in the source image, replace it with the nearest palette color.
#display the result.
#save the result to the hard drive.

files=[]

for filename in listdir():
	if ".png" in filename:
		files.append(filename)

for pokemon1 in files:
	for pokemon2 in files:
		Image.fromarray(palette_swap(pokemon1, pokemon2),mode="RGBA").save("./output/{}-{}.png".format(pokemon1.split(".")[0],pokemon2.split(".")[0]))
