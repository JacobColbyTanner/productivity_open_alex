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
    return ID, 




def number_of_authors(institute_ID):

    me = '&mailto=jctanner@iu.edu'

    url = 'https://api.openalex.org/authors?filter=last_known_institution.id:'+ institute_ID + me + '&per-page=200'

    json_obj = urllib.request.urlopen(url)

    data = json.load(json_obj)

    num_authors = data["meta"]["count"]
    
    return num_authors


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

def author_cited_by(cited_by_api_url,items_per_page,author_ID,first_pub_year,year_range,first_pub_date):
    

    me = '&mailto=jctanner@iu.edu'
  

    to_date = first_pub_year+year_range
    cited_by_url = cited_by_api_url+ '&filter=from_publication_date:'
    
    cited_by_url = cited_by_url + first_pub_date +',' + 'to_publication_date:' + str(to_date) +  '-01-01' + '&per-page=' + str(items_per_page) + me 
    
    json_obj = urllib.request.urlopen(cited_by_url)

    cited_by_data = json.load(json_obj)

    cited_count = cited_by_data["meta"]["count"]

    return cited_count


def works_by_author(author_ID,years_from_first_pub,year_range):
    items_per_page = 200
    

    me = '&mailto=jctanner@iu.edu'
    url = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&sort=publication_year:asc' + '&cursor=*&filter=author.id:'+ author_ID + me + '&cursor=*'
    json_obj = urllib.request.urlopen(url)
    data = json.load(json_obj)
    item = data["results"]
    total_citations = 0
    
    if data["meta"]["count"] > 0:
  
        first_pub_date = item[0]['publication_date']
        first_pub_year = item[0]['publication_year']

        W = -1
        #Pass through pages of author work
        current_pub_year = 1 #initialize in order to start while loop
        while  current_pub_year <= first_pub_year + years_from_first_pub and data['meta']['next_cursor']:
            W +=1
            for i in range(len(item)):

                bins2 = np.zeros((2,121)) #preallocate dummy here in the case that if condition is not satisfied
                if item[i]['cited_by_count'] > 0:  # if work was actually cited, then look through citations
                    current_pub_year = item[i]['publication_year']
                    if current_pub_year > first_pub_year + years_from_first_pub:
                        break
                    cited_by_api_url = item[i]['cited_by_api_url']
                    cited_count = author_cited_by(cited_by_api_url,items_per_page,author_ID,first_pub_year,year_range,first_pub_date)
                    

                    #print("Current Publication Year: ")
                    #print(current_pub_year)
                    #print("Number years to go")
                    #print(first_pub_year + years_from_first_pub - current_pub_year)


                    total_citations = total_citations + cited_count

            #update page
            next_cursor = data["meta"]["next_cursor"]

            url2 = 'https://api.openalex.org/works?per-page=' + str(items_per_page) + '&sort=publication_year:asc'+'&filter=author.id:'+ author_ID+ me + '&cursor='
            url2 = url2 + next_cursor

            json_obj = urllib.request.urlopen(url2)

            data = json.load(json_obj)

            item = data["results"]
        

        
    return total_citations