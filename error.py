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

def Uptown(x):
    uptowntext = ""
    manhattan = jsonDict["direction1"]["times"]
    print("manhattan ", manhattan)
    if manhattan[0]["minutes"] > x:
        uptowntext += str(manhattan[0]["route"])
        uptowntext += "  "
        uptowntext += str(manhattan[0]["minutes"])
        uptowntext += "min"
    elif manhattan[1]["minutes"] > x:
        uptowntext += str(manhattan[1]["route"])
        uptowntext += "  "
        uptowntext += str(manhattan[1]["minutes"])
        uptowntext += "min"
    elif manhattan[2]["minutes"] > x:
        uptowntext += str(manhattan[2]["route"])
        uptowntext += "  "
        uptowntext += str(manhattan[2]["minutes"])
        uptowntext += "min"
    else:
        return "delayed"
    return uptowntext

def Downtown(x):
    downtowntext = ""
    brooklyn = jsonDict["direction2"]["times"]
    print("brooklyn ", brooklyn)
    if brooklyn[0]["minutes"] > x:
        downtowntext += str(brooklyn[0]["route"])
        downtowntext += "  "
        downtowntext += str(brooklyn[0]["minutes"])
        downtowntext += "min"
    elif brooklyn[1]["minutes"] > x:
        downtowntext += str(brooklyn[1]["route"])
        downtowntext += "  "
        downtowntext += str(brooklyn[1]["minutes"])
        downtowntext += "min"
    elif brooklyn[2]["minutes"] > x:
        downtowntext += str(brooklyn[2]["route"])
        downtowntext += "  "
        downtowntext += str(brooklyn[2]["minutes"])
        downtowntext += "min"
    else:
        return "delayed"   
    return downtowntext

def Uptown45():
    text = "↑ "
    Jsonify(fourfiveURL)
    text += Uptown(0)
    return text
def Downtown45():
    text = "↓ "
    Jsonify(fourfiveURL)
    text += Downtown(0)
    return text
def Uptown23():
    text = "↑ "
    Jsonify(twothreeURL)
    text += Uptown(1)
    return text
def Downtown23():
    text = "↓ "
    Jsonify(twothreeURL)
    text += Downtown(1)
    return text
subwaytimeslist = []
def runall():
    subwaytimeslist.append(Uptown23())
    subwaytimeslist.append(Uptown45())
    subwaytimeslist.append(Downtown23())
    subwaytimeslist.append(Downtown45())
try:
    runall()
except (KeyboardInterrupt, SystemExit):
    raise
except:
    print("1st time failure")

#print(subwaytimeslist)
#if len(subwaytimeslist) == 4: 
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
        font.LoadFont("../../../fonts/5x8.bdf")
        blue = graphics.Color(0, 0, 255)
        red = graphics.Color(255, 0, 0)
        redcolor = graphics.Color(255,0,0)
        greencolor = graphics.Color(0, 255, 0)
        while asd == True:
            try:
                graphics.DrawText(canvas, font, 11, 7, redcolor, subwaytimeslist[0])
                graphics.DrawText(canvas, font, 11, 15, greencolor, subwaytimeslist[1])
                graphics.DrawText(canvas, font, 11, 23, redcolor, subwaytimeslist[2])
                graphics.DrawText(canvas, font, 11, 31, greencolor, subwaytimeslist[3])
            except:
                canvas.Clear()
                graphics.DrawText(canvas, font, 11, 7, redcolor, "Error")
                graphics.DrawText(canvas, font, 11, 15, redcolor, "Connecting")
                graphics.DrawText(canvas, font, 11, 23, redcolor, "To Server")
           # graphics.DrawText(canvas, font, 42, 16, blue, "RAWR")
           # graphics.DrawText(canvas, font, 42, 25, blue, "XC")
            subwaytimeslist.clear()
            try:
                runall()
                time.sleep(10)
                canvas.Clear()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                canvas.Clear()
                graphics.DrawText(canvas, font, 11, 7, redcolor, "Error")
                graphics.DrawText(canvas, font, 11, 15, redcolor, "Connecting")
                graphics.DrawText(canvas, font, 11, 23, redcolor, "To Server")
           
# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()


