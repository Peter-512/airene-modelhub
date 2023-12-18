# modelhub

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m modelhub
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker build -t modelhub .
docker run -p 8000:8000 modelhub
```

## Deployment

- `az webapp create --resource-group int5 --plan modelhub --name modelhub --multicontainer-config-type compose --multicontainer-config-file deploy/docker-compose.yml`

We are deploying on azure, on plan B1.
This is a highly scalable part of the application where a lot of the important
prediction and classification logic resides.

## Project structure

```bash
$ tree "modelhub"
modelhub
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
├── core # Where all the logic lives
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "MODELHUB_" prefix.

For example if you see in your "modelhub/settings.py" a variable named like
`random_parameter`, you should provide the "MODELHUB_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by
overriding `env_prefix` property
in `modelhub.settings.Settings.Config`.

An example of .env file:

```bash
MODELHUB_RELOAD="True"
MODELHUB_PORT="8000"
MODELHUB_ENVIRONMENT="dev"
```

You can read more about BaseSettings class
here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:

* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);

You can read more about pre-commit here: https://pre-commit.com/

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine.

2. Run the pytest.

```bash
pytest -vv .
```
