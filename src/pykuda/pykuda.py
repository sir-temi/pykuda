from pykuda.classes.service_type import ServiceType
from pykuda.utils import check_envs_are_set


class PyKuda(ServiceType):
    """
    PyKuda Class handles the authentication and initialization
    of credentials for the Kuda API service.
    """

    def __init__(self, credentials: dict | None = None):
        # Check if the environment variables are set or the provided
        # credentials dictionary is valid.
        response = check_envs_are_set(credentials)

        # If credentials are valid, 'response' will be a dictionary containing
        # the credentials. Otherwise, it will be a string with an error message.
        if not isinstance(response, dict):
            raise ValueError(response)

        # Store the valid credentials.
        self.credentials = response
