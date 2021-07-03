# Yield Volatility Oracle

This repository contains the [external adapter](https://docs.chain.link/docs/developers/) application code for Yield Volatility Oracle. 
Reference to this project [here](https://www.notion.so/Yield-Volatility-Oracle-derivatives-base-on-volatility-1e2bbc14669a464b84f8a85706a0489c)

## Development and running
The development environment is managed by docker-compose. The application code is mounted in a volume using docker compose meaning while running the application you're able edit the code while the application is running thanks to the use of uvicorn 
```
echo 'API_KEY=${DESIRED API KEY}' > .env.local
docker-compose build  
~~
docker-compose up 
```
The external-adapter/api can then be accessed at http://localhost:8000/docs
Currently there is an empty .env.local file, in the future this file may contain secrets for The Graph sub graphs 

### Python dependencies 
Python dependencies are managed by [poetry](https://python-poetry.org/). In order to add a new python dependency or package run the following:
```
poetry add $PACKAGE
```
This will require that you have poetry installed locally. In order to get your newly added dependency into the container you will need to run a docker-compose build again, luckily this should take less than 2 minutes. 