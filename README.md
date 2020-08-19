# literate-disco
Given an Apache combinedlog-formatted log file, this service will happily present a JSON endpoint at /stats that will share a bunch of interesting stats about those logs.

# How to use - quickstart
It is expected that your logs are standard Apache access logs and are in a directory `logs/`.

The service is presented as a docker container.  To start it, run the following command, replacing the last parameter with the name of the logfile in the logs dir you wish to parse and serve:
```
docker run --rm --name literate-disco -p 8080:5000 --mount src=$(pwd)/logs,target=/data,type=bind kalemeow/literate-disco:latest python3 /main.py access_log_20190520-125058.log

```    
Once the container is up and running, you can access the stats page at http://localhost:8080/stats .

To stop the service, hit ctrl-c.

# Build your own container
If you wish to build your own container instead of using the upstream dockerhub-hosted container, you can do so by running
```
docker build . -t kalemeow/literate-disco
```
and then running the service as described above.

# Data structure
The JSON blob returned by a request to http://localhost:8080/stats will contain the following:
```
{
    "response_codes_cnt": # dict, distribution of HTTP status codes returned
    "top_referers_GET_cnt": # dict, top 5 referrers for GET requests
    "hits_per_ip_cnt": # dict, map of IP address to number of requests
    "ips_uniq_cnt": # int, count of unique IP addresses
}
```

Example client queries with python:
```
import requests
r = requests.get("http://localhost:8080/stats")

response_codes_cnt = r.json()['response_codes_cnt']
print(response_codes_cnt)
# {u'200': 9003, u'404': 424, u'500': 200, u'301': 373}

hits_per_ip_cnt = r.json()['hits_per_ip_cnt']
print(hits_per_ip_cnt)
# {u'164.89.12.20': 1, u'192.88.108.64': 1, ... }

ips_uniq_cnt = r.json()['ips_uniq_cnt']
print(ips_uniq_cnt)
# 9884

top_referers_GET_cnt = r.json()['top_referers_GET_cnt']
print(top_referers_GET_cnt)
# {u'http://www.garcia.com/': 4, u'https://www.johnson.com/': 5, u'https://smith.com/': 4, u'https://johnson.com/': 5, u'https://www.williams.com/': 4}
```
