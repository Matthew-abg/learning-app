from dataclasses import dataclass, field
from enum import Enum
from typing import List
from datetime import datetime, timezone


class LearnableStatus(Enum):
    LOCKED = "locked"             
    AVAILABLE = "available"       
    IN_PROGRESS = "in_progress"   
    PAUSED = "paused"             
    DONE = "done"                 
    FAILED = "failed"             


class LearningUnitType(Enum):
    LESSON = "lesson"
    EXERCISE = "exercise"
    QUIZ = "quiz"
    MIXED = "mixed"

@dataclass
class LearningContent:
    id: str
    type: str  
    data: dict

@dataclass
class LearningBlock:
    id: str
    title: str
    content: list[LearningContent]
    state: LearnableStatus = LearnableStatus.LOCKED
    xp: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class LearningUnit:
    id: str
    title: str
    type: LearningUnitType
    blocks: List[LearningBlock]
    state: LearnableStatus = LearnableStatus.LOCKED
    xp: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


