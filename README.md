# literate-disco
Given an appropriately-formatted log file, this service will happily present a JSON endpoint at /stats that will share a bunch of interesting stats about those logs.

# How to use
It is expected that your logs are standard Apache access logs and are in a directory ./logs.

The service is presented as a docker container.  To start it, run the following command:
```
docker run -d --name literate-disco -p 8080:8080 -v logs:/data kalemeow/literate-disco:latest filename-to-parse.log
```    
Once the container is up and running, you can access the stats page at http://localhost:8080/stats .
