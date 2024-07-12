A Python package that simplifies using the Kuda Bank API. This package makes it seamless and easy to enjoy the beautiful Kuda Bank API. PyKuda uses Kuda's API v2, which authenticates using an API key and a token.

# Getting Started

Install PyKuda
To use this package, install it using the package manager pip:


# pip install pykuda

Our package, PyKuda, has some dependencies that will be installed (requests and python-decouple). requests is used by PyKuda to make HTTP requests to Kuda's endpoints, while python-decouple is responsible for getting the environmental variables that have to be set for the requests to be authenticated; more details are discussed below.

# Create Environmental Variables
After installation, the next step is to create a .env file where the environmental variables will be stored. Five variables are to be set in the .env file, and they are shown in the example below.

# Example
KUDA_KEY="Your Kuda Api Key"
TOKEN_URL="https://kuda-openapi.kuda.com/v2.1/Account/GetToken" # Kuda API v2.1 GetToken URL
REQUEST_URL="https://kuda-openapi.kuda.com/v2.1/" # Kuda API v2.1 Request URL
EMAIL="Your email used to register for the Kuda account"
MAIN_ACCOUNT_NUMBER="Your main Kuda account number"
Not setting these in the .env file will raise a value error as shown below.

# Example
>>> from pykuda.pykuda import PyKuda
>>> kuda = PyKuda()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/path/to/Python/version/lib/python/site-packages/pykuda/pykuda.py", line 16, in __init__
    raise ValueError(response)
ValueError: TOKEN_URL, REQUEST_URL, EMAIL, MAIN_ACCOUNT_NUMBER are not set, please set in the environment or pass them as a dictionary when initializing PyKuda.
NB: Please make sure you do not push your .env file to public repositories, as the details here are confidential.

# Initialize with Credentials
If you do not want to set the credentials in the .env file, you can also initialize PyKuda with a dictionary of your credentials.


>>> from pykuda.pykuda import PyKuda
>>> credentials = {
...   "KUDA_KEY": "KUDA_KEY",
...   "TOKEN_URL": "TOKEN_URL",
...   "REQUEST_URL": "REQUEST_URL",
...   "EMAIL": "EMAIL",
...   "MAIN_ACCOUNT_NUMBER": "MAIN_ACCOUNT_NUMBER",
... }
>>> kuda = PyKuda(credentials) # Will not raise a ValueError
Using PyKuda
Successful Request
from pykuda.pykuda import PyKuda

kuda = PyKuda()
response = kuda.banks_list()
print(response)
# Example Response:
# PyKudaResponse(status_code=200, data=[list_of_banks], error=False)
Failed Request
In case the request wasn't successful, the PyKudaResponse will be different. The data will be a Response Object, which you can check to investigate the cause (Maybe your Token is not correct, or the URL, or something else). Now, let's say the API Key in the .env file was not a correct one and a request was made, the example below shows the response to expect.


print(response)
# PyKudaResponse(status_code=401, data=<Response [401]>, error=True)

print(response.data.text)
# 'Invalid Credentials'

print(response.data.reason)
# 'Unauthorized'
Understanding PyKudaResponse
With PyKuda, every interaction with the Kuda API is elevated through the PyKudaResponse object, enriching the responses from Kuda. This custom response encapsulates three key attributes: status_code, data, and error.

PyKudaResponse serves as a tailored feedback mechanism provided by PyKuda. Its primary purpose is to enhance the interpretation of Kuda's responses and reliably confirm the success of a request. In cases where the request encounters issues, the error attribute is set to True, signaling that an error has occurred during the interaction. This nuanced approach ensures a more robust and dependable handling of API responses. It is imperative to systematically inspect the error attribute to ascertain the success of the method.

# Example:
This illustrative example outlines a conventional approach to leverage PyKuda for verifying the success of a request.

import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from pykuda.pykuda import PyKuda

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
As seen above, the PyKudaResponse returns the status_code, data, and error; the data attribute already contains the appropriate data received from the Kuda API. You can access the Kuda response data by executing response.data.

Important Note on Error Handling:
When interacting with the Kuda API, it is not recommended to rely solely on the status_code for error handling. The Kuda API may return a 200 status code even in cases where Kuda couldn't process the request due to client errors or typos.

For instance, when attempting to purchase airtime, passing an invalid tracking_reference will return a 200 status code from Kuda, but the request will not be processed successfully.

To ensure robust error handling, it is crucial to examine the response data and utilize the error attribute in the PyKudaResponse object. PyKuda intelligently checks that if the request is not successful and was not processed by Kuda, the PyKudaReponse.error will be True. This error attribute indicates whether the API request was successful or if there were issues.

# Example

response = kuda.virtual_account_purchase_bill(
    amount='10000',
    kuda_biller_item_identifier="KD-VTU-MTNNG",
    customer_identifier="08030001234",
    tracking_reference="invalid_tracking_reference", # Invalid tracking_reference
)

print(response)
# PyKudaResponse(status_code=200, data=<Response [200]>, error=True)
print(response.data.text)
# '{"message":"Invalid Virtual Account.","status":false,"data":null,"statusCode":"k-OAPI-07"}'
As shown in the Successful request section, it is recommended to use PyKudaResponse.error to ensure that the request was successful.

# What Else Can PyKuda Do?

PyKuda can be used to make other requests as well. Below are examples of how to use the other methods available in the ServiceType class.


# Create Virtual Account

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

# Virtual Account Balance

response = kuda.virtual_account_balance(tracking_reference="your_tracking_reference")

print(response.data)
# {
#     "ledger_balance": "10000", # Ledger Balance
#     "available_balance": "5000", # Available Balance
# }


# Virtual Account Transactions

response = kuda.virtual_account_transactions(tracking_reference="your_tracking_reference")

print(response.data)
# [
#     {
#         "transaction_type": "debit",
#         "amount": "1000",
#         "date": "2023-01-01",
#         "reference": "transactionReference",
#         "description": "Transfer to another account",
#     },
#     {
#         "transaction_type": "credit",
#         "amount": "2000",
#         "date": "2023-01-02",
#         "reference": "transactionReference",
#         "description": "Deposit from another account",
#     },
# ]


# Send Funds

response = kuda.virtual_account_send_funds(
    tracking_reference="your_tracking_reference",
    amount="1000",
    receiver_tracking_reference="receiver_tracking_reference",
    receiver_account_number="receiver_account_number",
    receiver_bank_code="receiver_bank_code",
    narration="Fund Transfer"
)

print(response.data)
# {
#     "transaction_reference": "transactionReference",
#     "status": "Success",
# }


# Beneficiary Name Enquiry

response = kuda.name_enquiry(
    beneficiary_account="beneficiary_account_number",
    beneficiary_bank_code="beneficiary_bank_code"
)

print(response.data)
# {
#     "account_name": "Account Name",
#     "account_number": "Account Number",
#     "bank_name": "Bank Name",
# }

# More Requests
For more methods and their usage, kindly check the ServiceType class.