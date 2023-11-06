# PyKuda

[![Downloads](https://static.pepy.tech/badge/pykuda)](https://pepy.tech/project/pykuda) [![Downloads](https://static.pepy.tech/badge/pykuda/month)](https://pepy.tech/project/pykuda) [![Downloads](https://static.pepy.tech/badge/pykuda/week)](https://pepy.tech/project/pykuda)

A python package that simplifies using the Kuda Bank API. While the Kuda Bank Api is quite easy to use, this python package makes it seamless and easy to enjoy the Kuda beautiful Open Api. PyKuda uses Kuda's Api v2 which uses an API key and Token for authentication.

## Getting started

### Install PyKuda

To use this package, install it using the package manager [pip](https://pip.pypa.io/en/stable/):

```bash
pip install pykuda
```

PyKuda has some dependencies which will be installed (requests and python-decouple). `requests` is used by PyKuda to make http requests to Kuda's endpoints, while the `python-decouple` is responsible for getting the environmental variables which has to be set for the requests to be authenticated; more to be discussed below.

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

### Using PyKuda

```python
from pykuda.pykuda import PyKuda

kuda = PyKuda()
response = kuda.banks_list()
print(response)
# Example Response:
# PyKudaResponse(status_code=200, data=[list_of_banks], error=False)
```

### Understanding PyKudaResponse

Every Python request is filtered, and the resulting PyKudaResponse object contains three attributes: `status_code`, `data`, and `error`. It's crucial to consistently check the `error` attribute to confirm the success of the method.

### Successful request

```python
import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from pykuda.pykuda import PyKuda, PyKudaResponse


logger = logging.getLogger(__name__)

# Initialize PyKuda instance
kuda = PyKuda()

class BanksListView(APIView):
    """
    API view to retrieve a list of banks.
    """

    def get(self, request) -> Response:
        """
        Handle GET request to retrieve a list of banks.

        Returns:
            Response: JSON response containing the list of banks or an error message.
        """
        # Retrieve list of banks from Kuda API
        response = kuda.banks_list()

        if not response.error:
            # The request was successful
            # Return the list of banks to the frontend
            return Response(response.data, status=response.status_code)
        else:
            # There was an error in the request
            # Log provider error details
            self.log_kuda_error(response.data)
            # Return an error and handle it in the frontend or according to your business model
            return Response("Your custom error", status="error_code")

    def log_kuda_error(self, error_response: PyKudaResponse) -> None:
        """
        Log details of Kuda API error.

        Args:
            error_response (PyKudaResponse): The PyKudaResponse object containing error details.
        """

        # Log error details
        logger.error(
            f"KUDA ERROR: \n"
            f"STATUS CODE - {error_response.status_code} \n"
            f"RESPONSE DATA - {error_response.data} \n"
            f"ERROR - {error_response.error}"
        )
```

As seen above, the PyKudaResponse returns the `status_code`, `data` and `error`; the data attribute already contains the appropriate data received from Kuda API. You can access the Kuda response data by executing `response.data`.

### Failed request

In case the request wasn't successful, the PyKudaResponse will be different. The data will be a `Response` Object which you can check to investigate the cause (Maybe your Token is not correct, or the URL, or something else). Now, let's say the API Key in the .env file was not a correct one and a request was made, the example below shows the response to expect.

```shell
>>> response
>>> PyKudaResponse(status_code=401, data=<Response [401]>, error=True)
>>>
>>> response.data.text # 'Invalid Credentials'
>>> response.data.reason # 'Unauthorized'
```

#### Important Note on Error Handling:

When interacting with the Kuda API, it is not recommended to rely solely on the response.status_code for error handling. The Kuda API may return a 200 status code even in cases where there are errors or typos in the request parameters.

For instance, when attempting to purchase airtime, passing an invalid tracking_reference will result in a 200 status code from Kuda, but the request will not be processed successfully.

To ensure robust error handling, it is crucial to examine the response data and utilize the error attribute in the PyKudaResponse object. `PyKuda` intelligently checks that if the request is not successful and was not processed by Kuda, the `response.error` will be `True`. This attribute indicates whether the API request was successful or if there were issues.

Example:

```python
response = kuda.virtual_account_purchase_bill(
    amount='10000', # Invalid amount for airtime purchase
    kuda_biller_item_identifier="KD-VTU-MTNNG",
    customer_identifier="08030001234",
    tracking_reference="invalid_tracking_reference",
)

print(response)
# PyKudaResponse(status_code=200, data=<Response [200]>, error=True)
print(response.data.text)
# '{"message":"Invalid Virtual Account.","status":false,"data":null,"statusCode":"k-OAPI-07"}'
```

As shown in the [Successful request](#successful-request) section, it is recommended to use response.error to ensure that the request was successful.

## What else can PyKuda do?

PyKuda can be used to make other requests also. Below are examples of how to use the other methods available in the `ServiceType` class.

### Create Virtual Account

```python
response = kuda.create_virtual_account(
    first_name="Ogbeni",
    last_name="Lagbaja",
    phone_number="08011122233",
    email="ogbeni@temi.com",
    middle_name="Middle",
    business_name="ABC Ltd",
)
print(response)
# Example Response:
# PyKudaResponse(status_code=200, data=<response_data>, error=False)

print(response.data)
# {
#     "account_number": "2000111222", # Newly generated account number from Kuda
#     "tracking_reference": "trackingReference", # Tracking reference
# }
```

### Virtual Account Balance

```python
response = kuda.virtual_account_balance(tracking_reference="your_tracking_reference")

print(response.data)
# {
#     "ledger": "ledgerBalance",
#     "available": "availableBalance",
#     "withdrawable": "withdrawableBalance",
# }
```

### Main Account Balance

```python
response = kuda.main_account_balance()
print(response.data)
# {
#     "ledger": "ledgerBalance",
#     "available": "availableBalance",
#     "withdrawable": "withdrawableBalance",
# }
```

### Fund Virtual Account

```python
response = kuda.fund_virtual_account(
    tracking_reference="your_tracking_reference",
    amount="1000",
    narration="Funding virtual account",
)
print(response.data)
# {"reference": "transactionReference"}
```

### Withdraw from Virtual Account

```python
response = kuda.withdraw_from_virtual_account(
    tracking_reference="your_tracking_reference",
    amount="500",
    narration="Withdrawing from virtual account",
)
print(response.data)
# {"reference": "transactionReference"}
```

### Confirm Transfer Recipient

```python
response = kuda.confirm_transfer_recipient(
    beneficiary_account_number="recipient_account_number",
    beneficiary_bank_code="recipient_bank_code",
    tracking_reference="your_tracking_reference",
)
print(response.data)
# {
#     "beneficiary_account_number":
#         "beneficiaryAccountNumber"
#     ),
#     "beneficiary_name": "beneficiaryName",
#     "beneficiary_code": "beneficiaryBankCode",
#     "session_id": "sessionID",
#     "sender_account": "senderAccountNumber",
#     "transfer_charge": "transferCharge",
#     "name_enquiry_id": "nameEnquiryID",
#     "tracking_reference": "SenderTrackingReference",
# }
```

### Send Funds from Main Account

```python
response = kuda.send_funds_from_main_account(
    client_account_number="sender_account_number",
    beneficiary_bank_code="recipient_bank_code",
    beneficiary_account_number="recipient_account_number",
    beneficiary_name="Recipient Name",
    amount="1000",
    naration="Sending funds",
    name_enquiry_session_id="name_enquiry_session_id",
    sender_name="Sender Name",
)
print(response.data)
# {
#     "transaction_reference": "transactionReference",
#     "request_reference": "requestReference",
# }
```

### Send Funds from Virtual Account

```python
response = kuda.send_funds_from_virtual_account(
    tracking_reference="your_tracking_reference",
    beneficiary_bank_code="recipient_bank_code",
    beneficiary_account_number="recipient_account_number",
    beneficiary_name="Recipient Name",
    amount="1000",
    naration="Sending funds",
    name_enquiry_session_id="name_enquiry_session_id",
    sender_name="Sender Name",
)

print(response.data)
# {
#     "transaction_reference": "transactionReference",
#     "request_reference": "requestReference",
# }
```

### Get Billers

```python
response = kuda.billers(biller_type="electricity")
print(response.data)
# {
#     "billers": ["list_of_billers"]
# }
```

### Verify Bill Customer

```python
response = kuda.verify_bill_customer(
    kuda_biller_item_identifier="bill_item_identifier",
    customer_identifier="customer_identifier",
)
print(response.data)
# {
#     "customer_name": "customerName,
# }
```

### Virtual Account Purchase Bill

```python
response = kuda.virtual_account_purchase_bill(
    amount="500",
    kuda_biller_item_identifier="bill_item_identifier",
    customer_identifier="customer_identifier",
    tracking_reference="your_tracking_reference",
    phone_number="customer_phone_number",
)
print(response.data)
# {
#     "reference": "reference",
# }
```

### Disable Virtual Account

```python
response = kuda.disable_virtual_account(
    tracking_reference="your_tracking_reference",
)
print(response.data)
# {
#     "account_number": "accountNumber",
# }
```

### Enable Virtual Account

```python
response = kuda.enable_virtual_account(
    tracking_reference="your_tracking_reference",
)
print(response.data)
# {
#     "account_number": "accountNumber",
# }
```

### Update Virtual Account Name

```python
response = kuda.update_virtual_account_name(
    tracking_reference="your_tracking_reference",
    first_name="New_First_Name",
    last_name="New_Last_Name",
)
print(response.data)
# {
#     "account_number": "accountNumber"
# }
```

### Update Virtual Account Email

```python
response = kuda.update_virtual_account_email(
    tracking_reference="your_tracking_reference",
    email="new_email@example.com",
)
print(response.data)
# {
#     "account_number": "accountNumber"
# }
```

### Retrieve Single Virtual Account

```python
response = kuda.retrieve_single_virtual_account(
    tracking_reference="customer_tracking_reference",
)
print(response.data)
# {
# 	  "accountNumber": "2504205433",
#     "email": "08011122233",
#     "phoneNumber": "08011111111",
#     "lastName": "Lagbaja",
#     "firstName": "Ogbeni",
#     "middleName": "Middle",
#     "bussinessName": "ABC LTD",
#     "accountName": "(ABC LTD)-Lagbaja Ogbeni",
#     "trackingReference": "tracking_reference",
#     "creationDate": "2023-04-24T16:35:23.6033333",
#     "isDeleted": false
# }
```

### Retrieve All Virtual Accounts

```python
response = kuda.retrieve_all_virtual_accounts()
print(response.data)
# [
    # {
    # 	"accountNumber": "2504205433",
    #     "email": "08011122233",
    #     "phoneNumber": "08011111111",
    #     "lastName": "Lagbaja",
    #     "firstName": "Ogbeni",
    #     "middleName": "Middle",
    #     "bussinessName": "ABC LTD",
    #     "accountName": "(ABC LTD)-Lagbaja Ogbeni",
    #     "trackingReference": "tracking_reference",
    #     "creationDate": "2023-04-24T16:35:23.6033333",
    #     "isDeleted": false
    # },
    # ........
# ]
```

## Contributions & Issues

-   If you would like to contribute and improve this package or its documentation, please feel free to fork the repository, make changes and open a pull request.
-   If you encounter any issue or bugs, please open an issue.

## Author

-   [Kayode TemiTope](https://github.com/sir-temi)
