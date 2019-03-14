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

## Building
Build a Kees Docker container with:

    npm run build
    docker build -t registry.gitlab.com/delta10/kees:latest .
    docker push registry.gitlab.com/delta10/kees:latest

## Deploying
You can easily deploy (or update) kees with:

    helm upgrade --install kees ./helm --namespace kees

