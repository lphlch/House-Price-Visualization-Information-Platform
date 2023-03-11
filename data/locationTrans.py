from urllib.request import urlopen
import urllib.parse
import json
from time import sleep

def transLocation(address):
    url = (
        "https://api.map.baidu.com/geocoding/v3/?address="
        + address
        + "&output=json&ak="
        + ak
    )
    url = urllib.parse.quote(url, safe=";/?:@&=+$,", encoding="utf-8")
    # print(url)
    request = urlopen(url)
    web_html = request.read().decode("utf-8")
    # print('web',web_html)

    text = json.loads(web_html)
    # print(text)

    status = text["status"]
    longtitute = text["result"]["location"]["lng"]
    latitude = text["result"]["location"]["lat"]

    return status, longtitute, latitude


def readData(fileName,start=0):
    datas = []
    f = open(fileName, "r")
    for line in f:
        if start > 0:
            start -= 1
            continue
        datas.append("".join(line.split("\t")[1:3]))

    f.close()
    return datas


datas = readData("data.txt", 9000)

address_file = open("address.txt", "a")

for address in datas[:500]:
    status, lng, lat = transLocation(address)
    print(address, status, lng, lat)
    if status == 0:
        address_file.write(address + "\t" + str(lng) + "\t" + str(lat) + "\n")
    sleep(0.05)
    
address_file.close()
