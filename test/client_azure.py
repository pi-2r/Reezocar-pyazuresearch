# -*- coding: utf-8 -*-
import sys
import unittest
from pyazuresearch import *

ESAZ = AzureSearch("serviceName", 
                "api-version=2014-07-31-Preview", 
                "apiKey")
subscriptionId = "00000-000-000-0000"
resourceGroupName = "BizSpark"
namekey = "namekey"
indexname =  "indexname"


class TestAzureSearch(unittest.TestCase):


    def test_stats(self):
    	ESAZ.stats("test")

    def test_listindexes(self):
        ESAZ.listindexes()

    def test_getindex(self):
        ESAZ.getindex("test")

    def test_deleteindex(self):
        ESAZ.deleteindex("test")
      

    def test_creatindex(self):
        creatindex =  {
              "name": "test",  
              "fields": [
                {"name": "ref", "type": "Edm.String", "key": True, "searchable": False},
                {"name": "link", "type": "Edm.String", "searchable": False},
                {"name": "actif", "type": "Edm.String", "searchable": False}] 
            }
        ESAZ.createindex("test", creatindex)

    def test_upload(self):
        doc = {
            "value": [
                    {
              "@search.action": "upload",
              "ref": "1234",
              "link": "http://github.com",
              "actif": "no"
              }
        ]}
        ESAZ.uploaddocument("test", doc)

    def test_DeleteDocument(self):
        ESAZ.uploaddocument("test", doc)
 
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAzureSearch)
    unittest.TextTestRunner(verbosity=2).run(suite)
