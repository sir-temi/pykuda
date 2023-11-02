from dataclasses import dataclass


@dataclass
class PyKudaResponse:
    status_code: int
    data: dict
    error: bool = False
