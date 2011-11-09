from imageData import ImageData
from linksDataParser import LinksDataParser
class ImageDataParser : 
   def getImage(self,dict):
       if('image' in dict):
           image_dict = dict["image"]
           image=ImageData()
           
           if('id' in image_dict):
               image.id=image_dict['id']
           if('links' in image_dict):
               image.links = LinksDataParser().getLinks(image_dict)
           return image      
             
               
           
