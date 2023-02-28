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

Login\
username: admin\
password: admin123456789\

Apache NiFi flow (NiFi_Flow.json) can be added by sliding in a Process Group:\
![image](https://user-images.githubusercontent.com/15192194/221881399-d53deae0-7830-4a0c-a143-8784b32893d6.png)

![image](https://user-images.githubusercontent.com/15192194/221877896-3709f480-ea3a-41c8-b3d4-633c71f2db7f.png)



## Data in GraphDB

### Building units
![image](https://user-images.githubusercontent.com/15192194/221879850-3b89e274-1fe4-439e-8cc2-47477d03ba2a.png)


### Parcels
![image](https://user-images.githubusercontent.com/15192194/221880584-8b966eaa-f2c0-4014-9ec5-5691c2ed631d.png)
