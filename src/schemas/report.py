from datetime import date

from pydantic import BaseModel


class ReportIn(BaseModel):
    start_date: date
    end_date: date
