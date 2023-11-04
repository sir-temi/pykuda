from pykuda.classes.service_type import ServiceType
from pykuda.utils import check_envs_are_set


class PyKuda(ServiceType):
    """
    PyKuda Class.
    """

    def __init__(self):
        response = check_envs_are_set()

        # If all credentials were properly set, response will
        # be a dictionary of credentials, else will be a string
        if not isinstance(response, dict):
            raise ValueError(response)

        self.credentials = response
