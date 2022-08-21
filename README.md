# PyKuda

A python package that simplifies using the Kuda Bank Api. While the Kuda Bank Api is quite easy to use, this python package makes it seamless and easy to enjoy Kuda beautiful Open Api. PyKuda uses Kuda's Api v2 two which uses an API key and Token for authentication.

# Getting started

## Install PyKuda

To use this package, use the package manage [pip](https://pip.pypa.io/en/stable/) to install PyKuda.

```bash
pip install pykuda
```

PyKuda has some dependencies which will be installed (requests and python-dotenv). `requests` is used by PyKuda to make http requests to Kuda's endpoints, while the `python-dotenv` is responsible for getting the environmental variables which has to be set for the requests to be authenticated; more to be discussed below.

## Create Environmental variables

After installation, the next thing is to create `.env` file where the environmental variables will be stored. Five variables are to be set in the `.env` file, and they are shown in an example below.

```shell
KUDA_KEY="Your Kuda Api Key"
TOKEN_URL="Kuda API v2 Get Token endpoint"
REQUEST_URL="Kuda API v2 Endpoint"
EMAIL="Your email used to register for the Kuda account"
MAIN_ACCOUNT_NUMBER="Your main Kuda account number"
```

NB: Please make sure you do not push your .env files to public repositories as the details here are confidential.

## Use PyKuda

It is now time to use PyKuda.

```python
from pykuda.pykuda import PyKuda

kuda = PyKuda()
banks = kuda.get_bank_list()

```
