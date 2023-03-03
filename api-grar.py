# Python script that retrieves RDF members out GraphDB via Sparql query

from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, CSV, RDF
from rdflib import Graph
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import pandas as pd

import json 

def gebouweenheid (input):

    # define the SPARQL query to retrieve RDF members
    gebouweenheid = """
    PREFIX adres: <https://data.vlaanderen.be/id/adres/>
    PREFIX gebouw: <https://data.vlaanderen.be/id/?gebouweenheid/>
    PREFIX gebouweenheid: <https://data.vlaanderen.be/ns/gebouw#>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX generiek: <https://data.vlaanderen.be/ns/generiek#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>


    select * where { 
        ?gebouweenheid <https://data.vlaanderen.be/ns/gebouw#Gebouweenheid.adres> <https://data.vlaanderen.be/id/adres/""" + str(input) + """> .

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
    }"""
    return gebouweenheid


def percelen(input):
    perceel= """

PREFIX gebouwregister: <https://basisregisters.vlaanderen.be/implementatiemodel/gebouwenregister#>
PREFIX adres: <https://data.vlaanderen.be/id/adres/>
PREFIX perceel: <https://data.vlaanderen.be/id/perceel/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX ns: <https://data.vlaanderen.be/ns/generiek#>

select * where { 
	?perceel gebouwregister:Adresseerbaar%20Object adres:"""+ str(input) + """ .
    OPTIONAL {	?perceel rdf:type ?type .
      			?perceel prov:generatedAtTime ?generatedAtTime .
   				?perceel ns:lokaleIdentificator ?lokaleIdentificator .
            	?perceel ns:naamruimte ?naamruimte .
    		    ?perceel ns:versieIdentificator ?versieIdentificator .}
   	#    		?perceel gebouwenregister:Perceel%3Astatus ?status .}
}


"""
    return perceel

def adres(input):
    adres =   '''
    PREFIX generiek:      <https://data.vlaanderen.be/ns/generiek#>
    PREFIX locn:          <https://www.w3.org/ns/locn#> 
    PREFIX geosparql:     <http://www.opengis.net/ont/geosparql#>
    PREFIX adres: <https://data.vlaanderen.be/ns/adres#>
    PREFIX prov: <http://www.w3.org/ns/prov#>

    select ?generatedAtTime ?naamruimte ?lokaleIdentificator ?versieIdentificator ?huisnummer ?locatie ?gemeente ?heeftPostinfo ?adresstatus ?officieelToegekend ?straat        where { 
    ?genid adres:volledigAdres "'''+ str(input) + '''"@nl .
	OPTIONAL { ?adres_id adres:isVerrijktMet ?genid .
    ?adres_id prov:generatedAtTime ?generatedAtTime .
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
} } limit 1 '''
    return adres
    
#REST API
#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/ld+json')
        self.end_headers()

    def do_GET(self):
        
        #ADRES INFO
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        input = self.path[1:]
        # connect to the GraphDB repository using the URL of the SPARQL endpoint
        sparql = SPARQLWrapper("http://localhost:7200/repositories/grar")
        adres_input = str(adres(input)).replace('%20', ' ')
        #print(adres_input)
        # set the SPARQL query and response format
        sparql.setQuery(adres_input)
        sparql.setReturnFormat(RDF)
        results = str(sparql.query().convert().decode('latin-1'))
        print(results)
        data = results.splitlines()
        if (len(data)==1):
            adres_json = ''
            output = 'Geen informatie in GraphDB'
        else :
            data = dict(zip(data[0].split(","), data[1].split(",")))
            adres_json = json.dumps(data, indent = 4) 
            id = data.get('lokaleIdentificator')
            input = id
            # connect to the GraphDB repository using the URL of the SPARQL endpoint
            sparql = SPARQLWrapper("http://localhost:7200/repositories/grar")
            gebouw_input = gebouweenheid(input)
            # set the SPARQL query and response format
            sparql.setQuery(gebouw_input)
            sparql.setReturnFormat(RDF)
            results = str(sparql.query().convert().decode('latin-1'))
            data = results.splitlines()
            if (len(data)==1):
                gebouweenheid_json = ''
            else :
                print('DIT ZIJN DE RESULTATEN :', results)
                data = dict(zip(data[0].split(","), data[1].split(",")))
                gebouweenheid_json = json.dumps(data, indent = 4) 
            print(gebouweenheid_json)
            
            sparql = SPARQLWrapper("http://localhost:7200/repositories/grar")
            perceel_input = percelen(input)
            # set the SPARQL query and response format
            sparql.setQuery(perceel_input)
            sparql.setReturnFormat(RDF)
            results = str(sparql.query().convert().decode('latin-1'))
            print('DIT ZIJN DE RESULTATEN :', results)
            data = results.splitlines()
            print('BESTAAT DIT?', len(data))
            if (len(data)==1):
                perceel_json = ''
            else :
                data = dict(zip(data[0].split(","), data[1].split(",")))
                perceel_json = json.dumps(data, indent = 4) 
            print(perceel_json)
            
            if (gebouweenheid_json == ''):
                json_output = perceel_json
            if (perceel_json == ''):
                json_output = gebouweenheid_json
            if (perceel_json == '' and gebouweenheid_json == ''):
                json_output = 'Geen gekoppelde informatie van adres en perceel'
            else:
                json_output = perceel_json + ', ' + gebouweenheid_json
            
            output = adres_json + ', ' + json_output
        

        self._set_response()
        self.wfile.write("{}".format(output).encode('utf-8'))
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('REST API server started on localhost:8080\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
