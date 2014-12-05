#!/usr/bin/env python2
## -*- coding: utf-8 -*-
import json
import io
from datetime import datetime, date
import urllib2
from simplejson import JSONDecodeError
from pyelasticsearch import ElasticSearch
from pyazuresearch import *

def RZC_Serializer(obj):
    
    if isinstance(obj, CreateAd):
        return { 
            "value": obj.car
        }

    if isinstance(obj, AdCar):
        return {
            "@search.action" : obj.action,
            "ref" : obj.ref,
            "label" : obj.label,
            "brand" : obj.brand,
            "model" : obj.model,
            "mileage" : obj.mileage,
            "title" : obj.title,
            "description" : obj.description,
            "img_url" : obj.img_url,
            "price" : obj.price,
            "year" : obj.year
        }
    raise TypeError(repr(obj) + " => Unable to serialize the object")


class CreateAd:
    def __init__(self):
        self.car = []


class AdCar:
    def __init__(self, ref, action,label, brand, model, mileage, title, description, img_url, price, year):
        self.ref = ref
        self.action = action
        self.label = label
        self.brand = brand
        self.model = model
        self.mileage = mileage
        self.title = title
        self.description = description
        self.img_url = img_url
        self.price = price
        self.year = year


class CreateJsonDump:
    def __init__(self):
        self.adfromES = CreateAd()
        self.servicename  = "servicename"
        self.indexname = "indexname"
        self.apiversion = "apiversion"
        self.apikey = "apikey"
        self.azure = AzureSearch(self.servicename, self.apiversion, self.apikey)

    def body(self, ref, action, label, brand, model, mileage, title, description, img_url, price, year):
        self.adfromES.car.append(AdCar(ref, action, label, brand, model, mileage, title, description, img_url, price, year))

    def printresult(self):
        json_acceptable_string = json.dumps(self.adfromES, indent=4, default=RZC_Serializer)
        d = json.loads(json_acceptable_string)
        self.azure.usedocument(self.indexname, d)
        with open('Test.json', 'w') as f:
           json.dump(self.adfromES, f, indent=4, default=RZC_Serializer)
