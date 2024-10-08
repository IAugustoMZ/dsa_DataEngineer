from pydantic import BaseModel

class Filter(BaseModel):
    start_date: str
    end_date: str
    production_line: str