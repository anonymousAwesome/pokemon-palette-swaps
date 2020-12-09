#converts all png files in a folder to non-indexed png files.
#requires the third-party software Imagemagick.

import os

files=[]

for filename in os.listdir():
	if ".png" in filename:
		files.append(filename)
		
for f in files:

	#overwrite existing file:

	os.system("convert {} -colorspace srgb PNG32:{}".format(f,f))


	#comment previous line and decomment next two lines to add prefix to exported files

	#prefix="RGB"
	#os.system("convert {} -colorspace srgb PNG32:{}{}".format(f,prefix,f))