from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from fonts.ttf import *
import time
import requests
from key import *

class Clock():

    def __init__(self,rotation=180):
        self.inky_display = InkyPHAT("red")
        self.inky_display.set_border(self.inky_display.BLACK)
        self.WIDTH = self.inky_display.WIDTH
        self.HEIGHT = self.inky_display.HEIGHT
        self.WHITE = self.inky_display.WHITE
        self.RED = self.inky_display.RED
        self.BLACK = self.inky_display.BLACK
        self.rotation=180

    def create_image(self, currenttime, currentdate, temp, tempmax, tempmin):
        img = Image.open("./images/backdrop.png")
        draw = ImageDraw.Draw(img)

        #Adding the time and date
        font = ImageFont.truetype(FredokaOne, 28)
        draw.text((6,15), currentdate, self.RED, font=font)

        font = ImageFont.truetype(FredokaOne, 40)
        draw.text((int(self.WIDTH/2), 5), currenttime, self.BLACK, font=font)


        #adding max temp
        font = ImageFont.truetype(FredokaOne, 20)
        draw.text((22, 70), temp, self.RED, font=font)
        draw.text((92, 70), tempmin, self.RED, font=font)
        draw.text((160, 70), tempmax, self.RED, font=font)

        self.display_img(img)

    def display_img(self, img):
        img = img.rotate(self.rotation)
        self.inky_display.set_image(img)
        self.inky_display.show()



    def test_image(self):
        img = Image.open("./images/TagTest-212x104.png")
        self.display_img(img)


def main():
    """
    Main loop that gets the data and sends to the display
    Needs the API key in the key file
    Updates display every 5 min, because it takes a few seconds to update the display
    Otherwise it keeps blinking a lot
    City is set to Gothenburg
    :return:
    """
    clock = Clock()
    GOT = 2711537
    temp = []
    maxtemp = []
    mintemp = []
    while(True):
        currentdate = time.strftime("%d/%m")
        currenttime = time.strftime("%H:%M")
        minutes = int(time.strftime("%M"))
        if minutes % 5 == 0:
            url = "http://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&APPID={APIKEY}".format(CITY_ID=GOT,APIKEY=KEY)
            r = requests.get(url)
            if r.status_code == 200:
                jsondata = r.json()
                #print(jsondata)
                temp = str(int(jsondata["main"]["temp"] -273.15))+"˚C"
                maxtemp = str(int(jsondata["main"]["temp_max"] -273.15))+"˚C"
                mintemp = str(int(jsondata["main"]["temp_min"] -273.15))+"˚C"
            clock.create_image(currenttime, currentdate, temp, maxtemp, mintemp)
        time.sleep(60)



if __name__ == "__main__":
    main()