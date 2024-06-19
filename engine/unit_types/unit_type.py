class UnitType:
    """
    Class for unit types.
    """
    ATTACK: int
    ATTACK_RANGE: int
    ATTACK_COOLDOWN: int
    MIN_ATTACK_RANGE: int
    MAX_HEALTH: int
    VISION_RANGE: int
    MOVEMENT_COOLDOWN: int

    @classmethod
    def get_unit_type(cls) -> str:
        """
        Get unit type.
        """
        return cls.__name__