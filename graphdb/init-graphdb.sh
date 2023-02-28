#!/bin/bash -ex
curl -X POST http://localhost:7200/rest/repositories -H 'Content-Type: multipart/form-data' -F config=@vsds-repo.ttl
