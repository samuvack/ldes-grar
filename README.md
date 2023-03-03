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

all info of an address:

```
PREFIX generiek:      <https://data.vlaanderen.be/ns/generiek#>
PREFIX locn:          <https://www.w3.org/ns/locn#> 
PREFIX geosparql:     <http://www.opengis.net/ont/geosparql#>
PREFIX adres: <https://data.vlaanderen.be/ns/adres#>
PREFIX prov: <http://www.w3.org/ns/prov#>

select ?generatedAtTime ?naamruimte ?lokaleIdentificator ?versieIdentificator ?huisnummer ?locatie ?gemeente ?heeftPostinfo ?adresstatus ?officieelToegekend ?straat        where { 
    ?genid adres:volledigAdres "Amsterdamstraat 18, 2000 Antwerpen"@nl .
	?adres_id adres:isVerrijktMet ?genid .
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
} 
```
![image](https://user-images.githubusercontent.com/15192194/222476055-e8e6ebae-c913-4750-b30f-9519eecefc82.png)

```
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
```


<https://data.vlaanderen.be/id/adres/1239307> <https://data.vlaanderen.be/ns/adres#volledigAdres> "Zelestraat 219, 9160 Lokeren"@nl .
<https://data.vlaanderen.be/id/adres/1239307> <https://data.vlaanderen.be/ns/generiek#naamruimte> "https://data.vlaanderen.be/id/adres" .
<https://data.vlaanderen.be/id/adres/1239307> <https://data.vlaanderen.be/ns/generiek#lokaleIdentificator> "1239307" .
<https://data.vlaanderen.be/id/adres/1239307> <https://data.vlaanderen.be/ns/generiek#versieIdentificator> "2022-04-28T08:20:26+02:00" .
<https://data.vlaanderen.be/id/adres/1239307> <https://data.vlaanderen.be/ns/adres#huisnummer> "219" .
<https://data.vlaanderen.be/id/adres/1239307> <http://www.opengis.net/ont/geosparql#asGML> "<gml:Point srsName=\"http://www.opengis.net/def/crs/EPSG/0/31370\" xmlns:gml=\"http://www.opengis.net/gml/3.2\"><gml:pos>124491.27 19
8750.89</gml:pos></gml:Point>"^^<http://www.opengis.net/ont/geosparql#gmlLiteral> .
<https://data.vlaanderen.be/id/adres/1239307> <https://data.vlaanderen.be/ns/adres#heeftGemeentenaam> "Lokeren"@nl .
<https://data.vlaanderen.be/id/adres/1239307> <https://data.vlaanderen.be/ns/adres#Straatnaam> "Zelestraat"@nl .
<https://data.vlaanderen.be/id/adres/1239307> <https://data.vlaanderen.be/ns/adres#officieelToegekend> "true"^^<http://www.w3.org/2001/XMLSchema#boolean> .
<https://data.vlaanderen.be/id/adres/1239307> <https://data.vlaanderen.be/ns/adres#heeftPostinfo> <https://data.vlaanderen.be/id/postinfo/9160> .
<https://data.vlaanderen.be/id/adres/1239307> <https://data.vlaanderen.be/ns/adres#Adres.status> <https://data.vlaanderen.be/id/conceptscheme/adresstatus/inGebruik> .

![image](https://user-images.githubusercontent.com/15192194/222680930-d793be66-c489-4c67-b67e-b7bd92d1d54e.png)


address:
![image](https://user-images.githubusercontent.com/15192194/222463320-c93fbfcb-1bba-42b4-a45a-53e75bef6715.png)

```
select * where { 
	?genid <https://data.vlaanderen.be/ns/adres#volledigAdres> "Amerikalei 152, 2000 Antwerpen"@nl .
   
    
}
```

all info of parcels based on addres:


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
    		    ?perceel ns:versieIdentificator ?versieIdentificator .}
   	#    		?perceel gebouwenregister:Perceel%3Astatus ?status .}
}
```
![image](https://user-images.githubusercontent.com/15192194/222114448-bfa79db4-b199-419f-82af-a09234ca1996.png)



all info of building units:

```
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

```
output:
![image](https://user-images.githubusercontent.com/15192194/222118282-a87550be-1dfc-463a-bcc6-a393d2c3af79.png)


