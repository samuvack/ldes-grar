# Proof of Concept

![image](https://user-images.githubusercontent.com/15192194/221877896-3709f480-ea3a-41c8-b3d4-633c71f2db7f.png)




# Apache NiFi SPARQL put processor

A processor that materialises an LDES stream into a triplestore.

# Build the NAR file (Jar for NiFi)
```
mvn package
```
This will result in a NAR file being written to the 'release' folder. This folder is shared with the NiFi docker container.

# Download the NiFi client
Download the latest LDES NiFi Processor, and put in 'release' folder
e.g. https://github.com/Informatievlaanderen/VSDS-LDESClient-NifiProcessor/packages/1581623

# Run the stack
```
docker-compose up
```
