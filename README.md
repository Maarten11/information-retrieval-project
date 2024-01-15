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

If you want to run the project 'locally' without using docker,
PyLucene should be installed in your environment.
Instructions for this can be found [here](https://lucene.apache.org/pylucene/install.html).

### Datasets

For an explanation of the needed data,
look in the [data directory](./data/README.md).

## Running the project

The data should first properly be set up as explained [here](./data/README.md).

### Webserver backend

```
docker compose build
docker compose up
```

#### Locally

For running the backend without docker use following commands.
Note that PyLucene must be properly set up.

```
cd src
pip install -r requirements.txt
python app.py
```

### Frontend

```
cd frontend
# Install required npm packages
npm i

# Run the frontend (in dev mode)
npm run dev
```
