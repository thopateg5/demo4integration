import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.documents as documents
import requests
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
import requests
from datetime import date
import os
import json

class DatabaseManagement():
	url = 'https://coedemo4.documents.azure.com:443/'
	key = 'OZ41MyknaZ5kZJgXpkqClPBo7AdxjrofDM490AR4biGfvgD0HiUf1ZBzMwQGT3yQKmlQwGr27n6Sf811bt7dRQ=='
	client = cosmos_client.CosmosClient(url, {'masterKey': key})
	DATABASE_ID = 'DeviceData'
	database_name = 'DeviceData'
	xms = '2016-07-11'
	x=0
	data_name = "ToDoList"
	containername = "DeviceData" #data_name + '_cont' 
	database = client.ReadDatabase("dbs/ToDoList")
		

	 

	def get_item(self,query,mydatabase,containername):  
		data = []	
		database_id = mydatabase['id']  
		for item in self.client.QueryItems("dbs/" + database_id + "/colls/" + containername ,query ,
								{'enableCrossPartitionQuery': True}):
			data.append(item)
		return (json.dumps(data,indent=True))

	def temp_greater_than(self,value):
	    min_val = str(value)
	    a = self.get_item('SELECT DeviceData.temperature, DeviceData.humidity,DeviceData.preasure   FROM DeviceData WHERE DeviceData.temperature>'+min_val  ,self.database, self.containername)
	    return (a)

		
	def temp_less_than(self,value):
	    min_val = str(value)
	    a = self.get_item('SELECT DeviceData.temperature, DeviceData.humidity,DeviceData.preasure   FROM DeviceData WHERE DeviceData.temperature<'+min_val ,self.database, self.containername)
	    return a
        #print(json.dumps(a, indent=True))


	def humidity_in_between(self,val_min,val_max):
	    min_val = str(val_min)
	    max_val = str(val_max)
	    a = self.get_item('SELECT DeviceData.temperature, DeviceData.humidity,DeviceData.preasure   FROM DeviceData WHERE DeviceData.humidity BETWEEN '+min_val+'  AND '+max_val ,self.database, self.containername)
	    return a
	      

	def between_time(self,val_min,val_max):
	    min_val = str(val_min)
	    max_val = str(val_max)
	    a = self.get_item('SELECT DeviceData.temperature, DeviceData.humidity,DeviceData.preasure   FROM DeviceData WHERE DeviceData.gateway_ts BETWEEN '+min_val+'  AND '+max_val ,self.database, self.containername)
	    print(a)
	      
	  
	def latest_data(self,value):
	    min_val = str(value)
	    a = self.get_item('SELECT top '+min_val+' DeviceData.temperature, DeviceData.humidity,DeviceData.preasure   FROM DeviceData order by DeviceData._ts desc',self.database, self.containername)
	    return a
	   
	def all_data(self,value):
	    min_val = str(value)
	    a = self.get_item('SELECT top '+min_val+' *   FROM DeviceData order by DeviceData._ts desc',self.database, self.containername)
	    print(a)
      
	      
	  
