from pykuda.classes.service_type import ServiceType

from pykuda.utils import check_envs_are_set


class PyKuda(ServiceType):
    def __init__(self):
        response = check_envs_are_set()

        if not isinstance(response, bool):
            raise ValueError(response)
