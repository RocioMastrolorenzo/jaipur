from enum import Enum


class Resource(Enum):
    DIAMOND = 'di'
    GOLD = 'go'
    SILVER = 'si'
    CLOTH = 'cl'
    SPICES = 'sp'
    LEATHER = 'le'
    CAMEL = 'ca'
    TOKENX3 = 'x3'
    TOKENX4 = 'x4'
    TOKENX5 = 'x5'

    @classmethod
    def normal_resources(cls):
        return [cls.DIAMOND, cls.GOLD, cls.SILVER, cls.CLOTH, cls.SPICES, cls.LEATHER]

    @classmethod
    def expensive_resources(cls):
        return [cls.DIAMOND, cls.GOLD, cls.SILVER]

    @classmethod
    def bonus_tokens(cls):
        return [cls.TOKENX3, cls.TOKENX4, cls.TOKENX5]
