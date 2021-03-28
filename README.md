# Alita Explorer

Alita Explorer is the main dashboar of computing network. The front end is developed based on burst explorer, which adds information display to the computing network. The back-end developed an api service based on django in python.

## How to run

`cp .env.default .env`

Configure your .env:

See [DB ENGINES PARAMS](https://docs.djangoproject.com/en/2.2/ref/settings/#engine)

DB_JAVA_WALLET required read-only access.

See additional info about set up DB [here](java_wallet)

See [CACHE PARAMS](https://docs.djangoproject.com/en/2.2/topics/cache/)

See comments in .env

`docker-compose up`
