# VRP Challenge

This application aims to simplify the VRP (Vehicle Orientation Problem) output solved by vroom and to enable it to be used as a microservice. It uses a simple flask http router for python(3.5+) to achieve this. The router can be used in any of the following ways:
* Standalone Python App
* Single Docker Container
* Docker-Compose with vroom Dependency

# Usage

### Standalone Python App

It can be run as standalone with the following command

```sh
pip install -r requirements.txt
python app.py
```

By editing config.yml, vroom configuration and application port can be set.

### Single Docker Container

```sh
docker run -d -p 5000:5000 -v $(pwd)/router-conf/:/conf erdemuysal/vrprouter:latest
```

By editing router-conf/config.yml, vroom configuration and application port can be set.

### Docker-Compose with vroom Dependency

```sh
cd compose
docker-compose up -d
```

By editing compose/router-conf/config.yml, vroom configuration and application port can be set.

# Tests

The tests of the application can be run with the following command. For the tests work correctly, the vroom configuration in config.yml must be done correctly and vroom must be accessible.

```sh
pip install -r requirements.txt
python app_tests.py
```

# Docker Image Build

If you want to create the docker image, run the command below.

```sh
docker build -t erdemuysal/vrprouter:1.0.0 .
```


