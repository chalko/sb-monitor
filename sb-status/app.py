# flask_web/app.py

import requests
import requests_cache
from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify

requests_cache.install_cache( expire_after=300)

app = Flask(__name__)


@app.route('/')
def hello_world():
    r = requests.get("http://192.168.100.1")

    soup = BeautifulSoup(r.text, 'lxml')
    infoTables = soup.findAll('table', {'class': 'simpleTable'})

    downstream = infoTables[1]
    upstream = infoTables[2]

    downChannels = parseDownstream(downstream.find_all_next('td'))
    upChannels = parseUpstream(upstream.find_all_next('td'))
    return jsonify(downChannels=downChannels, upChannels=upChannels)


def parseDownstream(obj):
    channels = []
    channelDescr = []
    channelSet = {}

    skipNext = 0
    for v in obj:
        if skipNext:
            skipNext -= 1
            continue

        if v.string == "Channel ID":
            skipNext = 7
            continue

        # In case we get the whole bullshit.
        if v.string == "Channel":
            break

        channelDescr.append(v.string)

        if len(channelDescr) == 8:
            channels.append(channelDescr)
            channelDescr = []

    for channel in channels:
        channelDescr = {
            'id': int(channel[0]),
            'status': channel[1],
            'modulation': channel[2],
            'freq': int(channel[3].split()[0]),
            'power': float(channel[4].split()[0]),
            'snr': float(channel[5].split()[0]),
            'corrected': int(channel[6]),
            'uncorrected': int(channel[7])
        }

        channelSet[channelDescr["id"]] = channelDescr

    return channelSet


def parseUpstream(obj):
    channels = []
    channelDescr = []
    channelSet = {}

    skipNext = 0
    for v in obj:
        if skipNext:
            skipNext -= 1
            continue

        if v.string == "Channel":
            skipNext = 6
            continue

        channelDescr.append(v.string)

        if len(channelDescr) == 7:
            channels.append(channelDescr)
            channelDescr = []

    for channel in channels:
        channelDescr = {
            'id': int(channel[0]),
            'channel': int(channel[1]),
            'status': channel[2],
            'type': channel[3],
            'freq': int(channel[4].split()[0]),
            'width': int(channel[5].split()[0]),
            'power': float(channel[6].split()[0]),
        }

        channelSet[channelDescr['id']] = channelDescr

    return channelSet
