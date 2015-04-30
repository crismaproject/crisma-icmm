#!/usr/bin/env python
#
# Peter.Kutschera@ait.ac.at, 2015-04-16
#
# Test nextId generator

# ICMM Service endpoint:
icmm="http://localhost:/icmm_api"
# Test-Instance for external tests
#icmm="https://pinguin2.ait.ac.at/icmm_api"
icmm="https://crisma-pilotEv1.ait.ac.at/icmm_api"


import json
import requests
import re



def getNextIdOLD (clazz, baseUrl=icmm, domain="CRISMA"):
    """Get the next available id for the given class

    clazz: class name within ICMM
    """
    params = {
        'limit' :  999999999,
        'level': 1,
        'fields': None
        }
    headers = {'content-type': 'application/json'}
    response = requests.get("{0}/{1}.{2}".format (baseUrl, domain, clazz), params=params, headers=headers, verify=False) 
    # this was the request:
    #print response.url
    if response.status_code != 200:
        raise Exception ( "Error accessing ICMM at {0}: {1}".format (response.url, response.status_code))
    # Depending on the requests-version json might be an field instead of on method
    # print response.json()
    jsonData = response.json() if callable (response.json) else response.json
    maxid = 0;
    collection = jsonData['$collection']
    for r in collection:
        ref = r['$self']
        match = re.search ("/([0-9]+)$", ref)
        if (match):
            id = int (match.group(1))
            if (id > maxid):
                maxid = id
    return maxid + 1



def getNextId (clazz, baseUrl=icmm, domain="CRISMA"):
    """Get the next available id for the given class

    clazz: class name within ICMM
    domain: NEED TO BE 'CRISMA'
    """
    if not "CRISMA" == domain:
        raise Exception ("Only allowed domain is 'CRISMA'")
    params = {
        'domain': domain,
        'class': clazz
        }
    headers = {'content-type': 'application/json'}
    response = requests.get("{0}/nextId".format (baseUrl), params=params, headers=headers, verify=False) 
    if response.status_code == 404:
        # ICMM without Peter's Patch?
        return getNextIdOLD (clazz, baseUrl, domain)
    if response.status_code != 200:
        raise Exception ( "Error accessing ICMM at {0}: {1}".format (response.url, response.status_code))
     # Depending on the requests-version json might be an field instead of on method
    jsonData = response.json() if callable (response.json) else response.json
    # print jsonData
    return jsonData['nextId']


def listStoredDocuments ():
    params = {
        'limit' :  1000,
        'level': 1,
        'fields': None
        }
    headers = {'content-type': 'application/json'}
    response = requests.get("{0}/{1}.{2}".format (icmm, "CRISMA", "categories"), params=params, headers=headers, verify=False) 
    # this was the request:
    #print response.url
    if response.status_code != 200:
        raise Exception ( "Error accessing ICMM at {0}: {1}".format (response.url, response.status_code))
    # Depending on the requests-version json might be an field instead of on method
    jsonData = response.json() if callable (response.json) else response.json
    usedIds = [];
    collection = jsonData['$collection']
    for r in collection:
        ref = r['$self']
        match = re.search ("/([0-9]+)$", ref)
        if (match):
            id = int (match.group(1))
            usedIds.append (id)
    return usedIds
    

def putTestDocument (id):
    params = { }
    data = {
        "$self": "/CRISMA.categories/{0}".format (id),
        "id": id,
        "key": "Test-data"
        }
    headers = {'content-type': 'application/json'}
    response = requests.put("{0}/{1}.{2}/{3}".format (icmm, "CRISMA", "categories", id), data=json.dumps (data), params=params, headers=headers, verify=False) 
    if response.status_code != 200:
        raise Exception ( "Error ICMM PUT at {0}: {1}".format (response.url, response.status_code))
    

def deleteTestDocument (id):
    params = { }
    headers = {'content-type': 'application/json'}
    response = requests.delete("{0}/{1}.{2}/{3}".format (icmm, "CRISMA", "categories", id), params=params, headers=headers, verify=False) 
    if response.status_code != 200:
        raise Exception ( "Error ICMM DELETE at {0}: {1}".format (response.url, response.status_code))
    

if __name__ == "__main__":
    print ("test nextId generator")
    print ("Using icmm at {0}".format (icmm))

    print "Documents already stored: {0}".format (listStoredDocuments())

    id = getNextId ("categories")
    print ("Get next id: {0}".format (id))
    id = getNextId ("categories")
    print ("Get next id: {0}".format (id))



    if False:
        id = getNextId ("categories")
        print ("Get next id: {0}".format (id))
        
        print ("Now create an document with an id     from the nextId function: id={0}".format(id))
        putTestDocument (id)
        print ("Now create an document with an id NOT from the nextId function: id={0}".format(id+1))
        putTestDocument (id + 1)
        print "Documents now stored: {0}".format (listStoredDocuments())
        
        id3 = getNextId ("categories")
        print ("Get next id to see if this misuse created problems: {0}".format (id3))
        
        deleteTestDocument (id)
        deleteTestDocument (id+1)
        print ("Deleted documents {0} and {1}".format (id, id+1))
        
        print "Documents now stored: {0}".format (listStoredDocuments())
        
        id = getNextId ("categories")
        print ("Get next id: {0}".format (id))
