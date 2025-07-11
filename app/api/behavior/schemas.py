from pydantic import BaseModel
from typing import Dict


class BehaviorPayload(BaseModel):
    user_id: str
    year: int
    month: int
    profile: Dict
    mood_log: Dict
    challenge_log: Dict
    calendar_log: Dict
