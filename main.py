#!/usr/bin/python3

from datetime import datetime
from time import time
import requests
import hashlib
import random


def main():
    """ To get your API-key visit codeforces.com/settings/api
    Then click on 'Add API key' then pass your key and secret
    For more info about API visit codeforces.com/apiHelp ."""

    contests_list("YOUR_API",
                  "YOUR_SECRET")


def contests_list(apiKey, secret):
    """ Get info about coming contests """

    crnt_time = int(time())
    methodName = "contest.list"
    rand = random.randint(100000, 999999)
    encrypt = "{}/{}?apiKey={}&time={}#{}".format(
        rand, methodName, apiKey, crnt_time, secret)
    hash = hashlib.sha512(encrypt.encode('UTF-8')).hexdigest()
    apiSig = "{}{}".format(rand, hash)
    args = "apiKey={}&time={}&apiSig={}".format(apiKey, crnt_time, apiSig)
    target = "https://codeforces.com/api/{}?{}".format(methodName, args)
    data = requests.get(target).json()
    if (data["status"] == "FAILED"):
        print(f"\033[4mRequest failed...\033[0m\n{data['comment']}")
        return
    for contest in data['result']:
        if (contest["phase"] == "BEFORE"):
            remain = -contest["relativeTimeSeconds"]
            duration = contest["durationSeconds"]
            start_date = datetime.fromtimestamp(contest["startTimeSeconds"])
            start_date = start_date.strftime("%A, %B %d, %I:%M")
            print(f"\033[4m{contest['name']}\033[0m"
                  f"\nStarts at: {start_date}\nTime Remaining: "
                  f"{int(remain/(60*60*24)):02d} day(s), "
                  f"{int(remain%(60*60*24)/(60*60)):02d}:"
                  f"{int(remain%(60*60)/60):02d}\n"
                  f"Contest duration: {int(duration/(60*60)):02d}:"
                  f"{int(duration%(60*60)/60):02d}\n")


main()
