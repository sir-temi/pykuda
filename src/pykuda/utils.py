from dataclasses import dataclass
from decouple import config
import secrets
import requests

from pykuda.constants import KUDA_CREDENTIALS_KEYS


def check_envs_are_set(credentials: dict | None) -> bool | str:
    """
    Checks if important environmental variables are set.

    Returns:
        A dictionary of credentials if all environmental variables are set,
        otherwise a string with missing variables.
    """
    credentials = (
        credentials
        if credentials
        else {
            "KUDA_KEY": config("KUDA_KEY", default=None),
            "TOKEN_URL": config("TOKEN_URL", default=None),
            "REQUEST_URL": config("REQUEST_URL", default=None),
            "EMAIL": config("EMAIL", default=None),
            "MAIN_ACCOUNT_NUMBER": config("MAIN_ACCOUNT_NUMBER", default=None),
        }
    )

    unset_variables = [
        kuda_key for kuda_key in KUDA_CREDENTIALS_KEYS if not credentials.get(kuda_key)
    ]
    return (
        f"{', '.join(unset_variables)} are not set, please set in the environment or pass them as a dictionary when initialising PyKuda."
        if unset_variables
        else credentials
    )


@dataclass
class Utils:
    """Attributes:
    credentials (dict): A dictionary containing KUDA service credentials including:
        - "KUDA_KEY": API key for authentication.
        - "TOKEN_URL": URL for generating tokens.
        - "REQUEST_URL": URL for making API requests.
        - "EMAIL": Email associated with the KUDA account.
        - "MAIN_ACCOUNT_NUMBER": Main account number."""

    credentials = None

    def _get_token(self) -> str:
        """
        Generates a token from KUDA's TOKEN URL.

        Returns:
            A string representing the generated token.
        """

        return requests.post(
            self.credentials["TOKEN_URL"],
            json={
                "email": self.credentials["EMAIL"],
                "apiKey": self.credentials["KUDA_KEY"],
            },
            headers={"content-type": "application/json"},
            timeout=10,
        )

    def _generate_headers(self) -> requests.models.Response | dict:
        """
        Generates headers for requests.

        Returns:
            A dictionary containing headers for API requests or a response object.
        """
        response = self._get_token()

        return (
            {
                "content-type": "application/json",
                "Authorization": f"bearer {response.text}",
            }
            if response.status_code == 200
            else response
        )

    def _generate_common_data(
        self, service_type: str, tracking_reference: str | None = None
    ):
        """
        Generate common data structure for various service requests.

        Args:
            service_type (str): The type of service.
            tracking_reference (str, optional): Tracking reference for the request.
            Defaults to None.

        Returns:
            dict: Common data structure for service requests.
        """
        data = {
            "serviceType": service_type,
            "requestref": secrets.token_hex(6),
            "Data": {"trackingReference": tracking_reference},
        }

        if not tracking_reference:
            del data["Data"]["trackingReference"]

        return data
