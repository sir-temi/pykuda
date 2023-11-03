# PyKuda

A python package that simplifies using the Kuda Bank Api. While the Kuda Bank Api is quite easy to use, this python package makes it seamless and easy to enjoy the Kuda beautiful Open Api. PyKuda uses Kuda's Api v2 which uses an API key and Token for authentication.

## Getting started

### Install PyKuda

To use this package, install it using the package manager [pip](https://pip.pypa.io/en/stable/):

```bash
pip install pykuda
```

PyKuda has some dependencies which will be installed (requests and python-dotenv). `requests` is used by PyKuda to make http requests to Kuda's endpoints, while the `python-dotenv` is responsible for getting the environmental variables which has to be set for the requests to be authenticated; more to be discussed below.

### Create Environmental variables

After installation, the next thing is to create `.env` file where the environmental variables will be stored. Five variables are to be set in the `.env` file, and they are shown in an example below.

```shell
KUDA_KEY="Your Kuda Api Key"
TOKEN_URL="https://kuda-openapi.kuda.com/v2.1/Account/GetToken" # Kuda API v2.1 GetToken URL
REQUEST_URL="https://kuda-openapi.kuda.com/v2.1/" # Kuda API v2.1 Request URL
EMAIL="Your email used to register for the Kuda account"
MAIN_ACCOUNT_NUMBER="Your main Kuda account number"
```

NB: Please make sure you do not push your `.env` file to public repositories as the details here are confidential.

### Use PyKuda

```python
from pykuda.pykuda import PyKuda

kuda = PyKuda()
response = kuda.get_bank_list()

# response contains PyKudaResponse which has the status code and data.
```

### Understanding PyKudaResponse

Every Python request is filtered, and the resulting PyKudaResponse object contains three attributes: `status_code`, `data`, and `error`. It's crucial to consistently check the `error` attribute to confirm the success of the method.

Users should specifically validate that `error` is `False`. Despite Kuda returning a 200 HTTP response code, potential errors in the operation might exist. For example, when creating a virtual account with incorrect data, Kuda might respond with a 200 but set `status` to `False`. PyKuda handles this intelligently: if a 200 response is received but the `status` is `False`, PyKudaResponse is returned with `error` set to `True`. This mechanism aids in determining the success of the request.

#### Successful request

Using the response above as an example;

```shell
>>> response
>>> PyKudaResponse(status_code=200, data=[list_of_banks], error=False)
```

As seen above, the PyKudaResponse returns the status_code, data and error; the data is an already filtered data of which you can access directly by executing `response.data`.

#### Failed request

Incase the request wasn't successful, the PyKudaResponse will be different. The data will be a rRsponse Object which you can check to investigate the cause (Maybe your Token is not correct, or the URL, or something else.). Now, let's say the API Key in the .env file was not a correct one and a request was made, the example below shows the response to expect.

```shell
>>> response
>>> PyKudaResponse(status_code=401, data=<Response [401]>, error=True)
>>>
>>> respose.data.text # 'Invalid Credentials'
>>> respose.data.reason # 'Unauthorized'
```

## What else can PyKuda do?

PyKuda can be used to make other requests also, if you would like to learn more about how to use PyKuda to make other requests, please check the source code. Hopefully, I would be able to improve this documentation to show examples of how it can be used to make other requests. A list of request PyKuda can make are listed below.

`BANK_LIST`, `ADMIN_CREATE_VIRTUAL_ACCOUNT`, `RETRIEVE_VIRTUAL_ACCOUNT_BALANCE`, `ADMIN_RETRIEVE_MAIN_ACCOUNT_BALANCE`, `FUND_VIRTUAL_ACCOUNT`, `WITHDRAW_VIRTUAL_ACCOUNT`, `NAME_ENQUIRY`, `SINGLE_FUND_TRANSFER`, `VIRTUAL_ACCOUNT_FUND_TRANSFER`, `GET_BILLERS_BY_TYPE`, `VERIFY_BILL_CUSTOMER`, and `PURCHASE_BILL`.

Please refer to the [Kuda's Documentation](https://kudabank.gitbook.io/kudabank/) to read more about these requests.

## Contributions & Issues

-   If you would like to contribute and improve this package or it's documentation, please feel free to fork the repository, make changes and open a pull request.
-   If you encounter any issue or bugs, please open an issue.

## Author

-   [Kayode TemiTope](https://github.com/sir-temi)
