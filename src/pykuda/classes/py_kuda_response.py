from dataclasses import dataclass


@dataclass
class PyKudaResponse:
    """
    Helps simplify Kuda' response
    """

    status_code: int
    data: dict
    error: bool = False
