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
              im = Image.open(f'C:\\Users\\jjoan\\Desktop\\BeeCode\\BeeImages\\{folderName}\\'+fileName)
              im.verify() 
              im.close() 
              im = Image.open(f'C:\\Users\\jjoan\\Desktop\\BeeCode\\BeeImages\\{folderName}\\'+fileName)
              im.transpose(Image.FLIP_LEFT_RIGHT)
              im.close()
          except(IOError,SyntaxError)as e:
              count+=1
              print('Bad file  :  '+fileName)


  print(' Number of bad images : ', count)

```

After removing all the corrupt images, the total images came down to 7219 images. With the data now ready to be processed, it was time to move on to initializing and training a model.

## Initializing and training the model 

In this section, I am just going to give a higher-level explanation of the process. If you would like to see the more technical code, it is available on my GitHub page. 

The images were trained on a convolutional neural network with the following architecture :

```
input_shape = (BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNELS)
n_classes = 2

model = models.Sequential([
    resize_rescale,
    data_augmentation,
    layers.Conv2D(32, kernel_size = (3,3), activation='relu', input_shape=input_shape),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64,  kernel_size = (3,3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64,  kernel_size = (3,3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(n_classes, activation='softmax'),
    
])

model.build(input_shape=input_shape)
```

The model was trained on 50 epochs and achieved the following scores on its final epoch :

Epoch 50/50
180/180 [==============================] - 300s 2s/step - loss: 0.2242 - accuracy: 0.9107 - val_loss: 0.2521 - val_accuracy: 0.8821

And below are the model's training and validation accuracy and its training and validation loss :

![1673477813447](https://user-images.githubusercontent.com/56068645/211942187-f3e031a5-5825-48fa-93f6-f4b241624155.png)

Overall, the model performed well and achieved what it set out to do. In the near future, the model will be further trained on more than 2 species and hopefully, we can expect similar results. 
