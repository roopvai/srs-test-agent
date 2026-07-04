from pydantic import BaseModel
from typing import Literal

class TestCase(BaseModel):
    id: str
    title: str
    requirement_id: str
    preconditions: str
    steps: list[str]
    expected_result: str
    priority: Literal["High", "Medium", "Low"]
    test_type: Literal["functional", "negative", "boundary", "security", "performance"]

class EdgeCase(BaseModel):
    id: str
    title: str
    requirement_id: str
    preconditions: str
    steps: list[str]
    expected_result: str
    priority: Literal["High", "Medium", "Low"]
    rationale: str

class QualityRisk(BaseModel):
    requirement_id: str
    description: str
    category: Literal["ambiguity", "missing_acceptance_criteria", "conflict", "untestable", "security_gap"]
    severity: Literal["High", "Medium", "Low"]