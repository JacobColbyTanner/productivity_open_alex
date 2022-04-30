import urllib.request
import json
import ssl
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import requests
  

from open_author_simple_up_to_date_session import institute_id
from open_author_simple_up_to_date_session  import author_by_institute
from open_author_simple_up_to_date_session  import works_by_author
from open_author_simple_up_to_date_session  import author_cited_by
from open_author_simple_up_to_date_session  import number_of_authors


#parameters
#number_of_authors_searched = 100
university_name = 'Harvard%20University'
years_from_first_pub = 10
cited_by_year_range = 10

institute_ID = institute_id(university_name)

#select all possible authors
number_of_authors_searched = number_of_authors(institute_ID)


num_citations_by_researcher = np.zeros(number_of_authors_searched)

for i in range(number_of_authors_searched):
    print("Author Number: ")
    print(i)
    author_ID = author_by_institute(institute_ID,i)

    num_citations_by_researcher[i] = works_by_author(author_ID,years_from_first_pub,cited_by_year_range)


    #save every 10 
    if i%10 == 0:
        dirr = 'citations/'
        post = university_name + "_num_authors_" + str(i) + "_of_" + str(number_of_authors_searched) + ".mat"

        name_it = dirr+post

        sio.savemat(name_it, mdict={'num_citations': num_citations_by_researcher})
    





#create log plot



researcher_with_num_citations = np.histogram(num_citations_by_researcher,bins=10000, range=(0,20000))


num_citations = np.arange(1,10001)
num_citations = np.log10(num_citations)

num_researchers = np.log10(researcher_with_num_citations[0])




plt.plot(num_citations,num_researchers)
plt.savefig(f"log_plot_{number_of_authors_searched}.png")
plt.clf()