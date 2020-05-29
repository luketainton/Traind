#!/usr/bin/env python3

import argparse
import json
import os
import pprint
import pyttsx3
import requests


APP_HOST = "http://transportapi.com/v3"
APP_ID = "186cc4e2"
APP_KEY = "02c6fc426a52f46d7d7048cb91fc03e7"


def speak(speech):
    os.system(f"say '{speech}' &")


def get_data(APP_HOST, APP_ID, APP_KEY, STN):
    api_endpoint = f'{APP_HOST}/uk/train/station/{STN}/live.json?app_id={APP_ID}&app_key={APP_KEY}'
    data_raw = requests.get(api_endpoint).content.decode("utf-8")
    data = json.loads(data_raw)
    return data


def live_print_trains(dep,dest,op,plat):
    print(f"Scheduled: {dep}")
    print(f"Destination: {dest}")
    if op == "Virgin Trains":
        print(f"Operator: Avanti West Coast")
    else:
        print(f"Operator: {op}")
    print(f"Platform: {plat}")
    print(f"")


def get_next_train(data):
    try:
        train = data["departures"]["all"][0]
    except IndexError:
        text = "This station does not exist."
        print(text)
        speak(text)
        exit()
    result = f"The next train to depart from"
    if train['platform'] != None:
        result += f" platform {train['platform']} at"
    result += f" {data['station_name']} will be the {train['aimed_departure_time']} "
    if train["operator_name"] == "Virgin Trains":
        result += "Avanti West Coast"
    else:
        result += f"{train['operator_name']}"
    result += f" service from {train['origin_name']} to {train['destination_name']}."
    if train['aimed_departure_time'] != train['expected_departure_time']:
        result += f" It is currently expected to depart at {train['expected_departure_time']}."
    speak(result)
    print(f"Speaking...\n{result}\n")
    # print(json.dumps(train))


def main():
    parser = argparse.ArgumentParser(description='Get next departure from station.')
    parser.add_argument('-s', '--station', dest='stn', action='store', help='Station code')
    args = parser.parse_args()
    data = get_data(APP_HOST, APP_ID, APP_KEY, args.stn)
    get_next_train(data)
    # print(json.dumps(data))


try:
    main()
except KeyboardInterrupt:
    exit()
