from pydantic import BaseModel


class ReportSummary(BaseModel):
    total_checks: int
    total_incidents: int
    critical_incidents: int
    warning_incidents: int
    top_problem_objects: list[str]
