import secrets

from pykuda.classes.py_kuda_response import PyKudaResponse
from pykuda.constants import ServiceTypeConstants
from pykuda.service_type_utils import ServiceTypeUtils


class ServiceType(ServiceTypeUtils):
    """
    This class handles all the Service functionalities, it
    has methods that handle each type of transaction.
    """

    def banks_list(self) -> PyKudaResponse:
        """
        Get the list of banks.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(ServiceTypeConstants.BANK_LIST.value)
        return self._banks_list_request(data)

    def create_virtual_account(
        self,
        first_name: str,
        last_name: str,
        phone_number: str,
        email: str,
        middle_name: str | None = None,
        business_name: str | None = None,
    ) -> PyKudaResponse:
        """
        Create a virtual account.

        Args:
            first_name (str): First name of the account holder.
            last_name (str): Last name of the account holder.
            phone_number (str): Phone number associated with the account.
            email (str): Email address associated with the account.
            middle_name (str, optional): Middle name of the account holder. Defaults to None.
            business_name (str, optional): Business name if applicable. Defaults to None.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.ADMIN_CREATE_VIRTUAL_ACCOUNT.value
        )
        data["Data"].update(
            {
                "phoneNumber": phone_number,
                "email": email,
                "lastName": last_name,
                "firstName": first_name,
                "middleName": middle_name if middle_name else None,
                "businessName": business_name if business_name else None,
                "trackingReference": secrets.token_hex(8),
            }
        )

        return self._create_virtual_account_request(data)

    def virtual_account_balance(self, tracking_reference: str) -> PyKudaResponse:
        """
        Get the balance of a virtual account.

        Args:
            tracking_reference (str): Tracking reference of the virtual account.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.RETRIEVE_VIRTUAL_ACCOUNT_BALANCE.value
        )
        data["Data"].update({"trackingReference": tracking_reference})
        return self._virtual_account_balance_request(data)

    def main_account_balance(self) -> PyKudaResponse:
        """
        Get the account balance of the main account.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.ADMIN_RETRIEVE_MAIN_ACCOUNT_BALANCE.value
        )
        return self._main_account_balance_request(data)

    def fund_virtual_account(
        self, tracking_reference: str, amount: str, narration: str
    ) -> PyKudaResponse:
        """
        Withdraw money from the main account and deposit into a virtual account.

        Args:
            tracking_reference (str): Tracking reference of the virtual account.
            amount (str): Amount to be funded.
            narration (str): Description of the transaction.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.FUND_VIRTUAL_ACCOUNT.value, tracking_reference
        )
        data["Data"].update({"amount": amount, "narration": narration})
        return self._fund_virtual_account_request(data)

    def withdraw_from_virtual_account(
        self, tracking_reference: str, amount: str, narration: str
    ) -> PyKudaResponse:
        """
        Withdraw money from a virtual account and deposit into the main account.

        Args:
            tracking_reference (str): Tracking reference of the virtual account.
            amount (str): Amount to be withdrawn.
            narration (str): Description of the transaction.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.WITHDRAW_VIRTUAL_ACCOUNT.value, tracking_reference
        )
        data["Data"].update({"amount": int(amount), "narration": narration})
        return self._withdraw_from_virtual_account_request(data)

    def confirm_transfer_recipient(
        self,
        beneficiary_account_number: str,
        beneficiary_bank_code: str,
        tracking_reference: str | None = None,
    ) -> PyKudaResponse:
        """
        Confirm recipient details for fund transfer.

        Args:
            beneficiary_account_number (str): Account number of the recipient.
            beneficiary_bank_code (str): Bank code of the recipient's bank.
            tracking_reference (str, optional): Tracking reference for virtual
            account transfer. Defaults to None.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(ServiceTypeConstants.NAME_ENQUIRY.value)
        data["Data"].update(
            {
                "beneficiaryAccountNumber": beneficiary_account_number,
                "beneficiaryBankCode": beneficiary_bank_code,
                "SenderTrackingReference": tracking_reference
                if tracking_reference
                else "",
                "isRequestFromVirtualAccount": bool(tracking_reference),
            }
        )
        return self._confirm_transfer_recipient_request(data)

    def send_funds_from_main_account(
        self,
        client_account_number: str,
        beneficiary_bank_code: str,
        beneficiary_account_number: str,
        beneficiary_name: str,
        amount: str,
        naration: str,
        name_enquiry_session_id: str,
        sender_name: str,
    ) -> PyKudaResponse:
        """
        Send funds from the main account to another account.

        Args:
            client_account_number (str): Your Kuda Business account number.
            beneficiary_bank_code (str): Bank code of the recipient's bank.
            beneficiary_account_number (str): Account number of the recipient.
            beneficiary_name (str): Name of the recipient.
            amount (str): Amount to be transferred.
            naration (str): Description of the transaction.
            name_enquiry_session_id (str): ID for name enquiry session.
            sender_name (str): Name of the sender.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.SINGLE_FUND_TRANSFER.value
        )
        data["Data"].update(
            {
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
            }
        )
        return self._send_funds_from_main_account_request(data)

    def send_funds_from_virtual_account(
        self,
        tracking_reference: str,
        beneficiary_bank_code: str,
        beneficiary_account_number: str,
        beneficiary_name: str,
        amount: str,
        naration: str,
        name_enquiry_session_id: str,
        sender_name: str,
    ) -> PyKudaResponse:
        """
        Send funds from a virtual account to another account.

        Args:
            tracking_reference (str): Tracking reference of the virtual account.
            beneficiary_bank_code (str): Bank code of the recipient's bank.
            beneficiary_account_number (str): Account number of the recipient.
            beneficiary_name (str): Name of the recipient.
            amount (str): Amount to be transferred.
            naration (str): Description of the transaction.
            name_enquiry_session_id (str): ID for name enquiry session.
            sender_name (str): Name of the sender.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.VIRTUAL_ACCOUNT_FUND_TRANSFER.value, tracking_reference
        )
        data["Data"].update(
            {
                "beneficiaryBankCode": beneficiary_bank_code,
                "beneficiaryAccount": beneficiary_account_number,
                "beneficiaryName": beneficiary_name,
                "amount": int(amount),
                "narration": naration,
                "nameEnquiryId": name_enquiry_session_id,
                "senderName": sender_name,
                "clientFeeCharge": 0,
            }
        )
        return self._send_funds_from_virtual_account_request(data)

    def billers(
        self,
        biller_type: str,
    ) -> PyKudaResponse:
        """
        Get billers by a specified biller type.

        Args:
            biller_type (str): Type of billers to retrieve.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.GET_BILLERS_BY_TYPE.value
        )
        data["Data"].update({"BillTypeName": biller_type})
        return self._billers_request(data)

    def verify_bill_customer(
        self,
        kuda_biller_item_identifier: str,
        customer_identifier: str,
    ) -> PyKudaResponse:
        """
        Verify a bill by customer.

        Args:
            kuda_biller_item_identifier (str): Identifier of the bill item in Kuda.
            customer_identifier (str): Identifier of the customer.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.VERIFY_BILL_CUSTOMER.value
        )
        data["Data"].update(
            {
                "KudaBillItemIdentifier": kuda_biller_item_identifier,
                "CustomerIdentification": customer_identifier,
            }
        )
        return self._verify_bill_customer_request(data)

    def virtual_account_purchase_bill(
        self,
        amount: str,
        kuda_biller_item_identifier: str,
        customer_identifier: str,
        tracking_reference: str,
        phone_number: str | None = None,
    ) -> PyKudaResponse:
        """
        Purchase a bill with a virtual account.

        Args:
            amount (str): Amount to pay for the bill.
            kuda_biller_item_identifier (str): Identifier of the bill item in Kuda.
            customer_identifier (str): Identifier of the customer.
            tracking_reference (str): Tracking reference for the virtual account.
            phone_number (str, optional): Phone number of the customer. Defaults to None.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.PURCHASE_BILL.value, tracking_reference
        )
        data["Data"].update(
            {
                "Amount": amount,
                "BillItemIdentifier": kuda_biller_item_identifier,
                "PhoneNumber": phone_number,
                "CustomerIdentifier": customer_identifier,
            }
        )
        return self._virtual_account_purchase_bill_request(data)

    def disable_virtual_account(self, tracking_reference: str) -> PyKudaResponse:
        """
        Disables a virtual account

        Args:
            tracking_reference (str): Tracking reference for the virtual account.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """

        data = self._generate_common_data(
            ServiceTypeConstants.ADMIN_DISABLE_VIRTUAL_ACCOUNT.value, tracking_reference
        )
        return self._disable_virtual_account_request(data)

    def enable_virtual_account(self, tracking_reference: str) -> PyKudaResponse:
        """
        Enables a virtual account

        Args:
            tracking_reference (str): Tracking reference for the virtual account.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.ADMIN_ENABLE_VIRTUAL_ACCOUNT.value, tracking_reference
        )
        return self._enable_virtual_account_request(data)

    # Virtual account update. According to Kuda, you can only update first name, last name,
    # and email. You can't update the phone number.

    def retrieve_single_virtual_account(
        self,
        tracking_reference: str,
    ) -> PyKudaResponse:
        """
        Retrieves a single virtual acccount

        Args:
            tracking_reference (str): Tracking reference for the virtual account.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.ADMIN_RETRIEVE_SINGLE_VIRTUAL_ACCOUNT.value,
            tracking_reference,
        )
        return self._retrieve_single_virtual_account_request(data)

    def retrieve_all_virtual_accounts(self) -> PyKudaResponse:
        """
        Retrieves all virtual accounts

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.ADMIN_VIRTUAL_ACCOUNTS.value
        )
        data["data"] = {"PageSize": "30", "PageNumber": "1"}

        return self._retrieve_all_virtual_accounts_request(data)

    # To prevent errors, kuda recommends not to update email and names in the same request
    # So both methods are seperated
    def update_virtual_account_name(
        self,
        tracking_reference: str,
        first_name: str,
        last_name: str,
    ) -> PyKudaResponse:
        """
        Update a virtual accounts name

        Args:
            tracking_reference (str): Tracking reference for the virtual account.
            first_name (str): new First name that the account should be updated to.
            last_name (str): new Last name that the account should be updated to.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.ADMIN_UPDATE_VIRTUAL_ACCOUNT.value, tracking_reference
        )
        data["Data"].update(
            {
                "lastName": first_name,
                "firstName": last_name,
            }
        )
        return self._update_virtual_account_info_request(data)

    def update_virtual_account_email(
        self,
        tracking_reference: str,
        email: str,
    ) -> PyKudaResponse:
        """
        Updates a virtual account email

        Args:
            tracking_reference (str): Tracking reference for the virtual account.
            email (str): new email that the account should be updated to.

        Returns:
            PyKudaResponse: Response object containing the result of the request.
        """
        data = self._generate_common_data(
            ServiceTypeConstants.ADMIN_UPDATE_VIRTUAL_ACCOUNT.value, tracking_reference
        )
        data["Data"].update(
            {
                "email": email,
            }
        )
        return self._update_virtual_account_info_request(data)
