import requests
import json 

import geopandas as gpd
import matplotlib.pyplot as plt

url = 'https://commons.wikimedia.org/w/api.php?action=query&prop=revisions&rvslots=*&rvprop=content&format=json&titles=Data:Germany.map&origin=*'

response = requests.get(url)

data = response.json()['query']['pages']
geoshape = json.loads(data[list(data.keys())[0]]['revisions'][0]['slots']['main']['*'])['data']

gdf = gpd.GeoDataFrame.from_features(geoshape["features"])

gdf.plot()
plt.show()