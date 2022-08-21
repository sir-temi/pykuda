import json
import os
from dotenv import load_dotenv
import requests

from pykuda.classes.py_kuda_response import PyKudaResponse


load_dotenv()

KUDA_KEY = os.getenv("KUDA_KEY")
TOKEN_URL = os.getenv("TOKEN_URL")
REQUEST_URL = os.getenv("REQUEST_URL")
EMAIL = os.getenv("EMAIL")


def get_token():
    data = {"email": EMAIL, "apiKey": KUDA_KEY}
    response = requests.post(
        TOKEN_URL, data=json.dumps(data), headers={"content-type": "application/json"}
    )
    return response


def generate_headers():
    response = get_token()
    if response.status_code == 200:
        return {
            "content-type": "application/json",
            "Authorization": f"bearer {response.text}",
        }
    return response


def get_bank_list_request(data):
    """
    FUnction responsible for getting list of Nigerian
    Banks.
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        pykuda_response = PyKudaResponse(status_code=headers.status_code, data=headers)
        return pykuda_response
    else:
        response = requests.post(
            REQUEST_URL,
            data=data,
            headers=headers,
        )

        if response.status_code == 200:
            response_data = response.json()
            pykuda_data = json.loads(response_data["data"])
            return PyKudaResponse(status_code=200, data=pykuda_data["Data"]["banks"])
        else:
            pykuda_response = PyKudaResponse(
                status_code=response.status_code, data=response
            )
            return pykuda_response


def create_virtual_account_request(data, tracking_reference):
    """
    This function is responsible for creating a virtual
    account.
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        pykuda_response = PyKudaResponse(status_code=headers.status_code, data=headers)
        return pykuda_response
    else:
        response = requests.post(
            REQUEST_URL,
            data=data,
            headers=headers,
        )

        if response.status_code == 200:
            response_data = (
                response.json()
            )  # {'account_number': '2504102532', 'tracking_reference': '455132842804269457'}
            response_data = json.loads(response_data["data"])
            if response_data["Status"]:
                pykuda_data = {
                    "account_number": response_data["Data"]["AccountNumber"],
                    "tracking_reference": tracking_reference,
                }
                pykuda_response = PyKudaResponse(status_code=201, data=pykuda_data)
                return pykuda_response

            else:
                pykuda_response = PyKudaResponse(
                    status_code=response.status_code, data=response
                )
                return pykuda_response
        else:
            pykuda_response = PyKudaResponse(
                status_code=response.status_code, data=response
            )
            return pykuda_response


def get_virtaul_account_balance_request(data):
    """
    This function is responsible for getting balance
    account.
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        pykuda_response = PyKudaResponse(status_code=headers.status_code, data=headers)
        return pykuda_response
    else:
        response = requests.post(
            REQUEST_URL,
            data=data,
            headers=headers,
        )

        if response.status_code == 200:
            response_data = (
                response.json()
            )  # {'data': '{"Status":true,"Message":"Operation successful","Data":{"LedgerBalance":0.00,"AvailableBalance":0.00,"WithdrawableBalance":0.00}}', 'password': ''}
            response_data = json.loads(response_data["data"])
            if response_data["Status"]:
                balance = {
                    "ledger": response_data["Data"]["LedgerBalance"],
                    "available": response_data["Data"]["AvailableBalance"],
                    "withdrawable": response_data["Data"]["WithdrawableBalance"],
                }
                pykuda_response = PyKudaResponse(status_code=200, data=balance)
                return pykuda_response
            else:
                return PyKudaResponse(status_code=response.status_code, data=response)
        else:
            return PyKudaResponse(status_code=response.status_code, data=response)


def get_main_account_balance_request(data):
    """
    This function is responsible for getting the Total
    balance in the main account.
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        pykuda_response = PyKudaResponse(status_code=headers.status_code, data=headers)
        return pykuda_response
    else:
        response = requests.post(
            REQUEST_URL,
            data=data,
            headers=headers,
        )

        if response.status_code == 200:
            response_data = (
                response.json()
            )  # {'data': '{"Status":true,"Message":"Operation successful","Data":{"LedgerBalance":4968878514153.00,"AvailableBalance":4968878514153.00,"WithdrawableBalance":4968878514153.00}}', 'password': ''}
            response_data = json.loads(response_data["data"])
            if response_data["Status"]:
                balance = {
                    "ledger": response_data["Data"]["LedgerBalance"],
                    "available": response_data["Data"]["AvailableBalance"],
                    "withdrawable": response_data["Data"]["WithdrawableBalance"],
                }
                pykuda_response = PyKudaResponse(status_code=200, data=balance)
                return pykuda_response
            else:
                return PyKudaResponse(status_code=response.status_code, data=response)
        else:
            return PyKudaResponse(status_code=response.status_code, data=response)


def fund_virtual_account_request(data):
    """
    This function helps to fund a virtual account from the main
    Kuda account
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        pykuda_response = PyKudaResponse(status_code=headers.status_code, data=headers)
        return pykuda_response
    else:
        response = requests.post(
            REQUEST_URL,
            data=data,
            headers=headers,
        )

        if response.status_code == 200:
            response_data = (
                response.json()
            )  # {'RequestReference': 'de6260d96ed9', 'TransactionReference': '2208140204', 'ResponseCode': '00', 'Status': True, 'Message': 'Transaction successful', 'Data': None}
            response_data = json.loads(response_data["data"])
            if response_data["Status"]:
                return PyKudaResponse(status_code=200, data=response_data)
            else:
                return PyKudaResponse(status_code=response.status_code, data=response)
        else:
            return PyKudaResponse(status_code=response.status_code, data=response)


def withdraw_from_virtual_account_requesr(data):
    """
    This function is responsible for withdrawing funds from a virtual account
    and deposit to a virtual account
    """
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        pykuda_response = PyKudaResponse(status_code=headers.status_code, data=headers)
        return pykuda_response
    else:
        response = requests.post(
            REQUEST_URL,
            data=data,
            headers=headers,
        )

        if response.status_code == 200:
            response_data = (
                response.json()
            )  # {'RequestReference': '56a585e3f535', 'TransactionReference': '2208140206', 'ResponseCode': '00', 'Status': True, 'Message': 'Transaction successful', 'Data': None}
            response_data = json.loads(response_data["data"])
            if response_data["Status"]:
                return PyKudaResponse(status_code=200, data=response_data)
            else:
                return PyKudaResponse(status_code=response.status_code, data=response)
        else:
            return PyKudaResponse(status_code=response.status_code, data=response)


def confirm_transfer_recipient_request(data, tracking_reference):
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        pykuda_response = PyKudaResponse(status_code=headers.status_code, data=headers)
        return pykuda_response
    else:
        response = requests.post(
            REQUEST_URL,
            data=data,
            headers=headers,
        )

        if response.status_code == 200:
            response_data = response.json()
            response_data = json.loads(response_data["data"])
            if response_data["Status"]:
                return PyKudaResponse(
                    status_code=200,
                    data={
                        "response_data": response_data,
                        "tracking_reference": tracking_reference,
                    },
                )
                # {'Status': True, 'Message': 'Request successful.', 'Data': {'BeneficiaryAccountNumber': '0016545400', 'BeneficiaryName': 'Kuda User', 'SenderAccountNumber': '', 'SenderName': None, 'BeneficiaryCustomerID': 0, 'BeneficiaryBankCode': '999058', 'NameEnquiryID': 0, 'ResponseCode': '00', 'TransferCharge': 0.0, 'SessionID': 'BFCA47296DA84C338CE3D7E6561B370E'}})
            else:
                return PyKudaResponse(status_code=response.status_code, data=response)
        else:
            return PyKudaResponse(status_code=response.status_code, data=response)


def send_funds_from_main_account_request(data):
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        pykuda_response = PyKudaResponse(status_code=headers.status_code, data=headers)
        return pykuda_response
    else:
        response = requests.post(
            REQUEST_URL,
            data=data,
            headers=headers,
        )

        if response.status_code == 200:
            response_data = response.json()
            response_data = json.loads(response_data["data"])
            if response_data["Status"]:
                return PyKudaResponse(status_code=200, data=response_data)
            else:
                return PyKudaResponse(status_code=response.status_code, data=response)
        else:
            return PyKudaResponse(status_code=response.status_code, data=response)


def send_funds_from_virtual_account_request(data):
    headers = generate_headers()

    if isinstance(headers, requests.models.Response):
        pykuda_response = PyKudaResponse(status_code=headers.status_code, data=headers)
        return pykuda_response
    else:
        response = requests.post(
            REQUEST_URL,
            data=data,
            headers=headers,
        )

        if response.status_code == 200:
            response_data = response.json()
            response_data = json.loads(response_data["data"])
            if response_data["Status"]:
                return PyKudaResponse(status_code=200, data=response_data)
            else:
                return PyKudaResponse(status_code=response.status_code, data=response)
        else:
            return PyKudaResponse(status_code=response.status_code, data=response)
