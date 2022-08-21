import os
from dotenv import load_dotenv

from pykuda.classes.service_type import ServiceType


class PyKuda(ServiceType):
    def __init__(self):
        response = check_envs_are_set()

        if not isinstance(response, bool):
            raise ValueError(response)


def check_envs_are_set():
    load_dotenv()

    variables = {
        "KUDA_KEY": os.getenv("KUDA_KEY"),
        "TOKEN_URL": os.getenv("TOKEN_URL"),
        "REQUEST_URL": os.getenv("REQUEST_URL"),
        "EMAIL": os.getenv("EMAIL"),
        "MAIN_ACCOUNT_NUMBER": os.getenv("MAIN_ACCOUNT_NUMBER"),
    }

    if all(list(variables.values())):
        return True

    for variable, value in variables.items():
        if not value:
            return f"{variable} is not set, please set in the env and try again."
