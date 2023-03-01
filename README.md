# Proof of Concept

In this Proof of Concept, an Rest API is developed that makes it possible to harvest information of building units and parcels via its address. The data of building units, parcels and addresses is available as Linked Data Event Streams.
First, the three Linked Data Event Streams are consumed and inserted into a GraphDB. Hereafter, a Sparql query provides for a linkage between these LDES'es.



## Start Docker of Apache Nifi and GraphDB
```
docker-compose up --build
```

## Load data flow in Apache Nifi

Apache Nifi will run on port 8443:8443/tcp\
https://localhost:8443

Login \
username: admin \
password: admin123456789

Apache NiFi flow (NiFi_Flow.json) can be added by sliding in a Process Group:\
![image](https://user-images.githubusercontent.com/15192194/221881399-d53deae0-7830-4a0c-a143-8784b32893d6.png)

![image](https://user-images.githubusercontent.com/15192194/221877896-3709f480-ea3a-41c8-b3d4-633c71f2db7f.png)



## Data in GraphDB

### Building units
![image](https://user-images.githubusercontent.com/15192194/221879850-3b89e274-1fe4-439e-8cc2-47477d03ba2a.png)
![image](https://user-images.githubusercontent.com/15192194/221898400-56a46d02-6d84-4c66-9610-63a23af37605.png)


### Parcels
![image](https://user-images.githubusercontent.com/15192194/221880584-8b966eaa-f2c0-4014-9ec5-5691c2ed631d.png)


# Sparql queries

all info of addresses:

```
PREFIX adres: <https://data.vlaanderen.be/id/adres/>

select * where { 
	adres:40000681 ?p ?o .
} limit 100 
```

all info of parcels:


```
select * where { 
	?perceel <https://basisregisters.vlaanderen.be/implementatiemodel/gebouwenregister#Adresseerbaar%20Object> ?adres .
}
```
![image](https://user-images.githubusercontent.com/15192194/222112272-db122f0f-7ad1-41da-aa5f-315bc4a8afc8.png)

```
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
    		    ?perceel ns:versieIdentificator ?versieIdentificator .
    			?perceel ?p ?output .}
   	#    		?perceel gebouwenregister:Perceel%3Astatus ?status .}
}
```

```
PREFIX perceel: <https://data.vlaanderen.be/id/perceel/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX ns: <https://data.vlaanderen.be/ns/generiek#>
PREFIX gebouwenregister: <https://basisregisters.vlaanderen.be/implementatiemodel/gebouwenregister#>

select * where { 
    OPTIONAL {	perceel:45502A0395-00H000 rdf:type ?type .
   				perceel:45502A0395-00H000 prov:generatedAtTime ?generatedAtTime .
    			perceel:45502A0395-00H000 ns:lokaleIdentificator ?lokaleIdentificator .
            	perceel:45502A0395-00H000 ns:naamruimte ?naamruimte .
    			perceel:45502A0395-00H000 ns:versieIdentificator ?versieIdentificator .
        		perceel:45502A0395-00H000 gebouwenregister:Perceel%3Astatus ?status .}
}
```
output:
![image](https://user-images.githubusercontent.com/15192194/222111537-8c51808a-a01d-468d-b628-0c5fb398a7ed.png)



all info of building units:

```
PREFIX adres: <https://data.vlaanderen.be/id/adres/>
PREFIX gebouw: <https://data.vlaanderen.be/id/gebouweenheid/>
PREFIX gebouweenheid: <https://data.vlaanderen.be/ns/gebouw#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX generiek: <https://data.vlaanderen.be/ns/generiek#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

select * where { 

gebouw:11337438 prov:generatedAtTime ?generatedAtTime .
gebouw:11337438 rdf:type ?type .
gebouw:11337438 gebouweenheid:Gebouweenheid.geometrie ?geometrie .
gebouw:11337438 gebouweenheid:Gebouweenheid.status ?status .
gebouw:11337438 gebouweenheid:functie ?functie .
gebouw:11337438 generiek:lokaleIdentificator ?lokaleIdentificator .
gebouw:11337438 generiek:naamruimte ?naamruimte .
gebouw:11337438 generiek:versieIdentificator ?versieIdentificator .  
    
}
```
output:
![image](https://user-images.githubusercontent.com/15192194/222107672-f67914a0-f818-43d7-ab96-05a552d8e13c.png)




combined:


