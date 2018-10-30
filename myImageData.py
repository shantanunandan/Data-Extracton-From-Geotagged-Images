import os
import fnmatch
import pysrt
import csv
import simplekml
import argparse
from ImageMetaData import ImageMetaData
from geopy.distance import vincenty
from datetime import datetime, timedelta
from math import asin, cos, radians, sin, sqrt


class image():
    def imageMapping(self, imgDir, imgPattern):
        """Used a dicsnory to """
        imgToGPS = {}
        listOfImages = os.listdir(imgDir)
        for image in listOfImages:
            if fnmatch.fnmatch(image, imgPattern):
                img_path = '/'.join([imgDir, image])
                lat, lng = ImageMetaData(img_path).getLngLat()
            if lat and lng:
                imgToGPS[image] = (lat, lng)
        return imgToGPS

    def csvWrite(self, data, csvFileName):
        """Writes the given data row-wise to the given csv file."""
        with open(csvFileName, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in data.items():
               writer.writerow([key,value])

    def readCSV(self, csvFileName):
        """Read a CSV file and returns a dict containing its data."""
        data = []
        with open(csvFileName) as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                data.append(row)
        return data

    # Created this module to identify locations given in asserts.csv file but fall short of time
    def findSpot(self, fileName):
        data = self.readCSV(fileName)
        for i in data:
             pass

d = image().imageMapping('images','*JPG')
image().csvWrite(d, "locationCoordinates.csv")
image().findSpot("locationCoordinates.csv")
