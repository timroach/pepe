import sys
import os
import requests
from bs4 import BeautifulSoup as bs

class imgurscraper:
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

    def scrapegallery(self, url):
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
            print("Scraped " + str(counter) + "images, " + str(unsuccessful) + " not scraped:")
            for item in failed:
                print(item)
            return imgurls


def main():

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
        imgurscrape = imgurscraper(gallery)
        imgurscrape.scrapegallery(url)


    sys.exit()


if __name__ == '__main__':
    main()
