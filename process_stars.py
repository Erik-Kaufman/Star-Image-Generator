"""
Author: Erik Kaufman
Date: 11/9/2024
Description: This is a work in progress script to generate an image of the stars in the night sky baised on their position.
It uses data in the BSC.json file that can be found here https://github.com/aduboisforge/Bright-Star-Catalog-JSON

This was created during the 2024 Hack K-State hackathon put on my MLH
"""
import json
import PIL.Image
import math


# get data from the json file
#
# Declaenation is the x, (DEC)
# Right Ascension is the y (RA)
#
x_size = 1000
y_size = 600

def convert_DEC_to_num(angle):
    # degrees minuets seconds
    # half is 90 degrees becasue plus or minus
    # full range is 3600 * 180 = 648000

    # in the format of "+00:00:00.00"

    pixle = 0
    pixle += int(angle[1:3]) * 3600 # degrees
    pixle += int(angle[4:6]) * 60 # minuet
    pixle += int(angle[7:9]) # seconds

    if angle[0] == "-":
        pixle = 32400 - pixle
    else:
        pixle = 32400 + pixle

    return pixle

# will return an intiger that will hold the position of the star as an int
def convert_RA_to_num(angle):
    # 1/24 of a circle per hour
    # 1/1440 of a circle per minuet
    # 1/86400 of a circle per second
    # total range is 24 * 3600 = 93600

    # in the format of "00:00:00.00"

    pixle = 0
    pixle += int(angle[0:2]) * 3600 # hour
    pixle += int(angle[3:5]) * 60 # minuet
    pixle += int(angle[6:8]) # seconds


    return pixle

with open("BSC.json") as file:
    # create the image
    im = PIL.Image.new(mode="RGB", size=(x_size, y_size))
    
    pixles = im.load()

    for x in range(im.size[0]):
        pixles[x, y_size/2] = (255, 255, 255)
    for y in range(im.size[1]):
        pixles[x_size/2, y] = (255, 255, 255)

    # loop through the data and update a pixle for each star
    for i, item in enumerate(json.load(file)):
        # convert the hours, degrees, minuts, seconds into a float, then scale it to the image and plot it
        dec_num = convert_DEC_to_num(item["DEC"])
        ra_num = convert_RA_to_num(item["RA"])

        # remap the pizles by dividing by the range of the pizles, then by multiplying by the screen size
        dec_pixle = math.floor((dec_num / 648000) * x_size)
        ra_pixle = math.floor((ra_num / 93600) * y_size)
        print(f"{i} x: {dec_pixle}")
        print(f"{i} y: {ra_pixle}")
        print(item)

        # set the pixles
        pixles[dec_pixle, ra_pixle] = (255, 255, 255)


im.show()

