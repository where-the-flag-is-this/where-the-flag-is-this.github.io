import sys
from typing import Dict, List

import pandas as pd
from SPARQLWrapper import JSON, SPARQLWrapper


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
        self.user_agent = "WDQS-example Python/%s.%s" % (
            sys.version_info[0],
            sys.version_info[1],
        )
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
                new_result[key] = result[key]["value"]
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
        results = self.sparql.queryAndConvert()["results"]["bindings"]
        results = self.__transform2dicts(results)
        return results


countries_information_query = """
    SELECT 
        ?countryLabel 
        (MAX(?flags) as ?flag) 
        (MAX(?locations) as ?location) 
        (MAX(?populations) as ?population) 
        (MAX(?areas) as ?area) 
        (MAX(?geoshapes) as ?geoshape) 
        (GROUP_CONCAT(DISTINCT ?continentLabel; separator=",") AS ?continents)

    WHERE 
    {
    ?country wdt:P31 wd:Q3624078. # select items with "country" classification
    FILTER NOT EXISTS {?country wdt:P31/wdt:P279* wd:Q1246}. # filter out recognized countries
    FILTER NOT EXISTS {?country wdt:P576 ?dissolved.} # filter out items with date of dissolution
    ?country wdt:P41 ?flags. # get flag of the country, if any
    OPTIONAL { ?country wdt:P625 ?locations. } # get location of the country, if any
    OPTIONAL { ?country wdt:P1082 ?populations. } # get population of the country, if any
    OPTIONAL { ?country wdt:P2046 ?areas. } # get area of the country, if any
    ?country wdt:P3896 ?geoshapes. # get geoshape of the country, if any
    ?country wdt:P30 ?continent.   # Located in continent
    # ?continent wdt:P31 wd:Q5107.   # Continents
    SERVICE wikibase:label { 
        bd:serviceParam wikibase:language "en". 
        ?country rdfs:label ?countryLabel .
        ?continent rdfs:label ?continentLabel .
    } # get label and description in English 
    }
    GROUP BY ?countryLabel
    """


def get_missing_items_query(item_qid="Q4628"):
    return f"""
    SELECT 
        (GROUP_CONCAT(DISTINCT ?names; separator=",") AS ?countryLabel)
        (MAX(?flags) as ?flag) 
        (MAX(?locations) as ?location) 
        (MAX(?populations) as ?population) 
        (MAX(?areas) as ?area) 
        (MAX(?geoshapes) as ?geoshape)
        (GROUP_CONCAT(DISTINCT ?continentLabel; separator=",") AS ?continents)
    {{
        wd:{item_qid} wdt:P1082 ?populations. 
        wd:{item_qid} wdt:P41 ?flags. 
        wd:{item_qid} rdfs:label ?names. 
        wd:{item_qid} wdt:P3896 ?geoshapes. 
        wd:{item_qid} wdt:P2046 ?areas. 
        wd:{item_qid} wdt:P625 ?locations.
        wd:{item_qid} wdt:P30 ?continent.
        FILTER(lang(?names)='en')

        SERVICE wikibase:label {{ 
            bd:serviceParam wikibase:language "en". # get label and description in English 
            ?continent rdfs:label ?continentLabel . # get label not Q-code
        }} 
    }}
    GROUP BY ?countryLabel
"""
