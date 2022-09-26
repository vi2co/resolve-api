# Response app
## Start the app
In order to start development environment Docker and docker-compose and jq (for better visual
representation) should be installed.

The environment can be launching the following command in the root directory of this repository:
```
docker-compose up
```
Docker compose will build the Dockerfile for the application and expose 3000 port to the host.\
The easiest was to test the rest api is to run curl commands:

Root path ("/"):
```
$ curl -s http://127.0.0.1:3000/ | jq .
{
  "date": 1664167879,
  "kubernetes": "false",
  "version": "0.1.0"
}
```

DNS lookup path /v1/tools/lookup path:
```
$ curl -s http://127.0.0.1:3000/v1/tools/lookup?domain=amazon.com | jq .
{
  "addresses": [
    "52.94.236.248",
    "54.239.28.85",
    "205.251.242.103"
  ],
  "client_ip": "192.168.112.1",
  "created_at": 1664168008,
  "domain": "amazon.com"
}
```
IPv4 validate path /v1/tools/validate:
```
# valide IPv4 address
$ curl -s -d "ip=192.255.255.255" -X POST http://127.0.0.1:3000/v1/tools/validate | jq .
{
  "status": true
}
# wrong IPv4 address
vs@rog:~/Work/Stakefish$ curl -s -d "ip=192.255.255.355" -X POST http://127.0.0.1:3000/v1/tools/validate | jq .
{
  "status": false
} 
```
Successful responses history /v1/tools/history:
```
$ curl -s http://127.0.0.1:3000/v1/tools/history | jq .
[
  {
    "addresses": [
      "20.84.181.62",
      "20.103.85.33",
      "20.53.203.50",
      "20.112.52.29",
      "20.81.111.85"
    ],
    "client_ip": "192.168.112.1",
    "created_at": "1664168268",
    "domain": "microsoft.com"
  },
  {
    "addresses": [
      "76.76.21.21"
    ],
    "client_ip": "192.168.112.1",
    "created_at": "1664168263",
    "domain": "bind.com"
  },
  {
    "addresses": [
      "151.101.1.69",
      "151.101.193.69",
      "151.101.65.69",
      "151.101.129.69"
    ],
    "client_ip": "192.168.112.1",
    "created_at": "1664168256",
    "domain": "stackoverflow.com"
  },
  {
    "addresses": [
      "74.6.143.26",
      "74.6.143.25",
      "74.6.231.21",
      "98.137.11.163",
      "98.137.11.164",
      "74.6.231.20"
    ],
    "client_ip": "192.168.112.1",
    "created_at": "1664168235",
    "domain": "yahoo.com"
  },
  {
    "addresses": [
      "142.251.46.206"
    ],
    "client_ip": "192.168.112.1",
    "created_at": "1664168227",
    "domain": "google.com"
  }
]
```
