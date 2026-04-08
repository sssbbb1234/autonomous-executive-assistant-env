from pydantic import BaseModel
from typing import List, Optional


class Email(BaseModel):
    id: str
    sender: str
    subject: str
    body: str
    processed: bool = False
    label: Optional[str] = None
    replied: bool = False


class Task(BaseModel):
    id: str
    description: str
    priority: Optional[str] = None
    deadline: Optional[str] = None
    status: str = "pending"
    source_email_id: str


class CalendarEvent(BaseModel):
    event_id: str
    title: str
    time: str
    location: Optional[str] = None
    linked_task_id: str


class Observation(BaseModel):
    emails: List[Email]
    tasks: List[Task]
    calendar: List[CalendarEvent]
    step_count: int


class Action(BaseModel):
    action_type: str

    email_id: Optional[str] = None
    task_id: Optional[str] = None

    label: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None

    time: Optional[str] = None
    location: Optional[str] = None

    message: Optional[str] = None