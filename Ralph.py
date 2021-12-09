from geocoder import ip
from requests import get
from json import loads
from datetime import datetime
import pytz
from time import sleep
from pygame import mixer

class Colors:
    red = '\033[91m'
    green = '\033[92m'
    yel = '\033[93m'
    end = '\033[0m'

mixer.init()
mixer.music.load('ralph.mp3')

now = datetime.now()
current_time = now.strftime("%H:%M")
print(f'{Colors.green}Start time: {Colors.end}{current_time}')

g = ip('me')
lat = g.lat
lng = g.lng

utc_fulltime = datetime.now(tz=pytz.UTC)
print(f'{Colors.green}Current time in UTC: {Colors.end}{str(utc_fulltime)[11:16]}')
utc_hour = str(utc_fulltime)[11:13]
current_hour = current_time[0:2]
offset = int(current_hour) - int(utc_hour)

print(f'{Colors.green}Latitude: {Colors.end}{lat}\n{Colors.green}Longtitude: {Colors.end}{lng}')

params = {"lat": lat, "lng": lng, "date": current_time}

def sunset(f):
    a = get(f, params=params)
    a = loads(a.text)
    a = a["results"]
    return a["sunset"]

f = r"https://api.sunrise-sunset.org/json?"
in_time = datetime.strptime(sunset(f), "%I:%M:%S %p")
sunset_hour = datetime.strftime(in_time, "%H")
sunset_minute = datetime.strftime(in_time, "%M")
sunset_time = str(int(sunset_hour) + offset) + ':' + sunset_minute
print(f'{Colors.green}Time of sunset: {Colors.end}{sunset_time}\n')

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    print(f'Current time is: {current_time}')
    if current_time == sunset_time:
        print(f'{Colors.red}THE SUN IS SETTING!!!!!!{Colors.end}\n')
        mixer.music.play()
        mixer.music.set_volume(0.5)
    else:
        print(f"{Colors.yel}The sun doesn't really feel like setting rn{Colors.end}\n")
    sleep(60)