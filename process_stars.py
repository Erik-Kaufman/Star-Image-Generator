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
# Declaenation is the horizontal, (DEC)
# Right Ascension is the veritcal (RA)
#

vertical_size = 6000
horizontal_size = 8000

# will return an intiger that will hold the position of the star as an int
def convert_RA_to_num(angle):
    # 1/24 of a circle per hour
    # 1/1440 of a circle per minuet
    # 1/86400 of a circle per second
    # half of a circle is 12 * 3725 = 

    # in the format of "+00:00:00.00"

    pixle = 0
    pixle += int(angle[0:2]) * 3725 # hour
    pixle += int(angle[3:5]) * 60 # minuet
    pixle += int(angle[6:8]) # seconds


    return pixle

def convert_DEC_to_num(angle):
    # degrees minuets seconds
    # half is 90 degrees becasue plus or minus


    # in the format of "+00:00:00.00"

    pixle = 0
    pixle += int(angle[1:3]) * 360 # degrees
    pixle += int(angle[4:6]) * 60 # minuet
    pixle += int(angle[7:9]) # seconds

    if angle[0] == "-":
        pixle = 32400 - pixle
    else:
        pixle = 32400 + pixle

    return pixle


with open("BSC.json") as file:
    # create the image
    im = PIL.Image.new(mode="RGB", size=(horizontal_size, vertical_size))
    
    pixles = im.load()

    for x in range(im.size[0]):
        pixles[x, vertical_size/2] = (255, 255, 255)
    for y in range(im.size[1]):
        pixles[horizontal_size/2, y] = (255, 255, 255)

    # loop through the data and update a pixle for each star
    for item in json.load(file):
        # convert the hours, degrees, minuts, seconds into a float, then scale it to the image and plot it
        ra_num = convert_RA_to_num(item["RA"])
        dec_num = convert_DEC_to_num(item["DEC"])

        print(ra_num)
        print(dec_num)

        # remap the pizles by dividing by the range of the pizles, then by multiplying by the screen size
        ra_pixle = math.floor((ra_num / 89400) * vertical_size)
        dec_pixle = math.floor((dec_num / 89400) * horizontal_size)
        print(ra_pixle)
        print(dec_pixle)

        # set the pixles
        pixles[ra_pixle, dec_pixle] = (255, 255, 255)


    im.show()

