#!/usr/bin/env python
# Display a runtext with double-buffering.
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
    manhattan = jsonDict["direction1"]["times"][0:2]
    for i in range(0,2):
        # NextTrainsManhattan = ("There is a", manhattan[i]["route"], "train to", manhattan[i]["lastStation"],":", manhattan[i]["minutes"], "minutes away")
        uptowntext += str(manhattan[i]["route"])
        uptowntext += " train in "
        uptowntext += str(manhattan[i]["minutes"])
        uptowntext += " min / "
        return uptowntext

def Downtown():
    downtowntext = ""
    brooklyn = jsonDict["direction2"]["times"][0:2]
    for j in range(0,2):
        # NextTrainsBrooklyn = ("There is a", brooklyn[j]["route"], "train to", brooklyn[j]["lastStation"],":", brooklyn[j]["minutes"], "minutes away")
        downtowntext += str(brooklyn[j]["route"])
        downtowntext += " train in "
        downtowntext += str(brooklyn[j]["minutes"])
        downtowntext += " min / "
        return downtowntext

def main(): 
    global uptowntext
    totaluptowntext = ""
    totaldowntowntext = ""
    Jsonify(twothreeURL)
    Info()
    totaluptowntext += Uptown()
    Jsonify(fourfiveURL)
    totaluptowntext += Uptown()
    print(totaluptowntext)
    print('---------')
    Jsonify(twothreeURL)
    totaldowntowntext += Downtown()
    Jsonify(fourfiveURL)
    totaldowntowntext += Downtown()
    print(totaldowntowntext)
    return totaldowntowntext
main() # set time limit






class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default=main())

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, "Dave Wake. Dave Code. Dave Sleep")
            len = graphics.DrawText(offscreen_canvas, font, pos, 30, textColor, "John Bloch 3:023")
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
