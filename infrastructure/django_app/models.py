from django.db import models

from domain.models import LearnableState, LearningUnitType


class LearningContentModel(models.Model):
    # Because the id is a string in the domain model
    id = models.CharField(primary_key=True, max_length=64)
    data: models.JSONField[dict[str, str]] = models.JSONField()

    def __str__(self):
        return f"Content {self.id}"


class LearningBlockModel(models.Model):
    # Because the id is a string in the domain model
    id = models.CharField(primary_key=True, max_length=64)
    
    title = models.CharField(max_length=255)

    # I used type ignore in the next line
    # Because these fields are added dynamically by django
    # and as much as I know there's currently no way in the
    # Python type system to tell a static type checker that they will exist.
    content = models.ManyToManyField(LearningContentModel, related_name="blocks")  # type: ignore
    
    # Because the enum is defined in the domain model
    # Single Source of Truth
    state = models.CharField(
        max_length=20,
        choices=[(s.value, s.name.title()) for s in LearnableState],
        default=LearnableState.LOCKED.value,
    )

    xp = models.IntegerField(default=0)

    # Because these fields are managed by domain layer
    # Single Source of Truth
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.title


class LearningUnitModel(models.Model):
    # 
    id = models.CharField(primary_key=True, max_length=64)
    title = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=[(t.value, t.name.title()) for t in LearningUnitType],
        default=LearningUnitType.LESSON.value,
    )

    # I used type ignore in the next line
    # Because these fields are added dynamically by django
    # and as much as I know there's currently no way in the
    # Python type system to tell a static type checker that they will exist.
    blocks = models.ManyToManyField(LearningBlockModel, related_name="units")  # type: ignore

    # Because the enum is defined in the domain model
    # Single Source of Truth
    state = models.CharField(
        max_length=20,
        choices=[(s.value, s.name.title()) for s in LearnableState],
        default=LearnableState.LOCKED.value,
    )

    xp = models.IntegerField(default=0)

    # Because these fields are managed by domain layer
    # Single Source of Truth
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.title
