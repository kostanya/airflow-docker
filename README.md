# airflow-docker
This repository contains the docker-compose file for automated execution of a set of tasks, the mysql init script, and python scripts for DAGs to execute these tasks.

## To run airflow in docker with mysql as backend
1. If you don't have Docker Desktop Application, download it from [here](https://docs.docker.com/get-docker/).
2. Clone this repo and run docker-compose as follows: 
```bash
docker-compose up -d
```
Here the -d flag indicates detached mode. In this mode containers run in the background.

3. You should be able to see the running containers with the command below.
```bash
docker ps
```
4. In order to launch the airflow webserver, go to ```localhost:8080```. Credentials are both `kartaca`. There you can see the DAGs.
5. You can use any database tool you want to connect to the database. (I suggest [DBeaver](https://dbeaver.io/).) Database, username and password fields must be filled as `kartaca` and port must be set to `3306` in order to establish the connection. 
6. Triggered DAGs will cause changes in the database tables.


**Note:** If port 3306 is in use, you can make the following modifications in the code:
- Change services -> mysql -> ports to `3307:3306` from `3306:3306` in the docker-compose file.
- Change the connection ports in python scripts under the dags folder to `3307` from `3306`.
- When making a database connection via a database tool, enter the port as `3307` instead of `3306`.






