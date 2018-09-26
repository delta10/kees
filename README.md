# Kees
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
