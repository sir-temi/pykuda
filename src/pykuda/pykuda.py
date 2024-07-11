from pykuda.classes.service_type import ServiceType
from pykuda.utils import check_envs_are_set


class PyKuda(ServiceType):
    """
    PyKuda Class.
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
            ValueError: If the credentials are not properly set.
        """
        response = check_envs_are_set(credentials)

        # If all credentials were properly set, response will
        # be a dictionary of credentials, else will be a string
        if not isinstance(response, dict):
            raise ValueError(response)

        self.credentials = response
