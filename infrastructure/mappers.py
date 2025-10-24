from domain.models import LearningUnit, LearningBlock, LearningContent, LearnableState, LearningUnitType
from infrastructure.django_app.models import LearningUnitModel, LearningBlockModel, LearningContentModel


class LearningContentMapper:
    """
    Converts between the Django ORM model (LearningContentModel)
    and the Domain Entity (LearningContent).
    """

    @staticmethod
    def to_domain(model: LearningContentModel) -> LearningContent:
        """Convert ORM model → Domain entity."""
        return LearningContent(
            id = model.id,
            data = model.data,
        )

    @staticmethod
    def to_model(entity: LearningContent) -> LearningContentModel:
        """Convert Domain entity → ORM model."""
        return LearningContentModel(
            id = entity.id,
            data = entity.data,
        )




class LearningBlockMapper:
    """
    Converts between the Django ORM model (LearningBlockModel)
    and the Domain Entity (LearningBlock).
    """

    @staticmethod
    def to_domain(model: LearningBlockModel) -> LearningBlock:
        """Convert ORM model → Domain entity."""
        return LearningBlock(
            id = model.id,
            title = model.title,
            content = [LearningContentMapper.to_domain(content) for content in model.content.all()],

            # Because we saved it with title() in the model
            state = LearnableState(model.state.lower()),

            xp = model.xp,
            created_at = model.created_at,
            updated_at = model.updated_at,
        )

    @staticmethod
    def to_model(entity: LearningBlock) -> LearningBlockModel:
        """Convert Domain entity → ORM model."""
        new_block_obj = LearningBlockModel(
            id = entity.id,
            title = entity.title,
            
            # Because we need to save it as title() in the model
            # Just to be consistent with the choices defined in the model
            state = entity.state.value.title(),

            xp = entity.xp,
            created_at = entity.created_at,
            updated_at = entity.updated_at,
        )

        # We don't want to save related objects here
        # So we just prepare a prefetched list for later use
        new_block_obj._prefetched_content = [LearningContentMapper.to_model(content) for content in entity.content]
        return new_block_obj


class LearningUnitMapper:
    """
    Converts between the Django ORM model (LearningUnitModel in Infrastructure.django_app.models)
    and the Domain Entity (LearningUnit in Domain.models).
    """

    @staticmethod
    def to_domain(model: LearningUnitModel) -> LearningUnit:
        """Convert ORM model → Domain entity."""
        return LearningUnit(
            id = model.id,
            title = model.title,

            # Because we saved it with title() in the model
            type = LearningUnitType(model.type.lower()),

            blocks = [LearningBlockMapper.to_domain(block) for block in model.blocks.all()],
            
            # Because we saved it with title() in the model
            state = LearnableState(model.state.lower()),

            xp = model.xp,
            created_at = model.created_at,
            updated_at = model.updated_at,
        )
