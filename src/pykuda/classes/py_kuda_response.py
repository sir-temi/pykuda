from dataclasses import dataclass

@dataclass
class PyKudaResponse:
    """
    A class to simplify and standardize the response from Kuda API.

    Attributes:
        status_code (int): The HTTP status code of the response.
        data (dict): The data payload of the response.
        error (bool): Indicates whether there was an error in the response (default is False).
    """
    status_code: int
    data: dict
    error: bool = False
