# Password Management

> Password Management System. Uses Argon2 for hashing passwords in sqlite database

## Getting Started

The project uses [Pipenv](https://github.com/pypa/pipenv) to make it easier dealing with dependencies. Follow the 

### Using `pipenv`

Ensure you have `pipenv` installed, please see the [pipenv readme](https://github.com/pypa/pipenv/#installation). Once `pipenv` is setup, follow the steps in the [**Install** section](#Install).

### Using `venv`

In the project root, run the following

```sh
python3 -m venv env

# or, if python3 is default
python -m venv env
```

Activate your virtual environment:

```sh
source env/bin/activate

# or
source env/bin/activate.fish   # (pick extension for your shell e.g. .fish, .csh)
```

Ensure that `virtualenv` is setup properly:

```sh
which python
# You should see something like this: ./env/bin/python
```

To exit `virtualenv`:

```sh
deactivate
```

## Install

### With `pipenv`

```sh
pipenv install
```

That will take care of installing project dependencies as well as setting up a `virtualenv` for the project.

### With `virtualenv`

```sh
pip install -r requirements.txt
```

## Usage

### `pipenv`

To run `enroll` program:

```sh
pipenv run enroll <username> <password>
```

To run `authenticate` program:

```sh
pipenv run authenticate <username> <password>
```

### `virtualenv`

To run `enroll` program:

```sh
python password_management/enroll <username> <password>
```

To run `authenticate` program:

```sh
pipenv password_management/authenticate <username> <password>
```

## Run tests

### `pipenv`

```sh
pipenv run test
```

### `virtualenv`

```sh
python test/runner.py
```

## Author

**Artem Golovin**
