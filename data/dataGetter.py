from time import sleep
from random import randint
from urllib.request import urlopen
from bs4 import BeautifulSoup as bf


def getDataFromUrl(url):
    html = urlopen(url)
    obj = bf(html.read(), "html.parser")
    table = obj.find("table")
    items = table.find_all("tr")
    datas = []
    for item in items:
        information = item.find_all("td")
        datas.append(
            [i.get_text() for i in information]
        )  # arranges the single data into a list
    return datas[1:]


def saveData(data, count):
    with open("data.txt", "a") as f:
        for i in data:
            f.write(str(count) + "\t")
            f.write("\t".join(i))
            f.write("\n")


def getDatas(count):
    print("Start to get data from url...")
    for i in range(count, 643):
        url = "https://fangjia.gotohui.com/house-3/{}.html".format(i)
        sleepTime = randint(3, 7)
        sleep(sleepTime)
        print(url, sleepTime)
        data = getDataFromUrl(url)
        saveData(data, i)


def loadDatas():
    datas = []
    f = open("data.txt", "r")
    for line in f:
        datas.append(line.split("\t")[1:-1])
    return datas


def processDatas(datas):
    count = len(datas)
    sum = 0
    distict = {}
    dict = {}
    for data in datas:
        sum += float(data[2])
        last = distict.get(data[0], [0, 0])
        distict[data[0]] = last[0] + 1, last[1] + float(data[2])
    for dist in distict:
        dict[dist] = distict[dist][1] / distict[dist][0]
    return sum / count, dict


# count = 0
# getDatas(count + 1)
datas = loadDatas()
avg, dict = processDatas(datas)
for key in dict:
    print(key, dict[key])
# print(str(processDatas(datas)),'k')
# print(datas[:10])
