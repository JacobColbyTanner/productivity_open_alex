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

    url = 'https://api.openalex.org/authors?filter=last_known_institution.id:'+ institute_ID + me

    json_obj = urllib.request.urlopen(url)

    data = json.load(json_obj)

    item = data["results"]
    
    ID = item[author_num]['id']
    if ID.startswith('https://openalex.org/'):
        return ID[len('https://openalex.org/'):]
    return ID



def works_by_author(author_ID):
    items_per_page = 10
    me = '&mailto=jctanner@iu.edu'

    url = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&cursor=*&filter=author.id:'+ author_ID + me


    json_obj = urllib.request.urlopen(url)

    data = json.load(json_obj)

    num_pages = 10 #np.round(data["meta"]["count"]/items_per_page)

    item = data["results"]

    cited_count = np.zeros(len(item))
    publication_year = np.zeros(len(item))
    binned_citations = np.zeros((num_pages,len(item),121))


    #Pass through first page author work
    for i in range(len(item)):
        #store number of citations for paper and also 
        #cited_count[i] = item[i]['cited_by_count']

        #publication_year[i] = item[i]['publication_year']
        bins2 = np.zeros((2,121))
        if item[i]['cited_by_count'] > 0:
            cited_by_url = item[i]['cited_by_api_url']+'&per-page=' + str(items_per_page) + me + "&cursor=*"
            
            json_obj = urllib.request.urlopen(cited_by_url)

            cited_by_data = json.load(json_obj)

            results = cited_by_data["results"]
            num_pages2 = 10 #np.round(cited_by_data["meta"]["count"]/items_per_page)
            bins2 = np.zeros((num_pages2,121))
            cited_year = np.zeros(len(results))

            #Pass through first page  - works that cited author
            for j in range(len(results)):
                cited_year[j] = results[j]['publication_year']
            
            bin = np.histogram(cited_year, bins=121, range=(1900,2021))
            bins2[0,:] = bin[0]
            
            #Pass through rest of pages  - works that cited author
            for pp in range(num_pages2-1):
                next_cursor = cited_by_data["meta"]["next_cursor"]

                

                url2 = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&filter=author.id:'+ author_ID + me + '&cursor='+str(next_cursor)


                json_obj = urllib.request.urlopen(url2)

                results = json.load(json_obj)


                cited_year = np.zeros(len(results))
                for j in range(len(results)):
                    cited_year[j] = results[j]['publication_year']
                
                bin = np.histogram(cited_year, bins=121, range=(1900,2021))
                bins2[pp+1,:] = bin[0]
        binned_citations[0,i,:] = np.sum(bins2,axis=0)

    #Pass through rest of pages -  author work
    for p in range(num_pages-1):

        next_cursor = data["meta"]["next_cursor"]

        url2 = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&filter=author.id:'+ author_ID + me + '&cursor='+str(next_cursor)

        json_obj = urllib.request.urlopen(url2)

        data = json.load(json_obj)

        item = data["results"]

        cited_count = np.zeros(len(item))
        publication_year = np.zeros(len(item))
        binned_citations = np.zeros((len(item),121))
        for i in range(len(item)):
            #store number of citations for paper and also 
            #cited_count[i] = item[i]['cited_by_count']

            #publication_year[i] = item[i]['publication_year']
            bins2 = np.zeros((2,121))
            if item[i]['cited_by_count'] > 0:
                cited_by_url = item[i]['cited_by_api_url']+'&per-page='+ str(items_per_page) + me + "&cursor=*"

                json_obj = urllib.request.urlopen(cited_by_url)

                cited_by_data = json.load(json_obj)

                results = cited_by_data["results"]

                cited_year = np.zeros(len(results))
    
                

                #Pass through first page  - works that cited author
                num_pages2 = 10 #np.round(cited_by_data["meta"]["count"]/items_per_page)
                bins2 = np.zeros((num_pages2,121))
                for j in range(len(results)):
                    cited_year[j] = results[j]['publication_year']
                
                bin = np.histogram(cited_year, bins=121, range=(1900,2021))
                bins2[pp,:] = bin[0]
                
                #Pass through rest of pages  - works that cited author
                for pp in range(num_pages2-1):
                    next_cursor = cited_by_data["meta"]["next_cursor"]

                    url2 = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&filter=author.id:'+ author_ID + me + '&cursor='+str(next_cursor)

                    json_obj = urllib.request.urlopen(url2)

                    results = json.load(json_obj)


                    cited_year = np.zeros(len(results))
                    for j in range(len(results)):
                        cited_year[j] = results[j]['publication_year']
                    
                    bin = np.histogram(cited_year, bins=121, range=(1900,2021))
                    bins2[pp+1,:] = bin[0]
        binned_citations[p+1,i,:] = np.sum(bins2,axis=0)
            

    binned_citations = np.sum(binned_citations,axis=0)    
    return binned_citations





