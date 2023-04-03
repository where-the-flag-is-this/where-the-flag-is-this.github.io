import sys
import pandas as pd
from typing import List, Dict
from pprint import pprint
from SPARQLWrapper import SPARQLWrapper, JSON

class WikiDataQueryResults:
    """
    A class that can be used to query data from Wikidata using SPARQL and return the results as a Pandas DataFrame or a list
    of values for a specific key.
    """
    def __init__(self, query: str):
        """
        Initializes the WikiDataQueryResults object with a SPARQL query string.

        :param query: A SPARQL query string.
        """
        self.user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        self.endpoint_url = "https://query.wikidata.org/sparql"
        self.sparql = SPARQLWrapper(self.endpoint_url, agent=self.user_agent)
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)

    def __transform2dicts(self, results: List[Dict]) -> List[Dict]:
        """
        Helper function to transform SPARQL query results into a list of dictionaries.

        :param results: A list of query results returned by SPARQLWrapper.
        :return: A list of dictionaries, where each dictionary represents a result row and has keys corresponding to the
        variables in the SPARQL SELECT clause.
        """
        new_results = []
        for result in results:
            new_result = {}
            for key in result:
                new_result[key] = result[key]['value']
            new_results.append(new_result)
        return new_results

    def load_as_dataframe(self) -> pd.DataFrame:
        """
        Executes the SPARQL query and returns the results as a Pandas DataFrame.

        :return: A Pandas DataFrame representing the query results.
        """
        results = self._load()
        return pd.DataFrame.from_dict(results)

    def load_as_list(self, key: str) -> List[str]:
        """
        Executes the SPARQL query and returns a list of values for a specific key.

        :param key: The key for which to retrieve values.
        :return: A list of string values for the specified key.
        """
        results = self._load()
        return [x[key] for x in results]

    def _load(self) -> List[Dict]:
        """
        Helper function that loads the data from Wikidata using the SPARQLWrapper library, and transforms the results into
        a list of dictionaries.

        :return: A list of dictionaries, where each dictionary represents a result row and has keys corresponding to the
        variables in the SPARQL SELECT clause.
        """
        results = self.sparql.queryAndConvert()['results']['bindings']
        results = self.__transform2dicts(results)
        return results

countries_information_query = """
SELECT ?countryLabel ?countryDescription ?flag ?location ?population ?area ?geoshape 
WHERE 
{
  ?country wdt:P31 wd:Q3624078. # select items with "country" classification
  FILTER NOT EXISTS {?country wdt:P31/wdt:P279* wd:Q1246}. # filter out recognized countries
  FILTER NOT EXISTS {?country wdt:P576 ?dissolved.} # filter out items with date of dissolution
  OPTIONAL { ?country wdt:P41 ?flag. } # get flag of the country, if any
  OPTIONAL { ?country wdt:P625 ?location. } # get location of the country, if any
  OPTIONAL { ?country wdt:P1082 ?population. } # get population of the country, if any
  OPTIONAL { ?country wdt:P2046 ?area. } # get area of the country, if any
  OPTIONAL { ?country wdt:P3896 ?geoshape. } # get geoshape of the country, if any
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } # get label and description in English 
}
"""

def get_missing_items_query(item_qid = "Q4628"):
    return """SELECT ?name ?description ?flag ?location  ?population ?area ?geoshape 
    WHERE {""" +f"wd:{item_qid} wdt:P1082 ?population."+f"wd:{item_qid} wdt:P41 ?flag." +f"wd:{item_qid} rdfs:label ?name."+f"wd:{item_qid} wdt:P3896 ?geoshape."+f"wd:{item_qid} wdt:P2046 ?area."+f"wd:{item_qid} wdt:P625 ?location."+f"wd:{item_qid} schema:description ?description."+"""  
        FILTER (LANG(?name) = 'en')
        FILTER (LANG(?description) = 'en')
        
        SERVICE wikibase:label { bd:serviceParam wikibase:language 'en'. }
        }"""

dutch_provinces_query = """
SELECT ?countryLabel ?countryDescription ?flag ?location ?population ?area ?geoshape WHERE {
  ?country wdt:P31 wd:Q134390. # sovereign state
  ?country rdfs:label ?countryLabel filter (lang(?countryLabel) = "en").
   OPTIONAL { ?country wdt:P41 ?flag. } # get flag of the country, if any
  OPTIONAL { ?country wdt:P625 ?location. } # get location of the country, if any
  OPTIONAL { ?country wdt:P1082 ?population. } # get population of the country, if any
  OPTIONAL { ?country wdt:P2046 ?area. } # get area of the country, if any
  OPTIONAL { ?country wdt:P3896 ?geoshape. } # get geoshape of the country, if any
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en".
  }
}
"""
