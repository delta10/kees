# Kees
Kees is a minimalistic case management solution.

## Preparing
First install the npm dependencies with:

```bash
cd frontend/
npm install
```

Next install the Pyton dependencies with:
```bash
cd ../
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Now create the database with:

```bash
cd ../
python manage.py migrate
```

(Optionally) load the test data with:

```bash
python manage.py loaddata fixtures/testdata.json
```

Create a superuser with:

```bash
python manage.py createsuperuser
```

## Developing
Run a frontend watch server with:

```bash
cd frontend/
npm run serve
```

And a backend watch server with:

```bash
cd ../
python manage.py runserver
```

## Testing
Run the unit tests with:

```bash
( cd frontend/ && npm run test )
python manage.py test
```

## Contributing

Contributions are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md) for more details. By contributing to this project, you accept and agree the the terms and conditions as specified in the [Contributor Licence Agreement](CLA.md).

## Licence

The software is distributed under the EUPLv1.2 licence, see the [LICENCE](LICENCE) file.
