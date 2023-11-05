from pydantic import BaseModel


class ReportBase(BaseModel):
    pass


class ReportCreate(ReportBase):
    pass


class ReportRead(ReportBase):
    id: int


class ReportUpdate(ReportBase):
    pass
