from enum import Enum


class Resource(Enum):
    DIAMOND = '\033[91mdi\033[0m'  # Red
    GOLD = '\033[93mgo\033[0m'  # Yellow
    SILVER = '\033[96msi\033[0m'  # Cyan
    CLOTH = '\033[95mcl\033[0m'  # Magenta
    SPICES = '\033[92msp\033[0m'  # Green
    LEATHER = '\033[33mle\033[0m'  # Dark Yellow / Brown
    CAMEL = '\033[37mca\033[0m'  # Light Gray / White
    TOKENX3 = '\033[34mx3\033[0m'
    TOKENX4 = '\033[34mx4\033[0m'
    TOKENX5 = '\033[34mx5\033[0m'

    @classmethod
    def normal_resources(cls):
        return [cls.DIAMOND, cls.GOLD, cls.SILVER, cls.CLOTH, cls.SPICES, cls.LEATHER]

    @classmethod
    def expensive_resources(cls):
        return [cls.DIAMOND, cls.GOLD, cls.SILVER]

    @classmethod
    def bonus_tokens(cls):
        return [cls.TOKENX3, cls.TOKENX4, cls.TOKENX5]

#print("\033[91m[di] \033[93m[go] \033[96m[si] \033[95m[cl] \033[92m[sp] \033[33m[le] \033[37m[ca] " )