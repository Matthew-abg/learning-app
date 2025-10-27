from domain.models import LearningUnit, LearningBlock, LearningContent, LearnableState, LearningUnitType
from infrastructure.django_app.models import LearningUnitModel, LearningBlockModel, LearningContentModel


class LearningContentMapper:
    """
    Converts between the Django ORM model (LearningContentModel)
    and the Domain Entity (LearningContent).
    For now, just a simple direct mapping. From model to domain.
    """

    @staticmethod
    def to_domain(model: LearningContentModel) -> LearningContent:
        """Convert ORM model → Domain entity."""
        return LearningContent(
            id = model.id,
            data = model.data,
        )



class LearningBlockMapper:
    """
    Converts between the Django ORM model (LearningBlockModel)
    and the Domain Entity (LearningBlock).
    For now, just a simple direct mapping. From model to domain.
    """

    @staticmethod
    def to_domain(model: LearningBlockModel) -> LearningBlock:
        """Convert ORM model → Domain entity."""
        return LearningBlock(
            id = model.id,
            title = model.title,
            content_ids = [content.id for content in model.contents.all()],

            # Because we saved it with title() in the model
            state = LearnableState(model.state.lower()),

            xp = model.xp,
            created_at = model.created_at,
            updated_at = model.updated_at,
        )

class LearningUnitMapper:
    """
    Converts between the Django ORM model (LearningUnitModel in Infrastructure.django_app.models)
    and the Domain Entity (LearningUnit in Domain.models).
    For now, just a simple direct mapping. From model to domain.
    """

    @staticmethod
    def to_domain(model: LearningUnitModel) -> LearningUnit:
        """Convert ORM model → Domain entity."""
        return LearningUnit(
            id = model.id,
            title = model.title,

            # Because we saved it with title() in the model
            type = LearningUnitType(model.type.lower()),

            block_ids = [block.id for block in model.blocks.all()],
            
            # Because we saved it with title() in the model
            state = LearnableState(model.state.lower()),

            xp = model.xp,
            created_at = model.created_at,
            updated_at = model.updated_at,
        )
