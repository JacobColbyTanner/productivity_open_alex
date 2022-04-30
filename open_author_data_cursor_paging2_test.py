import urllib.request
import json
import ssl
import numpy as np
import matplotlib.pyplot as plt

ssl._create_default_https_context = ssl._create_unverified_context



#Get instituition ID

def institute_id(school_name):

    me = '&mailto=jctanner@iu.edu'

    url = 'https://api.openalex.org/institutions?filter=display_name:'+ school_name + me

    json_obj = urllib.request.urlopen(url)

    data = json.load(json_obj)

    item = data["results"]


    ID = item[0]["id"]
    if ID.startswith('https://openalex.org/'):
        return ID[len('https://openalex.org/'):]
    return ID







def author_by_institute(institute_ID,author_num):

    me = '&mailto=jctanner@iu.edu'

    url = 'https://api.openalex.org/authors?filter=last_known_institution.id:'+ institute_ID + me + '&per-page=200'

    json_obj = urllib.request.urlopen(url)

    data = json.load(json_obj)

    item = data["results"]
    
    ID = item[author_num]['id']
    if ID.startswith('https://openalex.org/'):
        return ID[len('https://openalex.org/'):]
    return ID

def author_cited_by(cited_by_api_url,items_per_page,author_ID):

    me = '&mailto=jctanner@iu.edu'
    cited_by_url = cited_by_api_url+ '&sort=publication_year:asc' + '&per-page=' + str(items_per_page) + me + "&cursor=*"
    
    json_obj = urllib.request.urlopen(cited_by_url)

    cited_by_data = json.load(json_obj)
    W = -1
    bins2 = np.zeros((5000,121))
    while W < 1: #cited_by_data['meta']['next_cursor']:
        W += 1
        results = cited_by_data["results"]

        cited_year = np.zeros(len(results))

        #Pass through this page  - works that cited author
        for j in range(len(results)):
            cited_year[j] = results[j]['publication_year']
        
        bin = np.histogram(cited_year, bins=121, range=(1900,2021))
        bins2[W,:] = bin[0]


        #update page
        next_cursor = cited_by_data["meta"]["next_cursor"]

        url2 = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&filter=author.id:'+ author_ID + me + '&cursor='+ next_cursor

        json_obj = urllib.request.urlopen(url2)

        cited_by_data = json.load(json_obj)
    return bins2


def works_by_author(author_ID):
    items_per_page = 200
    

    me = '&mailto=jctanner@iu.edu'
    url = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&sort=publication_year:asc' + '&cursor=*&filter=author.id:'+ author_ID + me
    json_obj = urllib.request.urlopen(url)
    data = json.load(json_obj)
    item = data["results"]
    binned_citations = np.zeros((5000,len(item),121))
    

    W = -1
    #Pass through pages of author work
    while W < 1: #data['meta']['next_cursor']:
        W +=1
        for i in range(len(item)):

            bins2 = np.zeros((2,121)) #preallocate dummy here in the case that if condition is not satisfied
            if item[i]['cited_by_count'] > 0:  # if work was actually cited, then look through citations
                cited_by_api_url = item[i]['cited_by_api_url']
                bins2 = author_cited_by(cited_by_api_url,items_per_page,author_ID)
                
            binned_citations[W,i,:] = np.sum(bins2,axis=0)

        #update page
        next_cursor = data["meta"]["next_cursor"]

        url2 = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&filter=author.id:'+ author_ID + me + '&cursor='+ next_cursor

        json_obj = urllib.request.urlopen(url2)

        data = json.load(json_obj)

        item = data["results"]
       

    binned_citations = np.sum(binned_citations,axis=0)    
    return binned_citations