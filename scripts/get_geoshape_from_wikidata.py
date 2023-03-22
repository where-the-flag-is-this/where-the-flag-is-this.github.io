import requests
import json 
import random

import geopandas as gpd
import matplotlib.pyplot as plt
from queries import WikiDataQueryResults, countries_information_query
random.seed(20)

def get_geoshape(name_geoshape:str):
    url = f'https://commons.wikimedia.org/w/api.php?action=query&prop=revisions&rvslots=*&rvprop=content&format=json&titles=Data:{name_geoshape}.map&origin=*'
    

    response = requests.get(url)

    data = response.json()['query']['pages']
    geoshape = json.loads(data[list(data.keys())[0]]['revisions'][0]['slots']['main']['*'])['data']

    return geoshape["features"][0]

query = WikiDataQueryResults(countries_information_query)

country_list = query.load_as_list('countryLabel') 
geoshapes = [get_geoshape(x) for x in random.sample(country_list, 10)]
geoshapes_dict = {'type': 'FeatureCollection', }
geoshapes_dict['features'] = geoshapes

gdf = gpd.GeoDataFrame.from_features(geoshapes_dict)

gdf.boundary.plot()
plt.show()