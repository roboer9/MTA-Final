#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from bs4 import BeautifulSoup
import requests
import re
import json
twothreeURL = 'http://traintimelb-367443097.us-east-1.elb.amazonaws.com/getTime/2/232?callback=angular.callbacks._0'
fourfiveURL = 'http://traintimelb-367443097.us-east-1.elb.amazonaws.com/getTime/4/423?callback=angular.callbacks._0'

def Jsonify(trainURL):
    r = requests.get(trainURL)
    soup = BeautifulSoup(r.text,'html.parser')
    #json1 since need to call an actual json funtion later on
    json1 = soup.text
    json1 = json1.split('(')
    json1 = json1[1].split(')')
    json1 = json1[0]
    global jsonDict
    jsonDict = json.loads(json1)

def Info():
    updateTime = jsonDict["lastUpdatedTime"]
    station = jsonDict["stationName"]
    print(station, updateTime)
    print('----------')
    # print(updateTime)
    # print('----------')

def Uptown():
    uptowntext = ""
    manhattan = jsonDict["direction1"]["times"]
    if manhattan[0]["minutes"] > 0:
        uptowntext += str(manhattan[0]["route"])
        uptowntext += ":"
        uptowntext += str(manhattan[0]["minutes"])
        uptowntext += "min"
    elif manhattan[1]["minutes"] > 0:
        uptowntext += str(manhattan[1]["route"])
        uptowntext += ":"
        uptowntext += str(manhattan[1]["minutes"])
        uptowntext += "min"
    else:
        return "delayed"
    return uptowntext

def Downtown():
    downtowntext = ""
    brooklyn = jsonDict["direction2"]["times"]
    if brooklyn[0]["minutes"] > 0:
        downtowntext += str(brooklyn[0]["route"])
        downtowntext += ":"
        downtowntext += str(brooklyn[0]["minutes"])
        downtowntext += "min"
    elif brooklyn[1]["minutes"] > 0:
        downtowntext += str(brooklyn[1]["route"])
        downtowntext += ":"
        downtowntext += str(brooklyn[1]["minutes"])
        downtowntext += "min"
    else:
        return "delayed"   
    return downtowntext

def Uptown45():
    text = "↑ "
    Jsonify(fourfiveURL)
    text += Uptown()
    return text
def Downtown45():
    text = "↓ "
    Jsonify(fourfiveURL)
    text += Downtown()
    return text
def Uptown23():
    text = "↑ "
    Jsonify(twothreeURL)
    text += Uptown()
    return text
def Downtown23():
    text = "↓ "
    Jsonify(twothreeURL)
    text += Downtown()
    return text
subwaytimeslist = []
def runall():
    subwaytimeslist.append(Uptown23())
    subwaytimeslist.append(Uptown45())
    subwaytimeslist.append(Downtown23())
    subwaytimeslist.append(Downtown45())

runall()

#print(subwaytimeslist)
asd = True
# run all add values to list
# up45 = Uptown45()
# down45 = Downtown45()
# up23 = Uptown23()
# down23 = Downtown23()
# DowntownPrint = AllDowntown()
# UptownPrint = AllUptown()
class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("../../../fonts/6x9.bdf")
        blue = graphics.Color(0, 0, 255)
        red = graphics.Color(255, 0, 0)
        redcolor = graphics.Color(255,0,0)
        greencolor = graphics.Color(0, 255, 0)
        while asd == True:
            graphics.DrawText(canvas, font, 2, 6, redcolor, subwaytimeslist[0])
            graphics.DrawText(canvas, font, 2, 14, greencolor, subwaytimeslist[1])
            graphics.DrawText(canvas, font, 2, 22, redcolor, subwaytimeslist[2])
            graphics.DrawText(canvas, font, 2, 30, greencolor, subwaytimeslist[3])
            subwaytimeslist.clear()
            runall()
            time.sleep(10)
            canvas.Clear()

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()


