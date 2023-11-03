import json
import os
from typing import Union
from dotenv import load_dotenv
import requests

from pykuda.classes.py_kuda_response import PyKudaResponse


load_dotenv()

KUDA_KEY = os.getenv("KUDA_KEY")
TOKEN_URL = os.getenv("TOKEN_URL")
REQUEST_URL = os.getenv("REQUEST_URL")
EMAIL = os.getenv("EMAIL")


def check_envs_are_set():
    config = {
        "KUDA_KEY": os.getenv("KUDA_KEY"),
        "TOKEN_URL": os.getenv("TOKEN_URL"),
        "REQUEST_URL": os.getenv("REQUEST_URL"),
        "EMAIL": os.getenv("EMAIL"),
        "MAIN_ACCOUNT_NUMBER": os.getenv("MAIN_ACCOUNT_NUMBER"),
    }

    if all(list(config.values())):
        return True

    for variable, value in config.items():
        if not value:
            return (
                f"{variable} is not set, please set in the environment and try again."
            )


def get_token():
    data = {"email": EMAIL, "apiKey": KUDA_KEY}
    response = requests.post(
        TOKEN_URL, data=json.dumps(data), headers={"content-type": "application/json"}
    )
    return response


def generate_headers() -> Union[requests.models.Response, dict]:
    response = get_token()
    if response.status_code == 200:
        return {
            "content-type": "application/json",
            "Authorization": f"bearer {response.text}",
        }
    return response


def get_bank_list_request(data) -> PyKudaResponse:
    """
    FUnction responsible for getting list of Nigerian
    Banks.
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if (
            response.status_code == 200
            and response_data
            and response_data.get("status")
            and response_data.get("data")
            and response_data.get("data").get("banks")
        ):
            # Check if the response returns a status=True and
            # response_data["data"]["banks"] is not None
            return PyKudaResponse(status_code=200, data=response_data["data"]["banks"])
        else:
            pykuda_response = PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )
            return pykuda_response


def create_virtual_account_request(data) -> PyKudaResponse:
    """
    This function is responsible for creating a virtual
    account.
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if (
            response.status_code == 200
            and response_data
            and response_data.get("status")
            and response_data.get("data")
            and response_data.get("data").get("accountNumber")
        ):
            pykuda_data = {
                "account_number": response_data["data"]["accountNumber"],
                "tracking_reference": data["Data"]["trackingReference"],
            }
            return PyKudaResponse(status_code=201, data=pykuda_data)

        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )


def get_virtaul_account_balance_request(data):
    """
    This function is responsible for getting balance
    account.
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if response.status_code == 200 and response_data.get("status"):
            balance = {
                "ledger": response_data["data"]["ledgerBalance"],
                "available": response_data["data"]["availableBalance"],
                "withdrawable": response_data["data"]["withdrawableBalance"],
            }
            return PyKudaResponse(status_code=200, data=balance)
        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )


def get_main_account_balance_request(data):
    """
    This function is responsible for getting the Total
    balance in the main account.
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if response.status_code == 200 and response_data.get("status"):
            balance = {
                "ledger": response_data["data"]["ledgerBalance"],
                "available": response_data["data"]["availableBalance"],
                "withdrawable": response_data["data"]["withdrawableBalance"],
            }
            return PyKudaResponse(status_code=200, data=balance)
        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )


def fund_virtual_account_request(data):
    """
    This function helps to fund a virtual account from the main
    Kuda account
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if (
            response.status_code == 200
            and response_data.get("status")
            and response_data.get("transactionReference")
        ):
            return PyKudaResponse(
                status_code=200,
                data={"reference": response_data.get("transactionReference")},
            )
        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )


def withdraw_from_virtual_account_requesr(data):
    """
    This function is responsible for withdrawing funds from a virtual account
    and deposit to a virtual account
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if (
            response.status_code == 200
            and response_data.get("status")
            and response_data.get("transactionReference")
        ):
            return PyKudaResponse(
                status_code=200,
                data={"reference": response_data.get("transactionReference")},
            )
        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )


def confirm_transfer_recipient_request(data):
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if (
            response.status_code == 200
            and response_data.get("status")
            and response_data.get("data")
            and response_data.get("data").get("beneficiaryAccountNumber")
            and response_data.get("data").get("beneficiaryName")
        ):
            beneficiary_data = response_data.get("data")
            return PyKudaResponse(
                status_code=200,
                data={
                    "beneficiary_account_number": beneficiary_data.get(
                        "beneficiaryAccountNumber"
                    ),
                    "beneficiary_name": beneficiary_data.get("beneficiaryName"),
                    "beneficiary_code": beneficiary_data.get("beneficiaryBankCode"),
                    "session_id": beneficiary_data.get("sessionID"),
                    "sender_account": beneficiary_data.get("senderAccountNumber"),
                    "transfer_charge": beneficiary_data.get("transferCharge"),
                    "name_enquiry_id": beneficiary_data.get("nameEnquiryID"),
                    "tracking_reference": data["Data"]["SenderTrackingReference"],
                },
            )
        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )


def send_funds_from_main_account_request(data):
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if (
            response.status_code == 200
            and response_data.get("status")
            and response_data.get("transactionReference")
        ):
            return PyKudaResponse(
                status_code=200,
                data={
                    "transaction_reference": response_data.get("transactionReference"),
                    "request_reference": response_data.get("requestReference"),
                },
            )
        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )


def send_funds_from_virtual_account_request(data):
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if (
            response.status_code == 200
            and response_data.get("status")
            and response_data.get("transactionReference")
        ):
            return PyKudaResponse(
                status_code=200,
                data={
                    "transaction_reference": response_data.get("transactionReference"),
                    "request_reference": response_data.get("requestReference"),
                },
            )
        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )


def get_billers(data):
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if (
            response.status_code == 200
            and response_data.get("status")
            and response_data.get("data")
            and response_data.get("data").get("billers")
        ):
            return PyKudaResponse(
                status_code=200,
                data={
                    "billers": response_data.get("data").get("billers"),
                },
            )
        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )


def verify_bill_customer(data):
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if (
            response.status_code == 200
            and response_data.get("status")
            and response_data.get("data")
            and response_data.get("data").get("customerName")
        ):
            return PyKudaResponse(
                status_code=200,
                data={
                    "customerName": response_data.get("data").get("customerName"),
                },
            )
        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )


def virtual_account_purchase_bill(data):
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        return PyKudaResponse(status_code=headers.status_code, data=headers)
    else:
        response = requests.post(
            REQUEST_URL,
            json=data,
            headers=headers,
        )

        response_data = response.json()

        if (
            response.status_code == 200
            and response_data.get("status")
            and response_data.get("data")
            and response_data.get("data").get("reference")
        ):
            return PyKudaResponse(
                status_code=200,
                data={
                    "reference": response_data.get("data").get("reference"),
                },
            )
        else:
            return PyKudaResponse(
                status_code=response.status_code, data=response, error=True
            )
