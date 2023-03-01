# Python script that retrieves RDF members out GraphDB via Sparql query

from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, CSV, RDF
from rdflib import Graph
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import pandas as pd


# connect to the GraphDB repository using the URL of the SPARQL endpoint
sparql = SPARQLWrapper("http://localhost:7200/repositories/grar")

# define the SPARQL query to retrieve RDF members
gebouweenheid = """
PREFIX adres: <https://data.vlaanderen.be/id/adres/>
PREFIX gebouw: <https://data.vlaanderen.be/id/?gebouweenheid/>
PREFIX gebouweenheid: <https://data.vlaanderen.be/ns/gebouw#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX generiek: <https://data.vlaanderen.be/ns/generiek#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>


select * where { 
	?gebouweenheid <https://data.vlaanderen.be/ns/gebouw#Gebouweenheid.adres> <https://data.vlaanderen.be/id/adres/1864311> .

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
"""

perceel= """

PREFIX gebouwregister: <https://basisregisters.vlaanderen.be/implementatiemodel/gebouwenregister#>
PREFIX adres: <https://data.vlaanderen.be/id/adres/>
PREFIX perceel: <https://data.vlaanderen.be/id/perceel/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX ns: <https://data.vlaanderen.be/ns/generiek#>

select * where { 
	?perceel gebouwregister:Adresseerbaar%20Object adres:2327687 .
    OPTIONAL {	?perceel rdf:type ?type .
      			?perceel prov:generatedAtTime ?generatedAtTime .
   				?perceel ns:lokaleIdentificator ?lokaleIdentificator .
            	?perceel ns:naamruimte ?naamruimte .
    		    ?perceel ns:versieIdentificator ?versieIdentificator .}
   	#    		?perceel gebouwenregister:Perceel%3Astatus ?status .}
}


"""

# set the SPARQL query and response format
sparql.setQuery(gebouweenheid)
sparql.setReturnFormat(RDF)

# execute the SPARQL query and parse the results into an RDF graph
results = str(sparql.query().convert())
data = results.replace("\\r\\n", "\\n")
data = data.splitlines("\\n")

print(data)
#graph = Graph().parse(data=results.serialize(format='turtle'), format='turtle')

# iterate over the RDF triples in the graph and print them
#for s, p, o in graph:
#    print(s, p, o)

"""

#REST API
#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/rdf')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("{}".format(results).encode('utf-8'))
        
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
"""