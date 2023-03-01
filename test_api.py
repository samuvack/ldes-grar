# Python script that retrieves RDF members out GraphDB via Sparql query

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph


# connect to the GraphDB repository using the URL of the SPARQL endpoint
sparql = SPARQLWrapper("http://localhost:7200/repositories/grar")

# define the SPARQL query to retrieve RDF members
query = """
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o .
} 
LIMIT 100
"""

# set the SPARQL query and response format
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

# execute the SPARQL query and parse the results into an RDF graph
results = sparql.query().convert()
print(results)
graph = Graph().parse(data=results.serialize(format='turtle'), format='turtle')

# iterate over the RDF triples in the graph and print them
for s, p, o in graph:
    print(s, p, o)

