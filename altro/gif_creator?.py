import Image, ImageDraw, time
import os

file_names = sorted((fn for fn in os.listdir(os.getcwd()) if fn.endswith('.jpg')))

print file_names

#Open the files
print 'Opening the images'
images = [Image.open(os.getcwd() + '/' + fn) for fn in file_names]

from images2gif import writeGif
from time import time

#Set to 24FPS
runningtime = 0.0416

filename = "Gif/Gif" 
writeGif(filename   + str(int(time())) + ".gif", images, duration=runningtime, dither=1)