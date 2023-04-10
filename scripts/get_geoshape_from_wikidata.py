import requests
import json
import random

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from queries import WikiDataQueryResults, countries_information_query , get_missing_items_query

random.seed(20)

def get_geoshape_by_name(name_geoshape: str, extra_properties={}):
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
        return


def get_geoshape_by_url(url: str, extra_properties={}):
    try:

        r = requests.get(url)
        geoshape_dict = r.json()['data']['features'][0]
        geoshape_dict["properties"] = {
            **geoshape_dict["properties"],
            **extra_properties,
        }

        return geoshape_dict
    except:
        print(url)
        return



query = WikiDataQueryResults(countries_information_query)

country_df = query.load_as_dataframe()
country_df = country_df.drop_duplicates(subset="countryLabel")

# Get missing Kingdom Countries
missing_df_list = []
for missing_qid in ["Q4628", "Q35", "Q223", "Q55"]: # Fareo islands, Denmark, Greenland, Netherlands
    missing_query = WikiDataQueryResults(get_missing_items_query(missing_qid))
    missing_df_list.append(missing_query.load_as_dataframe())
missing_df = pd.concat(missing_df_list)
missing_df = missing_df.rename(columns = {"name":"countryLabel"})

country_df = pd.concat([country_df, missing_df])

# + in the links does not work 
country_df["geoshapeUrl"] = country_df.geoshape.str.replace("+", "_")


geoshapes = []
for country in country_df.to_dict(orient="records"):
    new_shape = get_geoshape_by_url(country["geoshapeUrl"], country)
    if new_shape:
        geoshapes.append(new_shape)
    else:
        # Mongolia is weird and geoshape is different that the rest
        new_shape = get_geoshape_by_name(country["countryLabel"], country)
        if new_shape:
            geoshapes.append(new_shape)
        print(country["countryLabel"])

print(len(geoshapes))

geoshapes_dict = {
    "type": "FeatureCollection",
}
geoshapes_dict["features"] = geoshapes

with open("../src/assets/allPlaces.json", "w") as fp:
    json.dump(geoshapes_dict, fp)

gdf = gpd.GeoDataFrame.from_features(geoshapes_dict)

gdf.boundary.plot()
plt.show()
