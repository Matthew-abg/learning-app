from domain.repository_interfaces import Repository
from application.dto import LearningUnitViewDTO

class GetUnitDetailsService:
    """Use case: Fetch full details of a Unit for display."""

    # Dependency Injection of the repository
    def __init__(self, unit_repository: Repository):
        self.unit_repository = unit_repository

    def execute(self, unit_id: str) -> LearningUnitViewDTO:
        # 1. Get domain entity from repository (Domain Layer)
        unit = self.unit_repository.get_unit_by_id(unit_id)

        # 2. Map domain entity to DTO (Application Layer)
        dto = LearningUnitViewDTO(
            title=unit.title,
            blocks_count=len(unit.block_ids),
            type=unit.type.value,
            state=unit.state.value,
            xp=unit.xp,
        )

        # 3. Return DTO to View
        return dto
