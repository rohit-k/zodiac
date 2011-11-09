from linkData import LinkData

class LinksDataParser : 
   def getLinks(self,dict):
       if('links' in dict):
           links_dict = dict["links"]
           links = []
           for link_dict in links_dict:
               links.append(LinkData(link_dict['href'],link_dict['rel']))
           return links
               
               
             
               
           
