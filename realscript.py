from bs4 import BeautifulSoup
import requests
import re
import json
#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time

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
    print()
    print(station, updateTime)
    print('----------')
    # print(updateTime)
    # print('----------')

def Uptown(totalText):
    manhattan = jsonDict["direction1"]["times"][0:2]
    for i in range(0,2):
        global NextTrainsManhattan
       # NextTrainsManhattan = str("There is a", manhattan[i]["route"], "train to", manhattan[i]["lastStation"],":", manhattan[i]["minutes"], "minutes away")
        totalText += "There is a"
        totalText += str(manhattan[i]["route"])
        totalText += "train to"
        totalText += str(manhattan[i]["lastStation"])
        totalText += ":"
        totalText += str(manhattan[i]["minutes"])
        totalText += "minutes away"

# def Downtown(totalText):
#     brooklyn = jsonDict["direction2"]["times"][0:2]
#     for j in range(0,2):
#         global NextTrainsBrooklyn
#         NextTrainsBrooklyn = ("There is a", brooklyn[j]["route"], "train to", brooklyn[j]["lastStation"],":", brooklyn[j]["minutes"], "minutes away")
#         totalText += NextTrainsBrooklyn
#     print()

def main(): 
    Jsonify(twothreeURL)
    Info()
    global totalText
    totalText += jsonDict["direction1"]["name"]
    Uptown(totalText)
    Jsonify(fourfiveURL)
    Uptown(totalText)
    Jsonify(twothreeURL)
    totalText += jsonDict["direction2"]["name"]
 #   Downtown(totalText)
    Jsonify(fourfiveURL)
   # Downtown(totalText)
main() # set time limit
outputText = totalText

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default=outputText)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
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
