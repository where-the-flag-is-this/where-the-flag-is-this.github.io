import requests
import json 

import geopandas as gpd
import matplotlib.pyplot as plt


def get_geoshape(name_geoshape:str):
    url = f'https://commons.wikimedia.org/w/api.php?action=query&prop=revisions&rvslots=*&rvprop=content&format=json&titles=Data:{name_geoshape}.map&origin=*'
    

    response = requests.get(url)

    data = response.json()['query']['pages']
    geoshape = json.loads(data[list(data.keys())[0]]['revisions'][0]['slots']['main']['*'])['data']

    return geoshape["features"][0]

countries = ['Germany','Italy', 'Belgium','Poland' ]
geoshapes = [get_geoshape(x) for x in countries]
geoshapes_dict = {'type': 'FeatureCollection', }
geoshapes_dict['features'] = geoshapes

gdf = gpd.GeoDataFrame.from_features(geoshapes_dict)

gdf.plot()
plt.show()