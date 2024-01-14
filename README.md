# Information Retrieval Project

This is the project for the 2023-2024 Information Retrieval course (_UA_2001WETINR_2324_) at the University of Antwerp.
The project is made by Maarten and Sander.

## Requirements

The project uses [PyLucene](https://lucene.apache.org/pylucene/) to be able to use lucene in python.

For convenience, docker is used to run the project so that PyLucene does not need to be installed locally.

The project also contains a frontend created using [Vue.js](https://vuejs.org/).

Requirements:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [npm](https://www.npmjs.com/package/npm)

### Datasets

For an explanation of the needed data,
look in the [data directory](./data/README.md).

## Running the project

### Webserver backend

```
docker compose build
docker compose up
```

### Frontend

```
cd frontend
# Install required npm packages
npm i

# Run the frontend (in dev mode)
npm run dev
```
