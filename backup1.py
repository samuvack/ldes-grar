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

    
   



#REST API
#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        input = self.path[1:]
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
        if (perceel_json == '' && gebouweenheid_json == ''):
            json_output = 'Geen gekoppelde informatie van adres en perceel'
        else:
            json_output = perceel_json + ', ' + gebouweenheid_json
        
        self._set_response()
        self.wfile.write("{}".format(json_output).encode('utf-8'))
        
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
