from dataclasses import dataclass


# DTOs for transferring data between application layers
# So domain models are not exposed directly and they can be tailored
# to the needs of specific use cases.
# They are just simple data containers so should be immutable.
@dataclass(frozen=True)
class LearningUnitViewDTO:
    title: str
    blocks_count: int
    type: str
    state: str
    xp: int
