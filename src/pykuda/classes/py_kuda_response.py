from dataclasses import dataclass


@dataclass
class PyKudaResponse:
    """
    Helps simplify Kuda's response by encapsulating the response details in a structured format.
    
    Attributes:
        status_code (int): The HTTP status code returned by Kuda's API.
        data (dict): The response data from Kuda's API, usually in dictionary form.
        error (bool): A flag indicating whether the response indicates an error (default is False).
    """

    status_code: int
    data: dict
    error: bool = False
