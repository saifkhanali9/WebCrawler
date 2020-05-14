# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import time
from ..items import GetdataItem

proxies = {
    'http': 'http://proxy1.internal.vipfy.store:8888',
    'https': 'http://proxy1.internal.vipfy.store:8888',
}

tempArray = []
# with open(r'C:\Saif\Office\WebCrawler\trustPilot\Files\allSoftwareUrls.json') as f:
#     d = json.load(f)
#     for i in d:
#         tempArray = tempArray + i['urls']
# urlTempArray = []
# for i in tempArray:
#     if i not in urlTempArray:
#         urlTempArray.append(i)
# urlTempArray = ["https://www.trustpilot.com//review/biketowleash.com,,,,,cats_dogs",
#                 "https://www.trustpilot.com//review/dogwatchsepa.com,,,,,cats_dogs"]
fileNo = 4

path = r'C:\Saif\Office\Python Projects\Crawler\trustpilot\getData\urlList\urlFile'
# print("\n\n\n\n\n\n, "\n\n\n\n\n\n")
urlTempArray = []
f = open(path + str(fileNo) + '.txt', 'r')
urlTempArray = f.readlines()
urlTempArray = [w.replace('\n', '') for w in urlTempArray]
# Separating url and category
urlArray = []
catArray = []
f.close()
# print(urlTempArray[0])
for i in urlTempArray:
    temp = i.split(',,,,,')
    urlArray.append(temp[0])
    catArray.append(temp[1])


class GetdataSpider(scrapy.Spider):
    skipChecker = 0
    nextPage = 'temp'
    title = ''
    mainRating = ''
    noOfReviews = ''
    webSite = ''
    isClaimed = ''
    claimedDate = ''
    categories = ''
    email = ''
    phone = ''
    country = ''
    address = ''
    descriptionText = ''
    consumersStars = []
    consumersStarsDescription = []
    consumersReviewsSummary = []
    consumersReviewsDetail = []
    consumersName = []
    consumersUserId = []
    consumersUserIdLink = []
    reviewCounter = 0
    index = 0
    innerPage = 1
    firstReviewCheck = 0
    name = 'getdata'
    start_urls = [urlArray[0]]

    def parse(self, response):

        # print('length: ', GetdataSpider.nextPage)
        if GetdataSpider.reviewCounter == 0:
            mainRating = response.css('.header--inline::text').extract()
            title = response.css('.multi-size-header__big::text').extract()
            mainRating = mainRating[0].split('\n')
            noOfReviews = mainRating[1].replace(' ', '')
            mainRating = mainRating[-1].replace(' ', '')
            GetdataSpider.title = title[0]
            GetdataSpider.mainRating = mainRating
            GetdataSpider.noOfReviews = noOfReviews

            businessId = response.css('.review-list').extract()
            # businessId = businessId[0].split('$businessUnitId = \'')

            if '$businessUnitId = \'' in businessId[0]:
                businessId = businessId[0].split('$businessUnitId = \'')
                businessId = businessId[1].split('\'')
                businessId = businessId[0]
                urlActivityBox = 'https://www.trustpilot.com/businessunit/' + businessId + '/activitybox'
                urlCompanyInfoBox = 'https://www.trustpilot.com/businessunit/' + businessId + '/companyinfobox'
                # urlFacebook = 'https://www.trustpilot.com/businessunit/' + businessId + '/facebookbox'

                # Activity Box
                requestUrl = requests.get(urlActivityBox, proxies)
                requestJson = json.loads(requestUrl.text)
                webSite = requestJson['businessUnitIdentifyingName']
                isClaimed = requestJson['isClaimed']
                claimedDate = requestJson['claimedDate']

                # Company Info Box
                requestUrl = requests.get(urlCompanyInfoBox, proxies)
                requestJson = json.loads(requestUrl.text)
                categories = requestJson['categories'][0]['breadcrumb']['localizedName']
                email = requestJson['contact']['email']
                phone = requestJson['contact']['phone']
                country = requestJson['businessUnitCountry']
                address = requestJson['contact']['address']
                descriptionText = requestJson['descriptionText']
                GetdataSpider.webSite = webSite
                GetdataSpider.isClaimed = isClaimed
                GetdataSpider.claimedDate = claimedDate
                GetdataSpider.categories = categories
                GetdataSpider.email = email
                GetdataSpider.phone = phone
                GetdataSpider.country = country
                GetdataSpider.address = address
                GetdataSpider.descriptionText = descriptionText
            else:
                GetdataSpider.webSite = ''
                GetdataSpider.isClaimed = ''
                GetdataSpider.claimedDate = ''
                GetdataSpider.categories = ''
                GetdataSpider.email = ''
                GetdataSpider.phone = ''
                GetdataSpider.country = ''
                GetdataSpider.address = ''
                GetdataSpider.descriptionText = ''
            GetdataSpider.reviewCounter = 1
        else:
            GetdataSpider.firstReviewCheck = 1

            getAllData = response.css('.review').extract()

            # Remove Spam
            # print(len(getAllData))
            thing = 'data-review-is-reported=\"true\"'
            spamCounter = 0
            while spamCounter < len(getAllData):
                if thing in getAllData[spamCounter]:
                    getAllData.pop(spamCounter)
                else:
                    spamCounter += 1

            # Extracting fields
            for i in getAllData:

                # ConsumerId
                consumerId = i.split('consumerId\":\"')
                consumerId = consumerId[1].split('\"')
                GetdataSpider.consumersUserId.append(consumerId[0])

                # UserID Link
                userIdLink = 'https://www.trustpilot.com/users/' + consumerId[0]
                GetdataSpider.consumersUserIdLink.append(userIdLink)

                # Name
                consumerName = i.split('consumerName\":\"')
                consumerName = consumerName[1].split('\"')
                GetdataSpider.consumersName.append(consumerName[0])

                # Stars
                stars = i.split('stars\":')
                stars = stars[1].split('}')
                GetdataSpider.consumersStars.append(stars[0])
                #
                # Stars Description
                if stars[0] == '1':
                    starsDescription = i.split('star: ')
                else:
                    starsDescription = i.split('stars: ')
                starsDescription = starsDescription[1].split('\"')
                GetdataSpider.consumersStarsDescription.append(starsDescription[0])

                # Review Summary
                if "review-title" in i:
                    reviewsSummary = i.split('review-title')
                    reviewsSummary = reviewsSummary[1].split(r'}">')

                    reviewsSummary = reviewsSummary[1].split(r'</a')
                    GetdataSpider.consumersReviewsSummary.append(reviewsSummary[0])
                else:
                    GetdataSpider.consumersReviewsSummary.append("")

                # Reviews Detail
                if 'review-content__text\">' in i:
                    reviewsDetail = i.split('review-content__text\">')
                    reviewsDetail = reviewsDetail[1].split('</p>')
                    tempReviewsDetail = reviewsDetail[0].replace('\n', '')
                    tempReviewsDetail = tempReviewsDetail.replace('  ', '')
                    tempReviewsDetail = tempReviewsDetail.replace('<br>', '')
                    GetdataSpider.consumersReviewsDetail.append(tempReviewsDetail)
                else:
                    GetdataSpider.consumersReviewsDetail.append("")

            GetdataSpider.nextPage = response.css('.next-page').extract()
            GetdataSpider.innerPage += 1
            if len(GetdataSpider.nextPage) > 0:
                nextpages = urlArray[GetdataSpider.index] + '?page=' + str(
                    GetdataSpider.innerPage)
                print("\n\nForest:\n", GetdataSpider.reviewCounter, nextpages, ",\n\n")
                print("\n\nIndex", GetdataSpider.index, "\nTotal Length:", len(urlArray), '\n', "File: ", fileNo,
                      '.txt\nskipChecker:', GetdataSpider.skipChecker, '\n')
                arraytostop = 200
                # if '?page=200' in nextpages or '?page=300' in nextpages or '?page=450' in nextpages or '?page=600' in nextpages or '?page=750' in nextpages:
                if GetdataSpider.skipChecker == arraytostop:
                    GetdataSpider.skipChecker = 0
                    time.sleep(120)
                GetdataSpider.skipChecker += 1
                yield response.follow(nextpages, callback=self.parse)
            else:
                yield {
                    'title': GetdataSpider.title,
                    'category': GetdataSpider.categories,
                    'mainRating': GetdataSpider.mainRating,
                    'noOfReviews': GetdataSpider.noOfReviews,
                    'webSite': GetdataSpider.webSite,
                    'categories': GetdataSpider.categories,
                    'descriptionText': GetdataSpider.descriptionText,
                    'email': GetdataSpider.email,
                    'phone': GetdataSpider.phone,
                    'country': GetdataSpider.country,
                    'address': GetdataSpider.address,
                    'isClaimed': GetdataSpider.isClaimed,
                    'claimedDate': GetdataSpider.claimedDate,
                    'reviews': [{
                        'comsumerName': GetdataSpider.consumersName[i],
                        'comsumerUserId': GetdataSpider.consumersUserId[i],
                        'consumerUserIdLink': GetdataSpider.consumersUserIdLink[i],
                        'comsumerStars': GetdataSpider.consumersStars[i],
                        'comsumerReviewSummary': GetdataSpider.consumersReviewsSummary[i],
                        'comsumerReviewDetail': GetdataSpider.consumersReviewsDetail[i]
                    } for i in range(len(GetdataSpider.consumersName))]
                }

                # Deleting the old
                GetdataSpider.title = ''
                GetdataSpider.mainRating = ''
                GetdataSpider.consumersStars = []
                GetdataSpider.consumersStarsDescription = []
                GetdataSpider.consumersReviewsSummary = []
                GetdataSpider.consumersReviewsDetail = []
                GetdataSpider.consumersName = []
                GetdataSpider.consumersUserId = []
                GetdataSpider.consumersUserIdLink = []
                GetdataSpider.innerPage = 1
                GetdataSpider.reviewCounter = 0
                # Next URL
                if GetdataSpider.index < len(urlArray) - 1:
                    # GetdataSpider.skipChecker = 0
                    GetdataSpider.index += 1
                    yield response.follow(urlArray[GetdataSpider.index], callback=self.parse)
        if GetdataSpider.reviewCounter == 1 and GetdataSpider.index < len(urlArray):
            GetdataSpider.reviewCounter = 2
            print("Next page", urlArray[GetdataSpider.index])
            # time.sleep(4)
            yield response.follow(urlArray[GetdataSpider.index], callback=self.parse)
