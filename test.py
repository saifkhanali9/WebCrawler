# -*- coding: utf-8 -*-
import json
import math

# proxies = {
#     'http': 'http://proxy1.internal.vipfy.store:8888',
#     'https': 'http://proxy1.internal.vipfy.store:8888',
# }

tempArray = []
with open(r'C:\Saif\Office\WebCrawler\trustPilot\Files\allSoftwareUrls.json') as f:
    d = json.load(f)
    for i in d:
        tempArray = tempArray + i['urls']
urlTempArray = []

for i in tempArray:
    if i not in urlTempArray:
        urlTempArray.append(i)

# path = r'C:\Saif\Office\Python Projects\Crawler\trustpilot\getData\urlList\urlFile'
count = 1
i = 0
# for j in range(211):
#     if j == 0:
#         i = 0
#     else:
#         i = j * 17
#     f = open(path + str(j + 1) + '.txt', 'a+')
#     for k in range(i, i + 17):
#         if k == i+16:
#             f.write(urlTempArray[k])
#         else:
#             f.write(urlTempArray[k] + '\n')
#     f.close()
path = r'C:\Saif\Office\Python Projects\Crawler\trustpilot\getData\urlList\urlFile'
# urlTempArray = []
f = open(path + '1.txt', 'r')
urlTempArray = f.readlines()
urlTempArray = [w.replace('\n', '') for w in urlTempArray]
print(urlTempArray)
