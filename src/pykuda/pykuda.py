from pykuda.classes.service_type import ServiceType
from pykuda.utils import check_envs_are_set


class PyKuda(ServiceType):
    """
    PyKuda Class handles the authentication and initialization
    of credentials for the Kuda API service.
    """

    def __init__(self, credentials: dict | None = None):
        """
        Initializes the PyKuda instance with the provided credentials.

        This method performs the following steps:
        1. Calls the check_envs_are_set function to verify that all necessary
           environment variables or credentials are properly set.
        2. If the credentials are valid and properly set, the response will
           be a dictionary containing the credentials, which is then assigned
           to the self.credentials attribute.
        3. If the credentials are not properly set, a ValueError is raised with
           an appropriate error message.

        Args:
            credentials (dict | None): A dictionary of credentials, or None if
                                       the credentials are to be fetched from
                                       the environment variables.

        Raises:
            ValueError: If the environmental variables or credentials are not properly set.
        """

        response = check_envs_are_set(credentials)

        # If credentials are valid, 'response' will be a dictionary containing
        # the credentials. Otherwise, it will be a string with an error message.
        if not isinstance(response, dict):
            raise ValueError(response)

        # Store the valid credentials.
        self.credentials = response
