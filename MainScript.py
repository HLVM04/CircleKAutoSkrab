import requests
from random import randint
import json
import sys
import time
from win10toast import ToastNotifier
import datetime

from GuiHandler import openGui

headers = {
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Origin': 'https://skrab.circlek.one',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,da;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'content-type': 'application/json',
    'Accept': '*/*',
    'Referer': 'https://skrab.circlek.one/',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache'
}

phone_numbers_file = "phone_numbers.json"
toaster = ToastNotifier()

def getLoginToken(phone_number):
    data = '{"id":"L2ZyZ2d2YXRmL3F4X2ZyZ2d2YXRmLmN1Yw==","pid":"' + phone_number + '","permission":false,"referrer":"https://skrab.circlek.one/lib/php/login.php","device":{"brand":"","model":"","browser":"Netscape Navigator","browser_version":"9.0","os":"Windows","os_version":"98"}}'
    response = requests.post('https://skrab.circlek.one/lib/php/login.php', headers=headers, data=data)

    if response.status_code == 200:
        token = response.json()['cid']
        return token


def scratch(phone_number):
    token = getLoginToken(phone_number)
    if token is None:
        print("Token is empty :(")
        exit()

    data = '{"name":"scratch","id":"L2ZyZ2d2YXRmL3F4X2ZyZ2d2YXRmLmN1Yw==","cid":"' + token + '"}'
    response = requests.post('https://skrab.circlek.one/lib/php/scratch.php', headers=headers, data=data)

    if response.status_code == 200:
        scratch_result = response.json()
        won = scratch_result['state']

        if won:
            return won, scratch_result['title']
        else:
            return won, None


def randomScratch():
    def randomPhoneNumber():
        range_start = 10 ** (8 - 1)
        range_end = (10 ** 8) - 1
        return randint(range_start, range_end)

    while True:
        number = str(randomPhoneNumber())
        result, price = scratch(number)
        if result:
            print("You won: " + price + " (" + number + ")")
        else:
            print("You didn't win :(" + " (" + number + ")")

def dailyScratch():
    while True:
        with open("settings.json", 'r') as g:
            settings = json.load(g)

        if settings["last_scratch"] != None:
            last_scratch = datetime.datetime.strptime(settings["last_scratch"], "%Y-%m-%dT%H:%M:%S.%f")
        else:
            last_scratch = datetime.datetime(1970, 1, 1)

        if last_scratch < datetime.datetime.now() - datetime.timedelta(seconds=settings["scratch_time_offset_seconds"]):
            with open(phone_numbers_file, 'r') as f:
                phone_numbers = json.load(f)

            for phone_number in phone_numbers:
                result, price = scratch(phone_number)
                print(result)
                if result:
                    toaster.show_toast("CircleK Auto Skrab",
                                       "You Won a " + price + " on " + phone_number + "!",
                                       duration=settings["scratch_time_offset_seconds"],
                                       icon_path="app.ico",
                                       threaded=True)
                else:
                    if settings["show_notifications_when_not_winning"]:
                        toaster.show_toast("CircleK Auto Skrab",
                                           "You didn't win today :(",
                                           icon_path="app.ico",
                                           duration=settings["scratch_time_offset_seconds"],
                                           threaded=True)

            settings["last_scratch"] = datetime.datetime.now().isoformat()

            with open("settings.json", 'w') as g:
                json.dump(settings, g)

            print("Waiting for " + str(settings["scratch_time_offset_seconds"]) + " seconds")
            time.sleep(settings["scratch_time_offset_seconds"])
        else:
            seconds_till_next_scratch = settings["scratch_time_offset_seconds"] - (datetime.datetime.now() - last_scratch).total_seconds()
            print("Still waiting for " + str(seconds_till_next_scratch) + "seconds")
            time.sleep(seconds_till_next_scratch)


if len(sys.argv) > 1 and sys.argv[1] == "nogui":
    dailyScratch()
    #randomScratch()
else:
    openGui()
