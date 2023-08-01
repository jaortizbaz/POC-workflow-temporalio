from dataclasses import dataclass


@dataclass
class SftpProps:
    host: str
    port: int
    user: str
    password: str
    path: str
    filename: str
