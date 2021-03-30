from dataclasses import dataclass


@dataclass
class Song:
    page_url: str = None
    file_url: str = None
    title:    str = None
    uploader: str = None
    duration: str = None
