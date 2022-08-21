from dataclasses import dataclass
import json
import os
import secrets

from pykuda.utils import (
    confirm_transfer_recipient_request,
    create_virtual_account_request,
    fund_virtual_account_request,
    get_bank_list_request,
    get_main_account_balance_request,
    get_virtaul_account_balance_request,
    send_funds_from_main_account_request,
    send_funds_from_virtual_account_request,
    withdraw_from_virtual_account_requesr,
)


@dataclass
class ServiceType:
    """
    This class handles all the Service functionalities, it
    has methods that handle each type of transaction.
    """

    def get_bank_list(self):
        """
        Gets the list of banks.
        """
        data = json.dumps(
            {
                "serviceType": "BANK_LIST",
                "requestRef": secrets.token_hex(6),
            }
        )
        request_data = json.dumps({"data": data})

        response = get_bank_list_request(request_data)
        return response

    def create_virtual_account(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        email: str,
        middle_name: str = None,
        business_name: str = None,
    ):
        """
        Creates a virtual account.
        """
        data = json.dumps(
            {
                "servicetype": "ADMIN_CREATE_VIRTUAL_ACCOUNT",
                "requestref": secrets.token_hex(6),
                "data": {
                    "phoneNumber": phone_number,
                    "email": email,
                    "lastName": last_name,
                    "firstName": first_name,
                    "middleName": middle_name if middle_name else None,
                    "businessName": business_name if business_name else None,
                    "trackingReference": secrets.token_hex(8),
                },
            }
        )
        request_data = (
            json.dumps({"data": data}),
            json.loads(data)["data"]["trackingReference"],
        )

        response = create_virtual_account_request(*request_data)
        return response

    def get_virtaul_account_balance(self, tracking_reference):
        """
        Gets the balance of a virtual account.
        """
        data = json.dumps(
            {
                "servicetype": "RETRIEVE_VIRTUAL_ACCOUNT_BALANCE",
                "requestref": secrets.token_hex(6),
                "data": {"trackingReference": tracking_reference},
            }
        )

        request_data = json.dumps({"data": data})
        response = get_virtaul_account_balance_request(request_data)
        return response

    def get_main_account_balance(self):
        """
        Gets the account balance of the main account.
        """
        data = json.dumps(
            {
                "serviceType": "ADMIN_RETRIEVE_MAIN_ACCOUNT_BALANCE",
                "requestref": secrets.token_hex(6),
            }
        )
        request_data = json.dumps({"data": data})

        response = get_main_account_balance_request(request_data)
        return response

    def fund_virtual_account(self, tracking_reference, amount, narration=None):
        """
        Withdraws money from the main account and deposits into a virtual account.
        """
        data = json.dumps(
            {
                "serviceType": "FUND_VIRTUAL_ACCOUNT",
                "requestRef": secrets.token_hex(6),
                "data": {
                    "trackingReference": tracking_reference,
                    "amount": amount,
                    "narration": narration,
                },
            }
        )
        request_data = json.dumps({"data": data})

        response = fund_virtual_account_request(request_data)
        return response

    def withdraw_from_virtual_account(self, tracking_reference, amount, narration=None):
        """
        Withdraws money from a virtual account and deposits into the main account.
        """
        data = json.dumps(
            {
                "serviceType": "WITHDRAW_VIRTUAL_ACCOUNT",
                "requestRef": secrets.token_hex(6),
                "data": {
                    "trackingReference": tracking_reference,
                    "amount": amount,
                    "narration": narration,
                },
            }
        )
        request_data = json.dumps({"data": data})

        response = withdraw_from_virtual_account_requesr(request_data)
        return response

    def confirm_transfer_recipient(
        self, beneficiary_account_number, beneficiary_bank_code, tracking_reference=None
    ):
        """
        This function is responsible for confirming a recipient details, and if the funds
        is to be transfered from a virtual account, it returns the tracking reference
        so it can be easily passed to the send_funds_Out_of_account method.
        """
        data = json.dumps(
            {
                "serviceType": "NAME_ENQUIRY",
                "requestRef": secrets.token_hex(6),
                "data": {
                    "beneficiaryAccountNumber": beneficiary_account_number,
                    "beneficiaryBankCode": beneficiary_bank_code,
                    "SenderTrackingReference": tracking_reference
                    if tracking_reference
                    else "",  # Tracking reference of the virtual account trying to do the actual transfer. Leave it empty if the intended transfer is going to be from the main account
                    "isRequestFromVirtualAccount": True
                    if tracking_reference
                    else False,  # True or False value. If the intended transfer is to be made by the virtual account
                },
            },
        )
        request_data = json.dumps({"data": data})

        response = confirm_transfer_recipient_request(request_data, tracking_reference)
        return response

    def send_funds_from_main_account(
        self,
        client_account_number,
        beneficiary_bank_code,
        beneficiary_account_number,
        beneficiary_name,
        amount,
        naration,
        name_enquiry_session_id,
        sender_name,
    ):
        data = json.dumps(
            {
                "serviceType": "SINGLE_FUND_TRANSFER",
                "requestRef": secrets.token_hex(6),
                "data": {
                    "ClientAccountNumber": client_account_number,
                    "beneficiaryBankCode": beneficiary_bank_code,
                    "beneficiaryAccount": beneficiary_account_number,
                    "beneficiaryName": beneficiary_name,
                    "amount": amount,
                    "narration": naration,
                    "nameEnquirySessionID": name_enquiry_session_id,
                    "trackingReference": "",
                    "senderName": sender_name,
                },
            },
        )
        request_data = json.dumps({"data": data})

        response = send_funds_from_main_account_request(request_data)
        return response

    def send_funds_from_virtual_account(
        self,
        tracking_reference,
        beneficiary_bank_code,
        beneficiary_account_number,
        beneficiary_name,
        amount,
        naration,
        name_enquiry_session_id,
        sender_name,
    ):
        data = json.dumps(
            {
                "serviceType": "VIRTUAL_ACCOUNT_FUND_TRANSFER",
                "requestRef": secrets.token_hex(6),
                "data": {
                    "trackingReference": tracking_reference,
                    "beneficiaryBankCode": beneficiary_bank_code,
                    "beneficiaryAccount": beneficiary_account_number,
                    "beneficiaryName": beneficiary_name,
                    "amount": amount,
                    "narration": naration,
                    "nameEnquiryId": name_enquiry_session_id,
                    "senderName": sender_name,
                },
            },
        )
        request_data = json.dumps({"data": data})

        response = send_funds_from_virtual_account_request(request_data)
        return response

    def send_funds_out_of_account(
        self,
        beneficiary_account_number,
        beneficiary_bank_code,
        name_enquiry_session_id,
        naration,
        beneficiary_name,
        amount,
        sender_name,
        tracking_reference=None,
    ):
        """
        This function is responsible for sending funds from either the main account
        or a virtual account. If a tracking reference is passed into the function,
        it sends from the virtual account, if not, it sends from the main account.
        """
        if not tracking_reference:
            response = self.send_funds_from_main_account(
                os.getenv("MAIN_ACCOUNT_NUMBER"),
                beneficiary_bank_code,
                beneficiary_account_number,
                beneficiary_name,
                amount,
                naration,
                name_enquiry_session_id,
                sender_name,
            )

            return response
        else:
            response = self.send_funds_from_virtual_account(
                tracking_reference,
                beneficiary_bank_code,
                beneficiary_account_number,
                beneficiary_name,
                amount,
                naration,
                name_enquiry_session_id,
                sender_name,
            )

            return response
