# What the Bee

Often known as the great pollinators, bees are part of the biodiversity on which we all depend for our survival. Additionally, bees have an important part to play in maintaining our planet. We need them to pollinate the food we need to survive and many of the trees and flowers that provide habitats for lots of other wildlife. 

This project aims at raising the educational awareness around the importance of bees to our planet. This image classification tool allows users to upload an image of a bee and get its species name, as of currently it only can identify 2 types of bee species - Apis mellifera ( the common honey bee ) and Bombus Affinis ( The common Bumble Bee). The project is still in its early stages and there are plans to further expand it to allow for more information about Bees to be displayed. 


## Aquiring the data

Unfortunately, there are very little bee image datasets readily available on the internet. Hence, there was a need to create one. The images were scrapped off of a informative website called beespotter ( https://beespotter.org ). The bee images were scrapped from this website using the following code : 

```python
def get_images(initialUrl,pagedUrl,folderName, pageLimit):
  
  try:
    os.mkdir(os.path.join(os.getcwd(),folderName))
  except :
    print("File not made")

  os.chdir(os.path.join(os.getcwd(),folderName))
  r = requests.get(initialUrl)
  soup = bs(r.text,'html.parser')

  images = soup.select('a.gallery-item')

  links = [i.get("href") for i in images]
  countApis =1
  for l in links:
     with open(folderName + str(countApis) + '.jpg','wb') as f:
         im=requests.get(l)
         f.write(im.content)
     countApis+=1
     time.sleep(0.2)

 for i in range(2,pageLimit):
     r=requests.get(pagedUrl+str(i))
     soup=bs(r.text,'html.parser')
     images= soup.select('a.gallery-item')
     links= [i.get('href') for i in images]
     for l in links:
         with open(folderName + str(countApis) + '.jpg','wb') as f:
             im = requests.get(l)
             f.write(im.content)
         countApis+=1
         time.sleep(0.2)

 os.chdir('..')

```

Below are some some of the scrapped images : 

<figure>
  <figcaption><b>Apis mellifera</b></figcaption>
  <img
  src="https://beespotter.org/beedata/bees/109-6.jpg"
  alt="Apis-melli">
</figure>

<figure>
  <figcaption><b>Bombus Affinis</b></figcaption>
  <img
  src="https://beespotter.org/beedata/bees/1324-11.jpg"
  alt="Apis-melli">
</figure>

More than 7000 images were downloaded - 7219 remained after cleaning the data.

## Cleaning the data

There were not many issues with the images except for some of them being corrupt. To manually look through 7000+ images would take a pain stakingly long time and therefore, a script was created to find any corrupted images. 

```python
import os
from os import listdir
from PIL import Image

def find_bad_images(folderName):
  
  count=0
  for fileName in os.listdir(f'C:\\Users\\jjoan\\Desktop\\BeeCode\\BeeImages\\{folderName}'):
      if fileName.endswith('.jpg'):
          try:
              im = Image.open('C:\\Users\\jjoan\\Desktop\\BeeCode\\BeeImages\\Bombus vagans\\'+fileName)
              im.verify() 
              im.close() 
              im = Image.open('C:\\Users\\jjoan\\Desktop\\BeeCode\\BeeImages\\Bombus vagans\\'+fileName)
              im.transpose(Image.FLIP_LEFT_RIGHT)
              im.close()
          except(IOError,SyntaxError)as e:
              count+=1
              print('Bad file  :  '+fileName)


  print(' Number of bad images : ', count)

```
