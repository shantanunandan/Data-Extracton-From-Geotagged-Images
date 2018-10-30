"""Technical assingnment for Skylark Drones."""

import os
import fnmatch
import pysrt
import csv
import simplekml
import argparse
from ImageMetaData import ImageMetaData
from geopy.distance import vincenty
from datetime import datetime, timedelta
from myImageData import image

def imageBuilder(directory, pattern):
    """Used a dicsnory to map the image data i.e, cordinates to the 
		respective images in order to get required data after extracting 
		EXIF data from the geotagged images."""
    imageGPS = {}
    listingImage = os.listdir(directory)
    for image in listingImage:
        if fnmatch.fnmatch(image, pattern):
            path = '/'.join([directory, image])
            lat, lng = ImageMetaData(path).getLngLat()
        if lat and lng:
            imageGPS[image] = (lat, lng)
    return imageGPS


def imageMapping():
    """ImageBuilder function without argument so that it can be used in myImageData module."""
    imageGPS = {}
    path = '/'.join([directory, image])
    lat, lng = ImageMetaData(path).getLngLat()
    if lat and lng:
    	imageGPS['A'] = (lat, lng)
    return imageGPS



def imageRadius(currentCord, imageGPS, Radius):
    """Iterating through all the subtitled item in a given radius of all items 
	and gets a combined image list."""
    imageList = []
    for image, coords in imageGPS.items():
        #Uses vincenty's method to calculate distance between two coordinates.
        if vincenty(currentCord, coords).meters <= Radius:
            imageList.append(image)
    return imageList


def cordinateFromSrt(sub):
    """Aquiring the cordinate of the images from the given timestampped srt file."""
    currentLang, currentLat, elevation = sub.text.split(',')
    return (currentLat, currentLang)


def imageInRadian(subsList, imageGPS, RADIUS):
    """Go through a list of subtitle items, and gets a combined image list
    containing images in the given radius of all the items."""
    imageList = []
    for sub in subsList:
        imageList += imageRadius(cordinateFromSrt(sub), imageGPS, RADIUS)
    return imageList


def subsFromTime(subs, currentTime, endTime):
    """Slicing subtitle file to get item list lying between given time."""
    return subs.slice(
        starts_after={
            'minutes': currentTime.minute,
            'seconds': currentTime.second},
        starts_before={
            'minutes': endTime.minute,
            'seconds': endTime.second})


def writeDataToCSV(data, csvfile):
    """Function is used to write the data row wise into the respective csv file"""
    with open(csvfile, "w") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)


def prefixFileCreation(prefix, file, extension):
    """From the given prefix, file, and extensionension creates a appropriate file."""
    file = file.split(".")[0]
    return prefix + file + "." + extension


def videoProcessing(video, videoPath, imageGPS):
    """Function is used to write the data row wise into the respective csv file after 
	processing the SRT file data and getting the related images."""
    subs = pysrt.open(videoPath)
    currentTime = datetime(2000, 1, 1, minute=0, second=0)
    nextensionTime = currentTime + timedelta(seconds=1)
    data = []
    data.append(["time", "image_names"])
    while True:
        parts = subsFromTime(subs, currentTime, nextensionTime)
        if not parts:
            break
        imageList = imageInRadian(parts, imageGPS, videoRadius)
        currentTime, nextensionTime = nextensionTime, nextensionTime + timedelta(seconds=1)
        data.append([currentTime.strftime("%M:%S"), ", ".join(imageList)])
    writeDataToCSV(data, prefixFileCreation("Image_Data_", video, "csv"))


def createKmlFile(video, videoPath):
    """Creating KML file from given SRT file that contains timestampped GPS coordinates."""
    subs = pysrt.open(videoPath)
    data = []
    for sub in subs:
        latitude, longitude = cordinateFromSrt(sub)
        data.append([sub.start, latitude, longitude])
    csvfile = prefixFileCreation("KML_Data_", video, "csv")
    writeDataToCSV(data, csvfile)
    inputfile = csv.reader(open(csvfile, "r"))
    kml = simplekml.Kml()
    for row in inputfile:
        kml.newpoint(name=row[0], coords=[(row[2], row[1])])
    kml.save(prefixFileCreation("", video, "kml"))


def processAllVideosFiles(imageGPS, vidDir, vidPattern):
    """Using videoProcessing and createKmlFile on all the files in the given
    directory."""
    listOfVideos = os.listdir(vidDir)
    for video in listOfVideos:
        if fnmatch.fnmatch(video, vidPattern):
            videoPath = '/'.join([vidDir, video])
            videoProcessing(video, videoPath, imageGPS)
            createKmlFile(video, videoPath)


def readCSVFileData(csvfile):
    """Function is used to read the data row wise from the given csv file"""
    data = []
    with open(csvfile) as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            data.append(row)
    return data


def processPOIFile(imageGPS, csvfile):
    """Extracting information from file containing points of interest with their GPS coordinates
    and creating csv file which contains the images in the radius of the points in which we are
	interested."""
    assetsData = readCSVFileData(csvfile)
    imagesData = []
    imagesData.append(["asset_name", "image_names"])
    for asset in assetsData:
        currentCord = (asset["latitude"], asset["longitude"])
        imageList = imageRadius(currentCord, imageGPS, POI_RADIUS)
        imagesData.append([asset["asset_name"], ", ".join(imageList)])
    writeDataToCSV(imagesData, prefixFileCreation(
        "Image_Data_", csvfile, "csv"))

directory = "images" # Name of image directory
vidDir = "videos" # Name of video directory
pattern = "*.JPG" # Format of Image
vidPattern = "*.SRT" # Format of Video
videoRadius = int(input("Enter Video Radius : ")) 
POI_RADIUS = int(input("Enter Video Radius : "))
imageGPS = imageBuilder(directory, pattern)
processAllVideosFiles(imageGPS, vidDir, vidPattern)
processPOIFile(imageGPS, "assets.csv") 
