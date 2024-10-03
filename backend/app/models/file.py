from enum import Enum
from struct import error

from pydantic import BaseModel

class FileType(Enum):
    pdf = "PDF"
    docx = "DOCX"
    txt = "TXT"
    pptx = "PPTX"
    md = "MARKDOWN"
    csv = "CSV"
    xlsx = "XLSX"
    html = "HTML"
    json = "JSON"

    def suffix(self) -> str:
        suffixes = {
            "TXT": ".txt",
            "PDF": ".pdf",
            "MARKDOWN": ".md",
            "DOCX": ".docx",
            "CSV": ".csv",
            "XLSX": ".xlsx",
            "PPTX": ".pptx",
            "HTML": ".html",
            "JSON": ".json"
        }
        return suffixes[self.value]


class File(BaseModel):
    name: str | None = None
    metadata: dict | None = None

    @property
    def type(self) -> FileType | None:
        file_name = self.name
        if file_name:
            extension = file_name.split(".")[-1].lower()
            try:
                return FileType[extension]
            except KeyError:
                pass

        return None

    @property
    def suffix(self) -> str:
        file_type = self.type
        if file_type is not None:
            return file_type.suffix()
        else:
            pass