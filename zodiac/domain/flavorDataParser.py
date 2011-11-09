from flavorData import FlavorData
from linksDataParser import LinksDataParser
class FlavorDataParser : 
   def getFlavor(self,dict):
       if('flavor' in dict):
           flavor_dict = dict['flavor']
           flavor=FlavorData()
           
           if('id' in flavor_dict):
               flavor.id=flavor_dict['id']
           if('links' in flavor_dict):
               flavor.links = LinksDataParser().getLinks(flavor_dict)
           return flavor

             
               
           
