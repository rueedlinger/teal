from pydantic import BaseModel


class AppInfo(BaseModel):

    version: str | None = None
    details: dict | None = {}


class HealthCheck(BaseModel):

    status: str = "OK"
