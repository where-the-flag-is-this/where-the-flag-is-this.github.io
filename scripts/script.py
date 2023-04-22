import requests
import geopandas as gpd
import matplotlib.pyplot as plt
from queries import WikiDataQueryResults

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


usa_states_query = """
SELECT DISTINCT ?state ?stateLabel ?stateDescription ?flag ?location ?population ?area ?geoshape WHERE {
  ?state wdt:P31 wd:Q35657. # sovereign state
  ?state rdfs:label ?stateLabel filter (lang(?stateLabel) = "en").
   OPTIONAL { ?state wdt:P41 ?flag. } # get flag of the state, if any
  OPTIONAL { ?state wdt:P625 ?location. } # get location of the state, if any
  OPTIONAL { ?state wdt:P1082 ?population. } # get population of the state, if any
  OPTIONAL { ?state wdt:P2046 ?area. } # get area of the state, if any
  OPTIONAL { ?state wdt:P3896 ?geoshape. } # get geoshape of the state, if any
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en".
  }
}
"""

query = WikiDataQueryResults(usa_states_query)

state_df = query.load_as_dataframe()
state_df = state_df.drop_duplicates(subset="stateLabel")

# + in the links does not work 
state_df["geoshapeUrl"] = state_df.geoshape.str.replace("+", "_")
state_df = state_df.astype({"area": float, "population":int})


geoshapes = []
for state in state_df.to_dict(orient="records"):
    new_shape = get_geoshape_by_url(state["geoshapeUrl"], state)
    if new_shape:
        geoshapes.append(new_shape)

geoshapes_dict = {
    "type": "FeatureCollection",
}
geoshapes_dict["features"] = geoshapes


gdf = gpd.GeoDataFrame.from_features(geoshapes_dict)

gdf.plot(column="population", legend=True, missing_kwds={'color': 'lightgrey'})
plt.title('USA States by population')
plt.axis('off')
plt.show()
