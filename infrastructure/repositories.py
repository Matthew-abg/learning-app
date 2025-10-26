# TODO needs to be implemented
from typing import TYPE_CHECKING
from domain.repository_interfaces import Repository
from infrastructure.django_app.models import LearningUnitModel
from infrastructure.mappers import LearningUnitMapper

if TYPE_CHECKING:
    from domain.models import LearningUnit


class DjangoRepository(Repository):
    """Infrastructure implementation of UnitRepository using Django ORM."""

    def get_unit_by_id(self, unit_id: str) -> "LearningUnit":

        unit_obj = (
            LearningUnitModel.objects.get(id=unit_id)
        )

        return LearningUnitMapper.to_domain(unit_obj)
