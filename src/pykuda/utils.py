import os
import secrets
from dotenv import load_dotenv
import requests

load_dotenv()


class Utils:
    """Attributes:
    credentials (dict): A dictionary containing KUDA service credentials including:
        - "KUDA_KEY": API key for authentication.
        - "TOKEN_URL": URL for generating tokens.
        - "REQUEST_URL": URL for making API requests.
        - "EMAIL": Email associated with the KUDA account.
        - "MAIN_ACCOUNT_NUMBER": Main account number."""

    credentials = {
        "KUDA_KEY": os.getenv("KUDA_KEY"),
        "TOKEN_URL": os.getenv("TOKEN_URL"),
        "REQUEST_URL": os.getenv("REQUEST_URL"),
        "EMAIL": os.getenv("EMAIL"),
        "MAIN_ACCOUNT_NUMBER": os.getenv("MAIN_ACCOUNT_NUMBER"),
    }

    def check_envs_are_set(self) -> bool | str:
        """
        Checks if important environmental variables are set.

        Returns:
            True if all environmental variables are set, otherwise a string with missing variables.
        """
        if all(list(self.credentials.values())):
            return True

        for variable, value in self.credentials.items():
            if not value:
                return f"{variable} is not set, please set in the environment and try again."

    def get_token(self) -> str:
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

    def generate_headers(self) -> requests.models.Response | dict:
        """
        Generates headers for requests.

        Returns:
            A dictionary containing headers for API requests or a response object.
        """
        response = self.get_token()

        return (
            {
                "content-type": "application/json",
                "Authorization": f"bearer {response.text}",
            }
            if response.status_code == 200
            else response
        )

    def generate_common_data(
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
