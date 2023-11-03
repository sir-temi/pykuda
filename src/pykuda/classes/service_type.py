from dataclasses import dataclass
import json
import secrets
from pykuda.constants import (
    ADMIN_CREATE_VIRTUAL_ACCOUNT,
    ADMIN_RETRIEVE_MAIN_ACCOUNT_BALANCE,
    FUND_VIRTUAL_ACCOUNT,
    GET_BILLERS_BY_TYPE,
    NAME_ENQUIRY,
    PURCHASE_BILL,
    RETRIEVE_VIRTUAL_ACCOUNT_BALANCE,
    SINGLE_FUND_TRANSFER,
    VERIFY_BILL_CUSTOMER,
    VIRTUAL_ACCOUNT_FUND_TRANSFER,
    WITHDRAW_VIRTUAL_ACCOUNT,
)

from pykuda.utils import (
    confirm_transfer_recipient_request,
    create_virtual_account_request,
    fund_virtual_account_request,
    get_bank_list_request,
    get_billers,
    get_main_account_balance_request,
    get_virtaul_account_balance_request,
    send_funds_from_main_account_request,
    send_funds_from_virtual_account_request,
    verify_bill_customer,
    virtual_account_purchase_bill,
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
        data = {
            "serviceType": "BANK_LIST",
            "requestRef": secrets.token_hex(6),
        }

        return get_bank_list_request(data)

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
        data = {
            "servicetype": ADMIN_CREATE_VIRTUAL_ACCOUNT,
            "requestref": secrets.token_hex(6),
            "Data": {
                "phoneNumber": phone_number,
                "email": email,
                "lastName": last_name,
                "firstName": first_name,
                "middleName": middle_name if middle_name else None,
                "businessName": business_name if business_name else None,
                "trackingReference": secrets.token_hex(8),
            },
        }

        return create_virtual_account_request(data)

    def get_virtaul_account_balance(self, tracking_reference):
        """
        Gets the balance of a virtual account.
        """
        data = {
            "servicetype": RETRIEVE_VIRTUAL_ACCOUNT_BALANCE,
            "requestref": secrets.token_hex(6),
            "data": {"trackingReference": tracking_reference},
        }

        response = get_virtaul_account_balance_request(data)
        return response

    def get_main_account_balance(self):
        """
        Gets the account balance of the main account.
        """
        data = {
            "serviceType": ADMIN_RETRIEVE_MAIN_ACCOUNT_BALANCE,
            "requestref": secrets.token_hex(6),
        }

        return get_main_account_balance_request(data)

    def fund_virtual_account(
        self, tracking_reference: str, amount: str, narration: str
    ):
        """
        Withdraws money from the main account and deposits into a virtual account.
        """
        data = {
            "serviceType": FUND_VIRTUAL_ACCOUNT,
            "requestRef": secrets.token_hex(6),
            "Data": {
                "trackingReference": tracking_reference,
                "amount": amount,
                "narration": narration,
            },
        }

        return fund_virtual_account_request(data)

    def withdraw_from_virtual_account(
        self, tracking_reference: str, amount: str, narration: str
    ):
        """
        Withdraws money from a virtual account and deposits into the main account.
        """
        data = {
            "serviceType": WITHDRAW_VIRTUAL_ACCOUNT,
            "requestRef": secrets.token_hex(6),
            "Data": {
                "trackingReference": tracking_reference,
                "amount": int(amount),
                "narration": narration,
            },
        }

        return withdraw_from_virtual_account_requesr(data)

    def confirm_transfer_recipient(
        self,
        beneficiary_account_number: str,
        beneficiary_bank_code: str,
        tracking_reference=None,
    ):
        """
        This function is responsible for confirming a recipient details, and if the funds
        is to be transfered from a virtual account, it returns the tracking reference
        so it can be easily passed to the send_funds_Out_of_account method.
        """
        data = {
            "serviceType": NAME_ENQUIRY,
            "requestRef": secrets.token_hex(6),
            "Data": {
                "beneficiaryAccountNumber": beneficiary_account_number,
                "beneficiaryBankCode": beneficiary_bank_code,
                "SenderTrackingReference": tracking_reference
                if tracking_reference
                else "",  # Tracking reference of the virtual account trying to do the actual transfer. Leave it empty if the intended transfer is going to be from the main account
                "isRequestFromVirtualAccount": True
                if tracking_reference
                else False,  # True or False value. If the intended transfer is to be made by the virtual account
            },
        }

        return confirm_transfer_recipient_request(data)

    def send_funds_from_main_account(
        self,
        client_account_number,
        beneficiary_bank_code,
        beneficiary_account_number,
        beneficiary_name: str,
        amount: str,
        naration,
        name_enquiry_session_id,
        sender_name,
    ):
        """
        This function is responsible for sending funds from the main account
        """
        data = {
            "serviceType": SINGLE_FUND_TRANSFER,
            "requestRef": secrets.token_hex(6),
            "Data": {
                "ClientAccountNumber": client_account_number,
                "beneficiaryBankCode": beneficiary_bank_code,
                "beneficiaryAccount": beneficiary_account_number,
                "beneficiaryName": beneficiary_name,
                "amount": int(amount),
                "narration": naration,
                "nameEnquirySessionID": name_enquiry_session_id,
                "trackingReference": "",
                "senderName": sender_name,
                "clientFeeCharge": 0,
            },
        }

        return send_funds_from_main_account_request(data)

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
        """
        This function is responsible for sending funds from a virtual account
        """
        data = {
            "serviceType": VIRTUAL_ACCOUNT_FUND_TRANSFER,
            "requestRef": secrets.token_hex(6),
            "Data": {
                "trackingReference": tracking_reference,
                "beneficiaryBankCode": beneficiary_bank_code,
                "beneficiaryAccount": beneficiary_account_number,
                "beneficiaryName": beneficiary_name,
                "amount": int(amount),
                "narration": naration,
                "nameEnquiryId": name_enquiry_session_id,
                "senderName": sender_name,
                "clientFeeCharge": 0,
            },
        }

        return send_funds_from_virtual_account_request(data)

    def get_billers(
        self,
        biller_type,
    ):
        """
        This function is responsible getting billers by a biller type
        The list of available biller type are:
        airtime , betting , internet Data , electricity, cableTv.
        """
        data = {
            "serviceType": GET_BILLERS_BY_TYPE,
            "requestref": secrets.token_hex(6),
            "Data": {
                "BillTypeName": biller_type,
            },
        }

        return get_billers(data)

    def verify_bill_customer(
        self,
        kuda_biller_item_identifier,
        customer_identifier,
    ):
        """
        This function is responsible for verifying a bill by customer
        """
        data = {
            "serviceType": VERIFY_BILL_CUSTOMER,
            "requestref": secrets.token_hex(6),
            "Data": {
                "KudaBillItemIdentifier": kuda_biller_item_identifier,
                "CustomerIdentification": customer_identifier,
            },
        }

        return verify_bill_customer(data)

    def virtual_account_purchase_bill(
        self,
        amount,
        kuda_biller_item_identifier,
        customer_identifier,
        tracking_reference,
        phone_number=None,
    ):
        """
        This function is responsible for purchasings a bill with virtual account
        """
        data = {
            "serviceType": PURCHASE_BILL,
            "requestref": secrets.token_hex(6),
            "Data": {
                "Amount": amount,
                "BillItemIdentifier": kuda_biller_item_identifier,
                "PhoneNumber": phone_number,
                "CustomerIdentifier": customer_identifier,
                "TrackingReference": tracking_reference,
            },
        }

        return virtual_account_purchase_bill(data)
