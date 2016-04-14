#!/usr/bin/env python
# coding=utf-8
import datetime
import requests
import random
import json
import time
import sys
import re

# 記得把MYIP跟LINE_TOKEN改成自己的！
MYIP = "140.123.111.111"
LINE_TOKEN = "kerker-12344321"
DAY_LIMIT = 8300

def getDaysFromEpoch():
    today = datetime.date.today()
    epoch = datetime.date(1970, 1, 1)
    diff = today - epoch
    return diff.days

def readConf():
    config = json.loads(json.load(open(".flowrc", 'r')))
    now = getDaysFromEpoch()
    if now - config['days'] > 0:
        # a brand new day, reset all flags
        config = {'days': now, 'busted': 0, 'fifty': 0, 'seventy': 0, 'ninety': 0}
        writConf(config)

    return config

def writConf(config):
    json.dump(json.dumps(config), open(".flowrc",'w'))

def getFlowStats():
    url = "http://netflow.dorm.ccu.edu.tw/flows/%s" % MYIP
    try:
        r = requests.get(url, timeout=30)
    except requests.exceptions.Timeout:
        print "CNA不要搞笑啊, 花了好久都抓不到資料！"
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    match = re.findall('y: (\d+\.\d+)', r.text)
    if len(match) < 2 or len(match) & 0x1:
        print "怪怪, 流量資訊不正確"
        sys.exit(1)
    else:
        allTraffic = [float(i) for i in match]
        downloads = allTraffic[:len(allTraffic)/2]
        uploads = allTraffic[len(allTraffic)/2:]

        return sum(downloads), sum(uploads)

def sendAlert(config, msg, im):
    req_url = "https://csie.io/msgme?token=%s&msg=%s&im=%s" % (LINE_TOKEN, msg, im)
    r = requests.get(req_url)
    if r.text == "OK":
        # message sent. safe to update configs
        print "成功發送訊息"
        writConf(config)
    else:
        print "發送訊息時發生錯誤，等下次再試一次kerker"
        sys.exit(1)

def checkUsage(config, download, upload):
    index = ""
    usage_rate = (download + upload) / DAY_LIMIT
    msg_template = "您還剩%.2f MB (%.0f%%)的流量可用，本日還剩%d小時，統計資訊如下：\n\n下載量: %.2f MB\n上傳量: %.2f MB\n總使用量: %.2f MB"

    if usage_rate > 1.0:
        index = "busted"
    elif usage_rate > 0.9:
        index = "ninety"
    elif usage_rate > 0.7:
        index = "seventy"
    elif usage_rate > 0.5:
        index = "fifty"

    if index != "" and config[index] == 0:
        if index == "busted":
            msg = "已經超流要被斷線啦！悲劇啊啊啊啊啊～"
        else:
            msg = msg_template % (DAY_LIMIT-(download + upload), 100-usage_rate*100, (24 - datetime.datetime.now().hour), download, upload, (download + upload))

        config[index] = 1
        sendAlert(config, msg, "line") # for use "fb" for Facebook


if __name__ == "__main__":
    # sleep few seconds before we start
    # we don't want to DDoS newflow.dorm
    time.sleep(random.randint(1,10))

    # Fire in the hole!
    download, upload = getFlowStats()
    config = readConf()
    checkUsage(config, download, upload)
