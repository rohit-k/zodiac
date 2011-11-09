from serverData import ServerData
from imageDataParser import ImageDataParser
from flavorDataParser import FlavorDataParser
from linksDataParser import LinksDataParser


class ServerDataParser : 
   def getServer(self,dict):
       if('server' in dict):
           server_dict = dict['server']
           server=ServerData()
           
           if('status' in server_dict):
               server.status=server_dict['status']
           
           if('hostId' in server_dict):
               server.hostId=server_dict['hostId']
           
           if('user_id' in server_dict):
               server.userId=server_dict['user_id']
           
           if('name' in server_dict):
               server.name=server_dict['name']
           
           if('tenant_id' in server_dict):
               server.tenantId=server_dict['tenant_id']
           
           if('adminPass' in server_dict):
               server.adminPass=server_dict['adminPass']
           
           if('uuid' in server_dict):
               server.uuid=server_dict['uuid']
           
           if('accessIPv4' in server_dict):
               server.accessIPv4=server_dict['accessIPv4']
            
           if('accessIPv6' in server_dict):
               server.accessIPv6=server_dict['accessIPv6']
           
           if('image' in server_dict):
               server.image=ImageDataParser().getImage(server_dict)
           
           if('links' in server_dict):
               server.links=LinksDataParser().getLinks(server_dict)
           
           if('updated' in server_dict):
               server.updatedDateTime=server_dict['updated']
           
           if('created' in server_dict):
               server.createdDateTime=server_dict['created']
               
           if('id' in server_dict):
               server.id=server_dict['id']
               
           if('flavor' in server_dict):
               server.flavor=FlavorDataParser().getFlavor(server_dict)
           return server