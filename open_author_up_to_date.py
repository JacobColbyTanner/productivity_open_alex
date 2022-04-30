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

def author_cited_by(cited_by_api_url,items_per_page,author_ID,first_pub_year,year_range):
    

    me = '&mailto=jctanner@iu.edu'
    cited_by_url = cited_by_api_url+ '&sort=publication_year:asc' + '&per-page=' + str(items_per_page) + me + "&cursor=*"
    
    json_obj = urllib.request.urlopen(cited_by_url)

    cited_by_data = json.load(json_obj)
    W = -1
    bins2 = np.zeros((5000,121))

    this_cited_year = 1 #initialize small value to start while loop
    while this_cited_year <= first_pub_year+year_range: #cited_by_data['meta']['next_cursor']:
        W += 1
        results = cited_by_data["results"]

        cited_year = np.zeros(len(results))

        #Pass through this page  - works that cited author
        for j in range(len(results)):
            this_cited_year = results[j]['publication_year']
            if this_cited_year > first_pub_year+year_range:
                    break
            cited_year[j] = results[j]['publication_year']
            
            #print("Cited Year: ")
            #print(this_cited_year)

            

        bin = np.histogram(cited_year, bins=121, range=(1900,2021))
        bins2[W,:] = bin[0]


        #update page
        next_cursor = cited_by_data["meta"]["next_cursor"]

        url2 = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&sort=publication_year:asc' + '&filter=author.id:'+ author_ID + me + '&cursor='+ next_cursor

        json_obj = urllib.request.urlopen(url2)

        cited_by_data = json.load(json_obj)
    return bins2


def works_by_author(author_ID,years_from_first_pub,year_range):
    items_per_page = 200
    

    me = '&mailto=jctanner@iu.edu'
    url = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&sort=publication_year:asc' + '&cursor=*&filter=author.id:'+ author_ID + me
    json_obj = urllib.request.urlopen(url)
    data = json.load(json_obj)
    item = data["results"]
    binned_citations = np.zeros((5000,len(item),121))
    
    first_pub_year = item[0]['publication_year']

    W = -1
    #Pass through pages of author work
    current_pub_year = 1 #initialize in order to start while loop
    while  current_pub_year <= first_pub_year + years_from_first_pub: #data['meta']['next_cursor']:
        W +=1
        for i in range(len(item)):

            bins2 = np.zeros((2,121)) #preallocate dummy here in the case that if condition is not satisfied
            if item[i]['cited_by_count'] > 0:  # if work was actually cited, then look through citations
                current_pub_year = item[i]['publication_year']
                if current_pub_year > first_pub_year + years_from_first_pub:
                    break
                cited_by_api_url = item[i]['cited_by_api_url']
                bins2 = author_cited_by(cited_by_api_url,items_per_page,author_ID,first_pub_year,year_range)
                

                #print("Current Publication Year: ")
                #print(current_pub_year)
                print("Number years to go")
                print(first_pub_year + years_from_first_pub - current_pub_year)


            binned_citations[W,i,:] = np.sum(bins2,axis=0)

        #update page
        next_cursor = data["meta"]["next_cursor"]

        url2 = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&sort=publication_year:asc' +'&filter=author.id:'+ author_ID + me + '&cursor='+ next_cursor

        json_obj = urllib.request.urlopen(url2)

        data = json.load(json_obj)

        item = data["results"]
       

    binned_citations = np.sum(binned_citations,axis=0)    
    return binned_citations