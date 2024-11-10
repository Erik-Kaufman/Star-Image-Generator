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

# try converting to spherical cordinates to see it it is what I want

# from https://en.wikipedia.org/wiki/Equatorial_coordinate_system
# z sin del
# x cos del * cos ra
# y cos del * sin ra


# get data from the json file
#
# Declaenation is the x, (DEC)
# Right Ascension is the y (RA)
#
x_size = 2000
y_size = 2000

def convert_DEC_to_radians(angle):
    # degrees minuets seconds
    # half is 90 degrees becasue plus or minus
    # full range is 3600 * 180 = 648000

    # in the format of "+00:00:00.00"

    deg = 0.0
    deg += float(angle[1:3])  # degrees
    deg += float(angle[4:6]) / 60 # minuet
    deg += float(angle[7:12]) / 3600 # seconds

    if angle[0] == "-":
        deg = 90.0 - deg
    else: 
        deg = 90.0 + deg

    radians = (deg / 360.0) * (math.pi * 2)
    return radians

# will return an intiger that will hold the position of the star as an int
def convert_RA_to_radians(angle):
    # 1/24 of a circle per hour
    # 1/1440 of a circle per minuet
    # 1/86400 of a circle per second
    # total range is 24 * 3600 = 93600

    # in the format of "00:00:00.00"

    circle = 0
    circle += float(angle[0:2]) / 24.0 # hour
    circle += float(angle[3:5]) / 1440 # minuet
    circle += float(angle[6:11]) / 86400# seconds

    # multiply by two pi to get to radians
    return circle * 2 * math.pi

with open("BSC.json") as file:
    # create the image
    im = PIL.Image.new(mode="RGB", size=(x_size, y_size))
    
    pixles = im.load()

    #for x in range(im.size[0]):
    #    pixles[x, y_size/2] = (255, 255, 255)
    #for y in range(im.size[1]):
    #    pixles[x_size/2, y] = (255, 255, 255)

    # loop through the data and update a pixle for each star
    for i, item in enumerate(json.load(file)):
        # convert the hours, degrees, minuts, seconds into a float, then scale it to the image and plot it
        dec_rad = convert_DEC_to_radians(item["DEC"])
        ra_rad = convert_RA_to_radians(item["RA"])

        # remap the pizles by dividing by the range of the pizles, then by multiplying by the screen size
        x = math.cos(dec_rad) * math.cos(ra_rad) * x_size / 2.0
        y = math.cos(dec_rad) * math.sin(ra_rad) * y_size / 2.0

        # scale it back to positive numbers
        x += x_size / 2
        y += y_size / 2

        print(f"{i} x: {math.floor(x)}")
        print(f"{i} y: {math.floor(y)}")
        print(item)

        # set the pixles
        pixles[math.floor(x), math.floor(y)] = (255, 255, 255)


im.show()

