# Python script that retrieves RDF members out GraphDB via Sparql query

from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, CSV, RDF
from rdflib import Graph
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import pandas as pd
import json

def adres(input):
    adres= """

PREFIX generiek:      <https://data.vlaanderen.be/ns/generiek#>
PREFIX locn:          <https://www.w3.org/ns/locn#>
PREFIX geosparql:     <http://www.opengis.net/ont/geosparql#>
PREFIX adres: <https://data.vlaanderen.be/ns/adres#>
PREFIX prov: <http://www.w3.org/ns/prov#>

CONSTRUCT {
    ?adres_id adres:volledigAdres "Zelestraat 219, 9160 Lokeren"@nl.
    ?adres_id generiek:naamruimte ?naamruimte .
    ?adres_id generiek:lokaleIdentificator ?lokaleIdentificator .
    ?adres_id generiek:versieIdentificator ?versieIdentificator .
    ?adres_id adres:huisnummer ?huisnummer .
    ?adres_id  geosparql:asGML ?locatie .
    ?adres_id adres:heeftGemeentenaam ?gemeente .
    ?adres_id adres:Straatnaam ?straat .
    ?adres_id adres:officieelToegekend ?officieelToegekend .
    ?adres_id adres:heeftPostinfo ?heeftPostinfo .
    ?adres_id adres:Adres.status ?adresstatus .

}

where {
    ?genid adres:volledigAdres "Zelestraat 219, 9160 Lokeren"@nl .
    ?adres_id adres:isVerrijktMet ?genid .
    OPTIONAL { ?adres_id prov:generatedAtTime ?generatedAtTime .
    ?adres_id generiek:naamruimte ?naamruimte .
    ?adres_id generiek:lokaleIdentificator ?lokaleIdentificator .
    ?adres_id generiek:versieIdentificator ?versieIdentificator .
    ?adres_id adres:huisnummer ?huisnummer .
    ?adres_id adres:positie ?genid_positie .
    ?genid_positie locn:geometry ?genid_locatie .
    ?genid_locatie geosparql:asGML ?locatie .
    ?adres_id adres:heeftGemeentenaam ?heeftGemeentenaam .
    ?heeftGemeentenaam adres:Gemeentenaam ?genid_gemeente .
    ?genid_gemeente ?p ?gemeente .
    ?adres_id adres:heeftPostinfo ?heeftPostinfo .
    ?adres_id adres:Adres.status ?adresstatus .
    ?adres_id adres:officieelToegekend ?officieelToegekend .
    ?adres_id adres:heeftStraatnaam ?heeftStraatnaam .
    ?heeftStraatnaam adres:Straatnaam ?genid_straat .
    ?genid_straat ?p ?straat .
    }}

"""
    return adres


sparql = SPARQLWrapper("http://localhost:7200/repositories/grar")
adres_input = str(adres("Zelestraat 219, 9160 Lokeren"))

sparql.setQuery(adres_input)
sparql.setReturnFormat(RDF)
results = sparql.query().convert().decode('latin-1')

import rdflib
graph = rdflib.Graph()
graph.parse(data=results)

print(graph.serialize(format="turtle"))