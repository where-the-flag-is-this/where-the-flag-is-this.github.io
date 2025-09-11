import json
import random
import time
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import requests
from queries import (
    WikiDataQueryResults,
    countries_information_query,
    get_missing_items_query,
)
from tqdm import tqdm

random.seed(20)

URL_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def get_geoshape_by_name(name_geoshape: str, extra_properties={}):
    try:
        url = f"https://commons.wikimedia.org/w/api.php?action=query&prop=revisions&rvslots=*&rvprop=content&format=json&titles=Data:{name_geoshape}.map&origin=*"

        response = requests.get(url, headers=URL_HEADERS)

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
        r = requests.get(url, headers=URL_HEADERS)
        if r.status_code == 429:
            time.sleep(10)
            r = requests.get(url, headers=URL_HEADERS)
        geoshape_dict = r.json()["data"]["features"][0]
        geoshape_dict["properties"] = {
            **geoshape_dict["properties"],
            **extra_properties,
        }

        return geoshape_dict
    except:
        print(r.status_code, r.text, url)
        return


query = WikiDataQueryResults(countries_information_query)

country_df = query.load_as_dataframe()

# Get missing Kingdom Countries
missing_df_list = []
for missing_qid in [
    "Q4628",  # Fareo islands
    "Q35",  # Denmark
    "Q223",  # Greenland
    "Q55",  # Netherlands
    "Q712",  # Fiji
]:
    missing_query = WikiDataQueryResults(get_missing_items_query(missing_qid))
    missing_df_list.append(missing_query.load_as_dataframe())
missing_df = pd.concat(missing_df_list)
missing_df = missing_df.rename(columns={"name": "countryLabel"})

country_df = pd.concat([country_df, missing_df])
country_df = country_df.drop_duplicates(subset="countryLabel")

# + in the links does not work
country_df["geoshapeUrl"] = country_df.geoshape.str.replace("+", "_")


geoshapes = []
countries = country_df.to_dict(orient="records")
for country in tqdm(countries):
    new_shape = get_geoshape_by_url(country["geoshapeUrl"], country)
    if not new_shape:
        # Mongolia is weird and geoshape is different that the rest
        new_shape = get_geoshape_by_name(country["countryLabel"], country)

    # Turn continents into a list
    new_shape["properties"]["continents"] = new_shape["properties"]["continents"].split(
        ","
    )
    if new_shape:
        geoshapes.append(new_shape)

print(len(geoshapes))

geoshapes_dict = {
    "type": "FeatureCollection",
}
geoshapes_dict["features"] = geoshapes

with open("../src/assets/allPlaces.json", "w") as fp:
    json.dump(geoshapes_dict, fp, indent=4)

gdf = gpd.GeoDataFrame.from_features(geoshapes_dict)

gdf.boundary.plot()
plt.show()
