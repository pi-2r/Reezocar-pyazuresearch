#!/usr/bin/env python2
## -*- coding: utf-8 -*-
from datetime import datetime
from logging import getLogger
import httplib2
import requests
import json
import os
import simplejson as json 
from simplejson import JSONDecodeError

class AzureSearch(object):

        def __init__(self, serviceName, version, apiKey):
			self.serviceName = serviceName
			self.version = version
			self.apiKey = apiKey
			self.logger = getLogger('pyazuresearch')
			self.session = requests.session()
			self.http = httplib2.Http('.cache')
			self.headers = {'Content-type': 'application/json',
				'api-key': self.apiKey,
				'Host': self.serviceName + '.search.windows.net',
				'cache-control':'no-cache'}

        ## Define Url
        def geturl(self, index=None):
                if index is not None:
                        return 'https://' + self.serviceName + '.search.windows.net/indexes/' + index
                else:
                        return 'https://' + self.serviceName + '.search.windows.net/indexes/'
        def searchbyurl(self, index, query):
            return "https://" + self.serviceName + '.search.windows.net/indexes/' + index + "/docs?" + query + "&" + self.version

        ## Manage url
        def manageurl(self, subscriptionId, resourceGroupName, serviceName):
            return "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + resourceGroupName + "/providers/Microsoft.Search/searchServices/" + serviceName + "?" + self.version
       	
       	def manageadminkey(self, subscriptionId, resourceGroupName, serviceName):
            return "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + resourceGroupName + "/providers/Microsoft.Search/searchServices/" + serviceName + "/listAdminKeys?" + self.version
 
        def managecreatkey(self, subscriptionId, resourceGroupName, name):
            return "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + resourceGroupName + "/providers/Microsoft.Search/searchServices/" + self.serviceName + "/createQueryKey/" + name + "?" + self.version

        def managelistQueryKeys(self, subscriptionId, resourceGroupName):
            return "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + resourceGroupName + "/providers/Microsoft.Search/searchServices/" + self.serviceName + "/listQueryKeys?" + self.version 
        
        def managedeleteQuery(self, subscriptionId, resourceGroupName, key):
			return "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + resourceGroupName + "/providers/Microsoft.Search/searchServices/" + self.serviceName + "/deleteQueryKey/" + key + "?" + self.version    	

        def manageregenerateadminkey(self, subscriptionId, resourceGroupName, serviceName, regenerateKey):
                return "https://management.azure.com/subscriptions/" + subscriptionId + "/resourceGroups/" + resourceGroupName + "/providers/Microsoft.Search/searchServices/" + serviceName + "/regenerateAdminKey/" + regenerateKey + "?" + self.version    	



        ## Actions 
        def _send_request(self, url, methode, body=None):
            try:
                print url
                response, content  = self.http.request(url, methode, headers=self.headers, body=body)
            except Exception as e:
                """
                more information about HTTPException
                https://docs.python.org/2/library/httplib.html#httplib.HTTPException
                """
                print "[-] HTTP error: ", e
                exit(-1)
            print response, content

        ## Json actions
        def encode_json(self, value):
                try:
                        json_dump = json.dumps(value)
                except TypeError:
                        print("Unable to serialize the object")
                return json_dump

        def decode_json(self, value):
                try:
                        json_response = response.json()
                except JSONDecodeError:
                         print ('Decoding JSON has failed')
                return json_response
                
        def dateToday(self):
            d = datetime.now()
            now = str(d.year)+"-"+str(d.month)+"-"+str(d.day)+"T"+str(d.hour)+":"+str(d.minute)+":"+str(d.second)+"Z"
            return now



        ## Index operations              
        def createindex(self, indexname, body):
        	"""
        	You can create a new index within an Azure Search service using an 
        	HTTP POST or PUT request. The body of the request is a JSON schema 
        	that specifies the index name, fields, attributes to control query 
        	behavior, scoring profiles for custom scoring, and CORS options to 
        	support cross-origin queries.

        	arg indexname: The name of the index to which to add the document
        	arg body:  An iterable of Python mapping objects, convertible to JSON,
                representing documents to index
        	"""
                value = self.encode_json(body)
                url = self.geturl() + "?" + self.version
                self._send_request(url, "POST", value)

        def deleteindex(self, indexname):
        	"""
        	The Delete Index operation removes an index and associated documents 
        	from your Azure Search service. You can get the index name from the 
        	service dashboard in the Azure Preview portal, or from the API. 
        	See List Indexes (Azure Search API: http://msdn.microsoft.com/en-us/library/azure/dn832688.aspx) for details.
        	"""
                url = self.geturl(indexname) + '?' + self.version
                self._send_request(url, "DELETE")


    	def getindex(self, index):
                """
    		The Get Index operation gets the index definition from Azure Search.
    		"""
                url = self.geturl(index) + '?' + self.version
                self._send_request(url, "GET")

        def updateindex(self, indexname, body):
                """
                You can update an existing index within Azure Search using an HTTP PUT 
                request. In the Public Preview, valid update operations include adding 
                new fields to the existing schema, modifying CORS options, and modifying 
                scoring profiles (see Add scoring profiles to a search index (Azure Search API)).
                """
                value = self.encode_json(body)
                url = self.geturl(indexname) + "?" + self.version
                self._send_request(url, "PUT", value)
    			
        def listindexes(self, name=None):
        	"""
        	The List Indexes operation returns a list of the indexes currently 
        	in your Azure Search service.
        	"""
                url = self.geturl() + "?" + self.version 
                if name is not None:
                	url += '&$select=' + name
                self._send_request(url, "GET")

        def stats(self, indexname):
        	"""
        	The Get Index Statistics operation returns from Azure Search a document
        	count for the current index, plus storage usage.
        	"""
                url = self.geturl(indexname) + "/stats?" + self.version
                self._send_request(url, "GET")




    ## Document Operations
        def usedocument(self, indexname, body):
                """
                You can upload, merge or delete documents from a specified index using 
                HTTP POST. For large numbers of updates, batching of documents (up to 
                1000 documents per batch, or about 16 MB per batch) is recommended.
                """
                value = self.encode_json(body)
                url = self.geturl(indexname) + "/docs/index?" + self.version
                self._send_request(url, "POST", value)
                
    ##Search Documents
        def simplesearch(self, indexname, string):
                query = "search=" + string
                url =  self.searchbyurl(indexname, query)
                self._send_request(url, "GET") 





	## Index Admin API
        def count(self, indexname=None):
                """
                The Count Documents operation retrieves a count of the number of documents
                in a search index. The $count syntax is part of the OData protocol.
                """
                url = self.geturl(indexname) + '/docs/$count?api-version=2014-07-31-Preview'
                self._send_request(url, "GET")

        def createSearchService(self, subscriptionId, resourceGroupName, serviceName, body):
                """
                The Create Search Service operation provisions a new Search service with the specified 
                parameters. This API can also be used to update an existing service definition.

				arg subscriptionId: The subscriptionID for the Azure user. You can obtain this value from the Azure 
                                    Resource Manager API or the portal.           
                arg resourceGroupName: The name of the resource group within the user’s subscription. You can obtain 
                                       this value from the Azure Resource Manager API or the portal.
                arg serviceName: The name of the search service within the specified resource group. Service names must only 
                				 contain lowercase letters, digits or dashes, cannot use dash as the first two or last one 
                				 characters, cannot contain consecutive dashes, and must be between 2 and 15 characters in length. 
                				 Since all names end up being <name>.search.windows.net, service names must be globally unique. 
                				 No two services either within or across subscriptions and resource groups can have the same name. 
                				 You cannot change the service name after it is created.
                arg body: request body                      
                """
                value = self.encode_json(body)
                url = self.manageurl(subscriptionId, resourceGroupName, serviceName)
                self._send_request(url, "PUT", value)

        def listAdminKeys(self, subscriptionId, resourceGroupName, serviceName):
                """
                The List Admin Keys operation returns the primary and secondary admin keys for the specified
                Search service. The POST method is used because this action returns read-write keys.

                arg subscriptionId: The subscriptionID for the Azure user. You can obtain this value from the Azure 
                                    Resource Manager API or the portal.
                arg resourceGroupName: The name of the resource group within the user’s subscription. You can obtain 
                                       this value from the Azure Resource Manager API or the portal.
                """
                url = self.manageadminkey(subscriptionId, resourceGroupName, serviceName)
                self._send_request(url, "POST")

        def getSearchService(self, subscriptionId, resourceGroupName, serviceName):
                """
                The Get Search Service operation returns the properties for the specified Search service. Note 
                that admin keys are not returned. Use the List Admin Keys (Azure Search API) to retrieve the admin keys.

                arg subscriptionId: The subscriptionID for the Azure user. You can obtain this value from the Azure 
                                    Resource Manager API or the portal.
                arg resourceGroupName: The name of the resource group within the user’s subscription. You can obtain 
                                       this value from the Azure Resource Manager API or the portal.
                arg serviceName: The name of the search service within the specified resource group. If you don't 
                				 know the service name, you can obtain a list using List Search Services 
                				 (Azure Search API: http://msdn.microsoft.com/en-us/library/azure/dn832688.aspx).
                """
                url = self.manageurl(subscriptionId, resourceGroupName, serviceName)
                print url
                self._send_request(url, "GET")

        def createQueryKey(self, subscriptionId, resourceGroupName, name):
                """
                The Create Query Key operation generates a new query key for the Search service. 
                You can create up to 50 query keys per service.

                arg subscriptionId: The subscriptionID for the Azure user. You can obtain this value from the Azure 
                                    Resource Manager API or the portal.
                arg resourceGroupName: The name of the resource group within the user’s subscription. You can obtain 
                                       this value from the Azure Resource Manager API or the portal.
                arg name: The name of new key.
                """
                url = self.managecreatkey(subscriptionId, resourceGroupName, name)
                self._send_request(url, "POST")

        def listQueryKeys(self, subscriptionId, resourceGroupName):
                """
                The List Query Keys operation returns the query keys for the specified Search service. Query keys 
                are used to send query API (read-only) calls to a Search service. There can be up to 50 query keys per service.
                
                arg subscriptionId: The subscriptionID for the Azure user. You can obtain this value from the Azure 
                                    Resource Manager API or the portal.
                arg resourceGroupName: The name of the resource group within the user’s subscription. You can obtain 
                                       this value from the Azure Resource Manager API or the portal.
                """
                url = self.managelistQueryKeys(subscriptionId, resourceGroupName)
                self._send_request(url, "GET")

        def deleteSearchService(self, subscriptionId, resourceGroupName, serviceName):
        	"""
        	The Delete Search Service operation deletes the Search service and search data, including all indexes and 
        	documents.
        	
        	arg subscriptionId: The subscriptionID for the Azure user. You can obtain this value from the Azure 
        						Resource Manager API or the portal.
        	arg resourceGroupName: The name of the resource group within the user’s subscription. You can obtain 
        						   this value from the Azure Resource Manager API or the portal.
        	arg serviceName: The name of the search service within the specified resource group. If you don't 
                		     know the service name, you can obtain a list using List Search Services 
                			 (Azure Search API: http://msdn.microsoft.com/en-us/library/azure/dn832688.aspx).					
        	"""
        	url = self.manageurl(subscriptionId, resourceGroupName, serviceName)
        	self._send_request(url, "DELETE")

        def regenerateAdminKey(self, subscriptionId, resourceGroupName, serviceName, regenerateKey):
        	"""
        	The Regenerate Admin Keys operation deletes and regenerates either the primary or secondary key. 
        	You can only regenerate one key at a time. When regenerating keys, consider how you will maintain 
        	access to the service. A secondary key exists so that you have a key available when rolling over 
        	the primary key. Every service always has both keys. You can regenerate keys, but you cannot delete 
        	them or run a service without them.

        	arg subscriptionId: The subscriptionID for the Azure user. You can obtain this value from the Azure 
        						Resource Manager API or the portal.
        	arg resourceGroupName: The name of the resource group within the user’s subscription. You can obtain 
        						   this value from the Azure Resource Manager API or the portal.
        	arg serviceName: The name of the search service within the specified resource group. If you don't 
                		     know the service name, you can obtain a list using List Search Services 
                			 (Azure Search API: http://msdn.microsoft.com/en-us/library/azure/dn832688.aspx).
            arg regenerateKey: This action specifies that the primary or secondary admin key will be regenerated.
        	"""
        	url = self.manageregenerateadminkey(subscriptionId, resourceGroupName, serviceName, regenerateKey)
        	self._send_request(url, "POST")

        def updateSearchService(self, subscriptionId, resourceGroupName, serviceName, body):
        	"""
        	The Update Service operation changes Search service configuration. Valid changes include changing the tags, 
        	partition, or replica count, which adds or removes search units to your service as a billable event. If you 
        	try to decrease partitions below the amount needed to store the existing search corpus, an error will occur, 
        	blocking the operation. Changes to service topology can take a while. It takes time to relocate data, as well 
        	as setting up or tearing down clusters in the data center.
			Note that you cannot change the name, location, and sku. Changing any of these properties will require that
			you create a new service.

			arg subscriptionId: The subscriptionID for the Azure user. You can obtain this value from the Azure 
        						Resource Manager API or the portal.
        	arg resourceGroupName: The name of the resource group within the user’s subscription. You can obtain 
        						   this value from the Azure Resource Manager API or the portal.
        	arg serviceName: The name of the search service within the specified resource group. If you don't 
                		     know the service name, you can obtain a list using List Search Services 
                			 (Azure Search API: http://msdn.microsoft.com/en-us/library/azure/dn832688.aspx).
            arg body: request body
        	"""
        	value = self.encode_json(body)
                url = self.manageurl(subscriptionId, resourceGroupName, serviceName)
                self._send_request(url, "PUT", value)


        def deleteQueryKey(self, subscriptionId, resourceGroupName, key):
        	"""
        	The Delete Query Key operation deletes the specified query key. Query keys are optional and used for 
        	read-only queries.

        	arg subscriptionId: The subscriptionID for the Azure user. You can obtain this value from the Azure 
        						Resource Manager API or the portal.
        	arg resourceGroupName: The name of the resource group within the user’s subscription. You can obtain 
        						   this value from the Azure Resource Manager API or the portal.
        	arg key: The key to be deleted.
        	"""
                url = self.managedeleteQuery(subscriptionId, resourceGroupName, key)
                print url
                self._send_request(url, "DELETE")

