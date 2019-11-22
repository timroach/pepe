import sys
import os
import requests
from bs4 import BeautifulSoup as bs

class pagescraper:
    def __init__(self, targetfolder):
        self.targetfolder = "scrapedImages/" + targetfolder
        if not os.path.isdir("scrapedImages"):
            try:
                os.mkdir("scrapedImages")
            except OSError:
                print("Could not create scrapedImages directory, exiting.")
                sys.exit()
            else:
                print("Created directory scrapedImages")
        if not os.path.isdir(self.targetfolder):
            try:
                os.mkdir(self.targetfolder)
            except OSError:
                print("Error creating directory " + self.targetfolder)
            else:
                print("Created directory " + self.targetfolder)

    def saveimage(self, image, name):
        with open(self.targetfolder + "/" + name, "wb") as file:
            file.write(image)

    def scrapeimgurgallery(self, url):
        print("Scraping page " + url + " into folder " + self.targetfolder)
        counter = 0
        unsuccessful = 0
        failed = []
        reqresult = requests.get(url)
        if reqresult.status_code == 200:
            soup = bs(reqresult.content, "html.parser")
            imgiddivs = soup.findAll('div',{'class':['post-image-container post-image-container--spacer','post-image-container']})
            #testdiv = imgiddivs[1].attrs['id']
            imgids = []
            for div in imgiddivs:
                id = div.attrs['id']
                imgids.append(id)
            imgurls = []
            for id in imgids:
                imgurl = "http://imgur.com/" + id
                imgurls.append([imgurl, id])
            for imgurl in imgurls:
                imagepage = requests.get(imgurl[0])
                if imagepage and imagepage.status_code == 200:
                    imgsoup = bs(imagepage.content, features="html.parser")
                    imagetag = imgsoup.find('link', {'rel':'image_src'})
                    if imagetag:
                        imagelinktext = imagetag.attrs['href']
                        image = requests.get(imagelinktext)
                        if image.status_code == 200:
                            imgnameparts = image.url.split('/')
                            print("Scraping image " + str(counter) +" : " + imgnameparts[-1])
                            self.saveimage(image.content, imgnameparts[-1])
                            counter += 1
                    else:
                        unsuccessful += 1
                        failed.append(imgurl)
            print("Scraped " + str(counter) + " images, " + str(unsuccessful) + " not scraped:")
            for item in failed:
                print(item)
            return imgurls

    def scrapestickerpack(self, url):
        print("Scraping page " + url + " into folder " + self.targetfolder)
        counter = 0
        unsuccessful = 0
        imgurls = []
        failed = []
        reqresult = requests.get(url)
        if reqresult.status_code == 200:
            soup = bs(reqresult.content, "html.parser")
            imgdivs = soup.findAll('div',{'class':'md-avatar md-large-sticker md-theme-default'})
            for div in imgdivs:
                imgurl = div.contents[0].attrs['src']
                image = requests.get(imgurl)
                if image.status_code == 200:
                    imgnameparts = image.url.split('/')
                    print("Scraping image " + str(counter) + " : " + imgnameparts[-1])
                    self.saveimage(image.content, imgnameparts[-1])
                    counter += 1
                    imgurls.append(imgurl)
                else:
                    unsuccessful += 1
                    failed.append(imgurl)
        print("Scraped " + str(counter) + " images, " + str(unsuccessful) + " not scraped:")
        for item in failed:
            print(item)




def main():

    # Imgur section --------------------------------------
    alreadyscraped = ['SU4Qa',
                      'qzDNO',
                      'xpcl7',
                      'Bhh4d',
                      'XLElq',
                      'KmTN2',
                      'v06uS',
                      'UiFkr',
                      'yNZ7r',
                      'MarCX',
                      'ytyyY',
                      'L7X7u',
                      'tX27h'
                      ]
    # imgur gallery IDs to scrape, format as in list above
    gallerylist = [
                   ]
    # Scrape imgur galleries into scrapedImages folder
    for gallery in gallerylist:
        url = 'https://imgur.com/gallery/' + gallery
        imgurscrape = pagescraper(gallery)
        imgurscrape.scrapeimgurgallery(url)

    # stickers.cloud section -------------------------------
    alreadyscrapedpacks = ['fighting-pepe']
    packlist = ['pepe-fighting-hkg2',
                'random-pepe',
                'pepe-25',
                'pepe-smoke',
                'pepe-think',
                '叉雞飯呀dllm',
                'pepe-30',
                'cute-pepe']

    for pack in packlist:
        url = 'https://stickers.cloud/pack/' + pack
        stickerscrape = pagescraper(pack)
        stickerscrape.scrapestickerpack(url)
    sys.exit()


if __name__ == '__main__':
    main()
