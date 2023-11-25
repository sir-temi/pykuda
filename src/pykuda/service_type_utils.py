import requests

from pykuda.classes.py_kuda_response import PyKudaResponse
from pykuda.utils import Utils
from pykuda.constants import HTTP_REQUEST_TIMEOUT


class ServiceTypeUtils(Utils):
    """
    A utility class responsible for generating headers and making API calls to the respective endpoints for KUDA services.
    Manages account-related HTTP requests and bill payments.

    Methods:
        check_envs_are_set(): Checks if important environmental variables are set.
        get_token(): Generates a token from KUDA's TOKEN URL.
        generate_headers(): Generates headers for requests.
        bank_list_request(data: dict) -> PyKudaResponse: Retrieves a list of Nigerian banks.
        create_virtual_account_request(data: dict) -> PyKudaResponse: Creates a virtual account.
    """

    # Account HTTP requests

    def _banks_list_request(self, data: dict) -> PyKudaResponse:
        """
        Retrieves a list of Nigerian banks.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the list of banks or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
            )

            response_data = response.json()

            if (
                response.status_code == 200
                and response_data
                and response_data.get("status")
                and response_data.get("data")
                and response_data.get("data").get("banks")
            ):
                return PyKudaResponse(
                    status_code=200,
                    data=response_data["data"]["banks"],
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _create_virtual_account_request(self, data: dict) -> PyKudaResponse:
        """
        Function responsible for creating a virtual account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            PyKudaResponse: Response object with the virtual account details or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
            )

            response_data = response.json()

            if (
                response.status_code == 200
                and response_data
                and response_data.get("status")
                and response_data.get("data")
                and response_data.get("data").get("accountNumber")
            ):
                return PyKudaResponse(
                    status_code=201,
                    data={
                        "account_number": response_data["data"]["accountNumber"],
                        "tracking_reference": data["Data"]["trackingReference"],
                    },
                )

            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _virtual_account_balance_request(self, data: dict) -> PyKudaResponse:
        """
        Retrieves the balance of a virtual account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the account balance details or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
            )

            response_data = response.json()

            if response.status_code == 200 and response_data.get("status"):
                return PyKudaResponse(
                    status_code=200,
                    data={
                        "ledger": response_data["data"]["ledgerBalance"],
                        "available": response_data["data"]["availableBalance"],
                        "withdrawable": response_data["data"]["withdrawableBalance"],
                    },
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _main_account_balance_request(self, data: dict) -> PyKudaResponse:
        """
        Retrieves the total balance of the main account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the main account balance details or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
            )

            response_data = response.json()

            if response.status_code == 200 and response_data.get("status"):
                return PyKudaResponse(
                    status_code=200,
                    data={
                        "ledger": response_data["data"]["ledgerBalance"],
                        "available": response_data["data"]["availableBalance"],
                        "withdrawable": response_data["data"]["withdrawableBalance"],
                    },
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _fund_virtual_account_request(self, data: dict) -> PyKudaResponse:
        """
        Funds a virtual account from the main Kuda account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the transaction reference or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
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

    def _withdraw_from_virtual_account_request(self, data: dict) -> PyKudaResponse:
        """
        Withdraws funds from a virtual account and deposits to another virtual account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the transaction reference or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
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

    def _confirm_transfer_recipient_request(self, data: dict) -> PyKudaResponse:
        """
        Confirms that a recipient's information is correct.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the recipient's information or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
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

    def _send_funds_from_main_account_request(self, data: dict) -> PyKudaResponse:
        """
        Sends funds from the main account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the transaction reference or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
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
                        "transaction_reference": response_data.get(
                            "transactionReference"
                        ),
                        "request_reference": response_data.get("requestReference"),
                    },
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _send_funds_from_virtual_account_request(self, data: dict) -> PyKudaResponse:
        """
        Sends funds from a virtual account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the transaction reference or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
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
                        "transaction_reference": response_data.get(
                            "transactionReference"
                        ),
                        "request_reference": response_data.get("requestReference"),
                    },
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    # Bill Payments

    def _billers_request(self, data: dict) -> PyKudaResponse:
        """
        Gets billers.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the list of billers or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
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
                    data=response_data.get("data").get("billers"),
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _verify_bill_customer_request(self, data: dict) -> PyKudaResponse:
        """
        Verifies bill information.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the customer's name or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
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
                        "customer_name": response_data.get("data").get("customerName"),
                    },
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _virtual_account_purchase_bill_request(self, data: dict) -> PyKudaResponse:
        """
        Makes a bill payment using a virtual account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the payment reference or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
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

    def _disable_virtual_account_request(self, data: dict) -> PyKudaResponse:
        """
        Makes a bill payment using a virtual account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the payment reference or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
            )

            response_data = response.json()

            if response.status_code == 200 and response_data.get("status"):
                return PyKudaResponse(
                    status_code=200,
                    data={
                        "account_number": response_data.get("data").get(
                            "accountNumber"
                        ),
                    },
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _enable_virtual_account_request(self, data: dict) -> PyKudaResponse:
        """
        Makes a bill payment using a virtual account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the payment reference or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
            )

            response_data = response.json()

            if response.status_code == 200 and response_data.get("status"):
                return PyKudaResponse(
                    status_code=200,
                    data={
                        "account_number": response_data.get("data").get(
                            "accountNumber"
                        ),
                    },
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _update_virtual_account_info_request(self, data: dict) -> PyKudaResponse:
        """
        Makes a bill payment using a virtual account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the payment reference or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
            )

            response_data = response.json()

            if response.status_code == 200 and response_data.get("status"):
                return PyKudaResponse(
                    status_code=200,
                    data={
                        "account_number": response_data.get("data").get(
                            "accountNumber"
                        ),
                    },
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _retrieve_single_virtual_account_request(self, data: dict) -> PyKudaResponse:
        """
        Makes a bill payment using a virtual account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the payment reference or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
            )

            response_data = response.json()

            if (
                response.status_code == 200
                and response_data.get("status")
                and response_data.get("data")
            ):
                return PyKudaResponse(
                    status_code=200,
                    data=response_data.get("data"),
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )

    def _retrieve_all_virtual_accounts_request(self, data: dict) -> PyKudaResponse:
        """
        Makes a bill payment using a virtual account.

        Args:
            data (dict): Request data for the API call.

        Returns:
            A PyKudaResponse object with the payment reference or an error message.
        """
        headers = self._generate_headers()

        if isinstance(headers, requests.models.Response):
            return PyKudaResponse(status_code=headers.status_code, data=headers)
        else:
            response = requests.post(
                self.credentials["REQUEST_URL"],
                json=data,
                headers=headers,
                timeout=HTTP_REQUEST_TIMEOUT,
            )

            response_data = response.json()

            if (
                response.status_code == 200
                and response_data.get("status")
                and response_data.get("data")
                and response_data.get("data").get("accounts")
            ):
                return PyKudaResponse(
                    status_code=200,
                    data=response_data.get("data").get("accounts"),
                )
            else:
                return PyKudaResponse(
                    status_code=response.status_code, data=response, error=True
                )
