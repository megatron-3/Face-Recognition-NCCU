from bs4 import BeautifulSoup
import requests
import re
from urllib.request import Request, urlopen
import os
import json

def get_soup(url, header):
    return BeautifulSoup(urlopen(Request(url, headers=header)), 'html.parser')

# Ask the query to find the images from internet
query = input("query image : ")

image_type="Image"
query= query.split()
query='+'.join(query)

# Ask the Address where the image will be stored
ImageType = input ("Image Type : ")

url="https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
print (url)

#add the directory for your image here
DIR="Images/TestingImages/ImageType" + ImageType

header={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url, header)

# contains the link for Large original images, type of  image
ActualImages=[]

for a in soup.find_all("div",{"class":"rg_meta"}):
    link, Type =json.loads(a.text)["ou"], json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print ("there are total", len(ActualImages), "images")

# Saving the images in the specified Place
for i, (img, Type) in enumerate (ActualImages):
    try :
        req = Request (img, headers = {'User-Agent': 'Mozilla/5.0'})
        raw_img = urlopen (req).read()

        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
        
        print (cntr)
        
        if len(Type) == 0 or Type == 'jpg' :
            f = open(os.path.join(DIR , image_type + str(cntr)+".jpg"), 'wb')
        else :
            continue
        
        f.write (raw_img)    

    except Exception as e :
            print (e)
