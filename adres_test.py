
from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, CSV, RDF
from rdflib import Graph
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import pandas as pd
import json

def adres(input):
    adres = '''
PREFIX generiek:      <https://data.vlaanderen.be/ns/generiek#>
PREFIX geosparql:     <http://www.opengis.net/ont/geosparql#>
PREFIX adres: <https://data.vlaanderen.be/ns/adres#>
PREFIX prov: <http://www.w3.org/ns/prov#>

CONSTRUCT {
    ?adres_id adres:volledigAdres ?adresVolledig .
}

where {
?adres_id generiek:lokaleIdentificator "''' + str(input) + '''" .
OPTIONAL {
?adres_id adres:isVerrijktMet ?genid .
?genid adres:volledigAdres ?adresVolledig .
 } }
    '''
    return adres


def perceel(input):
    perceel = '''
    
    
    PREFIX gebouwregister: <https://basisregisters.vlaanderen.be/implementatiemodel/gebouwenregister#>
PREFIX adres: <https://data.vlaanderen.be/id/adres/>
PREFIX perceel: <https://data.vlaanderen.be/id/perceel/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX ns: <https://data.vlaanderen.be/ns/generiek#>

CONSTRUCT{
    
?perceel rdf:type ?type .
?perceel prov:generatedAtTime ?generatedAtTime .
?perceel ns:lokaleIdentificator ?lokaleIdentificator .
?perceel ns:naamruimte ?naamruimte .
?perceel ns:versieIdentificator ?versieIdentificator .




} where {
	?perceel gebouwregister:Adresseerbaar%20Object adres:'''+ str(input) + ''' .
    OPTIONAL {	?perceel rdf:type ?type .
      			?perceel prov:generatedAtTime ?generatedAtTime .
   				?perceel ns:lokaleIdentificator ?lokaleIdentificator .
            	?perceel ns:naamruimte ?naamruimte .
    		    ?perceel ns:versieIdentificator ?versieIdentificator .}
   	#    		?perceel gebouwenregister:Perceel%3Astatus ?status .}
}
    
    '''
    return perceel

def gebouw (input):
    gebouw = '''
    
    PREFIX adres: <https://data.vlaanderen.be/id/adres/>
PREFIX gebouw: <https://data.vlaanderen.be/id/?gebouweenheid/>
PREFIX gebouweenheid: <https://data.vlaanderen.be/ns/gebouw#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX generiek: <https://data.vlaanderen.be/ns/generiek#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>


construct {
?gebouweenheid prov:generatedAtTime ?generatedAtTime .
?gebouweenheid rdf:type ?type .
?gebouweenheid gebouweenheid:Gebouweenheid.geometrie ?geometrie .
?gebouweenheid gebouweenheid:Gebouweenheid.status ?status .
?gebouweenheid gebouweenheid:functie ?functie .
?gebouweenheid generiek:lokaleIdentificator ?lokaleIdentificator .
?gebouweenheid generiek:naamruimte ?naamruimte .
?gebouweenheid generiek:versieIdentificator ?versieIdentificator .  
    
    
    
    
} where { 
	?gebouweenheid <https://data.vlaanderen.be/ns/gebouw#Gebouweenheid.adres> <https://data.vlaanderen.be/id/adres/''' + str(input) + '''> .

    OPTIONAL{
    ?gebouweenheid prov:generatedAtTime ?generatedAtTime .
	?gebouweenheid rdf:type ?type .
	?gebouweenheid gebouweenheid:Gebouweenheid.geometrie ?geometrie .
	?gebouweenheid gebouweenheid:Gebouweenheid.status ?status .
	?gebouweenheid gebouweenheid:functie ?functie .
	?gebouweenheid generiek:lokaleIdentificator ?lokaleIdentificator .
	?gebouweenheid generiek:naamruimte ?naamruimte .
	?gebouweenheid generiek:versieIdentificator ?versieIdentificator .  

}
}
    
    
    
    
    '''
    return gebouw


sparql = SPARQLWrapper("http://localhost:7200/repositories/grar")
adres_input = adres("1043869")

sparql.setQuery(adres_input)
sparql.setReturnFormat(RDF)
results = sparql.query().convert().decode('latin-1')
print(results)
import rdflib
graph = rdflib.Graph()
graph.parse(data=results)
print(graph.serialize(format="turtle"))

sparql = SPARQLWrapper("http://localhost:7200/repositories/grar")

gebouw_input = gebouw(1043869)
print(gebouw_input)
sparql.setQuery(gebouw_input)
sparql.setReturnFormat(RDF)
gebouw_results = sparql.query().convert().decode('latin-1')
print(gebouw_results)
graph.parse(data=gebouw_results)
print(graph.serialize(format="turtle"))


perceel_input = perceel(1043869)
print(perceel_input)
sparql.setQuery(perceel_input)
sparql.setReturnFormat(RDF)
gebouw_results = sparql.query().convert().decode('latin-1')
print(gebouw_results)
graph.parse(data=gebouw_results)
print(graph.serialize(format="turtle"))
