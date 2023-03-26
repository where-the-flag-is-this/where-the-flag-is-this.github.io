import requests
import json
import random

import geopandas as gpd
import matplotlib.pyplot as plt
from queries import WikiDataQueryResults, countries_information_query

random.seed(20)


def get_geoshape(name_geoshape: str, extra_properties={}):
    try:
        url = f"https://commons.wikimedia.org/w/api.php?action=query&prop=revisions&rvslots=*&rvprop=content&format=json&titles=Data:{name_geoshape}.map&origin=*"

        response = requests.get(url)

        data = response.json()["query"]["pages"]
        geoshape = json.loads(
            data[list(data.keys())[0]]["revisions"][0]["slots"]["main"]["*"]
        )["data"]
        geoshape_dict = geoshape["features"][0]
        geoshape_dict["properties"] = {
            **geoshape_dict["properties"],
            **extra_properties,
        }

        return geoshape_dict
    except:
        pass


query = WikiDataQueryResults(countries_information_query)

country_list = query.load_as_list("countryLabel")
country_df = query.load_as_dataframe()
sample_countries = country_df.sample(10, random_state=10)
geoshapes = []
for country in sample_countries.to_dict(orient="records"):
    new_shape = get_geoshape(country["countryLabel"], country)
    if new_shape:
        geoshapes.append(new_shape)

geoshapes_dict = {
    "type": "FeatureCollection",
}
geoshapes_dict["features"] = geoshapes

with open("../src/assets/allPlaces.json", "w") as fp:
    json.dump(geoshapes_dict, fp)

gdf = gpd.GeoDataFrame.from_features(geoshapes_dict)

gdf.boundary.plot()
plt.show()
