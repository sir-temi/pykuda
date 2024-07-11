from enum import Enum


class ServiceTypeConstants(Enum):
    """ServiceType Constants
        This enumeration represents various service types that can be used in 
    the context of virtual account management and transactions. Each constant 
    corresponds to a specific service operation that can be performed, such as 
    creating a virtual account, retrieving balances, transferring funds, and 
    handling bill payments.

    These constants can be used to standardize the service type identifiers 
    across different parts of the application, ensuring consistency and 
    reducing the likelihood of errors caused by hardcoding strings.
    """

    BANK_LIST = "BANK_LIST"
    ADMIN_CREATE_VIRTUAL_ACCOUNT = "ADMIN_CREATE_VIRTUAL_ACCOUNT"
    RETRIEVE_VIRTUAL_ACCOUNT_BALANCE = "RETRIEVE_VIRTUAL_ACCOUNT_BALANCE"
    ADMIN_RETRIEVE_MAIN_ACCOUNT_BALANCE = "ADMIN_RETRIEVE_MAIN_ACCOUNT_BALANCE"
    FUND_VIRTUAL_ACCOUNT = "FUND_VIRTUAL_ACCOUNT"
    WITHDRAW_VIRTUAL_ACCOUNT = "WITHDRAW_VIRTUAL_ACCOUNT"
    NAME_ENQUIRY = "NAME_ENQUIRY"
    SINGLE_FUND_TRANSFER = "SINGLE_FUND_TRANSFER"
    VIRTUAL_ACCOUNT_FUND_TRANSFER = "VIRTUAL_ACCOUNT_FUND_TRANSFER"
    GET_BILLERS_BY_TYPE = "GET_BILLERS_BY_TYPE"
    VERIFY_BILL_CUSTOMER = "VERIFY_BILL_CUSTOMER"
    PURCHASE_BILL = "PURCHASE_BILL"
    ADMIN_PURCHASE_BILL = "ADMIN_PURCHASE_BILL"
    ADMIN_DISABLE_VIRTUAL_ACCOUNT = "ADMIN_DISABLE_VIRTUAL_ACCOUNT"
    ADMIN_ENABLE_VIRTUAL_ACCOUNT = "ADMIN_ENABLE_VIRTUAL_ACCOUNT"
    ADMIN_UPDATE_VIRTUAL_ACCOUNT = "ADMIN_UPDATE_VIRTUAL_ACCOUNT"
    ADMIN_RETRIEVE_SINGLE_VIRTUAL_ACCOUNT = "ADMIN_RETRIEVE_SINGLE_VIRTUAL_ACCOUNT"
    ADMIN_VIRTUAL_ACCOUNTS = "ADMIN_VIRTUAL_ACCOUNTS"
    ADMIN_UPGRADE_VIRTUAL_ACCOUNT = "ADMIN_UPGRADE_VIRTUAL_ACCOUNT"


HTTP_REQUEST_TIMEOUT = 60
KUDA_CREDENTIALS_KEYS = [
    "KUDA_KEY",
    "TOKEN_URL",
    "REQUEST_URL",
    "EMAIL",
    "MAIN_ACCOUNT_NUMBER",
]
