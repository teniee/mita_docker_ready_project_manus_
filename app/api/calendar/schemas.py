
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import date

class GenerateCalendarRequest(BaseModel):
    calendar_id: str
    start_date: date
    num_days: int
    budget_plan: Dict[str, float]

class CalendarDayOut(BaseModel):
    date: date
    expenses: Dict[str, float]
    total: float

class CalendarOut(BaseModel):
    calendar_id: str
    days: List[CalendarDayOut]

class EditDayRequest(BaseModel):
    updates: Dict[str, float]


class DayInput(BaseModel):
    user_id: str
    year: int
    month: int
    day: int

class CalendarDayStateOut(BaseModel):
    state: dict


class RedistributeInput(BaseModel):
    calendar: dict
    strategy: str = "balance"

class RedistributeResult(BaseModel):
    updated_calendar: dict


class ShellConfig(BaseModel):
    user_id: str
    savings_target: float
    income: float
    fixed: Dict[str, float]
    weights: Dict[str, float]
    year: int
    month: int

class ShellCalendarOut(BaseModel):
    calendar: dict
