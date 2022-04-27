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

    ID = data["id"]

    return ID


ID = institute_id('Harvard University')

print(ID)