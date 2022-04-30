import urllib.request
import json
import ssl
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

from open_author_up_to_date import institute_id
from open_author_up_to_date  import author_by_institute
from open_author_up_to_date  import works_by_author
from open_author_up_to_date  import author_cited_by

#parameters
number_of_authors_searched = 100
university_name = 'Harvard%20University'
years_from_first_pub = 10
cited_by_year_range = 10

institute_ID = institute_id(university_name)

citations_by_year = np.zeros((number_of_authors_searched,121))

for i in range(number_of_authors_searched):
    print("Author Number: ")
    print(i)
    author_ID = author_by_institute(institute_ID,i)

    binned_citations = works_by_author(author_ID,years_from_first_pub,cited_by_year_range)

    citations_by_year[i,:] = np.sum(binned_citations,axis = 0)

dirr = 'citations_by_year/'
post = university_name + "_num_authors_" + str(number_of_authors_searched) + ".mat"

name_it = dirr+post

sio.savemat(name_it, mdict={'citations_by_year': citations_by_year})

print(citations_by_year)
print(np.sum(citations_by_year))
plt.plot(np.sum(citations_by_year,axis=0))
plt.xticks(ticks=[0,20,40,60,80,100,120], labels=[1900,1920,1940,1960,1980,2000,2020])
plt.savefig(f"citations_by_year_num_authors_{number_of_authors_searched}.png")
plt.clf()

start_same = np.zeros((number_of_authors_searched,years_from_first_pub))
for i in range(number_of_authors_searched):
    f = np.nonzero(citations_by_year)
    index = f[1][0]

    start_same[i,:] = citations_by_year[i][index:index+years_from_first_pub]



plt.plot(np.sum(start_same,axis=0))
plt.savefig(f"start_same_num_authors_{number_of_authors_searched}.png")
plt.clf()


#create log plot

num_citations_per_researcher = np.sum(citations_by_year,axis = 1)

researcher_with_num_citations = np.histogram(num_citations_per_researcher,bins=10000, range=(0,20000))


num_citations = np.arange(1,10001)
num_citations = np.log10(num_citations)

num_researchers = np.log10(researcher_with_num_citations[0])




plt.plot(num_citations,num_researchers)
plt.savefig(f"log_plot_{number_of_authors_searched}.png")
plt.clf()