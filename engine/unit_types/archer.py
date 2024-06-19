from engine.unit_types.unit_type import UnitType


class Archer(UnitType):
    """
    Archer unit.    
    """
    ATTACK: int = 25
    ATTACK_RANGE: int = 8
    ATTACK_COOLDOWN: float = 3.0
    MIN_ATTACK_RANGE: int = 1
    MAX_HEALTH: int = 100
    VISION_RANGE: int = 41
    MOVEMENT_COOLDOWN: float = 3.0

