# Kees
[![pipeline status](https://gitlab.com/delta10/kees/badges/master/pipeline.svg)](https://gitlab.com/delta10/kees/commits/master)

[![coverage report](https://gitlab.com/delta10/kees/badges/master/coverage.svg)](https://gitlab.com/delta10/kees/commits/master)

Kees is a minimalistic case management solution.

## Preparing
First install the npm dependencies with:

    npm install

Then run the npm build command with:

    npm run build

Now create the database with:

    python manage.py migrate

And create a superuser with:

    python manage.py createsuperuser

## Developing
Run a watch server with:

    python manage.py runserver
