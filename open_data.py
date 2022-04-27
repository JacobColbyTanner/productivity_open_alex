import urllib.request
import json
import ssl
import numpy as np
import matplotlib.pyplot as plt

ssl._create_default_https_context = ssl._create_unverified_context



date_range = '1964-2004'

type = '&filter=type:journal-article' #,journal,proceedings-article

me = '&mailto=jctanner@iu.edu'

url = 'https://api.openalex.org/works?filter=publication_year:'+date_range+me+type

json_obj = urllib.request.urlopen(url)

data = json.load(json_obj)



def get_num_authors(data):
    i = 0
    num_authors = np.zeros(len(data["results"]))
    for item in data["results"]:
        #print(item["authorships"])
        
        num = 0
        for authors in item["authorships"]:
            num = num+1
        num_authors[i] = num
        i = i+1

    return num_authors



def avg_number_authors_over_time(start_date,end_date,type_article):
    dates = np.arange(start_date, end_date+1, 1)
    i = 0
    number_authors_year = np.zeros(len(dates))

    for d in dates:
        type = '&filter=type:'+ type_article #journal-article,journal,proceedings-article

        me = '&mailto=jctanner@iu.edu'

        url = 'https://api.openalex.org/works?filter=publication_year:'+np.array2string(d)+me+type

        json_obj = urllib.request.urlopen(url)

        data = json.load(json_obj)

        number_authors_year[i] = np.mean(get_num_authors(data))
        i = i+1

    return number_authors_year, dates

start_date = 1900
end_date = 2000


journal_a_num = avg_number_authors_over_time(start_date,end_date,'journal-article')
print("First")
journal_num = avg_number_authors_over_time(start_date,end_date,'journal')
print("Second")
proceedings_num, dates = avg_number_authors_over_time(start_date,end_date,'proceedings-article')
print("Third")

plt.plot(journal_a_num)
plt.ylabel("Avg num authors")
plt.xlabel("Dates")
plt.title("Journal Articles")
plt.show()

plt.plot(journal_num)
plt.ylabel("Avg num authors")
plt.xlabel("Dates")
plt.title("Journals")
plt.show()

plt.plot(proceedings_num)
plt.ylabel("Avg num authors")
plt.xlabel("Dates")
plt.title("Proceedings")
plt.show()


plt.plot(journal_a_num+ journal_num+ proceedings_num)
plt.ylabel("Avg num authors")
plt.xlabel("Dates")
plt.title("All types")
plt.show()