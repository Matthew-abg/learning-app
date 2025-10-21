# ============================================================
# ⚠️ DOMAIN LAYER — ARCHITECTURAL WARNING
# ------------------------------------------------------------
# Keep this file completely free of any framework-specific code.
# The domain layer must remain pure and independent of frameworks
# like Django, DRF, Celery, SQLAlchemy, etc.
#
# If a functionality depends on a specific framework or library,
# place it in the infrastructure layer, or provide an adapter
# that bridges the domain and infrastructure boundaries.
#
# Importing framework objects here (e.g., ORM models, serializers)
# will break the dependency rule and may create ⚠️ circular imports ⚠️
# — leading to hard-to-debug coupling and architectural decay.
# ============================================================


from dataclasses import dataclass, field
from enum import Enum
from typing import List
from datetime import datetime, timezone


class LearnableState(Enum):
    LOCKED = "locked"             
    AVAILABLE = "available"       
    IN_PROGRESS = "in_progress"   
    PAUSED = "paused"             
    DONE = "done"                 
    FAILED = "failed"

    def __str__(self) -> str:
        return self.value             


class LearningUnitType(Enum):
    LESSON = "lesson"
    EXERCISE = "exercise"
    QUIZ = "quiz"
    MIXED = "mixed"


@dataclass
class LearningContent:
    id: str
    data: dict[str, str]


@dataclass
class LearningBlock:
    id: str
    title: str
    content: list[LearningContent]
    state: LearnableState = LearnableState.LOCKED
    xp: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class LearningUnit:
    id: str
    title: str
    type: LearningUnitType
    blocks: List[LearningBlock]
    state: LearnableState = LearnableState.LOCKED
    xp: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


