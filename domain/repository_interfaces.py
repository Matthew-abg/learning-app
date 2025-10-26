from abc import ABC, abstractmethod
from domain.models import LearningUnit


class Repository(ABC):
    """Domain-level abstraction for accessing Unit aggregates."""

    @abstractmethod
    def get_unit_by_id(self, unit_id: str) -> LearningUnit:
        """Fetch a full Unit aggregate (with its Blocks and Contents) by ID."""
        pass
