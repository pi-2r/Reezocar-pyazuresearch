#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import unittest
from pyazuresearch import *

serviceName = "reezocar"
apiversion = "api-version=2014-07-31-Preview"
apiKey = "0000000000000000000000000"
subscriptionId = "00000-0000-00000-0000"
resourceGroupName = "BizSpark"
indexname =  "annonces"
createindex = "demo"

ESAZ = AzureSearch(serviceName, apiversion, apiKey)


class TestAzureSearch(unittest.TestCase):
              	## Index operations
                def test_createindex(self):
                	createbody =  {
                                                "name": createindex,  
                                                "fields": [
                                                                {"name": "ref", "type": "Edm.String", "key": True},
                                                                {"name": "label", "type": "Edm.String" },
                                                                {"name": "brand", "type": "Edm.String" },
                                                                {"name": "model", "type": "Edm.String" },
                                                                {"name": "mileage", "type": "Edm.Int32" },
                                                                {"name": "title", "type": "Edm.String" },
                                                                {"name": "description", "type": "Edm.String", "suggestions": True},
                                                                {"name": "img_url", "type": "Edm.String", "searchable": False},
                                                                {"name": "year", "type": "Edm.Int32" },
                                                                {"name": "price", "type": "Edm.Int32" }]  
                                }
                        ESAZ.createindex(indexname, createbody)
                
                def test_getindex(self):
                				ESAZ.getindex(createindex)
                
                def test_updateindex(self):
                	updateindex = {
                                                "name": createindex,  
                                                "fields": [
                                                                {"name": "ref", "type": "Edm.String", "key": True},
                                                                {"name": "label", "type": "Edm.String" },
                                                                {"name": "brand", "type": "Edm.String" },
                                                                {"name": "model", "type": "Edm.String" },
                                                                {"name": "mileage", "type": "Edm.Int32" },
                                                                {"name": "title", "type": "Edm.String" },
                                                                {"name": "description", "type": "Edm.String", "suggestions": True},
                                                                {"name": "img_url", "type": "Edm.String", "searchable": False},
                                                                {"name": "year", "type": "Edm.Int32" },
                                                                {"name": "price", "type": "Edm.Int32" },
                                                                {"name" : "updateindex", "type": "Edm.String"}]  
                                }
                        ESAZ.updateindex(createindex, updateindex)
                def test_listindexes(self):
                	ESAZ.listindexes(createindex)
                '''
                def test_deleteindex(self):
                				ESAZ.deleteindex(createindex)
                '''
                def test_stats(self):
                                ESAZ.stats(createindex)

                ##Document operations
                def test_usedocument(self):
                	body = {"value": [{
                                "@search.action": "upload",
                                "ref": "1",
                                "label": "demo",
                                "brand" : "brand",
                                "model" : "model",
                                "mileage" : 5001,
                                "title" : "title",
                                "description" : "description",
                                "img_url" : "img_url",
                                "year" : 2014,
                                "price" : 501
                        		},
                                {
                                "@search.action": "upload",
                                "ref": "2",
                                "label": "demo2",
                                "brand" : "brand2",
                                "model" : "model2",
                                "mileage" : 50002,
                                "title" : "title2",
                                "description" : "description2",
                                "img_url" : "img_url2",
                                "year" : 2014,
                                "price" : 502
                                },
                                {
                                "@search.action": "upload",
                                "ref": "3",
                                "label": "demo3",
                                "brand" : "brand3",
                                "model" : "model3",
                                "mileage" : 50003,
                                "title" : "title3",
                                "description" : "description3",
                                "img_url" : "img_url3",
                                "year" : 2014,
                                "price" : 503
                                },
            			{
              			"@search.action": "delete",
              			"ref": "3"
            }]}
                        ESAZ.usedocument(createindex, body)
               
                def test_simplesearch(self):
                	search ="brand3"
                	ESAZ.simplesearch(createindex, search)
                
                ## Index Admin API
                def test_count(self):
                	ESAZ.count(createindex)

                def test_createSearchService(self):
                	body = { 
							   "location": "West US", 
							   "tags": {
							      "key": "value"
							      }, 
							   "properties": { 
							      "sku": { 
							      "name": "free | standard | standard2" 
							      }, 
							      "replicaCount": 1 | 2 | 3 | 4 | 5 | 6, 
							      "partitionCount": 1 | 2 | 3 | 4 | 6 | 12 
							   } 
							}
                	ESAZ.createSearchService(subscriptionId, resourceGroupName, serviceName, body)

                def test_listAdminKeys(self):
                	ESAZ.listAdminKeys(subscriptionId, resourceGroupName, serviceName)

                def test_getSearchService(self):
                	ESAZ.getSearchService(subscriptionId, resourceGroupName, serviceName)

                def test_createQueryKey(self):
                	name = "RZCtest"
                	ESAZ.createQueryKey(subscriptionId, resourceGroupName, name)

                def test_listQueryKeys(self):
                                ESAZ.listQueryKeys(subscriptionId, resourceGroupName)

                def test_deleteSearchService(self):
                	ESAZ.deleteSearchService(subscriptionId, resourceGroupName, serviceName)

                def test_regenerateAdminKey(self):
                	regenerateKey = "primary"
                	ESAZ.regenerateAdminKey(subscriptionId, resourceGroupName, serviceName, regenerateKey)

                def test_updateSearchService(self):
                	body = {
							   "tags": {
							      "key": "value"
							      }, 
							   "properties": 
							      {
							      "replicaCount": 1 | 2 | 3 | 4 | 5 | 6,
							      "partitionCount": 1 | 2 | 3 | 4 | 6 | 12
							   }
							}
                	ESAZ.updateSearchService(subscriptionId, resourceGroupName, serviceName, body)
                def deleteQueryKey(self):
                	key = "RZCtest"
                	ESAZ.deleteQueryKey(subscriptionId, resourceGroupName, key)

                
 
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAzureSearch)
    unittest.TextTestRunner(verbosity=2).run(suite)
